import random
import math
from pprint import pprint

# LambdaPoisson = tasa de solicitudes por segundo 
# Lambda = tasa de segundos por solicitud 

def GenerarNuevoTiempo(instante, LambdaPoisson):
    return instante + exponencial(LambdaPoisson)


def exponencial(Lambda):
    U = random.random()
    return -(1/Lambda)*math.log(U)


def getTiempoServidorOcupado(llegadas,salidas):
    suma=0
    for i in range(len(llegadas)):
        suma+=salidas[i]-llegadas[i]
    
    return suma


def getTiempoServidorIdle(llegadas,salidas):
    suma=0
    for i in range(len(llegadas)-1):
        suma+=llegadas[i+1]-salidas[i]
    return suma


if __name__ == "__main__":
    # DEFINICIÓN DE VARIABLES 
    llegadas = []
    salidas = []

    llegadasCola = []
    salidasCola = []
    cola=[]
    Ytemp=0

    #Lambda = num. eventos/ num. unidades
    LambdaPoisson = 2400 / 60
    LambdaExponencial = 100
    t, Na, Nd, n = 0, 0, 0, 0
    T = 0.1

    T0 = GenerarNuevoTiempo(0, LambdaPoisson)
    ta = T0
    td = math.inf

    # Inicio del ciclo while
    while True:
        # CASO 1
        if ta <= td and ta <= T:
            t = ta
            Na += 1
            n += 1
            
            ta = GenerarNuevoTiempo(t, LambdaPoisson)
            
            if n == 1:
                Y = exponencial(LambdaExponencial)
                Ytemp=Y
                td = t + Y
            else:
                #sabemos que va para cola
                llegadasCola.append(t)

            llegadas.append(t)
        
        # CASO 2
        elif td < ta and td <= T:
            t = td
            n -= 1
            Nd += 1
            
            if n == 0:
                td = math.inf
            else:
                Y = exponencial(LambdaExponencial)
                td = t + Y
                salidasCola.append(t)
            
            salidas.append(t)
                

        # CASO 3
        elif min(ta, td) > T and n > 0:
            t = td
            n -= 1
            Nd += 1
            
            if n > 0:
                Y = exponencial(LambdaExponencial)
                td = t + Y
                salidasCola.append(t)
            salidas.append(t)


        # CASO 4
        elif min(ta, td) > T and n == 0:
            Tp = max(t - T, 0)
            break
