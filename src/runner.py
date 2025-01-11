#manipularndo a inteface com pygame e o inicia

import pygame
import controller

pygame.init()

LARGURA_JANELA = 300
ALTURA_JANELA = 300

#configurando a tela
tela = pygame.display.set_mode((LARGURA_JANELA, ALTURA_JANELA))
pygame.display.set_caption("Puzzle-8")

#criando e resolvendo puzzle
puzzle = controller.criarPuzzle()
solucao = controller.resolverPuzzle(puzzle, [1, 2, 3, 4, 0, 5, 6, 7, 8])
passo_atual = 0

rodando = True
while rodando:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False
    
    #desenha o puzzle na tela
    if solucao and passo_atual < len(solucao):
        controller.desenharPuzzle(tela, solucao[passo_atual])
        passo_atual += 1
        pygame.time.delay(1000)  # Intervalo entre os passos
    
    #atualiza a tela
    pygame.display.flip()

pygame.quit()


