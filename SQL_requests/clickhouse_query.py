create_vacancies = """
CREATE TABLE vacancies (
    id UUID DEFAULT generateUUIDv4,
    name String,
    city String,
    salary_bottom Nullable(Int32),
    salary_top Nullable(Int32),
    currency String,
    published_at DateTime,
    employer_name String,
    key_skills Nullable(String),
    schedule String,
    professional_role String,
    experience String
)
ENGINE = MergeTree ()
ORDER BY (published_at, professional_role, city)
"""

insert_data_to_vacancies = """
INSERT INTO vacancies (
    name,
    city,
    salary_bottom,
    salary_top,
    currency,
    published_at,
    employer_name,
    key_skills,
    schedule,
    professional_role,
    experience
)
VALUES (
    %(id)%,
    %(name)%,
    %(city)%,
    %(salary_bottom)%,
    %(salary_top)%,
    %(currency)%,
    %(published_at)%,
    %(employer_name)%,
    %(key_skills)%,
    %(schedule)%,
    %(professional_role)%,
    %(experience)%
)
"""

salary_by_role = """
SELECT 
    professional_role, 
    salary_bottom, 
    salary_top, 
    currency, 
    COUNT() OVER (PARTITION BY professional_role) as amount_roles
FROM vacancies 
WHERE
currency = 'RUR' AND salary_bottom IS NOT NULL AND salary_top IS NOT NULL
"""

drop_vacancies = """
DROP TABLE IF EXISTS vacancies
"""