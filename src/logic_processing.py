# given input: chip coords and chip info
# created output: row bindings 
# take chip-coordinate and make a map storing "row#side : pin_chip"
def bind_rows(chip_coords, chip_info, middle):
    # row_binds maps row#side : pin&chip
    row_binds = {}

    # go through each list of chip coords to bind coords to pins
    for chip_key in chip_coords:
        # get current chip
        curr_chip = chip_coords[chip_key]

        # get chip info for current chip using the chip name
        chip_name = curr_chip[0]
        curr_chip_info = chip_info[chip_name]

        # iterate through each coord in the chip
        for i in range(1, 15):
            # determine row and side of coord
            side, row = curr_chip[i]
            row_side = str(row) 
            row_side += "L" if side < middle else "R"

            # bind row_side to the pin+chip
            row_binds[row_side] = curr_chip_info[i] + "_" + chip_key

            # print(f"{row_side} -> {row_binds[row_side]}")
    return row_binds

# given input: endpoints + row bindings
# created output: relationships
# take coords and map coordinate to pin 
# coords are (x, y) --> side is determined by x, row is determined by y
def create_relationships(endpoints, row_bindings, middle):
    var_binding = {}
    vars = set()

    # given a coordinate, gets the pin_chip, or creates a var if it does not correspond to a pin
    def get_binding(coord, vars):
        # determine row#side, and use it to determine pin_chip
        side, row = coord
        side = "R" if side > middle else "L"
        key = str(row) + side
        # if the row#side is not bound to a pin_chip, then it is a var
        binding = row_bindings.get(key, key)

        # if the row#side is a var, add it to vars
        if binding == key:
            # also add row#side : var_name to var_binding, if it is not already in var_binding
            var_binding[key] = var_binding.get(key, chr(65 + len(var_binding)))
            # add var_name to set of vars
            vars.add(var_binding[key])
            return var_binding[key]
        return binding
    
    def check_output(var, pin):
        # find index before underscore
        i = 0 
        for char in pin:
            if char == "_":
                i -= 1
                break
            i += 1

        # if char is a Y, then the var is an output
        if pin[i] == "Y":
            return True
        return False
    
    connections = []
    inputs = set()
    outputs = set()
    for start, stop in endpoints:
        start = get_binding(start, vars)
        stop = get_binding(stop, vars)

        # if start is a var, determine if it is an input or an output
        if start in vars and start not in inputs and start not in outputs:
            if check_output(start, stop):
                outputs.add(start)
            else:
                inputs.add(start)
        # if stop is a var, determine if it is an input or an output
        elif stop in vars and stop not in inputs and stop not in outputs:
            if check_output(stop, start):
                outputs.add(stop)
            else:
                inputs.add(stop)
        connections.append((start, stop))

    return connections, inputs, outputs
