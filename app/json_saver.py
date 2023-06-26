import json
import os.path
from abs.saver import Saver
from app.utils import get_number, get_user_answer


class JSONSaver(Saver):
    __instance = None
    BASEDIR = os.path.abspath('')
    PATH_TO_DATA = os.path.join(BASEDIR, 'data')
    PATH_TO_JSON = os.path.join(PATH_TO_DATA, 'vacancies.json')

    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    @classmethod
    def __del__(cls):
        cls.__instance = None

    def add_vacancies(self, vacancies):
        data = self.load_vacancies()

        for vacancy in vacancies:
            data.append(vacancy.__dict__)

        with open(self.PATH_TO_JSON, mode='w', encoding='UTF-8') as file:
            json.dump(data, file, indent=2, ensure_ascii=False)

    def load_vacancies(self):
        if os.path.exists(self.PATH_TO_JSON):
            with open(self.PATH_TO_JSON, encoding='UTF-8') as json_file:
                try:
                    data = json.load(json_file)
                except json.decoder.JSONDecodeError:
                    data = []
            return data

    def clear_vacancies(self):
        if os.path.exists(self.PATH_TO_JSON):
            with open(self.PATH_TO_JSON, mode='w', encoding='UTF-8') as file:
                pass

        else:
            print('Файл отсутствует!')

    def show_history(self):
        json_data = self.load_vacancies()

        if json_data is None:
            return
        elif json_data:
            print('Выберите критерии просмотра вакансий\n'
                  '1. Без критериев\n'
                  '2. По зарплате\n')

            user_input = get_user_answer()

            if user_input == '1':
                resulting_search = json_data
            elif user_input == '2':
                resulting_search = self.get_vacancies_by_salary(json_data)

            return resulting_search

    def get_vacancies_by_salary(self, vacancy_data):
        print('Введите желаемую зарплату ОТ или просто нажмите ENTER')
        salary_from = get_number()

        print('Введите желаемую зарплату ДО или просто нажмите ENTER')
        user_input = get_number()
        salary_to = user_input if user_input else 1000000

        salary_sort = [data for data in vacancy_data if
                       salary_from < data['salary_info']['from'] and salary_to > data['salary_info']['to']]

        return salary_sort
