CREATE DATABASE base_vacancies;

CREATE TABLE employers
(
    employer_id SERIAL PRIMARY KEY,
    employer_name VARCHAR(255) NOT NULL,
    description TEXT,
    employer_url VARCHAR NOT NULL,
    url_vacancies VARCHAR(100) NOT NULL
);

CREATE TABLE vacancies
(
    vacancy_id SERIAL PRIMARY KEY,
    vacancy_name VARCHAR(255) NOT NULL,
    salary INT,
    vacancy_url VARCHAR NOT NULL,
    description TEXT,
    employer_id INTEGER NOT NULL,
    FOREIGN KEY (employer_id) REFERENCES employers (employer_id)
);

SELECT employer_name, COUNT(vacancy_id)
FROM employers
JOIN vacancies USING (employer_id) '
GROUP BY employer_name;

SELECT vacancy_name, employer_name, salary, vacancies.vacancy_url
FROM vacancies
JOIN employers USING (employer_id);

SELECT employer_name, ROUND(AVG(salary)) AS average_salary
FROM employers
JOIN vacancies USING (employer_id)
GROUP BY employer_name;

SELECT *
FROM vacancies
WHERE salary > (SELECT AVG(salary) FROM vacancies);

SELECT *
FROM vacancies
WHERE lower(vacancy_name) LIKE '%{keyword}%'
OR lower(vacancy_name) LIKE '%{keyword}'
OR lower(vacancy_name) LIKE '{keyword}%';
