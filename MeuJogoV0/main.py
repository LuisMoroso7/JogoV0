import pygame
import random
import os
import math
import tkinter as tk
from tkinter import messagebox
from recursos.funcoes import inicializarBancoDeDados, escreverDados
from recursos.extras import exibir_creditos
import json
from datetime import datetime

pygame.init()
inicializarBancoDeDados()

tamanho = (1000, 700)
relogio = pygame.time.Clock()
tela = pygame.display.set_mode(tamanho)
pygame.display.set_caption("Stranger Things de Luis")
icone = pygame.image.load("assets/vecna.png")
pygame.display.set_icon(icone)
logo = pygame.image.load("assets/icone.png").convert_alpha()

branco = (255, 255, 255)
preto = (0, 0, 0)
vermelho_escuro = (150, 0, 0)

# Imagens
eleven = pygame.image.load("assets/eleven.png")
fundoStart = pygame.image.load("assets/fundoStart.png")
fundoJogo = pygame.image.load("assets/fundoJogo.png")
fundoDead = pygame.image.load("assets/fundoVecna.png")
Vecna = pygame.image.load("assets/vecna.png")

lua_original = pygame.image.load("assets/lua.png").convert_alpha()
lua = pygame.transform.scale(lua_original, (290, 400))

# Sons e fontes
vecnaSound = pygame.mixer.Sound("assets/vecnaSound.mp3")
explosaoSound = pygame.mixer.Sound("assets/explosao.wav")
fonteMenu = pygame.font.SysFont("comicsans", 18)
fonteMorte = pygame.font.SysFont("arial", 120)
fontePause = pygame.font.SysFont("comicsans", 32)
fonteGameOver = pygame.font.SysFont("impact", 72)
fonteBoasVindas = pygame.font.SysFont("comicsans", 30)

pygame.mixer.music.load("assets/kids.mp3")

exibir_creditos(tela, tamanho, fonteMenu)

nome = ""

