import pygame
import time

def exibir_creditos(tela, tamanho, fonte):
    tela.fill((0, 0, 0))  # Fundo preto

    creditos = [
        "STRANGER THINGS DE LUIS",
        "Desenvolvido por: Luis Eduardo",
        "RA: 1138541",
        "",
        "Baseado no jogo Iron Man",
        "Disciplina: Pensamento Computacional",
        "Atitus Educação - 2025"
    ]

    y = 180
    for linha in creditos:
        texto = fonte.render(linha, True, (255, 0, 0))
        rect = texto.get_rect(center=(tamanho[0] // 2, y))
        tela.blit(texto, rect)
        y += 40

    pygame.display.update()
    time.sleep(5)