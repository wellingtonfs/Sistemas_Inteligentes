import pygame, random
from rede import Rede

width, height = 480, 600

class Jogador:
    def __init__(self) -> None:
        global width, height

        self.x = width // 2
        self.y = height - 50
        self.speed = 0.65
        self.rede = Rede(3, 2, 2)
        self.cor = (random.randint(50, 255), random.randint(50, 255), random.randint(50, 255))
        self.alive = True

        self.fitness = 0

    def addPontos(self, x):
        self.fitness += 1
        #self.fitness += 1000 / (abs(x - self.x) + 1e-3)

    def kill(self):
        self.alive = False

    def moveRight(self):
        global width
        self.x += self.speed if self.x + self.speed <= width - 30 else 0

    def moveLeft(self):
        self.x -= self.speed if self.x - self.speed >= 0 else 0

    def reset(self):
        self.x = width // 2
        self.fitness = 0
        self.alive = True

    def pensar(self, b):
        out = self.rede.forward([self.x, b.x, b.speed])

        if out[0] == 0:
            self.moveLeft()
        if out[1] == 0:
            self.moveRight()

    def plot(self, screen, b):
        if not self.alive:
            return

        self.pensar(b)

        pygame.draw.rect(screen, self.cor, pygame.Rect((self.x, self.y), (30, 8)))

def NovaGeracao(jogadores):
    ordem = sorted(jogadores, key = lambda x: x.fitness, reverse=True)

    soma = 0
    for o in ordem:
        soma += o.fitness

    print("media:", soma / len(ordem))
    #print("pior:", ordem[-1].fitness)
    #print("melhor:", ordem[0].fitness)

    new_players = ordem[:1]

    for j in ordem[1:]:
        if ordem[0].fitness > 0:
            j.rede.mutar(new_players[0].rede.getPesos())
        else:
            j.rede.mutar(j.rede.getPesos())
        new_players.append(j)

    for j in new_players:
        j.reset()
    
    return new_players