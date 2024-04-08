class GrafoPonderado:
    
    def __init__(self) -> None:
        self.adj_list = {}
        self.node_count = 0
        self.edge_count = 0

    def add_node(self, node):
        if node in self.adj_list:
            print(f"WARN: Node {node} already exists")
            return
        self.adj_list[node] = {}
        self.node_count += 1

    def add_edge(self, node1, node2, weight):
        if node1 not in self.adj_list:
            self.add_node(node1)
        if node2 not in self.adj_list:
            self.add_node(node2)
        self.adj_list[node1][node2] = weight
        self.edge_count += 1

    def add_nodes(self, nodes):
        for node in nodes:
            self.add_node(node)

    def add_two_way_edge(self, node1, node2, weight):
        self.add_edge(node1, node2, weight)
        self.add_edge(node2, node1, weight)

    def remove_edge(self, node1, node2):
        try:
          self.adj_list[node1].pop(node2)
          self.edge_count -= 1
        except KeyError as e:
            print(f"WARN: Edge {node1} -> {node2} does not exist")

    def __str__(self):
        output = str(self.node_count) + " " + str(self.edge_count) + "\n"
        for node in self.adj_list:
            for node2 in self.adj_list[node]:
                output += str(node).replace(" ","_") + " " + str(node2).replace(" ","_") + " " + str(self.adj_list[node][node2]) + "\n"
        return output
    
    
    
    def read_file(self, file_name):
        file = open(file_name, 'r')
        i = 0
        for line in file:
            i += 1
            if i == 1:
                continue
            line_content = line.strip().split(" ")
            u = line_content[0]
            v = line_content[1]
            w = int(line_content[2])
            self.add_edge(u, v, w)
        file.close()

    def remove_node(self, node):
        for node2 in self.adj_list:
            if node in self.adj_list[node2]:
                self.adj_list[node2].pop(node)
                self.edge_count -= 1
        self.edge_count -= len(self.adj_list[node])
        self.node_count -= 1
        self.adj_list.pop(node)

    def there_is_edge(self, node1, node2):
        if(node2 in self.adj_list[node1] and node1 in self.adj_list[node2]):
            return True
        return False
    
    def get_edge_weight(self, node1, node2):
        if not self.there_is_edge(node1, node2):
            return None
        return self.adj_list[node1][node2]
    
    def set_edge_weight(self, node1, node2, weight):
        if not self.there_is_edge(node1, node2):
            self.add_edge(node1, node2, weight)
        else:
            self.adj_list[node1][node2] = weight

    def extract_min(self, Q, dist):
        min_dist = float("inf")
        min_node = None
        for node in Q:
            if dist[node] < min_dist:
                min_dist = dist[node]
                min_node = node
        return min_node

    def disjkstra(self, s):
        dist = {}
        pred = {}
        Q = []
        for node in self.adj_list:
            dist[node] = float('inf')
            pred[node] = None
            Q.append(node)
        dist[s] = 0
        while len(Q) > 0:
            # u = min(Q, key=lambda x: dist[x])
            u = self.extract_min(Q, dist)
            Q.remove(u)
            for v in self.adj_list[u]:
                w = self.adj_list[u][v]
                if dist[v] > dist[u] + w:
                    dist[v] = dist[u] + w
                    pred[v] = u
        return (dist, pred)


    def bellman_ford(self, s):
        dist = {}
        pred = {}
        for node in self.adj_list:
            dist[node] = float('inf')
            pred[node] = None
        dist[s] = 0
        for i in range(self.node_count - 1):
            for u in self.adj_list:
                for v in self.adj_list[u]:
                    w = self.adj_list[u][v]
                    if dist[v] > dist[u] + w:
                        dist[v] = dist[u] + w
                        pred[v] = u
        for u in self.adj_list:
            for v in self.adj_list[u]:
                w = self.adj_list[u][v]
                if dist[v] > dist[u] + w:
                    # Negative cycle detected
                    print("WARN: Negative cycle detected")
                    return (None, None)
        return (dist, pred)

    def bellman_ford_improved(self, s):
        dist = {}
        pred = {}
        for node in self.adj_list:
            dist[node] = float('inf')
            pred[node] = None
        dist[s] = 0
        for i in range(self.node_count - 1):
            swapped = False
            for u in self.adj_list:
                for v in self.adj_list[u]:
                    w = self.adj_list[u][v]
                    if dist[v] > dist[u] + w:
                        dist[v] = dist[u] + w
                        pred[v] = u
                        swapped = True
            if not swapped:
                break
        return (dist, pred)
    
    def floyd_warshall(self):
        dist = {}
        pred = {}
        for i in self.adj_list:
            dist[i]= {}
            pred[i] = {}
            for j in self.adj_list:
                if i==j:
                    dist[i][j] = 0
                    pred[i][j] = None
                elif j in self.adj_list[i]:
                    dist[i][j] = self.adj_list[i][j]
                    pred[i][j] = i
                else:
                    dist[i][j] = float('inf')
                    pred[i][j] = None
        for k in self.adj_list:
            for i in self.adj_list:
                for j in self.adj_list:
                    if dist[i][j] > dist[i][k] + dist[k][j]:
                        dist[i][j] = dist[i][k] + dist[k][j]
                        pred[i][j] = pred[k][j]
        return (dist, pred)