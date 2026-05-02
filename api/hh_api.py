import os
from datetime import date, timedelta
import requests
from dotenv import load_dotenv
import logging

load_dotenv()


class HeadHunterApi:
    logger = logging.getLogger(__name__)

    access_token = os.getenv("ACCESS_TOKEN")
    if not access_token:
        raise ValueError("access_token не найден")
    else:
        logger.info("access_token найден")
    API_URL = "https://api.hh.ru"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "HH-User-Agent": "hh_course_project/1.0 (ahmadullin32@mail.ru)"
    }

    def send_request(self, method: str, **kwargs):
        response = requests.get(url=self.API_URL + method, headers=self.headers, params=kwargs)
        if response.status_code == 200:
            return response
        elif response.status_code == 400:
            self.logger.warning(f"Bad request. {method} с {kwargs}: {response.text}")
            return None
        else:
            response.raise_for_status()
        return None

    def get_professional_roles(self, **kwargs):
        response = self.send_request("/professional_roles", **kwargs)
        return response

    def get_vacancies(self, **kwargs):
        response = self.send_request(f"/vacancies", **kwargs)
        return response

    def get_vacancy(self, vacancy_id: int, **kwargs):
        response = self.send_request(f"/vacancies/{vacancy_id}", **kwargs)
        return response