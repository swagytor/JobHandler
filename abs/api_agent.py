from abc import ABC, abstractmethod
from pprint import pprint

import requests


class APIAgent(ABC):
    """
    Абстрактный класс для работы с API Агентами
    """
    @abstractmethod
    def get_vacancies(self, vacancy_title):
        pass
