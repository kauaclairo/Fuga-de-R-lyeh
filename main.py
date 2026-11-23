from pathlib import Path

import pygame
import random
from recursos.funcoes import inicializarBancoDeDados, limpar_tela, escreverDados, maior_pontuador

limpar_tela()
inicializarBancoDeDados()
nome_maior, maior_pontos, dataJogada = maior_pontuador()
pygame.init()

while True:
    nome = input("Informe o Nome do Competidor:")
    if len(nome) > 0: 
        break
    else:
        print("Nome Inválido!")
        
tamanho = (800,200)
pygame.display.set_caption("Fuga de R'lyeh")
icone  = pygame.image.load("bases/icone.png")
pygame.display.set_icon(icone)
relogio = pygame.time.Clock()
tela = pygame.display.set_mode( tamanho ) 
verde_abissal = (4, 30, 34)
verde_esmeralda = (92, 224, 172)
texto_claro = (232, 244, 238)

fundo = pygame.image.load("bases/background.jpg")
fundoDead = pygame.image.load("bases/backgroundDead.jpg")
fundoStart = pygame.image.load("bases/backgroundStart.jpg")
fundo = pygame.transform.scale(fundo, (1129, 200))
fundoDead = pygame.transform.scale(fundoDead, (800, 200))
fundoStart = pygame.transform.scale(fundoStart, (800, 200))

submarino = pygame.image.load("bases/submarino.png")
submarino = pygame.transform.scale(submarino, (116,51))
tentaculo = pygame.image.load("bases/tentaculo.png")
tentaculo = pygame.transform.scale(tentaculo, (125,25))
tentaculoSound = pygame.mixer.Sound(
    "bases/ataque.wav" if Path("bases/ataque.wav").is_file() else "bases/missile.wav"
)
explosaoSound = pygame.mixer.Sound(
    "bases/morte.wav" if Path("bases/morte.wav").is_file() else "bases/explosao.wav"
)
trilha = "bases/trilha.mp3" if Path("bases/trilha.mp3").is_file() else "bases/ironsound.mp3"
pygame.mixer.music.load(trilha)
fonteMenu = pygame.font.SysFont("Georgia",18)

def jogar():
    fundoMov1 = 0
    fundoMov2 = 1129
    posicaoXSubmarino = 0
    posicaoYSubmarino = 60
    movimentoXSubmarino  = 0
    movimentoYSubmarino  = 0
    velocidadeMovSubmarino = 5
    posicaoXTentaculo = 800
    posicaoYTentaculo = 100
    velocidadeTentaculo = 2
    pontos = 0
    pygame.mixer.Sound.play(tentaculoSound)
    pygame.mixer.music.play(-1)
    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                quit()
                movimentoXSubmarino = 0
            elif evento.type == pygame.KEYDOWN and evento.key == pygame.K_UP:
                movimentoYSubmarino = -velocidadeMovSubmarino
            elif evento.type == pygame.KEYDOWN and evento.key == pygame.K_DOWN:
                movimentoYSubmarino = velocidadeMovSubmarino
            elif evento.type == pygame.KEYUP and evento.key == pygame.K_UP:
                movimentoYSubmarino = 0
            elif evento.type == pygame.KEYUP and evento.key == pygame.K_DOWN:
                movimentoYSubmarino = 0
            elif evento.type == pygame.KEYDOWN and evento.key == pygame.K_RIGHT:
                movimentoXSubmarino = velocidadeMovSubmarino
            elif evento.type == pygame.KEYDOWN and evento.key == pygame.K_LEFT:
                movimentoXSubmarino = -velocidadeMovSubmarino
            elif evento.type == pygame.KEYUP and evento.key == pygame.K_RIGHT:
                movimentoXSubmarino = 0
            elif evento.type == pygame.KEYUP and evento.key == pygame.K_LEFT:
                movimentoXSubmarino = 0
                
        
        posicaoXSubmarino = posicaoXSubmarino + movimentoXSubmarino          
        posicaoYSubmarino = posicaoYSubmarino + movimentoYSubmarino            
        if posicaoXSubmarino < 0 :
            posicaoXSubmarino = 0
        elif posicaoXSubmarino > 685:
            posicaoXSubmarino = 685
        if posicaoYSubmarino < 0 :
            posicaoYSubmarino = 0
        elif posicaoYSubmarino > 150:
            posicaoYSubmarino = 150
            
            
        posicaoXTentaculo = posicaoXTentaculo - velocidadeTentaculo
        if posicaoXTentaculo < -125:
            pygame.mixer.Sound.play(tentaculoSound)
            posicaoXTentaculo = 800
            pontos = pontos + 1
            velocidadeTentaculo = min(velocidadeTentaculo + 1, 14)
            posicaoYTentaculo = random.randint(0,175)
                            
        tela.fill(texto_claro)
        tela.blit(fundo, (fundoMov1,0) )
        tela.blit(fundo, (fundoMov2,0) )
        fundoMov1 -= 1
        fundoMov2 -= 1
        if fundoMov1 <= -1129:
            fundoMov1 = 1129
        elif fundoMov2 <= -1129:
            fundoMov2 = 1129
        
        
        tela.blit(submarino, (posicaoXSubmarino,posicaoYSubmarino))
        tela.blit(tentaculo, (posicaoXTentaculo, posicaoYTentaculo))
        texto = fonteMenu.render("Pontos: "+str(pontos), True, texto_claro)
        tela.blit(texto, (700,15))
            
        hitboxSubmarino = pygame.Rect(
            posicaoXSubmarino, posicaoYSubmarino, *submarino.get_size()
        ).inflate(-15, -10)
        hitboxTentaculo = pygame.Rect(
            posicaoXTentaculo, posicaoYTentaculo, *tentaculo.get_size()
        ).inflate(-15, -10)
        if hitboxSubmarino.colliderect(hitboxTentaculo):
            escreverDados(nome, pontos)
            dead(pontos)
        
        
        pygame.display.update()
        relogio.tick(60)

