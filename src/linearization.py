# take in connections 
# process into adjaceny list 
from collections import defaultdict

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