import os
import requests

api_key = os.getenv("SJ_API_KEY")


class SuperJobAPI:
    """
    Агент для работы с сайтом SuperJob.ru для получения вакансий
    """
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
    def get_vacancies(cls, vacancy_title: str = None) -> list[dict]:
        """
        Получает список вакансий, согласно заданным параметрам
        :param vacancy_title: название вакансии, которую будем искать
        :return: список с обобщённой информацией о вакансии
        """
        cls.params['keyword'] = vacancy_title
        # делаем запрос на hh.ru, чтобы получить список с данными вакансий
        response = requests.get('https://api.superjob.ru/2.0/vacancies/', headers=cls.headers, params=cls.params)
        # с помощью метода parse_info() преобразовываем информацию о вакансии в обобщённый вид
        parsed_response = [SuperJobAPI.__parse_info(vacancy) for vacancy in response.json()['objects']]

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
        parsed_response['title'] = vacancy_response['profession']
        parsed_response['url'] = vacancy_response['link']
        parsed_response['city'] = vacancy_response['town']['title']
        parsed_response['experience'] = vacancy_response['experience']['title']
        parsed_response['salary_info'] = {'from': vacancy_response['payment_from'],
                                          'to': vacancy_response['payment_to'],
                                          'currency': vacancy_response['currency'],
                                          }

        return parsed_response
