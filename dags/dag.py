from datetime import datetime, timedelta

import time
from airflow import DAG
from airflow.exceptions import AirflowException
from airflow.models import Variable
from airflow.providers.common.sql.operators.sql import SQLExecuteQueryOperator
from airflow.decorators import task
from data_collector.VacancyCollector import VacancyCollector
import logging


default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2026, 1, 1),
    'retries': 3,
    'retry_delay': timedelta(minutes=5),
    'retry_exponential_backoff': True
}

with DAG(
    'etl_vacancy_data',
    default_args=default_args,
    schedule_interval='@daily',
    catchup=False,
    template_searchpath=['/opt/airflow/SQL_Requests'],
    max_active_tasks=4
) as dag:
    @task(task_id='collect_vacancies', execution_timeout=timedelta(minutes=10))
    def collect_vacancies():
        logger = logging.getLogger(__name__)
        try:
            collector = VacancyCollector(target_vacancies_per_day=500)
            vacancy_ids = collector.collect_vacancies()
            logger.info(f"Получено id ваканский в количестве: {len(vacancy_ids)}")
            return vacancy_ids
        except Exception as e:
            raise AirflowException(f"Сбор вакансий не удался: {str(e)}")
    vacancy_ids = collect_vacancies()

    @task(task_id='prepare_data', execution_timeout=timedelta(minutes=20))
    def prepare_data(vacancy_ids):
        logger = logging.getLogger(__name__)
        collector = VacancyCollector()
        target_vacancies = []
        processed_count = 1
        for vacancy_id in vacancy_ids:
            logger.info(f"Обрабатывается {processed_count} строка")
            logger.info(f"Вакансия {vacancy_id}")
            try:
                response = collector.get_vacancy(vacancy_id)
                if response is None:
                    logger.warning(f"Ошибка при получении. Пропуск вакансии {vacancy_id}")
                    continue
                vacancy = response.json()
                id = int(vacancy_id)
                experience = vacancy.get('experience', {})
                experience_name = experience.get('name')

                name = vacancy.get('name')
                published_at = vacancy.get('published_at')

                skills = vacancy.get('key_skills', [])
                skills_names = [skill.get('name') for skill in skills if skill.get('name')]
                skills_str = ', '.join(skills_names) if skills_names else None

                salary = vacancy.get("salary")
                salary_from = None
                salary_to = None
                currency = None
                if salary:
                    salary_from = int(salary.get("from")) if salary.get("from") is not None else None
                    salary_to = int(salary.get("to")) if salary.get("to") is not None else None
                    currency = salary.get("currency")

                area = vacancy.get("area")
                city = area.get("name") if area else None

                employer = vacancy.get("employer")
                employer_name = employer.get("name") if employer else None

                professional_roles = vacancy.get("professional_roles", [])
                professional_role = None
                if professional_roles:
                    professional_role = professional_roles[0].get("name")

                schedule = vacancy.get("schedule")
                schedule_name = schedule.get("name") if schedule else None
                logger.info((id, name, city, salary_from, salary_to, currency, published_at, employer_name,
                                         skills_str, schedule_name, professional_role, experience_name))
                target_vacancies.append({
                    'id': id,
                    'name': name,
                    'city': city,
                    'salary_bottom': salary_from,
                    'salary_top': salary_to,
                    'currency': currency,
                    'published_at': published_at,
                    'employer_name': employer_name,
                    'key_skills': skills_str,
                    'schedule': schedule_name,
                    'professional_role': professional_role,
                    'experience': experience_name
                })
                processed_count += 1
            except Exception as e:
                logger.warning(f"Ошибка при обработке вакансии: {str(e)}")
                continue
        logger.info(f"Получены данные ваканский в количестве: {len(target_vacancies)}")
        return target_vacancies

    prepared_data = prepare_data(vacancy_ids)

    # Проверка существует ли таблица
    create_vacancies = SQLExecuteQueryOperator(
        task_id='create_vacancies',
        sql='postgresql_query/create_query.sql',
        conn_id='postgres_default'
    )


    @task(task_id='insert_to_vacancies')
    def insert_to_vacancies(prepared_data):
        logger = logging.getLogger(__name__)

        if not prepared_data:
            logger.info("Нет данных для вставки")
            return
        try:
            from DBMS_Classes.PostgreSQLDatabase import PostgreSQLDatabase
            with PostgreSQLDatabase() as cur:
                with open("/opt/airflow/SQL_Requests/postgresql_query/insert_query.sql") as f:
                    insert_sql = f.read().strip()
                skipped = 0
                for row in prepared_data:
                    try:
                        cur.execute(insert_sql, row)
                    except Exception as e:
                        logger.error(f"Данные строки: {row}")
                        logger.error(f"ОШИБКА вставки id={row.get('id')}: {str(e)}")
                        skipped += 1
                        continue
                logger.info(f"Данные вставлены в таблицу. Пропущено {skipped} строк")
        except Exception as e:
            raise AirflowException(f"Ошибка вставки в Postgresql: {str(e)}")

    insert_to_vacancies = insert_to_vacancies(prepared_data)

    @task(task_id='transfer_to_clickhouse')
    def transfer_to_clickhouse():
        logger = logging.getLogger(__name__)
        try:
            from DBMS_Classes.PostgreSQLDatabase import PostgreSQLDatabase
            from DBMS_Classes.ClickHouseClient import ClickHouseClient

            with ClickHouseClient() as client_cur:
                # Удаление старых таблиц
                with open("/opt/airflow/SQL_Requests/clickhouse_query/drop_query.sql") as f:
                    client_cur.command(f.read())

                # Проверка существуют ли таблицы в ClickHouse
                with open("/opt/airflow/SQL_Requests/clickhouse_query/create_query.sql") as f:
                    client_cur.command(f.read())

                columns = ['name', 'city', 'salary_bottom', 'salary_top', 'currency', 'published_at',
                           'employer_name', 'key_skills', 'schedule', 'professional_role', 'experience']
                rows = []
                batch_size = int(Variable.get("CLICKHOUSE_BATCH_SIZE", default_var=20000))
                read_size = batch_size * 2
                with PostgreSQLDatabase() as cur:
                    cur.execute("SELECT COUNT(*) FROM vacancies")
                    count = cur.fetchone()[0]
                    logger.info(f"Найдено {count} строк в таблице vacancies")
                    skipped = 0
                    cur.execute("SELECT * FROM vacancies")
                    while True:
                        data = cur.fetchmany(read_size)
                        if not data:
                            break
                        for row in data:
                            try:
                                check_els_id = [1, 2, 5, 6, 7, 9, 10, 11]
                                if any(row[el_id] is None for el_id in check_els_id):
                                    continue
                                name = row[1]
                                city = row[2]
                                salary_bottom = int(row[3]) if row[3] is not None else None
                                salary_top = int(row[4]) if row[4] is not None else None
                                currency = row[5]
                                published_at = row[6].replace(tzinfo=None)
                                employer_name = row[7]
                                key_skills = row[8]
                                schedule = row[9]
                                professional_role = row[10]
                                experience = row[11]
                                rows.append([name, city, salary_bottom, salary_top, currency, published_at, employer_name,
                                                key_skills, schedule, professional_role, experience])
                                if len(rows) >= batch_size:
                                    client_cur.insert("vacancies", rows, column_names=columns)
                                    rows.clear()
                            except Exception as e:
                                skipped += 1
                                logger.warning(f"Пропуск некорректных строк. Ошибка: {str(e)}")
                                continue
                    try:
                        if rows:
                            client_cur.insert("vacancies", rows, column_names=columns)
                            logger.info(f"Последняя пачка из {len(rows)} строк добавлена в таблицу")
                            rows.clear()
                    except Exception as e:
                        skipped += 1
                        logger.warning(f"Пропуск некорректных строк. Ошибка: {str(e)}")
                    logger.info("transfer_to_clickhouse() Данные в clickhouse успешно вставлены. Пропущено {skipped} строк")
        except Exception as e:
            raise AirflowException(f"Ошибка переноса в ClickHouse: {str(e)}")

    transfer_to_clickhouse_task = transfer_to_clickhouse()

    vacancy_ids >> prepared_data >> create_vacancies >> insert_to_vacancies >> transfer_to_clickhouse_task