import requests

from abs.api_agent import APIAgent


class HeadHunterAPI(APIAgent):
    """
    Агент для работы с сайтом HH.ru для получения вакансий
    """
    __instance = None

    params = {'text': None,
              'area': 2,
              'page': 0,  # Индекс страницы поиска на HH
              'per_page': 50,
              }

    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    @classmethod
    def __del__(cls):
        cls.__instance = None

    @classmethod
    def get_vacancies(cls, vacancy_title: str = None) -> list[dict]:
        """
        Получает список вакансий, согласно заданным параметрам
        :param vacancy_title: название вакансии, которую будем искать
        :return: список с обобщённой информацией о вакансии
        """
        cls.params['text'] = vacancy_title

        # делаем запрос на hh.ru, чтобы получить список с данными вакансий
        vacancy_response = requests.get('https://api.hh.ru/vacancies', params=cls.params)
        # с помощью метода parse_info() преобразовываем информацию о вакансии в обобщённый вид
        parsed_response = [HeadHunterAPI.__parse_info(vacancy) for vacancy in vacancy_response.json()['items']]

        return parsed_response

    @staticmethod
    def __parse_info(vacancy_response: dict) -> dict:
        """
        Возвращает данные о вакансии в обобщенном виде
        :param vacancy_response: данные о вакансии
        :return: обобщённые данные о вакансии
        """
        parsed_response = {
            'vacancy_id': None,
            'title': None,
            'url': None,
            'city': None,
            'experience': None,
            'salary_info': None,
        }

        parsed_response['vacancy_id'] = vacancy_response['id']
        parsed_response['title'] = vacancy_response['name']
        parsed_response['url'] = f"https://hh.ru/vacancy/{vacancy_response['id']}"
        parsed_response['city'] = vacancy_response['area']['name']
        parsed_response['experience'] = vacancy_response['experience']['name']
        parsed_response['salary_info'] = vacancy_response['salary']

        return parsed_response
