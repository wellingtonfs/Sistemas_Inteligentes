import pygame, sys, random
from jogador import Jogador, NovaGeracao

pygame.init()
pygame.font.init()

size = width, height = 480, 600
populacao = 100
speed_init = 0.4
aceleracao = 1e-4

pygame.display.set_caption("Game")
screen = pygame.display.set_mode(size)
fonte = pygame.font.SysFont("Arial Black", 35)

def colision(b, r):
    if r.x <= b.x <= r.x + 30:
        return True
    
    return False

class Bola:
    def __init__(self) -> None:
        global width, height, aceleracao, speed_init

        self.x = 0
        self.y = 0
        self.inc = 0
        self.speed = speed_init
        self.size = 10
        self.viva = True
        self.aceleracao = aceleracao

        self.create()

    def acelera(self):
        self.speed += self.aceleracao

    def isAlive(self):
        return self.viva

    def create(self):
        global width, height

        self.y = -self.size
        self.x = random.randint(self.size, width - self.size)
        self.inc = random.gauss(0, 0.7)
        self.viva = True

    def plot(self, screen):
        global width, height, speed_init

        pygame.draw.circle(screen, (255, 255, 255), (self.x, self.y), self.size)

        self.y += self.speed
        x = self.x + self.inc * self.speed
        if x < self.size or x > width - self.size:
            self.inc *= -1
            self.x = self.x + self.inc * self.speed
        else:
            self.x = x

        if self.y + self.size >= height - 50:
            self.speed = speed_init
            self.viva = False

jogadores = [Jogador() for _ in range(populacao)]
bola = Bola()

game_over = False

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()

    key = pygame.key.get_pressed()

    #if key[pygame.K_LEFT]:
    #    raquete.moveLeft()
    #if key[pygame.K_RIGHT]:
    #    raquete.moveRight()
    #if game_over and (key[pygame.K_RETURN] or key[pygame.K_KP_ENTER]):
    #    game_over = False
    #    bola.create()
    #    raquete.reset()

    screen.fill((0, 0, 0))

    [ jogador.plot(screen, bola) for jogador in jogadores ]

    bola.plot(screen)

    if not bola.isAlive():# or all(not j.alive for j in jogadores):
        win = False

        for jogador in jogadores:
            if not jogador.alive:
                continue

            if colision(bola, jogador):
                jogador.addPontos(bola.x)
                win = True
            else:
                #jogador.addPontos(bola.x)
                jogador.kill()

        bola.create()

        if win:
            bola.acelera()
            #print("acelera")
        else:
            jogadores = NovaGeracao(jogadores)

        #screen.blit(
        #    fonte.render("Game Over", True, (255, 255, 255)),
        #    (width//2 - fonte.size("Game Over")[0]//2, height // 2)
        #)

    pygame.display.update()