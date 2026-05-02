import os
import clickhouse_connect
import logging

class ClickHouseClient:
    logger = logging.getLogger(__name__)

    def __init__(self):
        self._client = None
        user, password = os.getenv("CLICKHOUSE_USER"), os.getenv("CLICKHOUSE_PASSWORD")
        try:
            self._client = clickhouse_connect.get_client(host="clickhouse_server", port=8123, username=user, password=password)
            self.logger.info("Соединение с Clickhouse установлено")
        except Exception as e:
            self.logger.exception("Ошибка при соединении с клиентом Clickhouse", e)

    def __enter__(self):
        return self._client

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.logger.info("Соединение с клиентом Clickhouse закрыто")
