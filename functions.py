import parameters as p
from random import randint
import random

def geraPasso(ponto_atual, ponto_anterior):
    x_velho = ponto_atual[0]
    y_velho = ponto_atual[1]
    x_anterior = ponto_anterior[0]
    y_anterior = ponto_anterior[1]
    # baixo = 0
    # direita = 1
    # cima = 2
    # esquerda = 3
    direcao = randint(0, 3)
    rota = ''

    if direcao == 0:
        y_new = y_velho + p.SQUARE_SIZE
        x_new = x_velho
        rota = 'B'
    elif direcao == 1:
        x_new = x_velho + p.SQUARE_SIZE
        y_new = y_velho
        rota = 'D'
    elif direcao == 2:
        y_new = y_velho - p.SQUARE_SIZE
        x_new = x_velho
        rota = 'C'
    elif direcao == 3:
        x_new = x_velho - p.SQUARE_SIZE
        y_new = y_velho
        rota = 'E'

    if y_new == y_anterior and x_new == x_anterior:
        novo_ponto, nova_direcao = geraPasso((x_velho, y_velho), (x_anterior, y_anterior))
    elif y_new > p.WINDOW_SIZE or y_new < 0:
        novo_ponto, nova_direcao = geraPasso((x_velho, y_velho), (x_anterior, y_anterior))
    elif x_new > p.WINDOW_SIZE or x_new < 0:
        novo_ponto, nova_direcao = geraPasso((x_velho, y_velho), (x_anterior, y_anterior))
    else:
        novo_ponto = (x_new, y_new)
        nova_direcao = rota

    return novo_ponto, nova_direcao


def gera_passo_pela_direcao(direcao, direcao_anterior, ponto_atual):
    x_atual = ponto_atual[0]
    y_atual = ponto_atual[1]

    # Caso ele não esteja voltando por onde veio.
    if direcao == 'B':
        y_new = y_atual + p.SQUARE_SIZE
        x_new = x_atual
    elif direcao == 'D':
        x_new = x_atual + p.SQUARE_SIZE
        y_new = y_atual
    elif direcao == 'C':
        y_new = y_atual - p.SQUARE_SIZE
        x_new = x_atual
    elif direcao == 'E':
        x_new = x_atual - p.SQUARE_SIZE
        y_new = y_atual

    # Verifica se o individuo nao esta tentando voltar por onde veio
    if direcao_anterior == 'C' and direcao == 'B':
        direcao_nova = ['D', 'C', 'E']
        direcao_nova = random.choice(direcao_nova)
        ponto_prox, nova_direcao = gera_passo_pela_direcao(direcao_nova, direcao_anterior, ponto_atual)
    elif direcao_anterior == 'D' and direcao == 'E':
        direcao_nova = ['B', 'D', 'C']
        direcao_nova = random.choice(direcao_nova)
        ponto_prox, nova_direcao = gera_passo_pela_direcao(direcao_nova, direcao_anterior, ponto_atual)
    elif direcao_anterior == 'E' and direcao == 'D':
        direcao_nova = ['B', 'C', 'E']
        direcao_nova = random.choice(direcao_nova)
        ponto_prox, nova_direcao = gera_passo_pela_direcao(direcao_nova, direcao_anterior, ponto_atual)
    elif direcao_anterior == 'B' and direcao == 'C':
        direcao_nova = ['B', 'D', 'E']
        direcao_nova = random.choice(direcao_nova)
        ponto_prox, nova_direcao = gera_passo_pela_direcao(direcao_nova, direcao_anterior, ponto_atual)
    elif y_new > p.WINDOW_SIZE or y_new < 0:
        direcao_nova = ['B', 'D', 'E', 'C']
        direcao_nova = random.choice(direcao_nova)
        ponto_prox, nova_direcao = gera_passo_pela_direcao(direcao_nova, direcao_anterior, ponto_atual)
    elif x_new > p.WINDOW_SIZE or x_new < 0:
        direcao_nova = ['B', 'D', 'E', 'C']
        direcao_nova = random.choice(direcao_nova)
        ponto_prox, nova_direcao = gera_passo_pela_direcao(direcao_nova, direcao_anterior, ponto_atual)
    else:
        ponto_prox = (x_new, y_new)
        nova_direcao = direcao

    return ponto_prox, nova_direcao


def pontos_a_partir_de_direcoes(individuo_direcao):

    individuo_xy = []
    individuo_xy.append((0, 0))
    individuo_xy.append((15, 15))
    for pos in range(0, p.STEPS):

        direcao = individuo_direcao[pos]
        if pos == 0 :
            ponto_prox, nova_direcao = gera_passo_pela_direcao(direcao, '', individuo_xy[pos+1])
        else:
            direcao_antiga = individuo_direcao[pos-1]
            ponto_prox, nova_direcao = gera_passo_pela_direcao(direcao, direcao_antiga, individuo_xy[pos + 1])
        individuo_direcao[pos] = nova_direcao
        individuo_xy.append(ponto_prox)

    return individuo_xy, individuo_direcao
