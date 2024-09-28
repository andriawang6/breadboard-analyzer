# take in connections 
# process into adjaceny list 
from collections import defaultdict, deque

def generate_adjacency_map(connections, inputs, outputs):    
    def is_source(candidate): 
        if candidate in inputs:
            return True
        elif candidate in outputs:
            return False
        
        i = 0 
        for char in candidate:
            if char == "_":
                i -= 1
                break
            i += 1

        # if char is a Y, then the var is an output
        return candidate[i] == "Y"

    adjacency = defaultdict(list)
    for a, b in connections:
        if is_source(a):
            adjacency[a].append(b)
        else:
            adjacency[b].append(a)

    return adjacency

def topological_sort(adjacency_map, inputs):
    linearization = deque()
    visited = set()

    def topological_sort_helper(curr):
        visited.add(curr)
    
        neighbors = adjacency_map.get(curr, [])
        for neighbor in neighbors:
            if neighbor not in visited:
                topological_sort_helper(neighbor)
        linearization.appendleft(curr)

    for input in adjacency_map:
        topological_sort_helper(input)

    return linearization  

