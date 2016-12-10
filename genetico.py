import random
import functions as f
import parameters as p
import heapq
import itertools


def iniciaPopulacao(tam_pop):
    populacao_local = []
    populacao_direcao = []
    inicial_place = (0, 0)
    inicial_place_center = (p.SQUARE_SIZE // 2, p.SQUARE_SIZE // 2)
    populacao_cor = []

    for individuo in range(0, tam_pop):
        populacao_local.append([])
        populacao_direcao.append([])
        r = lambda: random.randint(0, 255)
        populacao_cor.append((r(), r(), r()))
        populacao_local[individuo].append(inicial_place)
        populacao_local[individuo].append(inicial_place_center)
        for x in range(0, p.STEPS):
            local_atual = populacao_local[individuo][-1]
            local_anterior = populacao_local[individuo][-2]
            passo = f.geraPasso(local_atual, local_anterior)
            populacao_local[individuo].append(passo[0])
            populacao_direcao[individuo].append(passo[1])
    return populacao_local, populacao_cor, populacao_direcao


def avalia(populacao, local_coin):
    pontuacao = 0
    fitness = []
    local_coin_aux = list(local_coin)
    for ind in range(0, p.TAM_POP):
        for ponto in range(0, p.STEPS):
            ponto_para_encontrar = ((populacao[ind][ponto][0]-p.SQUARE_SIZE//2), (populacao[ind][ponto][1]-p.SQUARE_SIZE//2))
            encontrou_ponto = local_coin_aux.count(ponto_para_encontrar)
            if encontrou_ponto >= 1:
                del local_coin_aux[local_coin_aux.index(ponto_para_encontrar)]
                pontuacao += 1
        fitness.append(pontuacao)
        pontuacao = 0
        local_coin_aux = list(local_coin)
    return fitness


def crossover(populacao_direcao, fitness):

    # Cria tuplas com o (fitness,numero) dos n melhores individuos, populaçao/2
    melhores_tupla = heapq.nlargest((p.TAM_POP // 2), zip(fitness, itertools.count()))
    populacao_nova = []
    populacao_xy = []
    pais = []
    for ind in range(0, p.TAM_POP):
        if (fitness[ind], ind) in melhores_tupla:
            pais.append(populacao_direcao[ind])
            populacao_nova.append(populacao_direcao[ind])

    for ind in range(0, (p.TAM_POP // 2)):
        novo_ind = []
        for step in range(0, (p.STEPS // 2)):
            if ind + 1 >= (p.TAM_POP // 2):
                novo_ind.append(pais[ind][step])
                novo_ind.append(pais[0][step])
            else:
                novo_ind.append(pais[ind][step])
                novo_ind.append(pais[ind + 1][step])
        populacao_nova.append(novo_ind)

    for ind in range(0, p.TAM_POP):
        individuo_xy, individuo_direcao = f.pontos_a_partir_de_direcoes(populacao_nova[ind])
        populacao_xy.append(individuo_xy)
        populacao_nova[ind] = individuo_direcao

    return populacao_nova, populacao_xy


def mutacao(populacao_direcao, populacao_xy, fitness):
    # Pega o pior individuo e refaz randomicamente
    pior_individuo = heapq.nsmallest(1, zip(fitness, itertools.count()))
    indice_pior_individuo = pior_individuo[0][1]

    pior_individuo_xy = []
    pior_individuo_direcao = []
    pior_individuo_xy.append((0, 0))
    pior_individuo_xy.append((p.SQUARE_SIZE // 2, p.SQUARE_SIZE // 2))

    for x in range(0, p.STEPS):
        local_anterior = pior_individuo_xy[-2]
        local_atual = pior_individuo_xy[-1]

        passo = f.geraPasso(local_atual, local_anterior)
        pior_individuo_xy.append(passo[0])
        pior_individuo_direcao.append(passo[1])

    populacao_xy[indice_pior_individuo] = pior_individuo_xy
    populacao_direcao[indice_pior_individuo] = pior_individuo_direcao

    return populacao_direcao, populacao_xy
