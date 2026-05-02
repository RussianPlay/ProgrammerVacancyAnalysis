SELECT
    professional_role,
    salary_bottom,
    salary_top,
    currency,
    COUNT() OVER (PARTITION BY professional_role) as amount_roles
FROM vacancies
WHERE
currency = 'RUR' AND salary_bottom IS NOT NULL AND salary_top IS NOT NULL