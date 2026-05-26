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


# from data_collector.VacancyCollector import VacancyCollector
# collector = VacancyCollector(target_vacancies_per_day=5)
# vacancy_ids = collector.collect_vacancies()
# print(len(vacancy_ids))


import requests

client_id = "T0UT7PLJVSL453O29JRPLLHL8N1H8233BCB7OI9HJO3CIKITRFV0UO06R0GDCFNQ"
client_secret = "RUJPB2LCE4HDN2EF86R6KKH3M86FV5RSLQFRCGAEIHEHOLRUT6Q20Q4FQ8FAOOGV"
auth_code = "PHE8488PBQIJ4KMT4V56858EID4H7VN2BG99JRH2O1AQJ5SPUTNRT662IHEDSCUH"
redirect_uri = "http://localhost:8080"

url = "https://hh.ru/oauth/token"
body = {
        'grant_type': 'authorization_code',
        'client_id': client_id,
        'client_secret': client_secret,
        'code': auth_code,
        'redirect_uri': redirect_uri }

response = requests.post(url, data=body)
# {'access_token': 'USERI536KBQ5IL4LDQFLOV42CVF0UDQD8IVPC78UCTA46LEJ8DC113249OQ8UR63', 'token_type': 'bearer', 'refresh_token': 'USERP9QNS3EI7KGE5GTRJDGULTP2BM4KEQA7856A42RCOG9EC2G74EO7SBJMU50D', 'expires_in': 1209599}
tokens = response.json()
print(tokens)