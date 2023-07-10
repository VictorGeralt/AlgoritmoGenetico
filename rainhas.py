import random
import time

inicio_contagem = time.time()

TAMANHO_POPULACAO = 100

MUTACAO = 0.1

MAX_GERACOES = 1000

TAMANHO_TABULEIRO = 8


def criar_individuo():
    return random.sample(range(1, TAMANHO_TABULEIRO + 1), TAMANHO_TABULEIRO)


def fitness(individuo):
    ataques = 0
    for i in range(len(individuo)):
        for j in range(i + 1, len(individuo)):
            if abs(individuo[i] - individuo[j]) == j - i:
                ataques += 1
            if individuo[i] == individuo[j]:
                ataques += 1
    return TAMANHO_TABULEIRO - ataques


def selecionar_pais(populacao):
    fitness_soma = sum(fitness(individuo) for individuo in populacao)
    pesos = [fitness(individuo) / fitness_soma for individuo in populacao]
    pais = random.choices(populacao, weights=pesos, k=2)
    return pais


def crossover(pais):
    crossover_point = random.randint(1, TAMANHO_TABULEIRO - 1)
    filho1 = pais[0][:crossover_point] + pais[1][crossover_point:]
    filho2 = pais[1][:crossover_point] + pais[0][crossover_point:]
    return filho1, filho2


def mutacao(individuo):
    if random.random() < MUTACAO:
        idx1, idx2 = random.sample(range(TAMANHO_TABULEIRO), 2)
        individuo[idx1], individuo[idx2] = individuo[idx2], individuo[idx1]


def criar_nova_populacao(populacao):
    nova_populacao = []
    nova_populacao.append(max(populacao, key=fitness))
    while len(nova_populacao) < TAMANHO_POPULACAO:
        pais = selecionar_pais(populacao)
        filhos = crossover(pais)
        for filho in filhos:
            mutacao(filho)
            nova_populacao.append(filho)
    return nova_populacao


def imprimir_tabuleiro(individuo):
    for linha in range(TAMANHO_TABULEIRO):
        valor = ""
        for coluna in range(TAMANHO_TABULEIRO):
            if individuo[coluna] == linha + 1:
                valor += " 1 "
            else:
                valor += " 0 "
        print(valor)
    print()

def main():
    populacao = [criar_individuo() for _ in range(TAMANHO_POPULACAO)]

    for geracao in range(MAX_GERACOES):
        melhor_individuo = max(populacao, key=fitness)
        print(f"Geração {geracao}: Ataques = {TAMANHO_TABULEIRO - fitness(melhor_individuo)}")
        imprimir_tabuleiro(melhor_individuo)
        if fitness(melhor_individuo) == TAMANHO_TABULEIRO:
            print("Solução ótima encontrada!")
            break
        populacao = criar_nova_populacao(populacao)

    fim_contagem = time.time()

    print(f"Solução: {melhor_individuo}")
    imprimir_tabuleiro(melhor_individuo)
    print(f"tempo de execução: {round(fim_contagem - inicio_contagem, 2)} segundos")
    print(f"ataques: {TAMANHO_TABULEIRO - fitness(melhor_individuo)}")
    
if __name__ == '__main__':
    main()

