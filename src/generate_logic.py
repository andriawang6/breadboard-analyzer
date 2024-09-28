# turn connections into map 
# 

def connections_undirected_map(connections):
    undirected_map = {}
    for a, b in connections:
        undirected_map[a] = b
        undirected_map[b] = a
    return undirected_map

def is_source(candidate, inputs, outputs): 
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

def generate_logic(connection_map, inputs, outputs):
    res = []
    visited = set()

    def trace_back(new_sink, curr):
        new_source = connection_map[new_sink]
        if new_source in inputs:
            # add new_source to curr
            return
        if sink in outputs:
            return 
        
        print(f"tracing back")

    for a in connection_map:
        b = connection_map[a]

        if a in visited or b in visited:
            continue

        # identify if a is source or b is source (or which is sink)
        # from there, logic can be same for all combos of a and b
        a_is_source = is_source(a, inputs, outputs)
        source = a if a_is_source else b
        sink = b if a_is_source else a

        cur = ""
        # process cur_sink (not recursive)
        
        # process cur_source (recursive)
        # then iterate thru cur_sink's pred (recursive)



        # process sink backwards (i.e. go through source) --> make sure sink data is filled in
        # process sink forwards --> see where it leads

        # 1. put current sink into cur string
        
        # 2. go backwards through source into new sink 
            # recursive method a
            # base case: source = input
            # otherwise, recursively go into a new sink related to that source
            # add result to cur
        # 3. go backwards through related operands (e.g. 1A is related to 1B)
            # same recursive method
            # add result to cur
        # 4. go forwards 
            # recursive method b
            # every time we go forwards to a new operator, we must first go backwards to check for other operands 
            # base case for going forwards is an input
            # base case for operator is an output 


        
        
        
        # if sink in outputs:
        #     cur += "=" + sink
            # process source
            # 1. get type of chip from CHIP_INFO
            # 2. trace back:
            #       i. determine what inputs are needed
            #       ii. find inputs by connection_map[input_needed]
            #       iii. recursively process the inputs
        # else:
            # go backwards
            # then go forwards 


        res.append(cur)
    return res


    
    