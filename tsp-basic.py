import math
import time

def read_tsp_file(filename):
    nodes = {}
    with open(filename, 'r') as f:
        for line in f:
            if line.startswith('NODE_COORD_SECTION'):  #this is the basic TSP code, it takes more time to run and not so efficient.
                break
        for line in f:
            if line.startswith('EOF'):
                break
            node_id, x, y = map(int, line.split()[0:3])
            nodes[node_id] = (x, y)
    return nodes

def distance(node1, node2):
    x1, y1 = node1
    x2, y2 = node2
    return round(math.sqrt((x1-x2)**2 + (y1-y2)**2))

def total_distance(route, nodes):
    dist = 0
    for i in range(len(route)-1):
        dist += distance(nodes[route[i]], nodes[route[i+1]])
    dist += distance(nodes[route[-1]], nodes[route[0]])
    return dist

def two_opt(route, nodes):
    improved = True
    while improved:
        improved = False
        for i in range(1, len(route)-2):
            for j in range(i+1, len(route)):
                if j-i == 1:
                    continue
                new_route = route[:]
                new_route[i:j] = route[j-1:i-1:-1]
                new_distance = total_distance(new_route, nodes)
                if new_distance < total_distance(route, nodes):
                    route = new_route
                    improved = True
        if improved:
            break
    return route

if __name__ == '__main__':
    nodes = read_tsp_file('att532.tsp')
    start_time = time.time()
    initial_route = list(nodes.keys())
    best_route = two_opt(initial_route, nodes)
    end_time = time.time()
    execution_time = end_time - start_time
    print('Best route found:', best_route)
    print('Total distance:', total_distance(best_route, nodes))
    print("Execution time:", execution_time)
