from abc import ABC, abstractmethod


class APIAgent(ABC):
    """
    Абстрактный класс для работы с API Агентами
    """
    @abstractmethod
    def get_vacancies(self, vacancy_title):
        pass
