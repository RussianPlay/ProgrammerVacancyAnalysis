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
    %(name)s,
    %(city)s,
    %(salary_bottom)s,
    %(salary_top)s,
    %(currency)s,
    %(published_at)s,
    %(employer_name)s,
    %(key_skills)s,
    %(schedule)s,
    %(professional_role)s,
    %(experience)s
)