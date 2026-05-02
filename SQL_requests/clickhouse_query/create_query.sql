CREATE TABLE IF NOT EXISTS vacancies (
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