# -*- coding: utf-8 -*-
import random
import matplotlib.pyplot as plt
import numpy as np

def inicializa_Pop(P, PO):
    for i in range(PO):
        linhas = []
        for j in range(36):
            if random.random() < 0.5:
                linhas.append(0)
            else:
                linhas.append(1)
        P.append(linhas)

def avalia_Pop(P, PO):
    for i in range(PO):
        fitness(P[i])

def fitness(b):
    if(len(b)== 36):
        aux=9+b[1]*b[4]-b[22]*b[13]+b[23]*b[3]-b[20]*b[9]+b[35]*b[14]-b[10]*b[25]+b[15]*b[16]+b[2]*b[32]+b[27]*b[18]+b[11]*b[33]-b[30]*b[31]-b[21]*b[24]+b[34]*b[26]-b[28]*b[6]+b[7]*b[12]-b[5]*b[8]+b[17]*b[19]-b[0]*b[29]+b[22]*b[3]+b[20]*b[14]+b[25]*b[15]+b[30]*b[11]+b[24]*b[18]+b[6]*b[7]++b[8]*b[17]+b[0]*b[32]
        b.append(aux)

def fitness_medio(P, PO):
    M=0.0
    for i in range(PO):
        M=M+P[i][36]
    M=M/PO
    return M

def indi_dif(P, PO):
    total=0
    marcacoes=[0 for x in range(PO)]
    for i in range(PO):
        if marcacoes[i]==0:
            marcacoes[i]=1
            for j in range(PO):
                if P[i]==P[j]:
                    marcacoes[j]=1
            total+=1
    return total

def two_pc(Q, S, Pc, PO):
    del Q[:]
    for i in range(0,PO,2):
        if random.random() < Pc:
            P1 = random.randrange(1,PO-1,1)
            P2 = random.randrange(P1+1,PO,1)
            F1 = []
            F2 = []
            for j in range(36):
                if(j<P1) or (j>=P2):
                    F1.append(S[i][j])
                    F2.append(S[i+1][j])
                else:
                    F1.append(S[i+1][j])
                    F2.append(S[i][j])
            Q.append(F1[:])
            Q.append(F2[:])
        else:
            Q.append(S[i][:])
            Q.append(S[i+1][:])

#--------------------------------------------------SELECAO-----------------------------------------------------------
def selecao(S, P, PO, x):
    del S[:]
    if x==0:
        selecao_torneio(S, P, PO)
    else:
        selecao_roleta(S, P, PO)

def selecao_torneio(S, P, PO):
    for i in range(PO):
        a = random.randrange(PO)
        b = random.randrange(PO)
        if b == a:
            if b+1 == PO:
                b = 0
            else:
                b += 1
        if P[a][36] >= P[b][36]:
            S.append(P[a][:])
        else:
            S.append(P[b][:])

def selecao_roleta(S,P,PO):
    acumula = []
    M = fitness_medio(P,PO)
    for i in range(PO):
        pi = P[i][36]/(PO*M)
        if i == 0:
            acumula.append(pi)
        else:
            acumula.append(pi+acumula[i-1])
    for i in range(PO):
        t = random.random()
        j = 0
        while 1:
            if t<acumula[j]:
                S.append(P[j][:])
                break
            elif j==29:
                S.append(P[j][:])
                break
            j=j+1
#--------------------------------------------------------------------------------------------------------------------

#--------------------------------------------------MUTACAO-----------------------------------------------------------
def mutacao(Q, Pm, PO, x):
    if x==0:
        mutacao_bit(Q, Pm, PO)
    else:
        mutacao_bit_bit(Q, Pm, PO)

def mutacao_bit_bit(Q, Pm, PO):
    for i in range(PO):
        aux = 0
        for j in range(36):
            if random.random() <= Pm:
                aux = 1
                Q[i][j] = 1 - Q[i][j]

        if aux == 1 and len(Q[i]) == 37:
            Q[i].pop(36)
            fitness(Q[i])
            aux -= 1

def mutacao_bit(Q, Pm, PO):
    for i in range(PO):
        if random.random <= Pm:
            j = random.randrange(36)
            Q[i][j] = 1 - Q[i][j]
            Q[i].pop()
            fitness(Q[i])
#--------------------------------------------------------------------------------------------------------------------

def substituicao(P, Q, PO):
    Quant_P=int(PO*0.3)
    Q.sort(key=lambda x: x[36])
    P.sort(key=lambda x: x[36], reverse= True)

    for i in range(Quant_P):
        Q.pop(0)
        Q.append(P.pop(0)[:])
    Q.sort(key=lambda x: x[36])

    return Q


def caixa_preta(Pc, Pm, PO, sele, mut):
    #Pc = 0.8 # probabilidade de cruzamento
    #Pm = 0.025 # probabilidade de mutacao
    #PO = 30  # tamanho populacao
    P = []
    S = []
    Q = []
    fit_medio = []
    fit_maior = []
    diferentes = []

    inicializa_Pop(P, PO)
    avalia_Pop(P, PO)
    fit_medio.append(fitness_medio(P, PO))
    fit_maior.append(P[PO-1][36])
    diferentes.append(indi_dif(P, PO))

    for i in range(50):
        selecao(S, P, PO, sele)
        two_pc(Q, S, Pc, PO)
        avalia_Pop(Q, PO)
        mutacao(Q, Pm, PO, mut)
        P = substituicao(P[:], Q[:], PO)

        fit_medio.append(fitness_medio(P, PO))
        fit_maior.append(P[PO - 1][36])
        diferentes.append(indi_dif(P, PO))


    return fit_medio, fit_maior,diferentes
    #return P[29][36]






#-----------------------------------------------MAIN-----------------------------------------------------------------------

# 0: torneiro , 1: roleta
# 0: bit ,1: bit a bit


fit_medio = []
fit_maior = []
diferentes = []


fit_medio, fit_maior, diferentes =caixa_preta(0.8, 0.0, 30, 0, 1)


#plt.figure(1)
#plt.subplot(2,1,1)
plt.ylim(0,45)
plt.title("Torneio, Bit a Bit, Pm=0.025")
plt.xlabel(u'Geração')
plt.ylabel('fitness')
plt.plot(range(51),fit_medio,label=u"fitness médio")
plt.plot(range(51),fit_maior,label="maior fitness")
plt.plot(range(51),diferentes,label="diferentes")
plt.legend(loc=0)
plt.grid(True)
plt.show()
#fit_medio, fit_maior, diferentes = caixa_preta(0.8, 0.025, 30, 1, 1)
#plt.subplot(2,1,2)
#plt.ylim(0,45)
#plt.title("Roleta")
#plt.ylabel('fitness')
#plt.plot(range(51),fit_medio,label=u"fitness médio")
#plt.plot(range(51),fit_maior,label="maior fitness")
#plt.plot(range(51),diferentes,label="diferentes")
#plt.legend(loc=0)
#plt.grid(True)"""
