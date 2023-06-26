import requests

from abs.api_agent import APIAgent


class HeadHunterAPI(APIAgent):
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
    def get_vacancies(cls, vacancy_title=None):
        cls.params['text'] = vacancy_title

        vacancy_response = requests.get('https://api.hh.ru/vacancies', params=cls.params)

        parsed_response = [HeadHunterAPI.__parse_info(vacancy) for vacancy in vacancy_response.json()['items']]

        return parsed_response

    @staticmethod
    def __parse_info(vacancy_response):
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
