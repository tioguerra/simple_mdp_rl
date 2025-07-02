

# -*- coding: utf-8 -*-
import random
import time
import json

# ----------------------------------------------------------------------------------
# DEFINIÇÃO DO AMBIENTE (O MESMO MDP)
# ----------------------------------------------------------------------------------
# O agente SARSA irá interagir com este mesmo ambiente.
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
# HIPERPARÂMETROS DO SARSA
# ----------------------------------------------------------------------------------
# Os hiperparâmetros são os mesmos do Q-Learning.
ALPHA = 0.1
GAMMA = 0.9
EPSILON = 0.1
NUM_EPISODIOS = 1000
PASSOS_POR_EPISODIO = 100

# ----------------------------------------------------------------------------------
# INICIALIZAÇÃO DA TABELA Q
# ----------------------------------------------------------------------------------
# A Tabela Q é inicializada da mesma forma, com zeros.
q_table = {}
for estado in MDP:
    q_table[estado] = {}
    for acao in MDP[estado]:
        q_table[estado][acao] = 0.0

# ----------------------------------------------------------------------------------
# FUNÇÕES AUXILIARES (AS MESMAS DO Q-LEARNING)
# ----------------------------------------------------------------------------------

def escolher_acao_epsilon_greedy(estado, q_table):
    if random.uniform(0, 1) < EPSILON:
        return random.choice(list(MDP[estado].keys()))
    else:
        return max(q_table[estado], key=q_table[estado].get)

def simular_ambiente(estado, acao):
    info_acao = MDP[estado][acao]
    recompensa = info_acao['recompensa']
    transicoes = info_acao['transicoes']
    estados_proximos = [t['proximo_estado'] for t in transicoes]
    probabilidades = [t['prob'] for t in transicoes]
    proximo_estado = random.choices(estados_proximos, weights=probabilidades, k=1)[0]
    return recompensa, proximo_estado

# ----------------------------------------------------------------------------------
# LOOP PRINCIPAL DE TREINAMENTO DO SARSA
# ----------------------------------------------------------------------------------

print("Iniciando o treinamento com SARSA...")

for episodio in range(NUM_EPISODIOS):
    estado_atual = 's0'
    # No SARSA, a primeira ação é escolhida *antes* do loop de passos começar.
    acao_atual = escolher_acao_epsilon_greedy(estado_atual, q_table)
    
    for passo in range(PASSOS_POR_EPISODIO):
        # 1. INTERAÇÃO COM O AMBIENTE
        # O agente executa a ação já decidida e observa o resultado.
        recompensa, proximo_estado = simular_ambiente(estado_atual, acao_atual)
        
        # 2. ESCOLHA DA PRÓXIMA AÇÃO
        # O agente escolhe a *próxima* ação (a') com base no *próximo* estado (s').
        # Esta é a principal diferença para o Q-Learning. A ação futura influencia a atualização presente.
        proxima_acao = escolher_acao_epsilon_greedy(proximo_estado, q_table)
        
        # 3. ATUALIZAÇÃO DA TABELA Q (A REGRA DO SARSA)
        # Esta é a fórmula do SARSA:
        # Q(s,a) <- Q(s,a) + α * [r + γ * Q(s',a') - Q(s,a)]
        
        # Pegamos o valor Q antigo para o par (estado, ação) atual.
        q_antigo = q_table[estado_atual][acao_atual]
        
        # Pegamos o valor Q do par (proximo_estado, proxima_acao).
        # Note que NÃO usamos max(). Usamos o valor da ação que realmente será executada.
        # Isso torna o algoritmo "on-policy", pois ele aprende com base na sua própria política de ação.
        q_proximo = q_table[proximo_estado][proxima_acao]
        
        # Calculamos o novo valor Q.
        novo_q = q_antigo + ALPHA * (recompensa + GAMMA * q_proximo - q_antigo)
        
        # Atualizamos a tabela com este novo valor aprendido.
        q_table[estado_atual][acao_atual] = novo_q
        
        # 4. ATUALIZAÇÃO DO ESTADO E DA AÇÃO
        # O agente se move para o próximo estado e a próxima ação se torna a ação atual.
        estado_atual = proximo_estado
        acao_atual = proxima_acao

    if (episodio + 1) % 100 == 0:
        print(f"Episódio {episodio + 1}/{NUM_EPISODIOS} concluído.")

print("\nTreinamento concluído!")

# ----------------------------------------------------------------------------------
# RESULTADOS FINAIS
# ----------------------------------------------------------------------------------

print("\nTabela Q Final (Aprendida com SARSA):")
print(json.dumps(q_table, indent=2))

politica_aprendida = {}
for estado in q_table:
    politica_aprendida[estado] = max(q_table[estado], key=q_table[estado].get)

print("\nPolítica Aprendida (Derivada da Tabela Q do SARSA):")
print(json.dumps(politica_aprendida, indent=2))

