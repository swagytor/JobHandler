import os
import requests
from pprint import pprint
from html2text import html2text

api_key = os.getenv("SJ_API_KEY")


# print(api_key)


class SuperJobAPI:
    __instance = None

    headers = {'X-Api-App-Id': api_key}

    params = {'keyword': None,
              'town': 'Санкт-Петербург',
              'page': 0,
              "count": 50
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
        cls.params['keyword'] = vacancy_title

        response = requests.get('https://api.superjob.ru/2.0/vacancies/', headers=cls.headers, params=cls.params)

        parsed_response = [SuperJobAPI.__parse_info(vacancy) for vacancy in response.json()['objects']]

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
        parsed_response['title'] = vacancy_response['profession']
        parsed_response['url'] = vacancy_response['link']
        parsed_response['city'] = vacancy_response['town']['title']
        parsed_response['experience'] = vacancy_response['experience']['title']
        parsed_response['salary_info'] = {'from': vacancy_response['payment_from'],
                                          'to': vacancy_response['payment_to'],
                                          'currency': vacancy_response['currency'],
                                          }

        return parsed_response
