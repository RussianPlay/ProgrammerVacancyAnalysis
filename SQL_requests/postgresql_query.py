#     id: int
#     name: str
#     city: str | None
#     salary_bottom: int | float | str | None
#     salary_top: int | float | str | None
#     currency: str | None
#     published_at: str
#     employer_name: str
#     key_skills: str | None
#     schedule: str
#     professional_role: str
#     professional_role_id: str
#     experience: str
create_query = '''
CREATE TABLE IF NOT EXISTS vacancies (
id INTEGER PRIMARY KEY,
name VARCHAR,
city VARCHAR,
salary_bottom VARCHAR,
salary_top VARCHAR,
currency VARCHAR,
published_at VARCHAR,
employer_name VARCHAR,
key_skills VARCHAR,
schedule VARCHAR,
professional_role VARCHAR,
experience VARCHAR
)
'''

insert_query = '''
INSERT INTO vacancies VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
'''


# '''
# CREATE TABLE vacancies_clean AS
# SELECT
# 	id,
# 	trim(BOTH '"' FROM NULLIF(name, '"None"')) AS name,
# 	trim(BOTH '"' FROM NULLIF(city, '"None"')) AS city,
# 	trim(BOTH '"' FROM NULLIF(salary_bottom, '"None"'))::INTEGER as salary_bottom,
# 	trim(BOTH '"' FROM NULLIF(salary_top, '"None"'))::INTEGER as salary_top,
# 	trim(BOTH '"' FROM NULLIF(currency, '"None"')) AS currency,
# 	trim(BOTH '"' FROM NULLIF(published_at, '"None"'))::TIMESTAMPTZ AS published_at,
# 	trim(BOTH '"' FROM NULLIF(employer_name, '"None"')) AS employer_name,
# 	trim(BOTH '"' FROM NULLIF(key_skills, '"None"')) AS key_skills,
# 	trim(BOTH '"' FROM NULLIF(schedule, '"None"')) AS schedule,
# 	trim(BOTH '"' FROM NULLIF(professional_role, '"None"')) AS professional_role,
# 	trim(BOTH '"' FROM NULLIF(experience, '"None"')) AS experience
# FROM vacancies
# '''

