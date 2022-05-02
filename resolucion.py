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
file = open("problema_uno.txt", 'r')
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

# agrego para cada sucursal como aristas el resto de las sucursales
for b in officeNodes:
    for c in officeNodes:
        if c != b:
            edge = Node(officeNodes[c].name, officeNodes[c].amount, officeNodes[c].coordinates)
            officeNodes[b].addEdge(edge)

for e in officeNodes:   # para cada sucursal
    currentOffice = officeNodes[e]
    currentAmount = currentOffice.amount   # indica la cantidad de dinero transportándos
    # si el monto del nodo actual supera los límites, lo descarto como origen
    if currentAmount > 30 or currentAmount < 0:
        continue
    resultAux = []
    resultAux.append(currentOffice.name)
    lastInvalidEdge = currentOffice
    hasValidPath = True
    invalidOffices = []
    for g in currentOffice.edges:
        if hasValidPath == False:
            heap = chargeHeap(dimension, officeNodes[currentOffice.name].edges, resultAux, invalidOffices)
            currentOffice = heap.remove()
            if currentOffice != False:
                hasValidPath = True
            else:
                break
        if currentOffice != False:
            heap = chargeHeap(dimension, officeNodes[currentOffice.name].edges, resultAux, invalidOffices)   # creo la cola de prioridad y le paso como parámetro la capacidad máxima de sucursales
            edgeCanBeVisited = False # indica si se puede visitar la sucursal (si esta no supera los límites de transporte de dinero)
            while edgeCanBeVisited == False:   # mientras se no se pueda visitar la sucursal porque pasa los límites de dinero
                currentEdge = heap.remove() # remuevo la sucursal más cercana a la actual del heap
                difference = -1
                if currentEdge != False:
                    difference = currentAmount + currentEdge.amount
                else:   # si el heap no contiene más sucursales que cumplan los límites de monto de dinero a transportar
                    hasValidPath = False
                    invalidOffices.append(lastInvalidEdge.name)
                    break
                if difference >= 0 and difference <= capacity:    # si el monto de la sucursal a visitar no supera los límites, la visito
                    currentAmount = difference # sumo el monto de la sucursal visitada
                    resultAux.append(currentEdge.name) # agrego a la lista (valor del diccionario de resultados) la sucursal
                    edgeCanBeVisited = True    # salgo del bucle
                    currentOffice = currentEdge
                    invalidOffices = []
                else:
                    lastInvalidEdge = currentEdge
    results[e] = resultAux

# obtengo el índice (nombre de sucusal origen) que tenga menor distancia recorrida
minDistance = 1000000
minDistanceIndex = 1
for i in results:
    currentDistance = 0
    for j in results[i]:
        if j < len(results[i]) - 1:
            nodeIndex = results[i][j]
            nextNodeIndex = nodeIndex = results[i][j + 1]
            currentCoordinates = officeNodes[nodeIndex].coordinates
            currentCoordinatesNext = officeNodes[nextNodeIndex].coordinates
            currentDistance += calculate_distances(currentCoordinates[0], currentCoordinates[1], currentCoordinatesNext[0], currentCoordinatesNext[1])
    if currentDistance < minDistance:
        minDistance = currentDistance
        minDistanceIndex = i

# dejo el resultado en formato de entrega
resultString = ""
for k in results[minDistanceIndex]:
    resultString += str(k) + " "

# limpio el archivo entrega_1.txt
open('entrega_1.txt', 'w').close()
# escribo el archivo entrega_1.txt
with open('entrega_1.txt', 'a') as f:
    f.write(resultString)