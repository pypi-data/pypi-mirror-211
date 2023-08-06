# macronutrientes.py
from .estrategia import Estrategia
from .ganho_massa_muscular import GanhoMassaMuscular
from .perda_gordura import PerdaGordura
from .manutencao_peso import ManutencaoPeso
from .perda_peso_ganho_massa_muscular import PerdaPesoGanhoMassaMuscular

NOME_PARA_OBJETIVO = {
    "Ganho de Massa Muscular": GanhoMassaMuscular,
    "Perda de Gordura": PerdaGordura,
    "Manutenção do Peso": ManutencaoPeso,
    "Perto do Peso - Ganho de Massa Muscular": PerdaPesoGanhoMassaMuscular
}

OBJETIVOS = {
    1: GanhoMassaMuscular,
    2: PerdaGordura,  
    3: ManutencaoPeso,
    4: PerdaPesoGanhoMassaMuscular
}

def calcular_macronutrientes(peso, objetivo):
    if isinstance(objetivo, str):
        objetivo = NOME_PARA_OBJETIVO.get(objetivo)
        if objetivo is None:
            raise ValueError("Objetivo inválido")

    elif isinstance(objetivo, int):
        objetivo = OBJETIVOS.get(objetivo)
        if objetivo is None:
            raise ValueError("Objetivo inválido")

    estrategia = objetivo()  
    return estrategia.calcular_macronutrientes(peso)
