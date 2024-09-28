# given input: chip coords and chip info
# created output: row bindings 
# take chip-coordinate and make a map storing "row#side : pin&chip"
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
            row_binds[row_side] = curr_chip_info[i - 1] + chip_key

            # print(f"{row_side} -> {row_binds[row_side]}")
    return row_binds

# given input: endpoints + row bindings
# created output: relationships
# take coords and map coordinate to pin 
# coords are (x, y) --> side is determined by x, row is determined by y
variables = {}
def create_relationships(endpoints, row_bindings, middle, variables):
    def get_binding(coord):
        side, row = coord[0], coord[1]
        side = "R" if side > middle else "L"
        key = str(row) + side
        binding = row_bindings.get(key, key)

        # if key is not a valid key in row_bindings, add it to variables
        if binding == key:
            variables[key] = variables.get(key, chr(65 + len(variables)))
            return variables[key]
        return binding
    
    bindings = []
    for start, stop in endpoints:
        start = get_binding(start)
        stop = get_binding(stop)
        bindings.append((start, stop))

    return bindings, variables