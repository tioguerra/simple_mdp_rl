

# -*- coding: utf-8 -*-
import random
import time
import json

# ----------------------------------------------------------------------------------
# DEFINIÇÃO DO AMBIENTE (O MESMO MDP DA SIMULAÇÃO ANTERIOR)
# ----------------------------------------------------------------------------------
# O agente irá interagir com este ambiente para aprender a política ótima.
# A estrutura é a mesma, representando as recompensas e as probabilidades de transição.

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
# HIPERPARÂMETROS DO Q-LEARNING
# ----------------------------------------------------------------------------------

# Alpha (α): Taxa de Aprendizado
# Controla o quão rápido o agente atualiza seus valores Q. Um valor alto faz com
# que o agente dê mais peso às novas informações, enquanto um valor baixo o torna
# mais conservador.
ALPHA = 0.1

# Gamma (γ): Fator de Desconto
# Determina a importância das recompensas futuras. Um valor próximo de 1 faz com
# que o agente se preocupe com o longo prazo, enquanto um valor próximo de 0 o
# torna "míope", focando apenas na recompensa imediata.
GAMMA = 0.9

# Epsilon (ε): Taxa de Exploração (para a política Epsilon-Guloso)
# Controla o equilíbrio entre "explorar" (tentar ações aleatórias para descobrir
# novas estratégias) e "explorar o que já sabe" (escolher a melhor ação conhecida).
# Um valor de 0.1 significa que 10% do tempo o agente fará uma ação aleatória.
EPSILON = 0.1

# Número de episódios de treinamento
# Um episódio é uma sequência de passos que o agente realiza no ambiente.
# Quanto mais episódios, mais o agente tem a chance de aprender.
NUM_EPISODIOS = 1000
PASSOS_POR_EPISODIO = 100

# ----------------------------------------------------------------------------------
# INICIALIZAÇÃO DA TABELA Q
# ----------------------------------------------------------------------------------
# A Tabela Q (Q-Table) é a "memória" do agente. Ela armazena o valor esperado
# (Qualidade) de se tomar uma determinada ação em um determinado estado.
# A estrutura é: Q[estado][acao] = valor
# Começamos com todos os valores em 0, pois o agente não sabe nada sobre o mundo.

q_table = {}
for estado in MDP:
    q_table[estado] = {}
    for acao in MDP[estado]:
        q_table[estado][acao] = 0.0

# ----------------------------------------------------------------------------------
# FUNÇÕES AUXILIARES
# ----------------------------------------------------------------------------------

def escolher_acao_epsilon_greedy(estado, q_table):
    """
    Escolhe uma ação usando a estratégia Epsilon-Guloso (ε-greedy).
    """
    # Decide se vai explorar ou usar o conhecimento atual
    if random.uniform(0, 1) < EPSILON:
        # --- MODO EXPLORAÇÃO ---
        # Escolhe uma ação aleatória dentre as disponíveis para o estado atual.
        return random.choice(list(MDP[estado].keys()))
    else:
        # --- MODO "GULOSO" (Exploitation) ---
        # Escolhe a melhor ação conhecida para o estado atual (a que tem o maior Q-valor).
        # A função max() com um dicionário como argumento retorna a chave com o maior valor.
        return max(q_table[estado], key=q_table[estado].get)

def simular_ambiente(estado, acao):
    """
    Simula a resposta do ambiente a uma ação.
    Retorna a recompensa e o próximo estado.
    """
    info_acao = MDP[estado][acao]
    recompensa = info_acao['recompensa']
    
    # Determina o próximo estado probabilisticamente
    transicoes = info_acao['transicoes']
    estados_proximos = [t['proximo_estado'] for t in transicoes]
    probabilidades = [t['prob'] for t in transicoes]
    proximo_estado = random.choices(estados_proximos, weights=probabilidades, k=1)[0]
    
    return recompensa, proximo_estado

# ----------------------------------------------------------------------------------
# LOOP PRINCIPAL DE TREINAMENTO DO Q-LEARNING
# ----------------------------------------------------------------------------------

print("Iniciando o treinamento com Q-Learning...")

for episodio in range(NUM_EPISODIOS):
    # No início de cada episódio, o agente começa do estado inicial.
    estado_atual = 's0'
    
    for passo in range(PASSOS_POR_EPISODIO):
        # 1. ESCOLHA DA AÇÃO
        # O agente escolhe a próxima ação com base no estado atual e na política ε-greedy.
        acao_escolhida = escolher_acao_epsilon_greedy(estado_atual, q_table)
        
        # 2. INTERAÇÃO COM O AMBIENTE
        # O agente executa a ação e observa o resultado (recompensa e novo estado).
        recompensa, proximo_estado = simular_ambiente(estado_atual, acao_escolhida)
        
        # 3. ATUALIZAÇÃO DA TABELA Q (O CORAÇÃO DO ALGORITMO)
        # Esta é a fórmula do Q-Learning:
        # Q(s,a) <- Q(s,a) + α * [r + γ * max_a'(Q(s',a')) - Q(s,a)]
        
        # Primeiro, pegamos o valor Q antigo para o par (estado, ação) atual.
        q_antigo = q_table[estado_atual][acao_escolhida]
        
        # Em seguida, encontramos o maior valor Q para o *próximo* estado.
        # Isso representa a melhor recompensa futura que o agente *espera* obter a partir de lá.
        max_q_futuro = max(q_table[proximo_estado].values())
        
        # Calculamos o novo valor Q.
        novo_q = q_antigo + ALPHA * (recompensa + GAMMA * max_q_futuro - q_antigo)
        
        # E finalmente, atualizamos a tabela com este novo valor aprendido.
        q_table[estado_atual][acao_escolhida] = novo_q
        
        # 4. ATUALIZAÇÃO DO ESTADO
        # O agente se move para o próximo estado para o passo seguinte.
        estado_atual = proximo_estado

    # Opcional: Imprimir o progresso a cada N episódios
    if (episodio + 1) % 100 == 0:
        print(f"Episódio {episodio + 1}/{NUM_EPISODIOS} concluído.")

print("\nTreinamento concluído!")

# ----------------------------------------------------------------------------------
# RESULTADOS FINAIS
# ----------------------------------------------------------------------------------

print("\nTabela Q Final (Valores de Qualidade aprendidos para cada par estado-ação):")
# Usamos json.dumps para uma impressão mais bonita do dicionário
print(json.dumps(q_table, indent=2))

# A política ótima é derivada diretamente da Tabela Q.
# Para cada estado, a melhor ação é aquela com o maior valor Q.
politica_otima = {}
for estado in q_table:
    politica_otima[estado] = max(q_table[estado], key=q_table[estado].get)

print("\nPolítica Ótima Aprendida (A melhor ação a ser tomada em cada estado):")
print(json.dumps(politica_otima, indent=2))
