#   -*- coding: utf-8 -*-
#   Lucas Tavares Zanuzzo
#   Yuri Molina Vale
#   Algoritmo Evoluitivo
#   Criacao de individuos -> Avaliacao -> Selecao -> Crossover -> Mutacao -> Rearranjo pop.
#
# Biblioteca com os conteúdos visuais
import pygame
# Biblioteca para finalizar a aplicação
import sys
# Biblioteca para gerar números aleatórios
import random
# Biblioteca de parâmetros
import parameters as p
# Biblioteca com as funções do AG
import genetico as ag
# Achar o index e valor de uma lista
import operator


def main():
    pygame.init()
    screen = pygame.display.set_mode(p.WINDOW_RESOLUTION3)
    # Pintar o fundo da tela
    screen.fill(p.WHITE)
    # Titulo da Janela
    pygame.display.set_caption('Algoritmo Genético')
    clock = pygame.time.Clock()
    # Carrega imagem da moeda
    coin = pygame.image.load('coin.png')
    random_i = pygame.image.load('random.png')
    reto = pygame.image.load('reto.png')
    ele = pygame.image.load('ele.png')
    # Coloca a moeda to tamanho do quadrado do grid
    coin = pygame.transform.scale(coin, (int(p.SQUARE_SIZE), int(p.SQUARE_SIZE)))
    img_random = pygame.transform.scale(random_i, (300, 300))
    img_reto = pygame.transform.scale(reto, (300, 300))
    img_ele = pygame.transform.scale(ele, (300, 300))

    # Declara a fonte para escrever na janela
    font = pygame.font.Font(None, 20)
    cont = 0
    # --------------------------------------------------------------
    # Para fazer as linhas vertical e horizontal
    # --------------------------------------------------------------
    linesh = []
    linesv = []
    while cont < p.WINDOW_SIZE:
        linesh.append((0, cont))
        linesh.append((0, cont + p.SQUARE_SIZE))
        linesh.append((p.WINDOW_SIZE, cont + p.SQUARE_SIZE))
        linesh.append((p.WINDOW_SIZE, cont + 2 * p.SQUARE_SIZE))
        linesh.append((0, cont + 2 * p.SQUARE_SIZE))
        linesv.append((cont, 0))
        linesv.append((cont + p.SQUARE_SIZE, 0))
        linesv.append((cont + p.SQUARE_SIZE, p.WINDOW_SIZE))
        linesv.append((cont + 2 * p.SQUARE_SIZE, p.WINDOW_SIZE))
        linesv.append((cont + 2 * p.SQUARE_SIZE, 0))
        cont += p.SQUARE_SIZE
    # --------------------------------------------------------------
    # Declara a populacao, seu vetor de cores e seu vetor de direcoes
    # --------------------------------------------------------------
    populacao_xy, cor, populacao_direcao = ag.iniciaPopulacao(p.TAM_POP)
    #for ind in range(0, p.TAM_POP):
    #    print(populacao_direcao[ind])
    # --------------------------------------------------------------
    # Determina a posicao das moedas aleatoriamente
    # --------------------------------------------------------------
    local_coin_random = []
    for quantidade in range(0, p.QNT_TESOUROS):
        y_coin = random.randrange(0, p.WINDOW_SIZE, p.SQUARE_SIZE)
        x_coin = random.randrange(0, p.WINDOW_SIZE, p.SQUARE_SIZE)
        local_coin_random.append((x_coin, y_coin))
    # --------------------------------------------------------------
    # Determina a posicao das moedas em linha
    # --------------------------------------------------------------
    local_coin_reto = []
    for quantidade in range(0, p.QNT_TESOUROS):
        y_coin = quantidade*30
        x_coin = 480
        local_coin_reto.append((x_coin, y_coin))
    # --------------------------------------------------------------
    # Determina a posicao das moedas em ele
    # --------------------------------------------------------------
    local_coin_ele = []
    for quantidade in range(0, p.QNT_TESOUROS//2):
        y_coin = 180+quantidade*30
        x_coin = 210
        local_coin_ele.append((x_coin, y_coin))
    for quantidade in range(0, p.QNT_TESOUROS//2):
        y_coin = 480
        x_coin = 210+quantidade*30
        local_coin_ele.append((x_coin, y_coin))
    # --------------------------------------------------------------

    deltat = clock.tick(p.FRAMES_PER_SECOND)
    escolha = 0
    escolha_coin = local_coin_random

    while escolha == 0:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if not hasattr(event, 'key'):
                    continue
                if event.key == pygame.K_ESCAPE:
                    sys.exit(0)  # Quit
                if event.key == pygame.K_1:
                    escolha = 1
                    escolha_coin = local_coin_random
                if event.key == pygame.K_2:
                    escolha = 2
                    escolha_coin = local_coin_reto
                if event.key == pygame.K_3:
                    escolha = 3
                    escolha_coin = local_coin_ele
                    # Repinta o fundo de branco

        screen.fill(p.WHITE)
        texto_geracao = font.render('Pressione o número do layout de premios que deseja utilizar', 1, (10, 10, 10))
        screen.blit(texto_geracao, (50, 30))
        texto_geracao = font.render('1', 1, (10, 10, 10))
        screen.blit(texto_geracao, (150, 150))
        texto_geracao = font.render('2', 1, (10, 10, 10))
        screen.blit(texto_geracao, (550, 150))
        texto_geracao = font.render('3', 1, (10, 10, 10))
        screen.blit(texto_geracao, (850, 150))
        screen.blit(img_random, (100, 200))
        screen.blit(img_reto, (450, 200))
        screen.blit(img_ele, (800, 200))
        pygame.display.flip()

    local_coin = escolha_coin
    # Avalia a populacao_xy
    fitness = ag.avalia(populacao_xy, local_coin)

    # conta gerações
    geracao = 0
    flag_melhor = 0

    while 1:

        # Eveto que irá verificar se uma tecla esta pressionada e fazer a geracao rodar
        keys = pygame.key.get_pressed()
        if keys[pygame.K_r]:
            geracao += 1
            # Crossover
            populacao_direcao, populacao_xy = ag.crossover(populacao_direcao, fitness)
            # Mutacao
            populacao_direcao, populacao_xy = ag.mutacao(populacao_direcao, populacao_xy, fitness)
            # Avalia
            fitness = ag.avalia(populacao_xy, local_coin)

            for individuo in range(0, p.TAM_POP):
                print(populacao_direcao[individuo])

        # Evento que verifica o pressionamento de teclas
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if not hasattr(event, 'key'):
                    continue
                if event.key == pygame.K_ESCAPE:
                    sys.exit(0)  # Quit
                if event.key == pygame.K_m:
                    if flag_melhor == 1:
                        flag_melhor = 0
                    else:
                        flag_melhor = 1
                if event.key == pygame.K_SPACE:
                    geracao += 1
                    # Crossover
                    populacao_direcao, populacao_xy = ag.crossover(populacao_direcao, fitness)
                    # Mutacao
                    populacao_direcao, populacao_xy = ag.mutacao(populacao_direcao, populacao_xy, fitness)
                    # Avalia
                    fitness = ag.avalia(populacao_xy, local_coin)

        # Repinta o fundo de branco
        screen.fill(p.WHITE)
        # Desenha novamente o grid
        pygame.draw.lines(screen, p.BLACK, False, linesh, 1)
        pygame.draw.lines(screen, p.BLACK, False, linesv, 1)

        # Desenha os ooins
        for quantidade in range(0, p.QNT_TESOUROS):
            screen.blit(coin, local_coin[quantidade])  # BLIT (Block Image Transfer)

        # Desenha os individuos e escreve seu fitness
        if flag_melhor == 0:
            for individuo in range(0, p.TAM_POP):
                pygame.draw.lines(screen, cor[individuo], False, populacao_xy[individuo], 5)
                caminho_individuo = font.render('Ind: ' + str(individuo) + ' Fit: ' + str(fitness[individuo]), 1, (10, 10, 10))
                screen.blit(caminho_individuo, (650, 70+(20*individuo)))

        else:
            melhor, value = max(enumerate(fitness), key=operator.itemgetter(1))
            pygame.draw.lines(screen, cor[melhor], False, populacao_xy[melhor], 5)
            caminho_individuo = font.render('Ind: ' + str(melhor) + ' Fit: ' + str(fitness[melhor]), 1, (10, 10, 10))
            screen.blit(caminho_individuo, (650, 70 + 20))


        texto_geracao = font.render('Geracao: ' + str(geracao) + '       Segure R para passar as gerações.', 1, (10, 10, 10))
        screen.blit(texto_geracao, (650, 10))
        texto_geracao = font.render('Pressione SPACE para passar as gerações passo a passo. E M para mostrar o melhor', 1, (10, 10, 10))
        screen.blit(texto_geracao, (650, 30))
        texto_geracao = font.render('O algoritmo está rodando com: ' + str(p.TAM_POP) + ' individuos e: ' + str(p.STEPS) + ' passos.', 1, (10, 10, 10))
        screen.blit(texto_geracao, (650, 50))

        pygame.display.flip()
    return


if __name__ == "__main__":
    main()
