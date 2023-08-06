# estrategia ganho_massa_muscular.py
from .estrategia import Estrategia

class PerdaPesoGanhoMassaMuscular(Estrategia):
    def calcular_macronutrientes(self, peso):
        return {
            "Carboidratos": 3.5 * peso,
            "Proteinas": 1.5 * peso,
            "Gorduras": 1 * peso
        }
