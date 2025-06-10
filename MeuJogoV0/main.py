import pygame
import random
import os
import tkinter as tk
from tkinter import messagebox
from recursos.funcoes import inicializarBancoDeDados, escreverDados
import json

# Commit 1: Inicialização do pygame, setup da janela e carregamento de assets
pygame.init()
inicializarBancoDeDados()

tamanho = (1000, 700)
relogio = pygame.time.Clock()
tela = pygame.display.set_mode(tamanho)
pygame.display.set_caption("Stranger Things de Luis")
icone = pygame.image.load("assets/vecna.png")
pygame.display.set_icon(icone)

branco = (255, 255, 255)
preto = (0, 0, 0)

# Commit 2: Carregamento de imagens, sons e fontes
eleven = pygame.image.load("assets/eleven.png")
fundoStart = pygame.image.load("assets/fundoStart.png")
fundoJogo = pygame.image.load("assets/fundoJogo.png")
fundoDead = pygame.image.load("assets/fundoVecna.png")
Vecna = pygame.image.load("assets/vecna.png")

vecnaSound = pygame.mixer.Sound("assets/vecnaSound.mp3")
explosaoSound = pygame.mixer.Sound("assets/explosao.wav")
fonteMenu = pygame.font.SysFont("comicsans", 18)
fonteMorte = pygame.font.SysFont("arial", 120)
fontePause = pygame.font.SysFont("comicsans", 32)

pygame.mixer.music.load("assets/kids.mp3")

