# estrategia ganho_massa_muscular.py
from .estrategia import Estrategia

class PerdaGordura(Estrategia):
    def calcular_macronutrientes(self, peso):
        return {
            "Carboidratos" : 3 * peso,
            "Proteinas" : 4 * peso,
            "Gorduras" : 3 * peso
        }
