import psycopg2
import requests
from config import config


class HHGetEmployersVacansies():
    """Получает инфорацию API о работодателях и вакансиях с сайта HH"""

    def __init__(self):
        self.vacansies = []
        self.employers = []
        self.__api_str = "https://api.hh.ru/vacancies"
        self.__first_key = 'items'
        self.__header = ''
        self.__param = {"text": '',
                        "page": 0,
                        "per_page": 100
                        }

    @property
    def get_api_str(self):
        return self.__api_str

    @property
    def get_first_key(self):
        return self.__first_key

    @property
    def get_header(self):
        return self.__header

    @property
    def get_param(self):
        return self.__param

    def get_response(self) -> list[dict]:
        """Парсинг одной страницы с вакансиями"""

        response = requests.get(self.get_api_str,
                                headers=self.get_header, params=self.get_param)
        if response.status_code == 200:
            return response.json()[self.get_first_key]

    def get_vacansies(self, count_page=10) -> list[dict]:
        """Получение списка вакансий"""

        while self.__param['page'] < count_page:
            one_page_vacansies = self.get_response()
            if one_page_vacansies is not None:
                self.vacansies.extend(one_page_vacansies)
                self.__param['page'] += 1
            else:
                print(f'Страница {self.__param["page"] + 1} ошибка получения данных')
                break

        print('\nСписок вакансий получен')

        return self.vacansies


class CreateDatabaseTables():
    """Создание базу данных HH и таблиц employers и vacansies"""

    def __init__(self):
        self.params = config()

    def create_database(self) -> None:
        """Создает базу данных HH"""
        conn = psycopg2.connect(dbname='postgres', **self.params)
        conn.autocommit = True
        cur = conn.cursor()

        try:
            cur.execute(f"CREATE DATABASE hh;")
            print('База данных hh создана')
        except:
            print('База данных hh найдена')

        cur.close()
        conn.close()

    def create_tables(self) -> None:
        """Создает таблицы employers и vacansies"""

        conn = psycopg2.connect(dbname='hh', **self.params)

        with conn.cursor() as cur:
            try:
                cur.execute("""
                CREATE TABLE employers (
                employer_id SERIAL PRIMARY KEY,
                employer_name VARCHAR(255)
                );            
                """)
                print('Таблица employers создана')
            except:
                print('Таблица employers найдена')

        with conn.cursor() as cur:
            try:
                cur.execute("""
                CREATE TABLE vacansies (
                employer_id INT REFERENCES employers(employer_id),                
                vacansy VARCHAR,
                salary INTEGER,
                url VARCHAR
                );
                """)
                print('Таблица vacansies создана')
            except:
                print('Таблица vacansies найдена')

        conn.commit()
        conn.close()


class SaveTables():
    """Сохраняет данные в таблицы employers и vacansies"""

    def __init__(self):
        self.params = config()
        self.employers_id = []

    def delete_data_employers_vacansies(self) -> None:
        """Удаляет предыдущие записи из таблиц employers и vacansies перед записью новых данных"""

        conn = psycopg2.connect(dbname='hh', **self.params)

        with conn.cursor() as cur:
            cur.execute("""DELETE FROM vacansies;""")
            cur.execute("""DELETE FROM employers;""")

        conn.commit()
        conn.close()


    def save_data_to_employers(self, vacansies):
        """Сохранение данных в таблицу employers"""

        conn = psycopg2.connect(dbname='hh', **self.params)

        with conn.cursor() as cur:
            for emp in vacansies:
                try:
                    if emp['employer']['id'] not in self.employers_id:
                        self.employers_id.append(emp['employer']['id'])
                        cur.execute("""
                        INSERT INTO employers (employer_id, employer_name)
                        VALUES (%s, %s)
                        RETURNING employer_id;
                        """,
                        (emp['employer']['id'], emp['employer']['name'])
                                    )
                    else:
                        continue
                except:
                        continue

            print('Таблица employers заполнена')

        conn.commit()
        conn.close()

    def save_data_to_vacansies(self, vacansies) -> None:
        """Сохранение данных в таблицу vacansies"""

        conn = psycopg2.connect(dbname='hh', **self.params)

        with conn.cursor() as cur:
            for vac in vacansies:
                if vac['salary'] is None:
                    continue
                elif vac['salary']['currency'] not in 'RUR':
                    continue
                elif vac['salary']['from'] is None and vac['salary']['to'] is not None:
                    salary = int(vac['salary']['to'])
                elif vac['salary']['from'] is not None and vac['salary']['to'] is None:
                    salary = int(vac['salary']['from'])
                else:
                    salary = (int(vac['salary']['from']) + int(vac['salary']['to'])) / 2

                try:
                    cur.execute(
                        """
                        INSERT INTO vacansies (employer_id, vacansy, salary, url)
                        VALUES (%s, %s, %s, %s)
                        RETURNING employer_id;
                        """,
                        (vac['employer']['id'], vac['name'], salary, vac['alternate_url'])
                    )
                except:
                    continue

            print('Таблица vacansies заполнена')

        conn.commit()
        conn.close()


