# estrategia ganho_massa_muscular.py
from .estrategia import Estrategia

class GanhoMassaMuscular(Estrategia):
    def calcular_macronutrientes(self, peso):
        return {
            "Carboidratos": 4 * peso,
            "Proteinas": 2 * peso,
            "Gorduras": 1 * peso
        }
