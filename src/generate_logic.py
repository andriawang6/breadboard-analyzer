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

    return candidate[i] == "Y"

def parse_pin_chip(pin_chip):
    i = 0 
    pin = ""
    for char in pin_chip:
        if char == "_":
            break
        pin += char
        i += 1
    chip = pin_chip[i + 1:]
    return pin, chip 

def get_operator(pin_chip, chip_info, outputs):
    # if pin_chip is an output, the operator is just "= variable"
    if pin_chip in outputs:
        return "=" + pin_chip, ""
    pin, chip = parse_pin_chip(pin_chip)
    operator = chip_info[chip][-1]
    if operator == "'":
        return "", "'"
    if len(operator) > 1:
        return operator[0], "'"
    return operator[0], ""

def is_gate_input(cand, pin):
    if cand == "GND" or cand == "VCC":
        return False
    cand_num, cand_let = parse_pin(cand)
    pin_num, pin_let = parse_pin(pin)
    if cand_num != pin_num:
        return False
    if cand_let == "Y":
        return False
    return True

def parse_pin(pin):
    i = 0
    for char in pin:
        if char.isnumeric():
            i += 1
        break

    num = pin[:i]
    let = pin[i + 1:]
    return num, let

def get_gate_inputs(pin_chip, chip_info):
    # search for pin --> look to the left and right of it until we reach a Y or GND or VCC
    pin, chip = parse_pin_chip(pin_chip)
    info = chip_info[chip]
    idx = info.index(pin)
    
    gate_inputs = []
    # look to left of idx
    for i in range(idx, 0, -1):
        if is_gate_input(info[i], pin):
            gate_inputs.append(info[i])
        break

    # look to right of idx 
    for i in range(idx, len(info)):
        if is_gate_input(info[i], pin):
            gate_inputs.append(info[i])
        break

    return gate_inputs

def generate_logic(connection_map, inputs, outputs, chip_info):
    res = []
    visited = set()

    def trace_back(source):
        if source in inputs:
            # base case; return source
            return source
        expr = "("
        operator, invert = get_operator(source, chip_info)
        
        children = get_gate_inputs(source)
        for child in children:
            child_source = connection_map[child]
            expr += trace_back(child_source)
            expr += operator

        # slice off extra operator
        expr = expr[:-1] if expr[-1] == operator else expr
        expr += ")" + invert
        return expr
            
        # now, find children of source
        # for child in children:
            # track_back(child.source)
            # cur += operands
        

        
        print(f"tracing back")

    for a in connection_map:
        b = connection_map[a]
        # MAKE SURE TO UPDATE VISITED SET 
        if a in visited or b in visited:
            continue

        # identify if a is source or b is source (or which is sink)
        # from there, logic can be same for all combos of a and b
        a_is_source = is_source(a, inputs, outputs)
        source = a if a_is_source else b
        sink = b if a_is_source else a

        cur = "("
        child = trace_back(source)
        cur += child
        
        sink_siblings = get_gate_inputs(sink)
        operator, invert = get_operator(sink, chip_info)

        # trace backwards
        for sibling in sink_siblings:
            cur += operator # being AND or OR, not NOT; if NAND or NOR, negate at end 
            sibling_source = connection_map[sibling]
            operand = trace_back(sibling_source)
            cur += operand
            
        cur += ")"
        cur += invert

        # trace forwards
        # now, navigate to the new source (i.e. what sink feeds into)
            # first check if sink is output --> if so return nothing (append on  = sink)
        
        


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


    
    