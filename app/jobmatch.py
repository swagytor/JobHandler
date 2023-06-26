import requests
import os.path
from app.api_hh import HeadHunterAPI
from app.api_sj import SuperJobAPI
from app.json_saver import JSONSaver
from app.utils import get_user_answer
from app.vacancy import Vacancy

BASEDIR = os.path.abspath('..')
PATH_TO_DATA = os.path.join(BASEDIR, 'data')
PATH_TO_JSON = os.path.join(PATH_TO_DATA, 'vacancies.json')
PLATFORMS = ("HeadHunter", "SuperJob")
STOP_COMMANDS = ('0', 'stop', 'стоп', 'флюгегехаймен')

headhunter_api = HeadHunterAPI()
superjob_api = SuperJobAPI()
json_saver = JSONSaver()


def get_vacancies(founded_vacancies):
    list_of_vacancies = [Vacancy(**vac) for vac in founded_vacancies]
    vacancies_amount = len(list_of_vacancies)
    print(f'По вашему запросу найдено {vacancies_amount} вакансий, сколько вам показать?')

    while True:
        user_input = input('Введите количество вакансий, не превышающее количество найденных вакансий: ')
        if user_input.isdigit() and int(user_input) <= vacancies_amount:
            top_n = int(user_input)
            break
        print('Необходимо ввести натуральное число, не превышающее количество найденных вакансий!')

    print('Как отсортировать вакансии?\n'
          '1. По популярности\n'
          '2. По зарплате\n')

    user_input = get_user_answer()
    if user_input == '1':
        filtered_vacancies = list_of_vacancies
    elif user_input == '2':
        filtered_vacancies = sorted(list_of_vacancies, reverse=True)

    return filtered_vacancies[:top_n]


def find_vacancies():
    vacancy_title = input('Введите название вакансии, которую будем искать:\n')
    print('Где вы хотите искать вакансию?\n'
          '1. HeadHunter\n'
          '2. SuperJob\n'
          '3. Везде\n')

    user_input = input('Введите команду:\n')

    if user_input == '1':
        vacancies = headhunter_api.get_vacancies(vacancy_title)
    elif user_input == '2':
        vacancies = superjob_api.get_vacancies(vacancy_title)
    elif user_input == '3':
        hh_vacancies = headhunter_api.get_vacancies(vacancy_title)
        sj_vacancies = superjob_api.get_vacancies(vacancy_title)
        vacancies = hh_vacancies + sj_vacancies
    else:
        print('Неизвестная команда, возврат в главное меню!\n')
        return

    return vacancies


def jobmatch():
    founded_vacancies = find_vacancies()
    if founded_vacancies is None:
        return
    elif not founded_vacancies:
        print('К сожалению, по вашему запросу ничего не было найдено!\n'
              'Смените город поиска или название вакансии\n')
    elif founded_vacancies:
        filtered_vacancies = get_vacancies(founded_vacancies)

        for vac in filtered_vacancies:
            print(vac)

        print('Хотите записать результаты поиска в отдельный файл?\n'
              '1. Да\n'
              '2. Нет\n')

        user_input = get_user_answer()

        if user_input == '1':
            json_saver.add_vacancies(filtered_vacancies)


def change_city_search():
    city_name = 'Санкт-Петербург'

    user_input = input('Введите название города, где искать вакансию: ').title()
    if not user_input or user_input.isdigit():
        print('Вы не указали корректное название города!')
    elif user_input.isalpha():
        try:
            HeadHunterAPI.params['area'] = requests.get(f'https://api.hh.ru/suggests/areas?text={user_input}'
                                                        ).json()['items'][0]['id']
            SuperJobAPI.params['town'] = user_input
            city_name = user_input

        except IndexError:
            print('Вы не указали корректное название города!')
            HeadHunterAPI.params['area'] = requests.get(f'https://api.hh.ru/suggests/areas?text={city_name}'
                                                        ).json()['items'][0]['id']
            SuperJobAPI.params['town'] = city_name

    print(f'Будем искать вакансии по городу - {city_name}\n')

    return city_name


def search_history():
    print('Что вы хотите сделать?\n'
          '1. Посмотреть историю поиска\n'
          '2. Стереть историю поиска\n')
    user_input = get_user_answer()

    if user_input == '1':
        selected_history = json_saver.show_history()
        if selected_history is None:
            return None
        elif selected_history:
            return [Vacancy(**data) for data in selected_history]

    elif user_input == '2':
        json_saver.clear_vacancies()


def user_interaction():
    city_search = change_city_search()

    while True:
        print(f'Город поиска: {city_search}\n'
              'Выберите команду:\n'
              '0. Выйти\n'
              '1. Искать вакансии\n'
              '2. Сменить город\n'
              '3. История поиска\n')

        user_input = input('Введите команду:\n').lower()

        if user_input in STOP_COMMANDS:
            print('Выход из приложения')
            return

        elif user_input == '1':
            jobmatch()

        elif user_input == '2':
            city_search = change_city_search()

        elif user_input == '3':
            search = search_history()
            if search is None:
                print('История пуста!\n')
            elif not search:
                print('Ничего не найдено по данному запросу, смените критерии поиска и повторите попытку\n')
            elif search:
                for vacancy in search:
                    print(vacancy)

        else:
            print('Неизвестная команда!\n')
