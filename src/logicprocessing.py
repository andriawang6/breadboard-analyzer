# given input: chip coords and chip info
# created output: row bindings 
# take chip-coordinate and make a hashmap storing "row#side : chip&pin"
MIDDLE = 5.5

chip_coords = {}

chip_coords["chip1"] = ["74HCT04", (5, 3), (5, 4), (5, 5), (5, 6), (5, 7), (5, 8), (5, 9), 
                                   (6, 9), (6, 8), (6, 7), (6, 6), (6, 5), (6, 4), (6, 3)]

chip_coords["chip2"] = ["74HCT00", (5, 12), (5, 13), (5, 14), (5, 15), (5, 16), (5, 17), (5, 18), 
                                   (6, 18), (6, 17), (6, 16), (6, 15), (6, 14), (6, 13), (6, 12)]


chip_info = {}
chip_info["74HCT04"] = ["1A", "1Y", "2A", "2Y", "3A", "3Y", "GND", "4Y", "4A", "5Y", "5A", "6Y", "6A", "VCC"]
chip_info["74HCT00"] = ["1A", "1B", "1Y", "2A", "2B", "2Y", "GND", "3Y", "3A", "3B", "4Y", "4A", "4B", "VCC"]

def bind_rows(chip_coords, chip_info):
    # row_binds maps row_side -> pin_chip
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
            row_side += "L" if side < MIDDLE else "R"

            # bind row_side to the pin+chip
            row_binds[row_side] = curr_chip_info[i - 1] + chip_key

            # print(f"{row_side} -> {row_binds[row_side]}")
    return row_binds

# what bind_rows() should output: 
row_binds = {}
# LEFT SIDE OF NOT
row_binds["3L"] = "1Achip1"
row_binds["4L"] = "1Ychip1"
row_binds["5L"] = "2Achip1"
row_binds["6L"] = "2Ychip1"
row_binds["7L"] = "3Achip1"
row_binds["8L"] = "3Ychip1"
row_binds["9L"] = "GNDchip1"
# RIGHT SIDE OF NOT 
row_binds["9R"] = "4Ychip1"
row_binds["8R"] = "4Achip1"
row_binds["7R"] = "5Ychip1"
row_binds["6R"] = "5Achip1"
row_binds["5R"] = "6Ychip1"
row_binds["4R"] = "6Achip1"
row_binds["3R"] = "VCCchip1"

# LEFT SIDE OF NAND
row_binds["12L"] = "1Achip2"
row_binds["13L"] = "1Bchip2"
row_binds["14L"] = "1Ychip2"
row_binds["15L"] = "2Achip2"
row_binds["16L"] = "2Bchip2"
row_binds["17L"] = "2Ychip2"
row_binds["18L"] = "GNDchip2"
# RIGHT SIDE OF NAND
row_binds["18R"] = "3Ychip2"
row_binds["17R"] = "3Achip2"
row_binds["16R"] = "3Bchip2"
row_binds["15R"] = "4Ychip2"
row_binds["14R"] = "4Achip2"
row_binds["13R"] = "4Bchip2"
row_binds["12R"] = "VCCchip2"

# print("test bind_rows()")
# result = bind_rows(chip_coords, chip_info)
# for key in row_binds:
#     if result[key] != row_binds[key]:
#         print(f"{result[key]}, {row_binds[key]}, {key}")

endpoints = [[(4, 0), (4, 3)], 
             [(4, 4), (4, 12)], 
             [(2, 14), (2, 20)],
             [(0, 0), (0, 5)], 
             [(0, 6), [0, 13]]]

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

# b, v = create_relationships(endpoints, row_binds, 5.5, {})
# print(b)
# print(v)