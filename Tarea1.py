##########################################################################
#                   TAREA 1 - ESTADOS
# LAB-BC1-10
# - Jaime Camacho Garcia
# - Esther Camacho Caro
# - Jorge Herrero Ubeda
##########################################################################

import json


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


def main():
    
    estructuraJSON = json.loads(input("Introduzca estructura JSON:"))

    estado = Estado(estructuraJSON, 10)  

    nBotella1= int(input("Indique botella numero 1 ("+str(0)+"-"+str(len(estructuraJSON)-1)+"): "))
    nBotella2= int(input("Indique botella numero 2 ("+str(0)+"-"+str(len(estructuraJSON)-1)+"): "))
    cantidad= int(input("Indique cantidad de liquido a mover: "))

    if estado.Accion(estado.listOfBottles[nBotella1], estado.listOfBottles[nBotella2], cantidad):
        print(estado.listOfBottles)
    else:
        print("Accion no posible")


main()
