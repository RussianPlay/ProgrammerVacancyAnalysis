import os
import psycopg2
from psycopg2 import DatabaseError, OperationalError
import logging



class PostgreSQLDatabase:
    logger = logging.getLogger(__name__)

    def __init__(self):
        pass

    def __enter__(self):
        user, password, host, port, dbname = (os.getenv("POSTGRES_USER"), os.getenv("POSTGRES_PASSWORD"),
                                              os.getenv("POSTGRES_HOST"), os.getenv("POSTGRES_PORT"),
                                              os.getenv("POSTGRES_DB"))

        conn_params = {
            "dbname": dbname,
            "user": user,
            "password": password,
            "host": host,
            "port": port
        }

        self._connection = None
        try:
            self._connection = psycopg2.connect(**conn_params)
            self._connection.autocommit = False
            self.cursor = self._connection.cursor()
            self.logger.info("Соединение PostgreSQL создано успешно")
            return self.cursor
        except OperationalError as e:
            self.logger.error("Превышено время ожидания подключения к PostgreSQL", e)
            raise
        except (Exception, DatabaseError) as e:
            self.logger.exception("Ошибка при соединении PostgreSQL", e)


    def __exit__(self, exc_type, exc_val, exc_tb):
        try:
            if hasattr(self, '_connection') and self._connection:
                if exc_type is None:
                    self._connection.commit()
                    self.logger.info("Транзакция успешно закоммичена")
                else:
                    self._connection.rollback()
                    self.logger.warning("Транзакция отменена")
        except Exception as e:
            self.logger.error(f"Ошибка при commit/rollback: {e}")
        finally:
            if hasattr(self, 'cursor') and self.cursor:
                try:
                    self.cursor.close()
                except Exception:
                    pass
            if hasattr(self, '_connection') and self._connection:
                try:
                    if not self._connection.closed:
                        self._connection.close()
                except Exception:
                    pass
            self.logger.info("Соединение PostgreSQL закрыто")