class DBManager():
    """Выводит данные из таблиц employers и vacansies"""

    def __init__(self):
        self.params = config()

    def get_companies_and_vacancies_count(self) -> None:
        """Получает список всех компаний и количество вакансий у каждой компании"""

        conn = psycopg2.connect(dbname='hh', **self.params)

        with conn.cursor() as cur:
            cur.execute("""
            SELECT employer_name, COUNT(vacansy) AS count_vacansy 
            FROM employers JOIN vacansies USING(employer_id) 
            GROUP BY employer_name 
            ORDER BY count_vacansy DESC;
            """)
            results = cur.fetchall()

        conn.commit()
        conn.close()

        for res in results:
            print(f"Работодатель: '{res[0]}' ->  вакансий: {res[1]}")

    def get_all_vacancies(self) -> None:
        """получает список всех вакансий с указанием названия компании,
        названия вакансии и зарплаты и ссылки на вакансию"""

        conn = psycopg2.connect(dbname='hh', **self.params)

        with conn.cursor() as cur:
            cur.execute("""
            SELECT vacansy, employers.employer_name, salary, url 
            FROM vacansies 
            LEFT JOIN employers USING (employer_id);
            """)
            results = cur.fetchall()

        conn.commit()
        conn.close()

        for res in results:
            print(f"Вакансия: {res[0]}   Работодатель: '{res[1]}'   Зарплата: {res[2]} руб   URL: {res[3]}")

    def get_avg_salary(self) -> None:
        """получает среднюю зарплату по вакансиям"""

        conn = psycopg2.connect(dbname='hh', **self.params)

        with conn.cursor() as cur:
            cur.execute("SELECT ROUND(AVG(salary), 2) FROM vacansies;")
            results = cur.fetchone()

        conn.commit()
        conn.close()

        print(f"Средняя зарплата в рублях составляет:", *results)

    def get_vacancies_with_higher_salary(self) -> None:
        """получает список всех вакансий, у которых зарплата выше средней по всем вакансиям"""

        conn = psycopg2.connect(dbname='hh', **self.params)

        with conn.cursor() as cur:
            cur.execute("""
                    SELECT vacansy, employers.employer_name, salary, url 
                    FROM vacansies left JOIN employers USING (employer_id) 
                    WHERE salary > (SELECT ROUND(AVG(salary), 2) FROM vacansies); 
                    """)
            results = cur.fetchall()

        conn.commit()
        conn.close()

        for res in results:
            print(f"Вакансия: {res[0]}   Работодатель: '{res[1]}'   Зарплата: {res[2]} руб   URL: {res[3]}")

    def get_vacancies_with_keyword(self) -> None:
        """получает список всех вакансий, в названии которых содержатся переданные в метод слова"""

        conn = psycopg2.connect(dbname='hh', **self.params)

        key_word = input("Введите ключевое слово: ").lower()

        with conn.cursor() as cur:
            cur.execute(f"""
                            SELECT vacansy, employers.employer_name, salary, url 
                            FROM vacansies left JOIN employers USING (employer_id) 
                            WHERE LOWER(vacansy) IN ('{key_word}'); 
                            """)
            results = cur.fetchall()

        conn.commit()
        conn.close()

        if len(results) == 0:
            print('По данному запросу вакансии не найдены')
        else:
            for res in results:
                print(f"Вакансия: {res[0]}   Работодатель: '{res[1]}'   Зарплата: {res[2]} руб   URL: {res[3]}")
