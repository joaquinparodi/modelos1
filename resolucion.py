import math

# ------------------ FUNCTIONS ------------------

# calcula la distancia entre sucursales pasándole como parámetros las coordenadas de ambas
def calculate_distances(Xi, Yi, Xj, Yj):
    return math.sqrt(((Xi - Xj) ** 2) + ((Yi - Yj) ** 2))

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
        self.edges[node.name].weight = calculate_distances(self.coordinates[0], node.coordinates[0], self.coordinates[1], node.coordinates[1])

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
for i in range(1, dimension + 1):
    office = Node(i, demands[i], coordinates[i])
    officeNodes[i] = office

# agrego para cada sucursal como aristas el resto de las sucursales
for i in range(1, dimension + 1):
    for j in range(1, dimension + 1):
        if i == j:  # verifica que no sea la misma sucursal para no agregarsela como arista
            continue
        edge = Node(officeNodes[j].name, officeNodes[j].amount, officeNodes[j].coordinates)
        officeNodes[i].addEdge(edge)

# creo una lista para cada posición de sucursal (tomando esta como inicio) para luego insertar el resultado de visitas
for i in range(1, dimension + 1):
    results[i] = []

for i in range(1, dimension + 1):   # para cada sucursal
    heap = MinHeap(dimension)   # creo la cola de prioridad y le paso como parámetro la capacidad máxima de sucursales
    currentOffice = officeNodes[i]
    for j in currentOffice.edges:   # para cada arista de la sucursal actual
        if j != currentOffice.name:
            heap.insert(currentOffice.edges[j]) # inserto la arista en el heap
    currentAmount = 0   # indica la cantidad de dinero transportándose
    heapIsEmpty = False
    for k in range(1, dimension + 1): # para cada arista de la sucursal actual
        edgeCanBeVisited = False # indica si se puede visitar la sucursal (si esta no supera los límites de transporte de dinero)
        remainEdges = []    # lista con las sucursales que superan los límites de dinero para luego volver a insertarlos en el heap
        while edgeCanBeVisited == False:   # mientras se no se pueda visitar la sucursal porque pasa los límites de dinero
            currentEdge = heap.remove() # remuevo la sucursal más cercana a la actual del heap
            if currentEdge == False:    # si el heap está vacío (porque devolvió False), salgo del bucle
                edgeCanBeVisited = True
                heapIsEmpty = True
            elif currentAmount + currentEdge.amount >= 0 and currentAmount + currentEdge.amount <= capacity:    # si el monto de la sucursal a visitar no supera los límites, la visito
                currentAmount += currentEdge.amount # sumo el monto de la sucursal visitada
                results[k].append(currentEdge.name) # agrego a la lista (valor del diccionario de resultados) el nombre de la sucursal
                print(results[k])
                edgeCanBeVisited = True    # salgo del bucle
            else:
                remainEdges.append(currentEdge) # si el monto de la sucursal supera los límites la agrego a la lista de aristas pendientes para volver a agregar al heap
        if len(remainEdges) > 0:    # si la lista de aristas que superaron los límites no está vacía
            for l in remainEdges:
                if heapIsEmpty == False:    # si el heap todavía contiene sucursales
                    heap.insert(l)  # inserto las sucursales que pasaron los límites de neuvo en el heap
                else:   # si el heap no contiene más sucursales que cumplan los límites de monto de dinero a transportar
                    results[k].append(currentEdge.name) # agrego a la lista (valor del diccionario de resultados) el nombre de la sucursal
                    break   # salgo del for k porque no hay más aristas a visitar que cumplan con los límites de dinero a transportar

#print(len(results[143]))
