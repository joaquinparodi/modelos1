import math

class Vertex:
    def __init__(self, name):
        self.name = name
        self.edges = {}
        self.weight = 0

    # Este metodo funciona porque los edges provistos por el problema son simetricos,
    def add_edge(self, other: "Vertex"):
        self.edges[other.name] = other

    def __str__(self):
        return str(self.name)

    def __repr__(self):
        return str(self)


class Bucket:
    def __init__(self, first_item: Vertex):
        self.items = [first_item]
        self.weight = first_item.weight

    def add_item(self, new_item: Vertex):
        if any(new_item in x.edges for x in self.items):
            return False
        self.items.append(new_item)
        if new_item.weight > self.weight:
            self.weight = new_item.weight
        return True

    def can_add(self, new_item: Vertex):
        if any(new_item.name in x.edges for x in self.items):
            return False
        return True

    def __str__(self):
        return str(self.items) + ", weight:" + str(self.weight)

    def __repr__(self):
        return str(self)

    def __contains__(self, key):
        return key in self.items




def distancia_entre_sucursales(Xi, Yi, Xj, Yj):
    return math.sqrt((Xi-Xj)^2+(Yi-Yj)^2)