def tela_boas_vindas():
    exibir = True
    while exibir:
        tela.blit(fundoStart, (0, 0))
        tela.blit(logo, (tamanho[0] - 100, 20))

        titulo = fonteGameOver.render("Bem-vindo, " + nome, True, vermelho_escuro)
        subtitulo = fonteBoasVindas.render("Use as setas para mover. Evite o Vecna!", True, branco)
        botao = pygame.Rect(tamanho[0] // 2 - 100, tamanho[1] // 2, 200, 50)

        pygame.draw.rect(tela, (200, 0, 0), botao, border_radius=10)
        texto_botao = fonteBoasVindas.render("Começar", True, branco)
        tela.blit(titulo, titulo.get_rect(center=(tamanho[0] // 2, 150)))
        tela.blit(subtitulo, subtitulo.get_rect(center=(tamanho[0] // 2, 220)))
        tela.blit(texto_botao, texto_botao.get_rect(center=botao.center))

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                quit()
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                if botao.collidepoint(evento.pos):
                    exibir = False

        pygame.display.update()
        relogio.tick(60)

def escreverDados(nome, pontos):
    try:
        with open("base.stranger", "r") as f:
            dados = json.load(f)
    except:
        dados = {}

    data = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    dados[nome] = [pontos, data]

    with open("base.stranger", "w") as f:
        json.dump(dados, f)

def atualizar_lua_pulsante(escala_base, frame):
    fator = 1 + 0.02 * math.sin(frame * 0.1)
    nova_escala = (int(escala_base[0] * fator), int(escala_base[1] * fator))
    return pygame.transform.scale(lua_original, nova_escala)

def mostrar_game_over():
    tela.blit(fundoDead, (0, 0))
    texto = fonteGameOver.render("GAME OVER", True, vermelho_escuro)
    tela.blit(texto, texto.get_rect(center=(tamanho[0] // 2, 100)))

    try:
        with open("base.stranger", "r") as f:
            dados = json.load(f)
    except:
        dados = {}

    ultimos = list(dados.items())[-5:]  # últimos 5 registros
    y_offset = 200
    for nick, (ponto, data) in reversed(ultimos):
        linha = f"{nick}: {ponto} pontos em {data}"
        texto_linha = fonteMenu.render(linha, True, branco)
        tela.blit(texto_linha, (tamanho[0] // 2 - 250, y_offset))
        y_offset += 40

    pygame.display.update()
    pygame.time.wait(4000)

morcego_img = pygame.image.load("assets/morcego.png").convert_alpha()
morcego = pygame.Rect(random.randint(0, tamanho[0]), random.randint(0, tamanho[1]), 32, 32)
morcego_vel = [random.choice([-2, 2]), random.choice([-2, 2])]

movimento_direcao = None

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

    tela_boas_vindas()

    global movimento_direcao
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
    frame = 0

    pygame.mixer.Sound.play(vecnaSound)
    pygame.mixer.music.play(-1)

    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                quit()
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_RIGHT and movimento_direcao != 'y':
                    movimentoXPersona = 15
                    movimentoYPersona = 0
                    movimento_direcao = 'x'
                elif evento.key == pygame.K_LEFT and movimento_direcao != 'y':
                    movimentoXPersona = -15
                    movimentoYPersona = 0
                    movimento_direcao = 'x'
                elif evento.key == pygame.K_UP and movimento_direcao != 'x':
                    movimentoYPersona = -15
                    movimentoXPersona = 0
                    movimento_direcao = 'y'
                elif evento.key == pygame.K_DOWN and movimento_direcao != 'x':
                    movimentoYPersona = 15
                    movimentoXPersona = 0
                    movimento_direcao = 'y'
                elif evento.key == pygame.K_SPACE:
                    pausar_jogo()
            elif evento.type == pygame.KEYUP:
                if evento.key in [pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN]:
                    movimentoXPersona = 0
                    movimentoYPersona = 0
                    movimento_direcao = None

        posicaoXPersona += movimentoXPersona
        posicaoYPersona += movimentoYPersona

        posicaoXPersona = max(0, min(posicaoXPersona, tamanho[0] - larguraPersona))
        posicaoYPersona = max(0, min(posicaoYPersona, tamanho[1] - alturaPersona))

        # Atualiza morcego
        morcego.x += morcego_vel[0]
        morcego.y += morcego_vel[1]
        if morcego.left < 0 or morcego.right > tamanho[0]:
            morcego_vel[0] *= -1
        if morcego.top < 0 or morcego.bottom > tamanho[1]:
            morcego_vel[1] *= -1

        # Atualiza lua com efeito pulsante
        lua_atualizada = atualizar_lua_pulsante((290, 400), frame)
        frame += 1

        tela.blit(fundoJogo, (0, 0))
        tela.blit(lua_atualizada, (tamanho[0] - 205, -135))
        tela.blit(eleven, (posicaoXPersona, posicaoYPersona))
        tela.blit(morcego_img, morcego)

        posicaoYVecna += velocidadeVecna
        if posicaoYVecna > tamanho[1]:
            posicaoYVecna = -alturaVecna
            pontos += 1
            velocidadeVecna += 1
            posicaoXVecna = random.randint(0, tamanho[0] - larguraVecna)
            pygame.mixer.Sound.play(vecnaSound)

        tela.blit(Vecna, (posicaoXVecna, posicaoYVecna))

        texto = fonteMenu.render("Pontos: " + str(pontos) + "  |  Press SPACE to Pause Game", True, branco)
        tela.blit(texto, (15, 15))

        if (set(range(posicaoYVecna, posicaoYVecna + alturaVecna)).intersection(range(posicaoYPersona, posicaoYPersona + alturaPersona))
            and set(range(posicaoXVecna, posicaoXVecna + larguraVecna)).intersection(range(posicaoXPersona, posicaoXPersona + larguraPersona))):
            if len(set(range(posicaoYVecna, posicaoYVecna + alturaVecna)).intersection(range(posicaoYPersona, posicaoYPersona + alturaPersona))) > dificuldade:
                mostrar_game_over()
                escreverDados(nome, pontos)
                jogar()

        pygame.display.update()
        relogio.tick(60)

import speech_recognition as sr
import pyttsx3

def ouvir_comando():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Aguardando comando de voz: diga 'começar' para iniciar...")
        falar("Diga 'começar' para iniciar o jogo.")
        try:
            audio = recognizer.listen(source, timeout=5)
            comando = recognizer.recognize_google(audio, language='pt-BR').lower()
            print("Você disse:", comando)
            if "começar" in comando:
                jogar()
            else:
                print("Comando não reconhecido. Iniciando normalmente.")
                jogar()
        except sr.UnknownValueError:
            print("Não entendi o que foi dito. Iniciando normalmente.")
            jogar()
        except sr.WaitTimeoutError:
            print("Tempo de espera excedido. Iniciando normalmente.")
            jogar()

def falar(texto):
    engine = pyttsx3.init()
    engine.setProperty('rate', 150)
    engine.say(texto)
    engine.runAndWait()

ouvir_comando()
import pygame
import random
import os
import math
import tkinter as tk
from tkinter import messagebox
from recursos.funcoes import inicializarBancoDeDados, escreverDados
from recursos.extras import exibir_creditos
import json
from datetime import datetime

pygame.init()
inicializarBancoDeDados()

tamanho = (1000, 700)
relogio = pygame.time.Clock()
tela = pygame.display.set_mode(tamanho)
pygame.display.set_caption("Stranger Things de Luis")
icone = pygame.image.load("assets/vecna.png")
pygame.display.set_icon(icone)
logo = pygame.image.load("assets/icone.png").convert_alpha()

branco = (255, 255, 255)
preto = (0, 0, 0)
vermelho_escuro = (150, 0, 0)

# Imagens
eleven = pygame.image.load("assets/eleven.png")
fundoStart = pygame.image.load("assets/fundoStart.png")
fundoJogo = pygame.image.load("assets/fundoJogo.png")
fundoDead = pygame.image.load("assets/fundoVecna.png")
Vecna = pygame.image.load("assets/vecna.png")

lua_original = pygame.image.load("assets/lua.png").convert_alpha()
lua = pygame.transform.scale(lua_original, (290, 400))

# Sons e fontes
vecnaSound = pygame.mixer.Sound("assets/vecnaSound.mp3")
explosaoSound = pygame.mixer.Sound("assets/explosao.wav")
fonteMenu = pygame.font.SysFont("comicsans", 18)
fonteMorte = pygame.font.SysFont("arial", 120)
fontePause = pygame.font.SysFont("comicsans", 32)
fonteGameOver = pygame.font.SysFont("impact", 72)
fonteBoasVindas = pygame.font.SysFont("comicsans", 30)

pygame.mixer.music.load("assets/kids.mp3")

exibir_creditos(tela, tamanho, fonteMenu)

nome = ""

def tela_boas_vindas():
    exibir = True
    while exibir:
        tela.blit(fundoStart, (0, 0))
        tela.blit(logo, (tamanho[0] - 100, 20))

        titulo = fonteGameOver.render("Bem-vindo, " + nome, True, vermelho_escuro)
        subtitulo = fonteBoasVindas.render("Use as setas para mover. Evite o Vecna!", True, branco)
        botao = pygame.Rect(tamanho[0] // 2 - 100, tamanho[1] // 2, 200, 50)

        pygame.draw.rect(tela, (200, 0, 0), botao, border_radius=10)
        texto_botao = fonteBoasVindas.render("Começar", True, branco)
        tela.blit(titulo, titulo.get_rect(center=(tamanho[0] // 2, 150)))
        tela.blit(subtitulo, subtitulo.get_rect(center=(tamanho[0] // 2, 220)))
        tela.blit(texto_botao, texto_botao.get_rect(center=botao.center))

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                quit()
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                if botao.collidepoint(evento.pos):
                    exibir = False

        pygame.display.update()
        relogio.tick(60)

def escreverDados(nome, pontos):
    try:
        with open("base.stranger", "r") as f:
            dados = json.load(f)
    except:
        dados = {}

    data = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    dados[nome] = [pontos, data]

    with open("base.stranger", "w") as f:
        json.dump(dados, f)

def atualizar_lua_pulsante(escala_base, frame):
    fator = 1 + 0.02 * math.sin(frame * 0.1)
    nova_escala = (int(escala_base[0] * fator), int(escala_base[1] * fator))
    return pygame.transform.scale(lua_original, nova_escala)

def mostrar_game_over():
    tela.blit(fundoDead, (0, 0))
    texto = fonteGameOver.render("GAME OVER", True, vermelho_escuro)
    tela.blit(texto, texto.get_rect(center=(tamanho[0] // 2, 100)))

    try:
        with open("base.stranger", "r") as f:
            dados = json.load(f)
    except:
        dados = {}

    ultimos = list(dados.items())[-5:]  # últimos 5 registros
    y_offset = 200
    for nick, (ponto, data) in reversed(ultimos):
        linha = f"{nick}: {ponto} pontos em {data}"
        texto_linha = fonteMenu.render(linha, True, branco)
        tela.blit(texto_linha, (tamanho[0] // 2 - 250, y_offset))
        y_offset += 40

    pygame.display.update()
    pygame.time.wait(4000)

morcego_img = pygame.image.load("assets/morcego.png").convert_alpha()
morcego = pygame.Rect(random.randint(0, tamanho[0]), random.randint(0, tamanho[1]), 32, 32)
morcego_vel = [random.choice([-2, 2]), random.choice([-2, 2])]

movimento_direcao = None

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

    tela_boas_vindas()

    global movimento_direcao
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
    frame = 0

    pygame.mixer.Sound.play(vecnaSound)
    pygame.mixer.music.play(-1)

    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                quit()
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_RIGHT and movimento_direcao != 'y':
                    movimentoXPersona = 15
                    movimentoYPersona = 0
                    movimento_direcao = 'x'
                elif evento.key == pygame.K_LEFT and movimento_direcao != 'y':
                    movimentoXPersona = -15
                    movimentoYPersona = 0
                    movimento_direcao = 'x'
                elif evento.key == pygame.K_UP and movimento_direcao != 'x':
                    movimentoYPersona = -15
                    movimentoXPersona = 0
                    movimento_direcao = 'y'
                elif evento.key == pygame.K_DOWN and movimento_direcao != 'x':
                    movimentoYPersona = 15
                    movimentoXPersona = 0
                    movimento_direcao = 'y'
                elif evento.key == pygame.K_SPACE:
                    pausar_jogo()
            elif evento.type == pygame.KEYUP:
                if evento.key in [pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN]:
                    movimentoXPersona = 0
                    movimentoYPersona = 0
                    movimento_direcao = None

        posicaoXPersona += movimentoXPersona
        posicaoYPersona += movimentoYPersona

        posicaoXPersona = max(0, min(posicaoXPersona, tamanho[0] - larguraPersona))
        posicaoYPersona = max(0, min(posicaoYPersona, tamanho[1] - alturaPersona))

        # Atualiza morcego
        morcego.x += morcego_vel[0]
        morcego.y += morcego_vel[1]
        if morcego.left < 0 or morcego.right > tamanho[0]:
            morcego_vel[0] *= -1
        if morcego.top < 0 or morcego.bottom > tamanho[1]:
            morcego_vel[1] *= -1

        # Atualiza lua com efeito pulsante
        lua_atualizada = atualizar_lua_pulsante((290, 400), frame)
        frame += 1

        tela.blit(fundoJogo, (0, 0))
        tela.blit(lua_atualizada, (tamanho[0] - 205, -135))
        tela.blit(eleven, (posicaoXPersona, posicaoYPersona))
        tela.blit(morcego_img, morcego)

        posicaoYVecna += velocidadeVecna
        if posicaoYVecna > tamanho[1]:
            posicaoYVecna = -alturaVecna
            pontos += 1
            velocidadeVecna += 1
            posicaoXVecna = random.randint(0, tamanho[0] - larguraVecna)
            pygame.mixer.Sound.play(vecnaSound)

        tela.blit(Vecna, (posicaoXVecna, posicaoYVecna))

        texto = fonteMenu.render("Pontos: " + str(pontos) + "  |  Press SPACE to Pause Game", True, branco)
        tela.blit(texto, (15, 15))

        if (set(range(posicaoYVecna, posicaoYVecna + alturaVecna)).intersection(range(posicaoYPersona, posicaoYPersona + alturaPersona))
            and set(range(posicaoXVecna, posicaoXVecna + larguraVecna)).intersection(range(posicaoXPersona, posicaoXPersona + larguraPersona))):
            if len(set(range(posicaoYVecna, posicaoYVecna + alturaVecna)).intersection(range(posicaoYPersona, posicaoYPersona + alturaPersona))) > dificuldade:
                mostrar_game_over()
                escreverDados(nome, pontos)
                jogar()

        pygame.display.update()
        relogio.tick(60)

import speech_recognition as sr
import pyttsx3

def ouvir_comando():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Aguardando comando de voz: diga 'começar' para iniciar...")
        falar("Diga 'começar' para iniciar o jogo.")
        try:
            audio = recognizer.listen(source, timeout=5)
            comando = recognizer.recognize_google(audio, language='pt-BR').lower()
            print("Você disse:", comando)
            if "começar" in comando:
                jogar()
            else:
                print("Comando não reconhecido. Iniciando normalmente.")
                jogar()
        except sr.UnknownValueError:
            print("Não entendi o que foi dito. Iniciando normalmente.")
            jogar()
        except sr.WaitTimeoutError:
            print("Tempo de espera excedido. Iniciando normalmente.")
            jogar()

def falar(texto):
    engine = pyttsx3.init()
    engine.setProperty('rate', 150)
    engine.say(texto)
    engine.runAndWait()

ouvir_comando()
