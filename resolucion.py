import math

# ------------------ FUNCTIONS ------------------

def calculate_distances(Xi, Yi, Xj, Yj):
    return math.sqrt(((Xi - Xj) ** 2) + ((Yi - Yj) ** 2))

# ------------------ CLASSES ------------------

class Node:
    def __init__(self, name, amount, coordinates):
        self.name = name
        self.amount = amount
        self.edges = {}
        self.weight = 0
        self.coordinates = coordinates

    def addEdge(self, node):
        self.edges[node.name] = node
        self.edges[node.name].weight = calculate_distances(self.coordinates[0], node.coordinates[0], self.coordinates[1], node.coordinates[1])


class MinHeap:
 
    def __init__(self, maxsize):
        self.maxsize = maxsize
        self.size = 0
        self.Heap = [0]*(self.maxsize + 1)
        for i in range(0, maxsize + 1):
            self.Heap[i] = Node(-1, 0, -1)
        self.FRONT = 1
 
    # Function to return the position of
    # parent for the node currently
    # at pos
    def parent(self, pos):
        return pos//2
 
    # Function to return the position of
    # the left child for the node currently
    # at pos
    def leftChild(self, pos):
        return 2 * pos
 
    # Function to return the position of
    # the right child for the node currently
    # at pos
    def rightChild(self, pos):
        return (2 * pos) + 1
 
    # Function that returns true if the passed
    # node is a leaf node
    def isLeaf(self, pos):
        return pos*2 > self.size
 
    # Function to swap two nodes of the heap
    def swap(self, fpos, spos):
        self.Heap[fpos], self.Heap[spos] = self.Heap[spos], self.Heap[fpos]
 
    # Function to heapify the node at pos
    def minHeapify(self, pos):
 
        # If the node is a non-leaf node and greater
        # than any of its child
        if not self.isLeaf(pos):
            if (self.Heap[pos].weight > self.Heap[self.leftChild(pos)].weight or
               self.Heap[pos].weight > self.Heap[self.rightChild(pos)].weight):
 
                # Swap with the left child and heapify
                # the left child
                if self.Heap[self.leftChild(pos)].weight < self.Heap[self.rightChild(pos)].weight:
                    self.swap(pos, self.leftChild(pos))
                    self.minHeapify(self.leftChild(pos))
 
                # Swap with the right child and heapify
                # the right child
                else:
                    self.swap(pos, self.rightChild(pos))
                    self.minHeapify(self.rightChild(pos))
 
    # Function to insert a node into the heap
    def insert(self, element):
        if self.size >= self.maxsize :
            return
        self.size+= 1
        self.Heap[self.size] = element
 
        current = self.size
 
        while self.Heap[current].weight < self.Heap[self.parent(current)].weight:
            self.swap(current, self.parent(current))
            current = self.parent(current)
 
    # Function to build the min heap using
    # the minHeapify function
    def minHeap(self):
 
        for pos in range(self.size//2, 0, -1):
            self.minHeapify(pos)
 
    # Function to remove and return the minimum
    # element from the heap
    def remove(self):
 
        popped = self.Heap[self.FRONT]
        self.Heap[self.FRONT] = self.Heap[self.size]
        self.size-= 1
        self.minHeapify(self.FRONT)
        return popped

# ------------------ MAIN ------------------

capacity = 0
dimension = 0
isCoordinates = False
coordinates = {}
demands = {}
officeNodes = {}

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

for i in range(1, dimension + 1):
    officeNodes[i] = Node(i, demands[i], coordinates[i])
    officeNodes[i].weight = i

heap = MinHeap(dimension)
for i in range(1, dimension + 1):
    heap.insert(officeNodes[i])

for i in range(1, dimension + 1):
    for j in range(1, dimension + 1):
        if i == j:
            continue
        officeNodes[i].addEdge(Node(officeNodes[j].name, officeNodes[j].amount, officeNodes[j].coordinates))

# for i in range(1, dimension + 1):
#     print("The Min val is " + str(heap.remove().weight))
