CREATE DATABASE hh; -- создание БД hh

CREATE TABLE employers (
employer_id SERIAL PRIMARY KEY,
employer_name VARCHAR(255)
);  -- создание таблицы employers

CREATE TABLE vacansies (
employer_id INT REFERENCES employers(employer_id),
vacansy VARCHAR,
salary INTEGER,
url VARCHAR
);  -- создание таблицы vacansies

DELETE FROM vacansies;   -- удаление всех строк из таблицы vacansies
DELETE FROM employers;   -- удаление всех строк из таблицы employers

INSERT INTO employers (employer_id, employer_name)
VALUES (%s, %s)
RETURNING employer_id;  -- запись данных в таблицу employers

INSERT INTO vacansies (employer_id, vacansy, salary, url)
VALUES (%s, %s, %s, %s)
RETURNING employer_id;  -- запись данных в таблицу vacansies

SELECT employer_name, COUNT(vacansy) AS count_vacansy
FROM employers JOIN vacansies USING(employer_id)
GROUP BY employer_name
ORDER BY count_vacansy DESC;  -- запрос для метода get_companies_and_vacancies_count класса DBManager

SELECT vacansy, employers.employer_name, salary, url
FROM vacansies
LEFT JOIN employers USING (employer_id);  -- запрос для метода get_all_vacancies класса DBManager

SELECT ROUND(AVG(salary), 2) FROM vacansies;  -- запрос для метода get_avg_salary класса DBManager

SELECT vacansy, employers.employer_name, salary, url
FROM vacansies left JOIN employers USING (employer_id)
WHERE salary > (SELECT ROUND(AVG(salary), 2) FROM vacansies);  -- запрос для метода get_vacancies_with_higher_salary класса DBManager

SELECT vacansy, employers.employer_name, salary, url
FROM vacansies left JOIN employers USING (employer_id)
WHERE LOWER(vacansy) IN ('{key_word}');   -- запрос для метода get_vacancies_with_keyword класса DBManager


