import pygame
from pygame.locals import*
from sys import exit
import os
from random import randrange, choice

pygame.init()
pygame.mixer.init()

diretorio_principal = os.path.dirname(__file__)

diretorio_imagens = os.path.join(diretorio_principal, 'spritessheet-dino')
diretorio_sons = os.path.join(diretorio_principal, 'pasta_sons')

tela = pygame.display.set_mode((800, 600))
pygame.display.set_caption('aula18')

sprite_sheet = pygame.image.load('spritessheet-dino/dinoSpritesheet.png').convert_alpha()

som_colisao = pygame.mixer.Sound(os.path.join(diretorio_sons, 'GameOverSound1.wav'))
som_colisao.set_volume(0.5)
colidiu = False

escolha_obstaculo = choice([0, 1])
pontos = 0
velocidade_jogo = 0

def exibe_mensagem(msg, tamanho, cor):
    fonte = pygame.font.SysFont('comicsansns', tamanho, True, False)
    mensagem = f'{msg}'
    texto_formatado = fonte.render(mensagem, True, cor)
    return texto_formatado

class Dino(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.dino = list()
        for c in range(3):
            img = sprite_sheet.subsurface((32*c, 0), (32, 32))
            self.dino.append(img)
        self.atual = 0
        self.som_pulo = pygame.mixer.Sound(os.path.join(diretorio_sons, 'Som_deColizao.wav'))
        self.som_pulo.set_volume(0.5)
        self.image = self.dino[self.atual]
        self.image = pygame.transform.scale(self.image, (128, 128))
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.center = (100, 504)
        self.comecar = False
        self.pulo = False


    def update(self):
        if self.pulo == True:
            if self.rect.y > 240:
                self.rect.y -= 6
            else:
                self.pulo = False
        else:
            if self.rect.center[1] < 504:
                self.rect.y += 6

            self.atual += 0.15
            if self.atual >= len(self.dino):
                self.atual = 0
            self.image = self.dino[int(self.atual)]
            self.image = pygame.transform.scale(self.image, (128, 128))

    def start(self):
        self.comecar = True

    def pular(self):
        self.pulo = True
        self.som_pulo.play()

class Nuvens(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.comecar = False
        self.image = sprite_sheet.subsurface((7*32, 0), (32, 32))
        self.image = pygame.transform.scale(self.image, (96, 96))
        self.rect = self.image.get_rect()
        self.rect.y = randrange(50, 200, 50)
        self.rect.x = 800 - randrange(30, 300, 90)

    def update(self):
        self.rect.x -= 1
        if self.rect.topright[0] <= 0:
            self.rect.y = randrange(50, 200, 50)
            self.rect.x = 800

    def start(self):
        self.comecar = True

class Chao(pygame.sprite.Sprite):
    def __init__(self, largura_inicial):
        pygame.sprite.Sprite.__init__(self)
        self.largura = largura_inicial
        self.image = sprite_sheet.subsurface((6*32, 0), (32, 32))
        self.image = pygame.transform.scale(self.image, (100, 100))
        self.rect = self.image.get_rect()
        self.rect.topleft = (self.largura, 500)

    def update(self):
        self.rect.x -= 2
        if self.rect.topright[0] <= 0:
            self.rect.topleft = 800, 500

class Cacto(pygame.sprite.Sprite):
        def __init__(self):
            pygame.sprite.Sprite.__init__(self)
            self.image = sprite_sheet.subsurface((5*32, 0), (32, 32))
            self.image = pygame.transform.scale(self.image, (64, 64))
            self.rect = self.image.get_rect()
            self.mask = pygame.mask.from_surface(self.image)
            self.escolha = escolha_obstaculo
            self.rect.topleft = 800, 500

        def update(self):
            self.escolha = escolha_obstaculo
            if self.escolha == 1: #ipccccccccccc
                self.rect.x -= 2


class DinoVoador(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.sprites = list()
        for c in range(2):
            img = sprite_sheet.subsurface((96 + c*32, 0), (32, 32))
            self.sprites.append(img)
        self.atual = 0
        self.image = self.sprites[self.atual]
        self.escolha = escolha_obstaculo
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.topleft = 800, 450
        self.image = pygame.transform.scale(self.image, (96, 96))

    def update(self):
        self.escolha = escolha_obstaculo
        if self.escolha == 0:
           self.atual += 0.1
           if self.atual >= 2:
               self.atual = 0
           self.image = self.sprites[int(self.atual)]
           self.image = pygame.transform.scale(self.image, (96, 96))
           self.rect.x -= 5

todas_sprites = pygame.sprite.Group()
grupo_obstacuos = pygame.sprite.Group()

dino = Dino()
todas_sprites.add(dino)

for c in range(4):
    nuvem = Nuvens()
    todas_sprites.add(nuvem)

for c in range(9):
    chao = Chao(c*100)
    todas_sprites.add(chao)

cacto = Cacto()
todas_sprites.add(cacto)
grupo_obstacuos.add(cacto)

dino_voador = DinoVoador()
todas_sprites.add(dino_voador)
grupo_obstacuos.add(dino_voador)

relogio = pygame.time.Clock()
while True:
    tela.fill((255, 255, 255))
    relogio.tick(100 + 5*velocidade_jogo)
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit()
        if event.type == KEYDOWN:
            if event.key == K_SPACE:
                if dino.rect.center[1] == 504:
                    dino.pular()

            if event.key == K_r:
                colidiu = False
                dino_voador.rect.x = 800
                cacto.rect.x = 800
                pontos = 0
                velocidade_jogo = 0

    colisoes = pygame.sprite.spritecollide(dino, grupo_obstacuos, False, pygame.sprite.collide_mask)
    todas_sprites.draw(tela)

    if cacto.rect.topright[0] <= 0 or dino_voador.rect.topright[0] <= 0:
        escolha_obstaculo = choice([0, 1, 1, 1])
        dino_voador.rect.topleft = 800, 450
        cacto.rect.topleft = 800, 500

    if colisoes and colidiu == False:
        som_colisao.play()
        colidiu = True

    elif colidiu == True:
        mensagem = exibe_mensagem('game over', 60, (0, 0, 0))
        pontuacao = exibe_mensagem(f'Pontuação: {int(pontos)}', 30, (0, 0, 0))
        recomeco = exibe_mensagem('aperte r para recomeçar', 25, (0, 0, 0))
        tela.blit(mensagem, (290, 250))
        tela.blit(pontuacao, (300, 300))
        tela.blit(recomeco, (20, 100))

    else:
        pontos += 0.25
        todas_sprites.update()
        texto_pontos = exibe_mensagem(int(pontos), 40, (0, 0, 0))
        tela.blit(texto_pontos, (660, 30))

    if pontos % 100 == 0:
        velocidade_jogo += 1

    pygame.display.flip()

