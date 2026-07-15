import pygame
import random

pygame.init()

#  CLASSE: Posicao
class Posicao:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def como_tupla(self):
        return (self.x, self.y)

    def __eq__(self, other):
        if isinstance(other, Posicao):
            return self.x == other.x and self.y == other.y
        return False

#  CLASSE: GeradorDePosicao
class GeradorDePosicao:
    CASAS = [25, 125, 225, 325, 425]
    PROIBIDAS = [(25, 25), (425, 425)]

    def __init__(self):
        self.ocupadas = []

    def gerar(self):
        while True:
            x = random.choice(self.CASAS)
            y = random.choice(self.CASAS)
            nova = Posicao(x, y)

            if nova in self.ocupadas:
                continue
            if nova.como_tupla() in self.PROIBIDAS:
                continue

            self.ocupadas.append(nova)
            return nova

    def resetar(self):
        self.ocupadas.clear()

#  CLASSE: Entidade  (base para todos os elementos)
class Entidade:
    def __init__(self, posicao, imagem):
        self.posicao = posicao
        self.imagem = imagem

    def get_rect(self, offset_y=100):
        return pygame.Rect(self.posicao.x, self.posicao.y + offset_y, self.imagem.get_width(), self.imagem.get_height())

    def desenhar(self, tela, offset_y=100):
        tela.blit(self.imagem, (self.posicao.x, self.posicao.y + offset_y))

#  CLASSE: Coletavel  (herda de Entidade)
class Coletavel(Entidade):
    def __init__(self, posicao, imagem):
        super().__init__(posicao, imagem)
        self.coletado = False

    def coletar(self):
        self.coletado = True

#  CLASSE: Componente  (herda de Coletavel)
class Componente(Coletavel):
    def __init__(self, posicao, imagem):
        super().__init__(posicao, imagem)

#  CLASSE: Bug  (herda de Coletavel)
class Bug(Coletavel):
    def __init__(self, posicao, imagem):
        super().__init__(posicao, imagem)

#  CLASSE: Jeraldo  (herda de Entidade)
class Jeraldo(Entidade):
    CASAS = [25, 125, 225, 325, 425]

    def __init__(self, imagem):
        super().__init__(Posicao(25, 25), imagem)
        self.vidas = 3

    def mover(self, dx, dy):
        novo_x = self.posicao.x + dx
        novo_y = self.posicao.y + dy
        if novo_x in self.CASAS and novo_y in self.CASAS:
            self.posicao.x = novo_x
            self.posicao.y = novo_y
            return True
        return False

    def perder_vida(self):
        self.vidas -= 1

    def esta_vivo(self):
        return self.vidas > 0

    def resetar(self):
        self.posicao = Posicao(25, 25)
        self.vidas = 3

#  CLASSE: Servidor  (herda de Entidade)
class Servidor(Entidade):
    def __init__(self, imagem):
        super().__init__(Posicao(425, 425), imagem)

#  CLASSE: Tabuleiro
class Tabuleiro:
    CINZA = (200, 200, 200)
    BRANCO = (255, 255, 255)

    def __init__(self):
        self.linhas = 5
        self.colunas = 5

    def desenhar(self, tela):
        for linha in range(self.linhas):
            for coluna in range(self.colunas):
                if (linha + coluna) % 2 == 0:
                    cor = self.CINZA
                else:
                    cor = self.BRANCO
                pygame.draw.rect(
                    tela, cor,
                    (coluna * 100, linha * 100 + 100, 100, 100))

#  CLASSE: HUD
class HUD:
    AZUL = (46, 54, 152)
    BRANCO = (255, 255, 255)

    def __init__(self, fonte, vida_img):
        self.fonte = fonte
        self.vida_img = vida_img

    def desenhar(self, tela, comp_coletados, vidas):
        pygame.draw.rect(tela, self.AZUL, (0, 0, 500, 100))

        texto = self.fonte.render(
            f"Componentes: {comp_coletados}/3", True, self.BRANCO
        )
        tela.blit(texto, (15, 35))

        for i in range(vidas):
            tela.blit(self.vida_img, (400 - i * 50, 5))

#  CLASSE: GerenciadorDeMensagens
class GerenciadorDeMensagens:
    def __init__(self, img_parede, img_aviso):
        self.img_parede = img_parede
        self.img_aviso = img_aviso
        self.mostrar_mensagem = False
        self.mostrar_aviso = False
        self.tempo_mensagem = 0
        self.tempo_aviso = 0

    def ativar_mensagem(self):
        self.mostrar_mensagem = True
        self.tempo_mensagem = pygame.time.get_ticks()

    def ativar_aviso(self):
        self.mostrar_aviso = True
        self.tempo_aviso = pygame.time.get_ticks()

    def desenhar(self, tela):
        agora = pygame.time.get_ticks()

        if self.mostrar_mensagem:
            if agora - self.tempo_mensagem < 1000:
                tela.blit(self.img_parede, (100, 178))
            else:
                self.mostrar_mensagem = False

        if self.mostrar_aviso:
            if agora - self.tempo_aviso < 30:
                fundo = pygame.Surface((800, 600))
                fundo.set_alpha(180)
                fundo.fill((0, 0, 0))
                tela.blit(fundo, (0, 0))
                tela.blit(self.img_aviso, (75, 171))
            else:
                self.mostrar_aviso = False