def dead(pontos):
    global nome_maior, maior_pontos, dataJogada
    nome_maior, maior_pontos, dataJogada = maior_pontuador()
    pygame.mixer.music.stop()
    pygame.mixer.Sound.play(explosaoSound)
    larguraButtonStart = 150
    alturaButtonStart  = 40
    larguraButtonQuit = 150
    alturaButtonQuit  = 40
    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                quit()
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                if startButton.collidepoint(evento.pos):
                    larguraButtonStart = 140
                    alturaButtonStart  = 35
                if quitButton.collidepoint(evento.pos):
                    larguraButtonQuit = 140
                    alturaButtonQuit  = 35

                
            elif evento.type == pygame.MOUSEBUTTONUP:
                # Verifica se o clique foi dentro do retângulo
                if startButton.collidepoint(evento.pos):
                    #pygame.mixer.music.play(-1)
                    larguraButtonStart = 150
                    alturaButtonStart  = 40
                    jogar()
                if quitButton.collidepoint(evento.pos):
                    #pygame.mixer.music.play(-1)
                    larguraButtonQuit = 150
                    alturaButtonQuit  = 40
                    quit()
            
        tela.fill(texto_claro)
        tela.blit(fundoDead, (0,0))
        startButton = pygame.draw.rect(tela, verde_abissal, (10,10, larguraButtonStart, alturaButtonStart), border_radius=15)
        pygame.draw.rect(tela, verde_esmeralda, startButton, width=2, border_radius=15)
        startTexto = fonteMenu.render("Iniciar Fuga", True, texto_claro)
        tela.blit(startTexto, startTexto.get_rect(center=startButton.center))
        
        quitButton = pygame.draw.rect(tela, verde_abissal, (10,60, larguraButtonQuit, alturaButtonQuit), border_radius=15)
        pygame.draw.rect(tela, verde_esmeralda, quitButton, width=2, border_radius=15)
        quitTexto = fonteMenu.render("Sair do Abismo", True, texto_claro)
        tela.blit(quitTexto, quitTexto.get_rect(center=quitButton.center))
        pontuacaoTexto = fonteMenu.render(
            f"Sanidade perdida! Pontos: {pontos}", True, texto_claro
        )
        tela.blit(pontuacaoTexto, pontuacaoTexto.get_rect(center=(400, 150)))


        pygame.display.update()
        relogio.tick(60)



def start():
    larguraButtonStart = 150
    alturaButtonStart  = 40
    larguraButtonQuit = 150
    alturaButtonQuit  = 40
    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                quit()
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                if startButton.collidepoint(evento.pos):
                    larguraButtonStart = 140
                    alturaButtonStart  = 35
                if quitButton.collidepoint(evento.pos):
                    larguraButtonQuit = 140
                    alturaButtonQuit  = 35

                
            elif evento.type == pygame.MOUSEBUTTONUP:
                # Verifica se o clique foi dentro do retângulo
                if startButton.collidepoint(evento.pos):
                    #pygame.mixer.music.play(-1)
                    larguraButtonStart = 150
                    alturaButtonStart  = 40
                    jogar()
                if quitButton.collidepoint(evento.pos):
                    #pygame.mixer.music.play(-1)
                    larguraButtonQuit = 150
                    alturaButtonQuit  = 40
                    quit()
            
        tela.fill(texto_claro)
        tela.blit(fundoStart, (0,0))
        startButton = pygame.draw.rect(tela, verde_abissal, (10,10, larguraButtonStart, alturaButtonStart), border_radius=15)
        pygame.draw.rect(tela, verde_esmeralda, startButton, width=2, border_radius=15)
        startTexto = fonteMenu.render("Iniciar Fuga", True, texto_claro)
        tela.blit(startTexto, startTexto.get_rect(center=startButton.center))
        
        quitButton = pygame.draw.rect(tela, verde_abissal, (10,60, larguraButtonQuit, alturaButtonQuit), border_radius=15)
        pygame.draw.rect(tela, verde_esmeralda, quitButton, width=2, border_radius=15)
        quitTexto = fonteMenu.render("Sair do Abismo", True, texto_claro)
        tela.blit(quitTexto, quitTexto.get_rect(center=quitButton.center))
        texto = fonteMenu.render(f" O melhor - {nome_maior} - {maior_pontos} - { dataJogada} ", True, texto_claro)
        tela.blit(texto, (480,15))
        

        pygame.display.update()
        relogio.tick(60)
           
start()