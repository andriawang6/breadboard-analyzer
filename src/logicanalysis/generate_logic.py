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

def get_operator(pin_chip, chip_info, outputs, chip_coords):
    # if pin_chip is an output, the operator is just "= variable"
    if pin_chip in outputs:
        return "=" + pin_chip, ""
    pin, chip = parse_pin_chip(pin_chip)
    operator = chip_info[chip_coords[chip][0]][-1]

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
    let = pin[i:]
    return num, let

def get_gate_inputs(pin_chip, chip_coords, chip_info):
    # search for pin --> look to the left and right of it until we reach a Y or GND or VCC
    pin, chip = parse_pin_chip(pin_chip)
    info = chip_info[chip_coords[chip][0]]
    idx = info.index(pin)
    
    gate_inputs = []
    # look to left of idx
    for i in range(idx - 1, 0, -1):
        if is_gate_input(info[i], pin_chip):
            gate_inputs.append(info[i] + "_" + chip)
        else: 
            break

    # look to right of idx 
    for i in range(idx + 1, len(info)):
        if is_gate_input(info[i], pin_chip):
            gate_inputs.append(info[i] + "_" + chip)
        else: 
            break
      
    return gate_inputs

def get_new_source(sink):
    pin, chip = parse_pin_chip(sink)
    num, let = parse_pin(pin)
    return num + "Y" + "_" + chip

def generate_logic(connections, inputs, outputs, chip_info, chip_coords):
    connection_map = connections_undirected_map(connections)
    res = []
    processed = set()

    def trace_back(source):
        if source in processed:
            return ""
        processed.add(source)
        processed.add(connection_map[source])

        if source in inputs:
            # base case; return source
            return source
        expr = "("
        operator, invert = get_operator(source, chip_info, outputs, chip_coords)

        children = get_gate_inputs(source, chip_coords, chip_info)
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
        

    for a in connection_map:
        b = connection_map[a]
        # MAKE SURE TO UPDATE VISITED SET 
        if a in processed or b in processed:
            continue

        # identify if a is source or b is source (or which is sink)
        # from there, logic can be same for all combos of a and b
        a_is_source = is_source(a, inputs, outputs)
        source = a if a_is_source else b
        sink = b if a_is_source else a

        cur = "("
        child = trace_back(source)
        cur += child
        sink_siblings = get_gate_inputs(sink, chip_coords, chip_info) if sink not in outputs else []

        operator, invert = get_operator(sink, chip_info, outputs, chip_coords)

        # trace backwards
        for sibling in sink_siblings:
            cur += operator # being AND or OR, not NOT; if NAND or NOR, negate at end 
            sibling_source = connection_map[sibling]
            operand = trace_back(sibling_source)
            cur += operand
            
        cur += ")"
        cur += invert
        

        # if sink is in outputs, we're done (append cur to res)
        # else: we trace forwards
        # now, navigate to the new source (i.e. what sink feeds into; by changing )
            # then get new_sink
            # first check if new_sink is output --> if we're completely done with this cur forever and add cur to results
            # otherwise, append a "(" at start of cur to be closed once we've fully traced forward on current new_sink
            # now, we trace backwards on new_sink's siblings (don't need to go to new_source since that's where we came from)
            # now, we can close ")" cur since we're done with new_sink's gate
            # CONTINUE TRACING FORWARD TO NEW_SINK'S NEW SOURCE
        processed.add(sink)
        processed.add(source)

        if sink not in outputs:
            new_source = get_new_source(sink)
            new_sink = connection_map[new_source]
            sink = new_sink

        while sink not in outputs:
            # calculate new source --> we don't care to store it 
            # use new_source to get new_sink
            
            cur = "(" + cur

            sink_siblings = get_gate_inputs(sink, chip_coords, chip_info)
            operator, invert = get_operator(sink, chip_info, outputs, chip_coords)

            for sibling in sink_siblings:
                cur += operator # being AND or OR, not NOT; if NAND or NOR, negate at end 
                sibling_source = connection_map[sibling]
                operand = trace_back(sibling_source)
                cur += operand
            
            cur += ")"
            cur += invert

            processed.add(sink)
            processed.add(connection_map[sink])

            new_source = get_new_source(sink)
            new_sink = connection_map[new_source]
            sink = new_sink
        processed.add(sink)
        processed.add(connection_map[sink])
        cur += "=" + sink
        res.append(cur)

    return res