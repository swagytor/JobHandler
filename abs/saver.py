from abc import abstractmethod, ABC


class Saver(ABC):
    @abstractmethod
    def add_vacancies(self, vacancy):
        """
        Добавляет вакансии в JSON-файл
        :param vacancy:
        :return:
        """
        pass

    @abstractmethod
    def load_vacancies(self):
        pass

    @abstractmethod
    def clear_vacancies(self):
        pass

    @abstractmethod
    def get_vacancies_by_salary(self, vacancy_data):
        pass

    @abstractmethod
    def show_history(self):
        pass
