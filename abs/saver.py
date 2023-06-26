from abc import abstractmethod, ABC


class Saver(ABC):
    @abstractmethod
    def add_vacancies(self, vacancy):
        pass

    @abstractmethod
    def load_vacancies(self):
        pass

    @abstractmethod
    def clear_vacancies(self):
        pass

    @abstractmethod
    def show_history(self):
        pass
