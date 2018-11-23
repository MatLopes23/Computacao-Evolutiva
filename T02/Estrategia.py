# -*- coding: utf-8 -*-
import random
import math
import time
import matplotlib.pyplot as plt

def inicializa_Populacao(P, n_var, TamP):
    for i in range(TamP):
        linhas = []
        for j in range(n_var):
            a = random.uniform(-5.12, 5.12)
            linhas.append(a)
        for j in range(n_var):
            b = abs(linhas[j])/math.pow(n_var, 0.5)
            linhas.append(b)
        P.append(linhas)

def fitness_medio(P, PO, n_var):
    M=0.0
    for i in range(PO):
        M=M+P[i][n_var*2]
    M=M/PO
    return M

def fitness(pena, P, n_var, TamP, FO):
    for i in range(TamP):
        x = 0
        for j in range(n_var):
            x += (P[i][j]*P[i][j]-10*math.cos(2*math.pi*P[i][j]))
        x += 10*n_var
        P[i].append(x)
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
            P[i][n_var*2] += (penalI * sumI) + (penalD * sumD)
    return FO

def gi(xi):
    return (math.sin(2 * math.pi * xi) + 0.5)

def hi(xi):
    return (math.cos(2 * math.pi * xi) + 0.5)

def recombinar(P, TamP, n_var):
    S = []
    for i in range(10):
        linha = []
        a = random.randrange(TamP)
        b = random.randrange(TamP)
        if b == a:
            if b+1 == 20:
                b = 0
            else:
                b += 1

        for j in range(n_var):
            aux = P[a][j]+(P[a][j]-P[b][j])*random.gauss(0, 1)
            if aux > 5.12:
                aux = 5.12
            elif aux < (-5.12):
                aux = (-5.12)
            linha.append(aux)
        for j in range(n_var):
            aux = P[a][j+n_var]+(P[a][j+n_var]-P[b][j+n_var])*random.gauss(0, 1)
            linha.append(aux)
        S.append(linha)
    return S[:]

def mutar(S, TamP, n_var, Delta1, Delta2):
    for i in range(10):
        Z = random.gauss(0, (Delta2**2))#### OBSERVAR
        for j in range(n_var):
            Zi = random.gauss(0, (Delta1**2))#### OBSERVAR
            S[i][j+n_var] = S[i][j+n_var] * math.exp(Zi) * math.exp(Z)
            #S[i][j] = S[i][j] + S[i][j+n_var] * random.gauss(0, 1)
            S[i][j] = S[i][j] + random.gauss(0, S[i][j+n_var]**2)

def substituicao(P, S, n_var):
    for i in range(10):
        P.append(S[i][:])
    P.sort(key=lambda x: x[n_var*2])
    for i in range(10):
        P.pop()
    del S[:]

def EE(n_var, pena, Delta1, Delta2):
    P = []
    S = []
    TamP = 20
    fitmedio = []
    fitmelhor = []
    FOO = []

    t= time.time()
    inicializa_Populacao(P, n_var, TamP)
    fitness(pena, P, n_var, TamP, 0)
    FO = 0

    while 1:
        S = recombinar(P, TamP, n_var)
        mutar(S, TamP, n_var, Delta1, Delta2)
        FO = fitness(pena, S, n_var, 10, FO)
        substituicao(P, S, n_var)

        fitmedio.append(fitness_medio(P, TamP, n_var))
        fitmelhor.append(P[0][n_var*2])
        FOO.append(time.time()-t)

        '''if FO >= 10000:
            break'''
        if time.time()-t >= 400:
            break

    '''for i in range(20):
        print i, P[i][n_var*2]'''

    return fitmelhor, fitmedio, FOO



#--------------------------------------------------------------
n_var = 10
Delta1 = (math.pow((2*math.pow(n_var, 0.5)), 0.5))
Delta2 = (math.pow(2*n_var, 0.5))

fitmelhor = []
fitmedio = []
FO = []

menor_tamanho = 1000000000000000000000000000
fitb = []
fitm = []
fom = []
teste = 1

for i in range(teste):
    print i
    a = []
    b = []
    c = []
    a, b, c = EE(n_var, 1, Delta1, Delta2)

    if(len(a)<menor_tamanho):
        menor_tamanho = len(a)
    fitmelhor.append(a)
    fitmedio.append(b)
    FO.append(c)


for i in range(menor_tamanho):
    aux = 0
    aux1 = 0
    aux2 = 0
    for j in range(teste):
        aux += fitmelhor[j][i]
        aux1 += fitmedio[j][i]
        aux2 += FO[j][i]
    fitb.append(aux/teste)
    fitm.append(aux1/teste)
    fom.append(aux2/teste)

aux = 0
for i in range(teste):
    aux += fitmelhor[i][len(fitmelhor[i])-1]

print aux/teste
print n_var


#plt.ylim(-2, 110)
#plt.xlim(-10, 10000)
#plt.title("Torneio, Bit a Bit, Pm=0.025")
plt.xlabel(u'Avaliação função Objetivo')
plt.ylabel('fitness')

if n_var == 3:
    plt.plot(fom, [43.33] * menor_tamanho, 'r--', label=u"ótimo global(45.33)")
elif n_var == 5:
    plt.plot(fom, [75.56] * menor_tamanho, 'r--', label=u"ótimo global(75.56)")
else:
    plt.plot(fom, [151.11] * menor_tamanho, 'r--', label=u"ótimo global(151.11)")
'''

plt.plot(fom, [0] * menor_tamanho, 'r--', label=u"ótimo global")'''
plt.plot(fom, fitm, label=u"fitness médio")
plt.plot(fom, fitb,'g-', label="melhor fitness", )
plt.legend(loc=0)
plt.grid(True)
plt.show()



