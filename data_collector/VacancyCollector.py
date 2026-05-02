import time
from datetime import timedelta, date
from api.hh_api import HeadHunterApi
import logging

class VacancyCollector:
    IT_WORDS = ["python", "java", "javascript", "c++", "c#", "golang", "skala",
                "разработчик", "программист", "developer", "engineer",
                "data scientist", "аналитик данных", "devops", "системный администратор",
                "backend", "frontend", "fullstack"]
    logger = logging.getLogger(__name__)

    def __init__(self, target_vacancies_per_day):
        self.target_vacancies_per_day = target_vacancies_per_day
        self.api = HeadHunterApi()

    def get_search_query(self):
        return " OR ".join(self.IT_WORDS)

    def collect_vacancies(self):
        self.logger.info("Начало сбора ваканский VacancyCollector collect_vacancies()")
        vacancy_ids = []
        page = 0
        per_page = 100
        if self.target_vacancies_per_day < per_page:
            per_page = self.target_vacancies_per_day
        search_text = self.get_search_query()
        date_from = str(date.today() - timedelta(days=1))

        while (per_page * page) < self.target_vacancies_per_day:
            response = self.api.get_vacancies(text=search_text, area=113, page=page, per_page=per_page,
                                                    date_from=date_from)
            if response is None:
                self.logger.warning(f"Пропуск для page: {page}")
                page += 1
                continue
            self.logger.info(f"Страница {page}. Получена пачка из {per_page} ваканский")
            data = response.json()
            vacancies = data.get("items", [])
            print(data)
            if not vacancies:
                break
            for vacancy in data.get("items", []):
                id = vacancy.get("id")
                vacancy_ids.append(id)
            page += 1
            time.sleep(0.1)
        self.logger.info(f"Окончание сбора ваканский VacancyCollector collect_vacancies(). "
                    f"Количество собранных id вакансий: {len(vacancy_ids)}. Цель: {self.target_vacancies_per_day}")
        return vacancy_ids
