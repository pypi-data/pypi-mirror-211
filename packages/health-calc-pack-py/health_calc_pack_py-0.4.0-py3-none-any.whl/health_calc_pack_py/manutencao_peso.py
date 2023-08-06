# estrategia ganho_massa_muscular.py
from .estrategia import Estrategia

class ManutencaoPeso(Estrategia):
    def calcular_macronutrientes(self, peso):
        return {
            "Carboidratos": 4 * peso,
            "Proteinas": 4 * peso,
            "Gorduras":  2 * peso
        }