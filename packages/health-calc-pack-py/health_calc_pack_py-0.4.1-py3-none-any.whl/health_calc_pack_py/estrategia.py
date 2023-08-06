# estrategia.py
from abc import ABC, abstractmethod

class Estrategia(ABC):
    @abstractmethod
    def calcular_macronutrientes(self, peso):
        pass
