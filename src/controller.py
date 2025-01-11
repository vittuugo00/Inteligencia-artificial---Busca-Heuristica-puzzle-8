# funções em relação a arvore do puzzle e da interface

from puzzle import Puzzle
import random
import pygame
import heapq
import time

def criarPuzzle():
    #peças = list(range(9))
    #random.shuffle(peças)
    #peçasMexidas = peças[:9]
    #estadoInicialPuzzle = Puzzle(peçasMexidas).array
    estadoInicialPuzzle = [8,7,6,5,4,3,2,1,0]
    return estadoInicialPuzzle


def desenharPuzzle(tela, puzzle):
    BRANCO = (255, 255, 255)
    PRETO = (0, 0, 0)
    AZUL_CLARO = (173, 216, 230)
    # fnte para desenhar os números
    fonte = pygame.font.Font(None, 72)

    tela.fill(BRANCO)
    tamanhoBloco = 100

    for i, numero in enumerate(puzzle):
        x = (i % 3) * tamanhoBloco
        y = (i // 3) * tamanhoBloco
        #posições dos blocos


        # desenha o bloco 
        if numero != 0:
            pygame.draw.rect(tela, AZUL_CLARO, (x, y, tamanhoBloco, tamanhoBloco))
            #desenha o número no centro do bloco
            texto = fonte.render(str(numero), True, PRETO)
            tela.blit(texto, (x + tamanhoBloco // 3, y + tamanhoBloco // 4))

def calcularDistanciaManhattan(estado, estadoFinal):
    # calcula a soma das distancias de manhattan (x1-y1 + x2-y2= distancia)
    distancia = 0
    for i, valor in enumerate(estado):
        if valor != 0: 
            posicaoFinal = estadoFinal.index(valor)
            x1, y1 = i % 3, i // 3
            x2, y2 = posicaoFinal % 3, posicaoFinal // 3
            distancia += abs(x1 - x2) + abs(y1 - y2)
    return distancia

def resolverPuzzle (puzzle, estadoFinal):
    estadoInicial = Puzzle(puzzle).array
    aberta = []

    #O heapq é uma biblioteca que implementa uma fila de prioridade mínima, ou seja, 
    # uma estrutura onde os elementos com menor valor são sempre retirados primeiro.
    heapq.heappush(aberta, (0, estadoInicial)) 
    fechados = set()
    caminho = {tuple(estadoInicial): None}
    g_custo = {tuple(estadoInicial): 0}

    estadosExpandidos = 0  # contar os nós

    # Inicia o cronômetro
    tempoInicio = time.time()

    while aberta:
        #usa o estado com menor custo total f = g + h
        _, estadoAtual = heapq.heappop(aberta)
        #ignorando o primeiro valor

        if estadoAtual == estadoFinal:

            tempo_fim = time.time()
            tempoTotal = tempo_fim - tempoInicio
            caminhoSolucao = reconstruirCaminho(caminho, estadoAtual)
            print(f"Tempo de execução: {tempoTotal:.4f} segundos")
            print(f"Estados expandidos: {estadosExpandidos}")

            return reconstruirCaminho(caminho, estadoAtual)

        fechados.add(tuple(estadoAtual))
        posicaoZero = estadoAtual.index(0)

         # contar os nós
        estadosExpandidos += 1

        for movimento in ["cima", "baixo", "esquerda", "direita"]:
            novoEstado = moverPeca(movimento, estadoAtual, posicaoZero)

            if novoEstado and tuple(novoEstado) not in fechados:
                custo = g_custo[tuple(estadoAtual)] + 1
                if tuple(novoEstado) not in g_custo or custo < g_custo[tuple(novoEstado)]:
                    g_custo[tuple(novoEstado)] = custo
                    f = custo + calcularDistanciaManhattan(novoEstado, estadoFinal)
                    heapq.heappush(aberta, (f, novoEstado))
                    caminho[tuple(novoEstado)] = estadoAtual

    return None

def reconstruirCaminho(caminho, estado):
    #reconstitui o caminho desde o estado inicial até o estado final, para exibir os passos
    sequencia = []
    while estado:
        sequencia.append(estado)
        estado = caminho[tuple(estado)]
    return sequencia[::-1]

def moverPeca(direcao, estado, posicaoZero):
    #gera um novo estado aplicando o movimento especificado ao estado atual
    novoEstado = estado[:]
    if direcao == "cima" and posicaoZero >= 3:
        novoEstado[posicaoZero], novoEstado[posicaoZero - 3] = novoEstado[posicaoZero - 3], novoEstado[posicaoZero]
    elif direcao == "baixo" and posicaoZero < 6:
        novoEstado[posicaoZero], novoEstado[posicaoZero + 3] = novoEstado[posicaoZero + 3], novoEstado[posicaoZero]
    elif direcao == "esquerda" and posicaoZero % 3 != 0:
        novoEstado[posicaoZero], novoEstado[posicaoZero - 1] = novoEstado[posicaoZero - 1], novoEstado[posicaoZero]
    elif direcao == "direita" and posicaoZero % 3 != 2:
        novoEstado[posicaoZero], novoEstado[posicaoZero + 1] = novoEstado[posicaoZero + 1], novoEstado[posicaoZero]
    else:
        return None  # movimento inválido
    return novoEstado