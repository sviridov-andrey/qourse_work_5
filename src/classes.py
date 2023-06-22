import os
import requests


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

        return self.vacansies

    def get_employers(self, count_employers=15):
        while len(self.employers) <= count_employers:
            for vac in self.vacansies:
                pass


