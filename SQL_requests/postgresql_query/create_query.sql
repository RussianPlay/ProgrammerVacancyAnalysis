CREATE TABLE IF NOT EXISTS vacancies (
    id BIGINT PRIMARY KEY,
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