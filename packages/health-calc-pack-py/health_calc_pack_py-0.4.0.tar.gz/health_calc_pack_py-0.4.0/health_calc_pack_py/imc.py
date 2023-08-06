# Constantes
MAGREZA_FAIXA1 = 18.5
NORMAL_FAIXA1 = 18.5
NORMAL_FAIXA2 = 24.9
SOBREPESO_FAIXA1 = 24.9
SOBREPESO_FAIXA2 = 29.9
OBESIDADE_FAIXA1 = 29.9
OBESIDADE_FAIXA2 = 39.9
GRAVE_FAIXA1 = 39.9

# Legendas
MAGREZA = "Magreza"
NORMAL = "Normal"
SOBREPESO = "Sobrepeso"
OBESIDADE = "Obesidade"
GRAVE = "Grave"
VALOR_PADRAO = "Invalido"

def calcular_imc(peso: float, altura: float) -> dict:
    imc = peso / (altura ** 2)
    imc = round(imc, 2)

    # Classificação do IMC
    if imc < MAGREZA_FAIXA1:
        classificacao = MAGREZA
    elif NORMAL_FAIXA1 <= imc < NORMAL_FAIXA2:
        classificacao = NORMAL
    elif SOBREPESO_FAIXA1 <= imc < SOBREPESO_FAIXA2:
        classificacao = SOBREPESO
    elif OBESIDADE_FAIXA1 <= imc < OBESIDADE_FAIXA2:
        classificacao = OBESIDADE
    elif imc >= GRAVE_FAIXA1:
        classificacao = GRAVE
    else:
        classificacao = VALOR_PADRAO

    return {"IMC": imc, "classificacao": classificacao}