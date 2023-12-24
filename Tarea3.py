##########################################################################
#             TAREA 3 - ALGORITMOS DE BUSQUEDA NO INFORMADA
# LAB-BC1-10
# - Jaime Camacho Garcia
# - Esther Camacho Caro
# - Jorge Herrero Ubeda
##########################################################################

from ast import Return
import hashlib
import json
import copy
from traceback import print_tb
from datetime import datetime
import bisect
import random

profundidadMax = 1000000

#######################################    TAREA_1    #######################################

class Estado():
    def __init__(self, listOfBottles, capacidad):
        self.listOfBottles = listOfBottles
        self.capacidad = capacidad
    
    def __eq__(self, other):
        if self.listOfBottles==other.listOfBottles and self.capacidad==other.capacidad:
            return True
        return False

    def amountBotella(self, botella):
        n=0
        for i in botella:
            n+=i[1]
        return n

    def ES_AccionPosible(self, Botella_origen, Botella_destino, Cantidad):
        if (self.amountBotella(Botella_origen)<Cantidad or self.capacidad-self.amountBotella(Botella_destino)<Cantidad):
            return False
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




#######################################    TAREA_3    #######################################

class Nodo():
    def __init__(self, id, costo, estado, padre, accion, profundidad, heuristica, valor):
        self.id = id
        self.costo = costo
        self.estado = estado
        self.padre = padre
        self.accion = accion
        self.profundidad = profundidad
        self.heuristica = heuristica
        self.valor = valor

    def __lt__(self, other):
        return self.valor < other.valor or (self.valor == other.valor and self.id < other.id)


class Frontera():
    def __init__(self):
        self.nodosFrontera = []
    
    def insertar(self, nodo):
        bisect.insort(self.nodosFrontera, nodo)
        #self.nodosFrontera.append(nodo)
        #self.nodosFrontera.insert(0, nodo)
        #       self.nodosFrontera.sort(key = lambda x: (x.valor, x.id))

    def obtener(self):
        return self.nodosFrontera.pop(0)


class Visitados():
    def __init__(self):
        self.estadosVisitados = []
    
    def insertar(self, nodo):
        self.estadosVisitados.append(nodo)
    
    def pertenece(self, estado):
        for x in self.estadosVisitados:
            if x == estado:
                return True
        return False


def busquedas(problema, frontera, estrategia):
    visitados = Visitados()
    nID = 0
    valor_inicio = calcularValor(estrategia, id, 0, 0)
    nodo = Nodo(nID, 0, problema.initState, None, 0, 0, 0, valor_inicio)
    frontera.insertar(nodo)

    while len(frontera.nodosFrontera) > 0:
        auxNodo = frontera.obtener()

        if not problema.objetivo(auxNodo.estado):
            
            if not visitados.pertenece(auxNodo.estado) and auxNodo.profundidad < 1000000:

                visitados.insertar(auxNodo.estado)
                listSucesores = sucesores(auxNodo.estado)   #   ACCION - ESTADO - COSTO

                if len(listSucesores) == 0 and frontera.nodosFrontera == []:
                    return None

                else:

                    for x in listSucesores:

                        #if not visitados.pertenece(x[1]):
                        #visitados.insertar(x[1])

                        nID += 1
                        #            ID      COSTO            ESTADO  PADRE   ACCION  PROFUNDIDAD              HEURISTICA                     VALOR
                        nodo = Nodo (nID, auxNodo.costo + x[2], x[1], auxNodo, x[0], auxNodo.profundidad + 1, round(random.uniform(0, 10)), calcularValor(estrategia, nID, auxNodo.profundidad+1, auxNodo.costo + x[2]))

                        frontera.insertar(nodo)
        
        else:
            return auxNodo

    return None


def calcularValor(estrategia, id, prof, costo):
    if estrategia=="BREADTH":
        return prof
    elif estrategia=="DEPTH":
        return 1/(prof+1)
    elif estrategia=="UNIFORM":
        return costo

def eliminarEspacios(cad): 
    return cad.replace(" ", "") 

def escribirFichero(nodo, nombre, estrategia):
    cad = ""

    while nodo.id>0:
        cad = "[" + str(nodo.id) + "] [" + str(nodo.costo) + ", " + hashlib.md5(eliminarEspacios(str(nodo.estado.listOfBottles)).encode()).hexdigest() + ", " + str(nodo.padre.id) + ", " + str(nodo.accion) + ", " + str(nodo.profundidad) + ", " + str(nodo.heuristica) + ", " + str(round(nodo.valor, 2)) + "]\n" + cad
        nodo = nodo.padre
    
    cad = "[" + str(nodo.id) + "] [" + str(nodo.costo) + ", " + hashlib.md5(eliminarEspacios(str(nodo.estado.listOfBottles)).encode()).hexdigest() + ", None, None, " + str(nodo.profundidad) + ", " + str(nodo.heuristica) + ", " + str(round(nodo.valor, 2)) + "]\n" + cad

    f = open(nombre+"_"+estrategia+".txt", "w")
    f.write(cad)
    print(cad)
    f.close()


def devolverEstrategia(estrategia_input,estrategias):
    estrategia = ""
    if estrategias.get(estrategia_input):
        estrategia = estrategias[estrategia_input]
        return estrategia
    else:
        raise Exception("La extrategia elegida es erronea o no existe")


def main():
    nombreArch = "p0"
    estado0 = leerJSON(nombreArch+".json")
    
    #estrategia = "UNIFORM"     

    print("Estrategias: \n - Anchura\n - Profundidad Acotada\n - Coste uniforme\n")
    estrategia_input = input("Seleccione la estrategia deseada: ").lower()
    estrategias = {"anchura": "BREADTH", "profundidad acotada": "DEPTH", "coste uniforme": "UNIFORM"}
    estrategia = devolverEstrategia(estrategia_input,estrategias)

    if estado0:
        t_inicio = datetime.now()    
        problema = Problema(estado0)
        solucion = busquedas(problema, frontera = Frontera(), estrategia = estrategia)

        if solucion:
            escribirFichero(solucion, nombreArch, estrategia)
            
            print("Tiempo en resolver el problema (en segundos):")
            print(datetime.now()-t_inicio)

        else:
            print("NO SE HA ENCONTRADO SOLUCIÓN")
    

main()