from abc import ABC, abstractmethod
from pprint import pprint

import requests


class APIAgent(ABC):
    @abstractmethod
    def get_vacancies(self, vacancy_title):
        pass
