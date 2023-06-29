from src.classes import HHGetEmployersVacansies, CreateDatabaseTables, SaveTables, DBManager


def main():

    input(f"""
     \n     Здравствуйте!
     Данная программа составит список последних актуальных вакансий с сайта hh.ru
     Для продолжения нажмите ENTER""")

    hh = HHGetEmployersVacansies()
    vacansies = hh.get_vacansies()
    CreateDatabaseTables().create_database()
    CreateDatabaseTables().create_tables()
    SaveTables().delete_data_employers_vacansies()
    SaveTables().save_data_to_employers(vacansies)
    SaveTables().save_data_to_vacansies(vacansies)

    while True:
        choise = input(f"""
        Выберите один из вариантов:
        1 - Вывести список всех компаний и количество вакансий у каждой компании
        2 - Вывести список всех вакансий с указанием названия компании,
            названия вакансии и зарплаты и ссылки на вакансию
        3 - Вывести среднюю зарплату по вакансиям
        4 - Вывести список всех вакансий, у которых зарплата выше средней по всем вакансиям
        5 - список всех вакансий, в названии которых содержится ключевое слово
        0 - Выход из программы \n
        """)

        if choise == '1':
            DBManager().get_companies_and_vacancies_count()
        elif choise == '2':
            DBManager().get_all_vacancies()
        elif choise == '3':
            DBManager().get_avg_salary()
        elif choise == '4':
            DBManager().get_vacancies_with_higher_salary()
        elif choise == '5':
            DBManager().get_vacancies_with_keyword()
        elif choise == '0':
            print("     До свидания!")
            break
        else:
            print('Недопустимый ввод!')


if __name__ == '__main__':
    main()
