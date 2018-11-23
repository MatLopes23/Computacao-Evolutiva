# -*- coding: utf-8 -*-
import random
import math
import time
import matplotlib.pyplot as plt


def inicializa_Populacao(P, n_var):
    for j in range(n_var):
        a = random.uniform(-5.12, 5.12)
        P.append(a)

def fitness(pena, P, n_var, FO):
    x = 0
    for i in range(n_var):
        x += (P[i]*P[i]-10*math.cos(2*math.pi*P[i]))
    x += 10*n_var
    P.append(round(x, 7))
    FO += 1
    if pena == 1:
        penalI = 10 ** 4
        penalD = 10 ** 4
        sumD = 0.0
        sumI = 0.0
        for j in range(n_var):
            sumAux = gi(P[j])
            if sumAux > 0:
                sumD += sumAux ** 2
        for j in range(n_var):
            sumAux = hi(P[j])
            sumI += sumAux ** 2
        P[n_var] += (penalI * sumI) + (penalD * sumD)
    return FO

def gi(xi):
    return (math.sin(2 * math.pi * xi) + 0.5)

def hi(xi):
    return (math.cos(2 * math.pi * xi) + 0.5)

def vizinho(pena,P, n_var, FO):
    Q = P[:]
    i = random.randrange(n_var)
    aux = random.uniform(-1, 1)
    Q[i] += aux
    if Q[i] > 5.12:
        Q[i] = 5.12
    elif Q[i] < (-5.12):
        Q[i] = (-5.12)
    Q.pop()
    FO = fitness(pena, Q, n_var, FO)
    return Q, FO

def RS(n_var, pena, Itermax):
    P = []
    Q = []
    IterT = 0
    T = 100000
    Tf = 10**(-10)
    alfa = 0.995

    fitmelhor = []
    FOO = []


    t = time.time()
    inicializa_Populacao(P, n_var)
    fitness(pena, P, n_var, 0)
    FO = 0
    Best = P[:]
    while(1):
        while IterT < Itermax:
            IterT += 1
            Q, FO = vizinho(pena, P, n_var, FO)
            delta = Q[n_var] - P[n_var]
            if delta < 0:
                P = Q[:]
                if Q[n_var] < Best[n_var]:
                    Best = Q[:]
            else:
                if random.random() < math.exp((-delta)/T):
                    P = Q[:]
        T *= alfa
        IterT = 0
        fitmelhor.append(P[n_var])
        FOO.append(FO)
        if FO >= 10000:
            break
        '''if time.time() - t >= 8:
            break'''

    return fitmelhor, FOO



#------------------------------------------------------------------------------
n_var = 3

fitmelhor = []
FO = []
menor_tamanho = 100000000000
fitb = []
fom = []

for i in range(100):
    print i
    a = []
    b = []
    a, b = RS(n_var, 0, n_var)

    if(len(a)<menor_tamanho):
        menor_tamanho = len(a)
    fitmelhor.append(a)
    FO.append(b)


for i in range(menor_tamanho):
    aux = 0
    aux1 = 0
    for j in range(100):
        aux += fitmelhor[j][i]
        aux1 += FO[j][i]
    fitb.append(aux/100)
    fom.append(aux1/100)

#plt.ylim(-2, 110)
#plt.xlim(-10, 10000)
#plt.title("Torneio, Bit a Bit, Pm=0.025")
plt.xlabel(u'Avaliação função Objetivo')
plt.ylabel('fitness')
plt.plot(fom, [0]*menor_tamanho, 'r--', label=u"ótimo global")
plt.plot(fom, fitb,'g-', label="melhor fitness", )
plt.legend(loc=0)
plt.grid(True)
plt.show()

aux = 0
for i in range(100):
    aux += fitmelhor[i][len(fitmelhor[i])-1]

print aux/100
