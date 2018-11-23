# -*- coding: utf-8 -*-

import random
import math
import time
import matplotlib.pyplot as plt

def fitness_medio(P, PO, n_var):
    M=0.0
    for i in range(PO):
        M=M+P[i][n_var]
    M=M/PO
    return M

def inicializa_Populacao(P, n_var):
    for i in range(20):
        linhas = []
        for j in range(n_var):
            a = random.uniform(-5.12, 5.12)
            linhas.append(a)
        P.append(linhas)

def fitness(pena, P, n_var, TamP, FO):
    for i in range(TamP):
        if len(P[i]) != n_var+1:
            x = 0
            for j in range(n_var):
               x += (P[i][j]*P[i][j]-10*math.cos(2*math.pi*P[i][j]))
            x += 10*n_var
            P[i].append(round(x, 7))
            FO += 1
    if pena == 1:
        for i in range(TamP):
            penalI = 10 ** 4
            penalD = 10 ** 4
            sumD = 0.0
            sumI = 0.0
            for j in range(n_var):
                sumAux = gi(P[i][j])
                if sumAux > 0:
                    sumD += sumAux ** 2
            for j in range(n_var):
                sumAux = hi(P[i][j])
                sumI += sumAux ** 2
            P[i][n_var] += (penalI * sumI) + (penalD * sumD)
    return FO

def gi(xi):
    return math.sin(2 * math.pi * xi) + 0.5

def hi(xi):
    return math.cos(2 * math.pi * xi) + 0.5

def selecao_torneio(P, n_var):
    S = []
    for i in range(40):
        a = random.randrange(20)
        b = random.randrange(20)
        if b == a:
            if b+1 == 20:
                b = 0
            else:
                b += 1
        if P[a][n_var] <= P[b][n_var]:
            S.append(P[a][:])
        else:
            S.append(P[b][:])
    return S[:]

def cruzamento_media(S, Tc, n_var):
    Q = []
    for i in range(0, 40, 2):
        if random.random() < Tc:
            F = []
            for j in range(n_var):
                F.append((S[i][j]+S[i+1][j])/2)
            Q.append(F)
        else:
            if S[i][n_var] <= S[i+1][n_var]:
                Q.append(S[i][:])
            else:
                Q.append(S[i+1][:])
    del S[:]
    return Q[:]

def mutacao(Q, n_var):
    for i in range(20):
        j = random.randrange(n_var)
        aux = random.uniform(-1, 1)
        Q[i][j] += aux
        if Q[i][j] > 5.12:
            Q[i][j] = 5.12
        elif Q[i][j] < (-5.12):
            Q[i][j] = (-5.12)

        if (len(Q[i]) == n_var + 1):
            Q[i].pop()

def mutacao_bit_bit(Q, n_var, Pm):
    for i in range(20):
        x = 0
        for j in range(n_var):
            if random.random() <= Pm:
                x = 1
                aux = random.gauss(0, 2)
                Q[i][j] += aux
        if x == 1 and len(Q[i]) == n_var+1:
            Q[i].pop()

def substituicao(P, Q, n_var, TamP):
    Quant_P = int(TamP * 0.1)
    Q.sort(key=lambda x: x[n_var],reverse= True)
    P.sort(key=lambda x: x[n_var])

    for i in range(Quant_P):
        Q.pop(0)
        Q.append(P.pop(0)[:])
    Q.sort(key=lambda x: x[n_var])

    return Q


#-----------------------main-------------------------


def AG(n_var, TamP, Tc, Tm, pena):
    P = []
    S = []
    Q = []
    FO = 0
    fitmedio = []
    fitmelhor = []
    FOO = []

    t = time.time()
    inicializa_Populacao(P, n_var)
    fitness(pena, P, n_var, TamP, FO)
    FO = 0

    while 1:
        S = selecao_torneio(P, n_var)
        Q = cruzamento_media(S, Tc, n_var)
        mutacao_bit_bit(Q, n_var, Tm)
        FO = fitness(pena, Q, n_var, 20, FO)
        P = substituicao(P, Q, n_var, TamP)

        fitmedio.append(fitness_medio(P, TamP, n_var))
        fitmelhor.append(P[0][n_var])
        FOO.append(time.time()-t)


        '''if FO >= 10000:
            break'''
        if time.time()-t >= 2:
            break
    '''for i in range(len(P)):
        print i, P[i]'''


    return fitmelhor, fitmedio, FOO

#----------------main-----------------------

fitmelhor = []
fitmedio = []
FO = []

menor_tamanho = 100000000000
fitb = []
fitm = []
fom = []

for i in range(1):
    print i
    a = []
    b = []
    c = []
    a, b, c = AG(10, 20, 0.8, 0.1, 1)

    if(len(a)<menor_tamanho):
        menor_tamanho = len(a)
    fitmelhor.append(a)
    fitmedio.append(b)
    FO.append(c)


for i in range(menor_tamanho):
    aux = 0
    aux1 = 0
    aux2 = 0
    for j in range(1):
        aux += fitmelhor[j][i]
        aux1 += fitmedio[j][i]
        aux2 += FO[j][i]
    fitb.append(aux/1)
    fitm.append(aux1/1)
    fom.append(aux2/1)



#plt.ylim(-2, 110)
#plt.xlim(-10, 10000)
#plt.title("Torneio, Bit a Bit, Pm=0.025")
plt.xlabel(u'Segundos')
plt.ylabel('fitness')
plt.plot(fom, [75.56]*menor_tamanho, 'r--', label=u"ótimo global(75.56)")
#plt.plot(fom, fitm, label=u"fitness médio")
plt.plot(fom, fitb,'g-', label="melhor fitness", )
plt.legend(loc=0)
plt.grid(True)
plt.show()

aux = 0
for i in range(1):
    aux += fitmelhor[i][len(fitmelhor[i])-1]

print aux/1
