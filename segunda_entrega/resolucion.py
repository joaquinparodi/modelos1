import math
from unittest import result

# ------------------ FUNCTIONS ------------------

# calcula la distancia entre sucursales pasándole como parámetros las coordenadas de ambas
def calculate_distances(Xi, Yi, Xj, Yj):
    return math.sqrt(((Xi - Xj) ** 2) + ((Yi - Yj) ** 2))

def chargeHeap(dimension, nodes, resultAux, invalidOffices):
    heap = MinHeap(dimension - 1)
    for i in nodes:
        if i not in resultAux and i not in invalidOffices:
            heap.insert(nodes[i])
    return heap

def chargeEdges(officeNodes, officeName):
    newEdgesDict = officeNodes
    for c in officeNodes:
        if c != officeName:
            edge = Node(officeNodes[c].name, officeNodes[c].amount, officeNodes[c].coordinates)
            newEdgesDict[officeName].addEdge(edge)
    return newEdgesDict

# ------------------ CLASSES ------------------

# clase nodo sucursal
class Node:

    def __init__(self, name, amount, coordinates):
        self.name = name
        self.amount = amount
        self.edges = {}
        self.weight = 0 # peso (distancia entre esta sucursal con otra)
        self.coordinates = coordinates

    def addEdge(self, node):
        self.edges[node.name] = node
        self.edges[node.name].weight = calculate_distances(self.coordinates[0], self.coordinates[1], node.coordinates[0], node.coordinates[1])

