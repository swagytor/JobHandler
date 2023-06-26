from abc import abstractmethod, ABC


class Saver(ABC):
    @abstractmethod
    def add_vacancies(self, vacancy):
        """
        Добавляет вакансии в JSON-файл
        :param vacancy: список с вакансиями
        """
        pass

    @abstractmethod
    def load_vacancies(self):
        """
        Возвращает данные об вакансиях из JSON-файла
        """
        pass

    @abstractmethod
    def clear_vacancies(self):
        """
        Очищает файл с вакансиями
        """
        pass

    @abstractmethod
    def get_vacancies_by_salary(self, vacancy_data):
        """
        Возвращает список вакансий с фильтром по зарплате
        :param vacancy_data: данные по вакансиям
        """
        pass

    @abstractmethod
    def show_history(self):
        """
        Возвращает недавно просмотренные вакансии по критериям
        """
        pass
