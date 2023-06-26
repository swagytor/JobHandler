import json
import os.path
from abs.saver import Saver
from app.utils import get_number, get_user_answer
from app.vacancy import Vacancy


class JSONSaver(Saver):
    """
    Класс для работы с JSON-файлами
    """
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

    def add_vacancies(self, vacancies: list[Vacancy]):
        """
        Добавляет новые вакансии в старый файл
        :param vacancies: список с экземплярами класса
        """
        # считываем информацию с файла
        data = self.load_vacancies()

        # заносим атрибуты каждого экземпляра в список
        for vacancy in vacancies:
            data.append(vacancy.__dict__)

        # перезаписываем старые данные на новые
        with open(self.PATH_TO_JSON, mode='w', encoding='UTF-8') as file:
            json.dump(data, file, indent=2, ensure_ascii=False)

    def load_vacancies(self) -> list:
        """
        Загружает данные из JSON-файла
        :return: список с данными
        """
        if os.path.exists(self.PATH_TO_JSON):
            with open(self.PATH_TO_JSON, encoding='UTF-8') as json_file:
                try:
                    data = json.load(json_file)
                except json.decoder.JSONDecodeError:
                    data = []
        else:
            data = []
        return data

    def clear_vacancies(self):
        """
        Очищает JSON-файл от данных
        :return:
        """
        if os.path.exists(self.PATH_TO_JSON):
            with open(self.PATH_TO_JSON, mode='w', encoding='UTF-8') as file:
                pass

        else:
            print('Файл отсутствует!')

    def show_history(self) -> list[dict] | None:
        """
        Показывает сохранённые вакансии, с возможностью установить критерии просмотра
        :return:
        """
        json_data = self.load_vacancies()

        if json_data is None:
            return None
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

    def get_vacancies_by_salary(self, vacancy_data: list[dict]) -> list[dict]:
        """
        Возвращает вакансии, которые совпадают по критериям зарплаты
        :param vacancy_data: данные о вакансиях
        :return: данные о вакансиях, с совпадающими критериями
        """
        print('Введите желаемую зарплату ОТ или просто нажмите ENTER')
        salary_from = get_number()

        print('Введите желаемую зарплату ДО или просто нажмите ENTER')
        user_input = get_number()
        salary_to = user_input if user_input else 1000000

        salary_sort = [data for data in vacancy_data if
                       salary_from < data['salary_info']['from'] and salary_to > data['salary_info']['to']]

        return salary_sort
