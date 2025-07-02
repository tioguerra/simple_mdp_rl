# -*- coding: utf-8 -*-
import random
import time

# ----------------------------------------------------------------------------------
# DEFINIÇÃO DO PROCESSO DE DECISÃO MARKOVIANO (MDP)
# ----------------------------------------------------------------------------------
# A estrutura do MDP permanece a mesma, representando as recompensas e as
# probabilidades de transição (a dinâmica do ambiente).

MDP = {
    's0': {
        'a0': {
            'recompensa': 10,
            'transicoes': [
                {'proximo_estado': 's0', 'prob': 1.0}
            ]
        },
        'a1': {
            'recompensa': 40,
            'transicoes': [
                {'proximo_estado': 's1', 'prob': 0.8 / 0.9},
                {'proximo_estado': 's2', 'prob': 0.1 / 0.9}
            ]
        },
        'a2': {
            'recompensa': 0,
            'transicoes': [
                {'proximo_estado': 's1', 'prob': 1.0}
            ]
        }
    },
    's1': {
        'a0': {
            'recompensa': 0,
            'transicoes': [
                {'proximo_estado': 's0', 'prob': 1.0}
            ]
        },
        'a2': {
            'recompensa': -50,
            'transicoes': [
                {'proximo_estado': 's2', 'prob': 1.0}
            ]
        }
    },
    's2': {
        'a1': {
            'recompensa': 0,
            'transicoes': [
                {'proximo_estado': 's1', 'prob': 0.1 / 0.9},
                {'proximo_estado': 's2', 'prob': 0.8 / 0.9}
            ]
        }
    }
}

# ----------------------------------------------------------------------------------
# DEFINIÇÃO DA POLÍTICA ESTOCÁSTICA DO AGENTE
# ----------------------------------------------------------------------------------
# A política agora é estocástica, como representado no diagrama do MDP.
# Ela define a probabilidade de escolher cada ação em um determinado estado.
#
# NOTA IMPORTANTE SOBRE O GRAFO:
# Assim como nas transições, as probabilidades de escolha de ação no diagrama
# nem sempre somam 1.0. Por exemplo, em s0, as probabilidades para a0, a1 e a2
# são 0.7, 1.0 e 0.2, somando 1.9. Normalizamos esses valores para criar uma
# distribuição de probabilidade válida, preservando a proporção entre eles.

POLITICA_ESTOCASTICA = {
    's0': [
        {'acao': 'a0', 'prob': 0.7 / 1.9}, # Normalizado de 0.7 / (0.7+1.0+0.2)
        {'acao': 'a1', 'prob': 1.0 / 1.9}, # Normalizado de 1.0 / (0.7+1.0+0.2)
        {'acao': 'a2', 'prob': 0.2 / 1.9}  # Normalizado de 0.2 / (0.7+1.0+0.2)
    ],
    's1': [
        {'acao': 'a0', 'prob': 1.0 / 2.0}, # Normalizado de 1.0 / (1.0+1.0)
        {'acao': 'a2', 'prob': 1.0 / 2.0}  # Normalizado de 1.0 / (1.0+1.0)
    ],
    's2': [
        {'acao': 'a1', 'prob': 1.0} # Ação única, determinística
    ]
}

# ----------------------------------------------------------------------------------
# FUNÇÕES AUXILIARES
# ----------------------------------------------------------------------------------

def escolher_com_probabilidade(escolhas):
    """
    Função genérica para escolher um item com base em probabilidades.

    Args:
        escolhas (list): Lista de dicionários, cada um com uma chave para o item
                         (e.g., 'acao' ou 'proximo_estado') e uma chave 'prob'.

    Returns:
        O item escolhido.
    """
    # Extrai os itens e suas respectivas probabilidades
    itens = [item[key] for item in escolhas for key in item if key != 'prob']
    probabilidades = [item['prob'] for item in escolhas]

    # random.choices escolhe um elemento da lista com base nos pesos (probabilidades)
    return random.choices(itens, weights=probabilidades, k=1)[0]

# ----------------------------------------------------------------------------------
# SIMULAÇÃO PRINCIPAL
# ----------------------------------------------------------------------------------

def simular_mdp(estado_inicial, politica, num_passos):
    """
    Executa uma simulação passo a passo do agente no MDP.

    Args:
        estado_inicial (str): O estado onde a simulação começa.
        politica (dict): O dicionário da política estocástica a ser seguida.
        num_passos (int): O número de passos (transições) a simular.
    """
    estado_atual = estado_inicial
    recompensa_acumulada = 0

    print(f"Iniciando a simulação a partir do estado '{estado_inicial}' por {num_passos} passos.")
    print("Usando uma POLÍTICA ESTOCÁSTICA.")
    print("-" * 80)

    for passo in range(1, num_passos + 1):
        print(f"Passo {passo}:")

        # 1. Agente observa o estado atual
        print(f"  - Estado Atual: {estado_atual}")

        # 2. Agente usa a política para escolher uma ação PROBABILISTICAMENTE
        opcoes_acao = politica[estado_atual]
        acao_escolhida = escolher_com_probabilidade(opcoes_acao)
        print(f"  - Política estocástica para '{estado_atual}' levou à escolha da ação: '{acao_escolhida}'")

        # 3. Ambiente dá a recompensa pela ação tomada no estado atual
        info_acao = MDP[estado_atual][acao_escolhida]
        recompensa_imediata = info_acao['recompensa']
        recompensa_acumulada += recompensa_imediata
        print(f"  - Recompensa Imediata: {recompensa_imediata:+.2f}")
        print(f"  - Recompensa Acumulada: {recompensa_acumulada:+.2f}")

        # 4. Ambiente determina o próximo estado com base nas probabilidades
        transicoes = info_acao['transicoes']
        proximo_estado = escolher_com_probabilidade(transicoes)
        print(f"  - O ambiente determinou a transição para o estado: '{proximo_estado}'")

        # 5. O estado do agente é atualizado
        estado_atual = proximo_estado

        print("-" * 80)
        time.sleep(1) # Pausa para facilitar a leitura

    print("Simulação concluída.")

# --- Ponto de Entrada do Script ---
if __name__ == "__main__":
    ESTADO_INICIAL = 's0'
    NUMERO_DE_PASSOS = 20
    simular_mdp(ESTADO_INICIAL, POLITICA_ESTOCASTICA, NUMERO_DE_PASSOS)