# Commit 3: Função de pausa com sombra e texto piscante
def pausar_jogo():
    pausado = True
    contador = 0
    while pausado:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                quit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_SPACE:
                    pausado = False

        tela.fill(preto)

        if (contador // 30) % 2 == 0:
            texto_pausa = fontePause.render("Jogo Pausado - Pressione ESPAÇO para voltar", True, branco)
            sombra = fontePause.render("Jogo Pausado - Pressione ESPAÇO para voltar", True, (50, 50, 50))
            texto_rect = texto_pausa.get_rect(center=(tamanho[0] // 2, tamanho[1] // 2))
            sombra_rect = texto_rect.copy()
            sombra_rect.move_ip(3, 3)
            tela.blit(sombra, sombra_rect)
            tela.blit(texto_pausa, texto_rect)

        pygame.display.update()
        relogio.tick(60)
        contador += 1

# Commit 4: Função principal de jogo (jogar)
def jogar():
    largura_janela = 300
    altura_janela = 50

    def obter_nome():
        global nome
        nome = entry_nome.get()
        if not nome:
            messagebox.showwarning("Aviso", "Por favor, digite seu nome!")
        else:
            root.destroy()

    root = tk.Tk()
    largura_tela = root.winfo_screenwidth()
    altura_tela = root.winfo_screenheight()
    pos_x = (largura_tela - largura_janela) // 2
    pos_y = (altura_tela - altura_janela) // 2
    root.geometry(f"{largura_janela}x{altura_janela}+{pos_x}+{pos_y}")
    root.title("Informe seu nickname")
    root.protocol("WM_DELETE_WINDOW", obter_nome)

    entry_nome = tk.Entry(root)
    entry_nome.pack()

    botao = tk.Button(root, text="Enviar", command=obter_nome)
    botao.pack()
    root.mainloop()

    posicaoXPersona = 400
    posicaoYPersona = 300
    movimentoXPersona = 0
    movimentoYPersona = 0
    posicaoXVecna = 400
    posicaoYVecna = -240
    velocidadeVecna = 1

    larguraPersona = 125
    alturaPersona = 188
    larguraVecna = 120
    alturaVecna = 180

    dificuldade = 30
    pontos = 0

    pygame.mixer.Sound.play(vecnaSound)
    pygame.mixer.music.play(-1)

    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                quit()
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_RIGHT:
                    movimentoXPersona = 15
                elif evento.key == pygame.K_LEFT:
                    movimentoXPersona = -15
                elif evento.key == pygame.K_UP:
                    movimentoYPersona = -15
                elif evento.key == pygame.K_DOWN:
                    movimentoYPersona = 15
                elif evento.key == pygame.K_SPACE:
                    pausar_jogo()
            elif evento.type == pygame.KEYUP:
                if evento.key in [pygame.K_LEFT, pygame.K_RIGHT]:
                    movimentoXPersona = 0
                elif evento.key in [pygame.K_UP, pygame.K_DOWN]:
                    movimentoYPersona = 0

        posicaoXPersona += movimentoXPersona
        posicaoYPersona += movimentoYPersona

        posicaoXPersona = max(0, min(posicaoXPersona, tamanho[0] - larguraPersona))
        posicaoYPersona = max(0, min(posicaoYPersona, tamanho[1] - alturaPersona))

        tela.blit(fundoJogo, (0, 0))
        tela.blit(eleven, (posicaoXPersona, posicaoYPersona))

        posicaoYVecna += velocidadeVecna
        if posicaoYVecna > tamanho[1]:
            posicaoYVecna = -alturaVecna
            pontos += 1
            velocidadeVecna += 1
            posicaoXVecna = random.randint(0, tamanho[0] - larguraVecna)
            pygame.mixer.Sound.play(vecnaSound)

        tela.blit(Vecna, (posicaoXVecna, posicaoYVecna))

        texto = fonteMenu.render("Pontos: " + str(pontos), True, branco)
        tela.blit(texto, (15, 15))

        if (set(range(posicaoYVecna, posicaoYVecna + alturaVecna)).intersection(range(posicaoYPersona, posicaoYPersona + alturaPersona))
            and set(range(posicaoXVecna, posicaoXVecna + larguraVecna)).intersection(range(posicaoXPersona, posicaoXPersona + larguraPersona))):
            if len(set(range(posicaoYVecna, posicaoYVecna + alturaVecna)).intersection(range(posicaoYPersona, posicaoYPersona + alturaPersona))) > dificuldade:
                escreverDados(nome, pontos)
                dead()

        pygame.display.update()
        relogio.tick(60)

# Commit 5: Telas de start e morte (start, dead)
def start():
    larguraButtonStart = 150
    alturaButtonStart = 40
    larguraButtonQuit = 150
    alturaButtonQuit = 40

    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                quit()
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                if startButton.collidepoint(evento.pos):
                    larguraButtonStart = 140
                    alturaButtonStart = 35
                if quitButton.collidepoint(evento.pos):
                    larguraButtonQuit = 140
                    alturaButtonQuit = 35
            elif evento.type == pygame.MOUSEBUTTONUP:
                if startButton.collidepoint(evento.pos):
                    jogar()
                if quitButton.collidepoint(evento.pos):
                    quit()

        tela.blit(fundoStart, (0, 0))

        startButton = pygame.draw.rect(tela, branco, (10, 10, larguraButtonStart, alturaButtonStart), border_radius=15)
        startTexto = fonteMenu.render("Iniciar Game", True, preto)
        tela.blit(startTexto, (25, 12))

        quitButton = pygame.draw.rect(tela, branco, (10, 60, larguraButtonQuit, alturaButtonQuit), border_radius=15)
        quitTexto = fonteMenu.render("Sair do Game", True, preto)
        tela.blit(quitTexto, (25, 62))

        pygame.display.update()
        relogio.tick(60)

def dead():
    pygame.mixer.music.stop()
    pygame.mixer.Sound.play(explosaoSound)

    root = tk.Tk()
    root.title("Tela da Morte")

    label = tk.Label(root, text="Log das Partidas", font=("Arial", 16))
    label.pack(pady=10)

    listbox = tk.Listbox(root, width=50, height=10, selectmode=tk.SINGLE)
    listbox.pack(pady=20)

    log_partidas = open("base.atitus", "r").read()
    log_partidas = json.loads(log_partidas)
    for chave in log_partidas:
        listbox.insert(tk.END, f"Pontos: {log_partidas[chave][0]} na data: {log_partidas[chave][1]} - Nickname: {chave}")

    root.mainloop()
    start()

start()
