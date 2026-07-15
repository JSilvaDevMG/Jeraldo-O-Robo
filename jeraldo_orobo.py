import pygame
import random

pygame.init()

#posições
casas = [25,125,225,325,425]
componentes = []
bugs = []
ocupadas = []

#Função para gerar posição aleatória
def gerar_posicao():
    while True:
        x = random.choice(casas)
        y = random.choice(casas)

        # Não permite repetir posição
        if (x, y) in ocupadas:
            continue
        # Não permite aparecer nessas duas posições 
        if (x, y) == (25, 25):
            continue
        if (x, y) == (425, 425):
            continue
        ocupadas.append((x, y))
        return x, y
    
#cria os componentes        
componentes = []
for _ in range(3):
    x, y = gerar_posicao()
    componentes.append({"x": x, "y": y, "coletado": False})

#cria os bugs
bugs = []
for _ in range(3):
    x, y = gerar_posicao()
    bugs.append({"x": x, "y": y, "coletado": False})

#posição inicial do jeraldo
jeraldo_x = 25
jeraldo_y = 25

#posição do servidor
servidor_x = 425
servidor_y = 425

#cores
AZUL = (46, 54, 152)
PRETO = (0, 0, 0)
CINZA = (200, 200, 200)
BRANCO = (255, 255, 255)

#tela
tamanho_tela = [500, 600]
tela = pygame.display.set_mode((tamanho_tela))
pygame.display.set_caption("Jeraldo - O robô")
pygame.display.set_icon(pygame.image.load("sprites/jeraldo_icon.png"))
jeraldo_img = pygame.image.load("sprites/jeraldo.png")
servidor_img = pygame.image.load("sprites/servidor.png")
mensagem_img = pygame.image.load("sprites/parede_mensagem.png")
gameover_img = pygame.image.load("sprites/gameover.png")
bug_img = pygame.image.load("sprites/bug.png")
comp_img = pygame.image.load("sprites/componente.png")
aviso_comp = pygame.image.load("sprites/aviso_comp.png")
vitoria_img = pygame.image.load("sprites/vitoria.png")
vida_img = pygame.image.load("sprites/vida.png")
aviso_comp = pygame.transform.scale(aviso_comp, (350, 350))
mostrar_img = pygame.transform.scale(mensagem_img, (300, 300))
gameover_img = pygame.transform.scale(gameover_img, (500, 500))
vitoria_img = pygame.transform.scale(vitoria_img, (500, 500))
vida_img = pygame.transform.scale(vida_img, (90, 90))

jeraldo = jeraldo_img.get_rect()
servidor = servidor_img.get_rect()

#variáveis do jogo
tempo_aviso = 0
tempo_mensagem = 0
comp_coletados = 0
vidas = 3
mostrar_mensagem = False
venceu = False
game_over = False
aviso_mensagem = False
bugs_coletados = False

#cria o relógio
relogio = pygame.time.Clock()

#define o tamanho do tabuleiro
altura_tab = (100)
largura_tab = (100)

#define a fonte do texto
fonte = pygame.font.Font("fontes/PixelOperatorMono-Bold.ttf", 30)

#Função para reiniciar o jogo
def reiniciar_jogo():
    global jeraldo_x, jeraldo_y
    global comp_coletados, vidas
    global venceu, game_over
    global componentes, bugs, ocupadas
    global mostrar_mensagem, aviso_mensagem, tempo_mensagem

    jeraldo_x = 25
    jeraldo_y = 25

    tempo_mensagem = 0
    comp_coletados = 0
    vidas = 3
    mostrar_mensagem = False
    aviso_mensagem = False  
    venceu = False
    game_over = False

    ocupadas = []
    componentes = []
    for _ in range(3):
        x, y = gerar_posicao()
        componentes.append({"x": x, "y": y, "coletado": False})

    bugs = []
    for _ in range(3):
        x, y = gerar_posicao()
        bugs.append({"x": x, "y": y, "coletado": False})