# clase min heap: cola de prioridad por menor valor de peso de nodo de sucursal
class MinHeap:

    def __init__(self, maxsize):
        self.maxsize = maxsize
        self.size = 0
        self.Heap = [0]*(self.maxsize + 1)
        for i in range(0, maxsize + 1):
            node = Node(-1, 0, -1)
            self.Heap[i] = node
        self.FRONT = 1
 
    def parent(self, pos):
        return pos//2
 
    def leftChild(self, pos):
        return 2 * pos
 
    def rightChild(self, pos):
        return (2 * pos) + 1
 
    def isLeaf(self, pos):
        return pos*2 > self.size
 
    def swap(self, fpos, spos):
        self.Heap[fpos], self.Heap[spos] = self.Heap[spos], self.Heap[fpos]
 
    def minHeapify(self, pos):
        if not self.isLeaf(pos):
            if (self.Heap[pos].weight > self.Heap[self.leftChild(pos)].weight or
               self.Heap[pos].weight > self.Heap[self.rightChild(pos)].weight):
                if self.Heap[self.leftChild(pos)].weight < self.Heap[self.rightChild(pos)].weight:
                    self.swap(pos, self.leftChild(pos))
                    self.minHeapify(self.leftChild(pos))
                else:
                    self.swap(pos, self.rightChild(pos))
                    self.minHeapify(self.rightChild(pos))
 
    def insert(self, element):
        if self.size >= self.maxsize :
            return
        self.size+= 1
        self.Heap[self.size] = element
 
        current = self.size
 
        while self.Heap[current].weight < self.Heap[self.parent(current)].weight:
            self.swap(current, self.parent(current))
            current = self.parent(current)
 
    def minHeap(self):
 
        for pos in range(self.size//2, 0, -1):
            self.minHeapify(pos)
 
    def remove(self):
        if self.size == 0:
            return False
        popped = self.Heap[self.FRONT]
        self.Heap[self.FRONT] = self.Heap[self.size]
        self.size-= 1
        self.minHeapify(self.FRONT)
        return popped

# ------------------ MAIN ------------------

capacity = 0            # máxima capacidad de transporte de dinero
dimension = 0           # cantidad de sucursales
isCoordinates = False   # booleano para identificar coordenadas de cantidad de dinero de cada sucursal
coordinates = {}        # diccionario clave nombre sucursal, valor tupla con coordenadas
demands = {}            # diccionario clave nombre sucursal, valor cantidad de dinero
officeNodes = {}        # diccionario clave nombre sucursal, valor nodo sucursal
results = {}            # diccionario clave nombre sucursal, valor lista con nombres sucursales ordendos por menor distancia a la sucursal

# abro el problema y lo parseo
file = open("problema2.txt", 'r')
for line in file.readlines():
    splited = line.split(" ")
    if splited[0] == "CAPACIDAD:":
        capacity = int(splited[1])
    elif splited[0] == "DIMENSION:":
        dimension = int(splited[1])
    elif splited[0] == "FIN":
        isCoordinates = True
    elif len(splited) == 1 or splited[0] == "EDGE_WEIGHT_TYPE:":
        continue
    elif isCoordinates == True:
        coordinates[int(splited[0])] = (float(splited[1]), float(splited[2]))
    else:
        demands[int(splited[0])] = int(splited[1])

# creo los nodos (sucursales)
for a in range(1, dimension + 1):
    office = Node(a, demands[a], coordinates[a])
    officeNodes[a] = office

officeNodesAux = {}
variableForBreak = False
for e in officeNodes:   # para cada sucursal origen
    invalidOffices = []
    resultAux = []
    currentAmount = 0
    file = open("entrega2.txt", 'r')
    for line in file.readlines():
        splited = line.split(" ")
        for p in splited:
            l = int(p)
            resultAux.append(l)
            currentAmount = currentAmount + officeNodes[l].amount
    if currentAmount > capacity or currentAmount < 0:
        continue
    initialLen = len(resultAux)
    print(initialLen)
    currentOffice = officeNodes[resultAux[len(resultAux) - 1]]
    # si el monto del nodo actual supera los límites, lo descarto como origen
    while variableForBreak == False:   # mientras no se consiga un resultado
        officeNodesAux = chargeEdges(officeNodes, currentOffice.name)
        heap = chargeHeap(dimension, officeNodesAux[currentOffice.name].edges, resultAux, invalidOffices)
        while variableForBreak == False:   # mientras no se pueda visitar la sucursal porque pasa los límites de dinero
            currentEdge = heap.remove() # remuevo la sucursal más cercana a la actual del heap
            difference = -1
            if currentEdge != False:    # si el heap no está vacío
                difference = currentAmount + currentEdge.amount
            else:   # si el heap no contiene más sucursales que cumplan los límites de monto de dinero a transportar
                # como no hay un camino posible desde el ultimo nodo a visitar, retrocedo al anteultimo nodo de los resultados
                popedOffice = resultAux.pop()
                currentAmount = currentAmount - officeNodes[popedOffice].amount
                invalidOffices.append(popedOffice)
                popedOffice = resultAux.pop()
                currentOffice = popedOffice
                resultAux.append(popedOffice)
                break
            if difference >= 0 and difference <= capacity:    # si el monto de la sucursal a visitar no supera los límites, la visito
                currentAmount = difference # sumo el monto de la sucursal visitada
                resultAux.append(currentEdge.name) # agrego a la lista (valor del diccionario de resultados) el nombre de la sucursal
                currentOffice = currentEdge
                invalidOffices = []
                if len(resultAux) == initialLen + 2:
                    resultString = ""
                    for k in resultAux:
                        resultString += str(k) + " "
                    open('entrega2.txt', 'w').close()
                    with open('entrega2.txt', 'a') as f:
                        f.write(resultString[0: -1])
                    print("stop")
                    variableForBreak = True
    # results[e] = resultAux
    break

# obtengo el índice (nombre de sucusal origen) que tenga menor distancia recorrida
# minDistance = 1000000000000000
# minDistanceIndex = 1
# for i in results:
#     currentDistance = 0
#     for j in results[i]:
#         if j < len(results[i]):
#             nodeIndex = results[i][j-1]
#             nextNodeIndex = results[i][j]
#             currentCoordinates = officeNodes[nodeIndex].coordinates
#             currentCoordinatesNext = officeNodes[nextNodeIndex].coordinates
#             currentDistance += calculate_distances(currentCoordinates[0], currentCoordinates[1], currentCoordinatesNext[0], currentCoordinatesNext[1])
#     if currentDistance < minDistance:
#         minDistance = currentDistance
#         minDistanceIndex = i

# dejo el resultado en formato de entrega
# resultString = ""
# for k in results[minDistanceIndex]:
#     resultString += str(k) + " "

''' resultString = ""
for k in results[1]:
    resultString += str(k) + " "

# limpio el archivo entrega_1.txt
open('entrega.txt', 'w').close()
# escribo el archivo entrega_1.txt
with open('entrega.txt', 'a') as f:
    f.write(resultString) '''