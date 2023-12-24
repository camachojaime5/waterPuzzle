##########################################################################
#                   TAREA 2 - PROBLEMA
# LAB-BC1-10
# - Jaime Camacho Garcia
# - Esther Camacho Caro
# - Jorge Herrero Ubeda
##########################################################################

import json
import copy
#from types import BuiltinMethodType


#######################################    TAREA_1    #######################################

class Estado():

    def __init__(self, listOfBottles, capacidad):
        self.listOfBottles = listOfBottles
        self.capacidad = capacidad

    def amountBotella(self, botella):
        n=0
        for i in botella:
            n+=i[1]
        return n

    def ES_AccionPosible(self, Botella_origen, Botella_destino, Cantidad):
        if (self.amountBotella(Botella_origen)<Cantidad or self.capacidad-self.amountBotella(Botella_destino)<Cantidad):
            return False
        else:
            return True

    def Accion(self, Botella_origen, Botella_destino, Cantidad):
        if (self.ES_AccionPosible(Botella_origen, Botella_destino, Cantidad)):
            contador=0

            while contador<Cantidad:

                if Cantidad-contador >= Botella_origen[0][1]:

                    contador+=Botella_origen[0][1]
                    Botella_destino.insert(0, Botella_origen.pop(0))

                else:

                    contador+=Botella_origen[0][1]-(Cantidad-contador)
                    Botella_destino.insert(0, [Botella_origen[0][0], Botella_origen[0][1]-(Cantidad-contador)])
                    Botella_origen[0][1]-=Cantidad-contador
            
            n=0
            while n+1<len(Botella_destino):
                if Botella_destino[n][0]==Botella_destino[n+1][0]:
                    Botella_destino[n][1]+=Botella_destino[n+1][1]
                    Botella_destino.pop(n+1)
                else:
                    n+=1

            return self

        else:
            return None


#######################################    TAREA_2    #######################################

class Problema():
    
    def __init__(self, initState):
        self.initState = initState
  
    def objetivo(self, estado):
        cont = 0
        for i in range(len(estado.listOfBottles)):
            if estado.listOfBottles[i] != []:
                if estado.listOfBottles[i][0][1] == estado.capacidad or not estado.listOfBottles[i]:
                    cont+=1
            
            else:
                cont+=1
        
        if cont == len(estado.listOfBottles):
            return True
        else:
            return False


def sucesores(estado):
    sucesores=[]
    
    for i in range(len(estado.listOfBottles)):
        for j in range(len(estado.listOfBottles)):
            if estado.listOfBottles[i] and i!=j and estado.ES_AccionPosible(estado.listOfBottles[i], estado.listOfBottles[j], estado.listOfBottles[i][0][1]) and (not estado.listOfBottles[j] or estado.listOfBottles[i][0][0]==estado.listOfBottles[j][0][0]):
                
                estadoAux = copy.deepcopy(estado)
                
                #cant = copy.deepcopy(estadoAux.listOfBottles[i][0][1])
                cant = estado.listOfBottles[i][0][1]

                estadoAux.Accion(estadoAux.listOfBottles[i], estadoAux.listOfBottles[j], cant)

                #sucesores.append(((i, j, cant), copy.deepcopy(estadoAux), 1))
                sucesores.append(((i, j, cant), estadoAux, 1))
    
    return sucesores


def leerJSON(arch):
    try:
        with open(arch,"r") as f:
            line = json.load(f)

        estado = Estado(line["initState"], line["bottleSize"])

        return estado

    except(Exception):
        print("No se pudo leer el archivo indicado.")
        return None


def main():
    nombreArch = "id"
    estado0 = leerJSON(nombreArch+".json")

    #
    print(estado0.listOfBottles)

    listSucesores = sucesores(estado0)

    #                                               REMOVE
    for x in listSucesores:
        print(x[1].listOfBottles)

    #   Estado para comprobar que funciona la funcion objetivo
    E = Estado( [[[3, 4]], [[1, 4]], [[2, 4]], [[0, 4]], [[4, 4]], [], []], 4)
    listSucesores.append(((0, 1, 4), E, 1))

    p = Problema(estado0)

    i = 0
    obj = False
    while i<len(listSucesores) and not obj:
        #   print(str(i)+"\t"+str(listSucesores[i][1].listOfBottles))
        obj = p.objetivo(listSucesores[i][1])                                           #   REMOVE

        print("Objetivo --> "+str(obj)+"\t"+str(listSucesores[i][1].listOfBottles))     #   REMOVE

        i+=1

    #print("Objetivo --> "+str(obj))

    
main()