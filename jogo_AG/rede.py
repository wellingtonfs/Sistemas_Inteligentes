import random, copy

def ReLU(x):
    return max(0, x)

class Neuronio:
    def __init__(self, size):
        self.pesos = [random.gauss(0, 1) for _ in range(size)]
        self.saida = 1

    def setPesos(self, pesos):
        self.pesos = copy.deepcopy(pesos)

    def setSaida(self, v):
        self.saida = v

    def forward(self, vetor):
        soma = 0
        for i in range(len(vetor)):
            soma += vetor[i] * self.pesos[i]

        self.saida = ReLU(soma)

class Camada:
    def __init__(self, tam, QtdNeuroniosAntes):
        self.neuronios = [Neuronio(QtdNeuroniosAntes) for _ in range(tam)]
        self.QtdNeuroniosAntes = QtdNeuroniosAntes
        self.QtdPesos = tam * QtdNeuroniosAntes

    def vetorSaida(self):
        return [n.saida for n in self.neuronios]

    def copiarParaSaida(self, vetor):
        for i in range(len(vetor)):
            self.neuronios[i].setSaida(vetor[i])

    def setPesos(self, pesos):
        p = 0

        for n in self.neuronios:
            n.setPesos(pesos[p : p + self.QtdNeuroniosAntes])
            p += self.QtdNeuroniosAntes

    def getPesos(self):
        pesos = []

        for n in self.neuronios:
            pesos.extend(n.pesos)

        return pesos

    def forward(self, vetor):
        for n in self.neuronios:
            n.forward(vetor)
        
        return self.vetorSaida()

class Rede:
    def __init__(self, sizeEntrada, sizeSaida, qtdCamadas):
        #self.entrada = Camada(sizeEntrada, 1)
        self.camadas = []

        tam_ant = sizeEntrada
        for c in range(qtdCamadas):
            self.camadas.append(Camada(sizeEntrada + 4, tam_ant))
            tam_ant = sizeEntrada + 4

        self.camadas.append(Camada(sizeSaida, tam_ant))

    def forward(self, vetor):
        out = vetor

        for c in self.camadas:
            out = c.forward(out)

        return out

    def printPesos(self):
        #print(self.entrada.getPesos())

        for c in self.camadas:
            print(c.getPesos())

    def setPesos(self, pesos):
        #self.entrada.setPesos(pesos[ : self.entrada.QtdPesos])
        #p = self.entrada.QtdPesos
        p = 0

        for c in self.camadas:
            c.setPesos(pesos[p : p + c.QtdPesos])
            p += c.QtdPesos

    def getPesos(self):
        pesos = []
        #pesos.extend(self.entrada.getPesos())

        for c in self.camadas:
            pesos.extend(c.getPesos())

        return pesos

    def mutar(self, base):
        b = copy.deepcopy(base)
        size = len(b)

        qtdMutes = random.randint(1, size)

        for _ in range(qtdMutes):
            indice = random.randint(0, size-1)
            tipo = random.randint(0, 2)

            if tipo == 0:
                b[indice] = random.gauss(0, 1)
            elif tipo == 1:
                b[indice] *= random.gauss(0, 0.05)
            else:
                b[indice] += random.gauss(0, 0.05)

        self.setPesos(b)

        

if __name__ == "__main__":
    import random

    #pesos = [-0.7172684556628974, -0.27186969181924486, -1.052004589144525, 0.22406201113679297, 0.8643308051459538, 0.2085811748325912, 0.5767260964357124]
    
    rede = Rede(1, 1, 1)
    #rede.setPesos(pesos)

    entrada = [-1]

    #print(entrada)

    while entrada[0] <= 1:
        print(rede.forward(entrada))
        entrada[0] += 0.1

    #print(rede.getPesos())
    #rede.mutar(pesos)
    #print(rede.getPesos())
    #rede.mutar(pesos)
    #print(rede.getPesos())
    
    #print([1, 1])
    #print(rede.forward([1, 1]))