#loop principal
while True:

    #faz o loop roda a 60 fps
    relogio.tick(60)
    tela.fill((0, 0, 0))

    #desenha a barra superior
    pygame.draw.rect(tela, AZUL, (0, 0, 500, 100))

    #desenha o texto de componentes coletados
    texto_componentes = fonte.render(f"Componentes: {comp_coletados}/3",True,BRANCO)
    tela.blit(texto_componentes, (15, 35))

    #cria os blocos de colisão
    jeraldo_rect = pygame.Rect(jeraldo_x, jeraldo_y + 100, jeraldo_img.get_width(), jeraldo_img.get_height())
    servidor_rect = pygame.Rect(servidor_x, servidor_y +100, servidor_img.get_width(), servidor_img.get_height())

    #desenhar tabuleiro
    for linha in range(5):
        for coluna in range(5):
            cor = CINZA if (linha + coluna) % 2 == 0 else BRANCO
            pygame.draw.rect(tela, cor,(coluna * 100, linha * 100 + 100, 100, 100))

    #cria o evento de sair do jogo
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                exit()
            if event.key == pygame.K_r and (game_over or venceu):
                reiniciar_jogo()
                continue
        
        #movimentação do jeraldo
            if event.key == pygame.K_UP or event.key == pygame.K_w:
                if jeraldo_y > 100:
                    jeraldo_y -= 100
                else:
                    mostrar_mensagem = True
                    tempo_mensagem = pygame.time.get_ticks()
            elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                if jeraldo_y < 400:
                    jeraldo_y += 100
                else:
                    mostrar_mensagem = True
                    tempo_mensagem = pygame.time.get_ticks()
            elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                if jeraldo_x > 100:
                    jeraldo_x -= 100
                else:
                    mostrar_mensagem = True
                    tempo_mensagem = pygame.time.get_ticks()
            elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                if jeraldo_x < 400:
                    jeraldo_x += 100
                else:
                    mostrar_mensagem = True
                    tempo_mensagem = pygame.time.get_ticks()
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                exit()

    #desenha as vidas do jeraldo
    for i in range(vidas):
        tela.blit(vida_img, (400 - i * 50, 5))

    #verifica colisão Jeraldo com os componentes e bugs
    for componente in componentes:
        if not componente["coletado"]:
            rect = pygame.Rect(componente["x"], componente["y"] + 100, comp_img.get_width(), comp_img.get_height())

            if jeraldo_rect.colliderect(rect):
                componente["coletado"] = True
                comp_coletados += 1

    #verifica colisão Jeraldo com os bugs
    for bug in bugs:
        if not bug["coletado"]:
            rect = pygame.Rect(bug["x"], bug["y"] + 100, bug_img.get_width(), bug_img.get_height())

            if jeraldo_rect.colliderect(rect):
                bug["coletado"] = True
                vidas -= 1

    #desenha os elementos na tela
    for componente in componentes:
        if componente["coletado"]:
            tela.blit(comp_img, (componente["x"], componente["y"] + 100))

    for bug in bugs:
        if bug["coletado"]:
            tela.blit(bug_img, (bug["x"], bug["y"] + 100))

    tela.blit(servidor_img, (servidor_x, servidor_y + 100))
    tela.blit(jeraldo_img, (jeraldo_x, jeraldo_y + 100))

    if mostrar_mensagem and pygame.time.get_ticks() - tempo_mensagem < 1000:
        tela.blit(mostrar_img, (100, 178))
        mostrar_mensagem = True
    else:
        mostrar_mensagem = False

    if aviso_mensagem and pygame.time.get_ticks() - tempo_aviso < 30:
        fundo = pygame.Surface((800, 600))
        fundo.set_alpha(180)
        fundo.fill((0, 0, 0))
        tela.blit(fundo, (0, 0))
        tela.blit(aviso_comp, (75, 171))

    if venceu:
        tela.fill((255, 255, 255))
        tela.blit(vitoria_img, (0, 25))
        texto = fonte.render("R - Reiniciar  ESC - Sair", True, PRETO)
        tela.blit(texto, (50, 550))

    if vidas == 0:
        tela.fill((255, 255, 255))
        tela.blit(gameover_img, (0, 25))
        game_over = True
        texto = fonte.render("R - Reiniciar  ESC - Sair", True, PRETO)
        tela.blit(texto, (50, 550))

    #verifica colisão Jeraldo com o servidor
    if jeraldo_rect.colliderect(servidor_rect) and not venceu:
        if comp_coletados == 3:
            venceu = True
            
        else:
            aviso_mensagem = True
            tempo_aviso = pygame.time.get_ticks()

    pygame.display.update()