Курсовая работа №5 Работа с базами данных 

Программа получает список вакансий с сайта HeadHanter. Создается база данных hh, таблицы employers и vacansies. 
Далее программа предлагает варианты обработки данных:
 1 - Вывести список всех компаний и количество вакансий у каждой компании
 2 - Вывести список всех вакансий с указанием названия компании,
     названия вакансии и зарплаты и ссылки на вакансию
 3 - Вывести среднюю зарплату по вакансиям
 4 - Вывести список всех вакансий, у которых зарплата выше средней по всем вакансиям
 5 - список всех вакансий, в названии которых содержится ключевое слово
 0 - Выход из программы

Виртуальное окружение venv
Запускающий модуль main.py
Последовательно запускаются методы get_response и get_vacansies класса HHGetEmployersVacansies. 
Создается список словарей с данными по актуальным вакансиям с API сайта hh.ru.
Запускаются методы create_database и create_tables - создается база данных hh и таблицы employers и vacansies.
Затем запускаются методы класса SaveTables. Метод delete_data_employers_vacansies удаляет все строки из таблиц employers и vacansies.
Методы save_data_to_employers и save_data_to_vacansies сохраняют данные в таблицы employers и vacansies соответственно.
Класс DBManager задействуется после выбора варианта обработки данных пользователем.
Метод get_companies_and_vacancies_count выводит список всех компаний и количество вакансий у каждой компании
Метод get_all_vacancies выводит список всех вакансий с указанием названия компании, названия вакансии и зарплаты и ссылки на вакансию
Метод get_avg_salary выводит среднюю зарплату по вакансиям
Метод get_vacancies_with_higher_salary выводит список всех вакансий, у которых зарплата выше средней по всем вакансиям
Метод get_vacancies_with_keyword выводит список всех вакансий, в названии которых содержатся переданные в метод слова

