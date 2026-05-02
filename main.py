# import requests
# import os
# from dotenv import load_dotenv
# url = "https://api.hh.ru/vacancies"
#
# load_dotenv()
#
# params = {
#     "text": "python разработчик",
#     "area": 1,
#     "per_page": 10,
#     "page": 0
# }
# access_token = os.getenv("ACCESS_TOKEN")
# headers = {
#     "Authorization": f"Bearer {access_token}",
#     "HH-User-Agent": "hh_course_project/1.0 (ahmadullin32@mail.ru)"
# }
# response = requests.get(url, headers=headers, params=params)
#
# print("Статус:", response.status_code)
#
# if response.status_code == 200:
#     data = response.json()
#     print(f"Найдено вакансий: {data.get('found')}")
#     for vacancy in data.get("items", []):
#         print(vacancy.get("name"), "-", vacancy.get("alternate_url"))
#         print(vacancy)
# else:
#     print("Ошибка:", response.text)
#


from data_collector.VacancyCollector import VacancyCollector
collector = VacancyCollector(target_vacancies_per_day=5)
vacancy_ids = collector.collect_vacancies()
print(len(vacancy_ids))