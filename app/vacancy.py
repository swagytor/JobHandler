from functools import total_ordering


@total_ordering
class Vacancy:
    """
    Класс вакансий
    Принимает:
    vacancy_id - ID вакансии
    title - название вакансии
    url - ссылка на вакансию
    city - город, в котором находится вакансия
    experience - требуемый опыт работы
    salary_info - информация об зарплате
    salary - информация об зарплате для вывода
    """
    def __init__(self, vacancy_id: str = None, title: str = None, url: str = None,
                 city: str = None, experience: str = None, salary_info: dict = None, salary=None):
        self.vacancy_id = vacancy_id
        self.title = title
        self.url = url
        self.city = city
        self.experience = experience
        self.salary_info = salary_info
        self.salary = self.__parse_salary()

    def __str__(self):
        return \
            f"Вакансия: {self.title}\n" \
            f"Город: {self.city}\n" \
            f"Ссылка: {self.url}\n" \
            f"Зарплата {self.salary}\n" \
            f"Опыт работы: {self.experience}\n"

    def __eq__(self, other):
        """
        Сравнивает среднее значение зарплаты между вакансиями
        """
        if issubclass(other.__class__, self.__class__):
            return (self.salary_info['to'] + self.salary_info['from']) / 2 \
                == (other.salary_info['to'] + other.salary_info['from']) / 2

    def __lt__(self, other):
        """
        Сравнивает среднее значение зарплаты между вакансиями
        """
        if issubclass(other.__class__, self.__class__):
            return (self.salary_info['to'] + self.salary_info['from']) / 2 \
                < (other.salary_info['to'] + other.salary_info['from']) / 2

    def __parse_salary(self):
        """
        Метод для получения информации об зарплате в формате строки
        :return: информацию об зарплате
        """
        if self.salary_info is None:
            self.salary_info = {'to': 0,
                                'from': 0,
                                'currency': None}
            salary = 'не указана'
        else:
            if self.salary_info.get('to') in (0, None):
                self.salary_info['to'] = self.salary_info.get('from')
                salary = f"от {self.salary_info['from']} {self.salary_info['currency']}"

            elif self.salary_info.get('from') in (0, None):
                self.salary_info['from'] = self.salary_info.get('to')
                salary = f"до {self.salary_info['to']} {self.salary_info['currency']}"

            else:
                salary = f"от {self.salary_info['from']} до {self.salary_info['to']} {self.salary_info['currency']}"

        return salary