#  CLASSE: Jogo  (orquestra tudo)
class Jogo:
    PRETO = (0, 0, 0)
    BRANCO = (255, 255, 255)

    def __init__(self):
        self.tela = pygame.display.set_mode((500, 600))
        pygame.display.set_caption("Jeraldo - O robô")
        pygame.display.set_icon(
            pygame.image.load("sprites/jeraldo_icon.png"))
        
        self.relogio = pygame.time.Clock()
        self.fonte = pygame.font.Font("fontes/PixelOperatorMono-Bold.ttf", 30)
        
        self.__carregar_imagens()
        self.__inicializar()

    def __carregar_imagens(self):
        self.img_jeraldo = pygame.image.load("sprites/jeraldo.png")
        self.img_servidor = pygame.image.load("sprites/servidor.png")
        self.img_bug = pygame.image.load("sprites/bug.png")
        self.img_comp = pygame.image.load("sprites/componente.png")
        self.img_vida = pygame.transform.scale(pygame.image.load("sprites/vida.png"), (90, 90))
        self.img_parede = pygame.transform.scale(pygame.image.load("sprites/parede_mensagem.png"), (300, 300))
        self.img_aviso = pygame.transform.scale(pygame.image.load("sprites/aviso_comp.png"), (350, 350))
        self.img_gameover = pygame.transform.scale(pygame.image.load("sprites/gameover.png"), (500, 500))
        self.img_vitoria = pygame.transform.scale(pygame.image.load("sprites/vitoria.png"), (500, 500))

    def __inicializar(self):
        self.gerador    = GeradorDePosicao()
        self.tabuleiro  = Tabuleiro()
        self.jeraldo    = Jeraldo(self.img_jeraldo)
        self.servidor   = Servidor(self.img_servidor)
        self.hud        = HUD(self.fonte, self.img_vida)
        self.mensagens  = GerenciadorDeMensagens(self.img_parede, self.img_aviso)
        self.comp_coletados = 0
        self.venceu     = False
        self.game_over  = False
        self.__criar_elementos()

    def __criar_elementos(self):
        self.componentes = [Componente(self.gerador.gerar(), self.img_comp)
            for _ in range(3)]
        
        self.bugs = [Bug(self.gerador.gerar(), self.img_bug)
            for _ in range(3)]

    def __reiniciar(self):
        self.gerador.resetar()
        self.jeraldo.resetar()
        self.comp_coletados = 0
        self.venceu    = False
        self.game_over = False
        self.__criar_elementos()

    def __processar_eventos(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return False

                if event.key == pygame.K_r:
                    if self.game_over or self.venceu:
                        self.__reiniciar()

                if not self.game_over and not self.venceu:
                    self.__mover_jeraldo(event.key)

        return True

    def __mover_jeraldo(self, tecla):
        movimentos = {
            pygame.K_UP:    ( 0,  -100),
            pygame.K_w:     ( 0,  -100),
            pygame.K_DOWN:  ( 0,   100),
            pygame.K_s:     ( 0,   100),
            pygame.K_LEFT:  (-100,   0),
            pygame.K_a:     (-100,   0),
            pygame.K_RIGHT: ( 100,   0),
            pygame.K_d:     ( 100,   0),
        }
        if tecla in movimentos:
            dx, dy = movimentos[tecla]
            if not self.jeraldo.mover(dx, dy):
                self.mensagens.ativar_mensagem()

    def __verificar_colisoes(self):
        j_rect = self.jeraldo.get_rect()

        for comp in self.componentes:
            if not comp.coletado:
                if j_rect.colliderect(comp.get_rect()):
                    comp.coletar()
                    self.comp_coletados += 1

        for bug in self.bugs:
            if not bug.coletado:
                if j_rect.colliderect(bug.get_rect()):
                    bug.coletar()
                    self.jeraldo.perder_vida()

        if j_rect.colliderect(self.servidor.get_rect()):
            if self.comp_coletados == 3:
                self.venceu = True
            else:
                self.mensagens.ativar_aviso()

        if not self.jeraldo.esta_vivo():
            self.game_over = True

    def __desenhar(self):
        self.tela.fill(self.PRETO)
        self.tabuleiro.desenhar(self.tela)

        for comp in self.componentes:
            if comp.coletado:
                comp.desenhar(self.tela)
        for bug in self.bugs:
            if bug.coletado:
                bug.desenhar(self.tela)

        self.servidor.desenhar(self.tela)
        self.jeraldo.desenhar(self.tela)
        self.mensagens.desenhar(self.tela)
        self.hud.desenhar(self.tela, self.comp_coletados, self.jeraldo.vidas)

        if self.venceu:
            self.tela.fill(self.BRANCO)
            self.tela.blit(self.img_vitoria, (0, 25))
            texto = self.fonte.render("R - Reiniciar  ESC - Sair", True, self.PRETO)
            self.tela.blit(texto, (50, 550))

        if self.game_over:
            self.tela.fill(self.BRANCO)
            self.tela.blit(self.img_gameover, (0, 25))
            texto = self.fonte.render("R - Reiniciar  ESC - Sair", True, self.PRETO)
            self.tela.blit(texto, (50, 550))

        pygame.display.update()

    def rodar(self):
        rodando = True
        while rodando:
            self.relogio.tick(60)
            rodando = self.__processar_eventos()
            if not self.game_over and not self.venceu:
                self.__verificar_colisoes()
            self.__desenhar()
        pygame.quit()

#  EXECUÇÃO
if __name__ == "__main__":
    jogo = Jogo()
    jogo.rodar()