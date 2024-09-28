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
chip_info["74HCT00"] = ["1A", "1B", "1Y" "2A", "2B", "2Y", "GND", "3Y", "3A", "3B", "4Y", "4A", "4B", "VCC"]

def bind_row():
    row_binds = {}

    # go through each list of chip coords to bind coords to pins
    for chip_key in chip_coords:
        # get current chip
        curr_chip = chip_coords[chip_key]

        # get chip info for chip
        curr_chip_info = chip_info[curr_chip[0]]

        # iterate through each coord in the chip
        for i in range(1, 15):
            # determine row and side of coord
            coord = curr_chip[i]
            row_side = str(coord[1])
            row_side += "L" if coord[0] < MIDDLE else "R"

            # bind row_side to the pin
            row_binds[row_side] = curr_chip_info[i - 1]

            print(f"{row_side} -> {row_binds[row_side]}")
        
    print("bind row&side : chip&pin")
    return row_binds


bind_row()

# what bind_row should output: 
row_binds = {}
# LEFT SIDE OF NOT
row_binds["3L"] = "1A"
row_binds["4L"] = "1Y"
row_binds["5L"] = "2A"
row_binds["6L"] = "2Y"
row_binds["7L"] = "3A"
row_binds["8L"] = "3Y"
row_binds["9L"] = "GND"
# RIGHT SIDE OF NOT 
row_binds["3R"] = "VCC"
row_binds["4R"] = "6A"
row_binds["5R"] = "6Y"
row_binds["6R"] = "5A"
row_binds["7R"] = "5Y"
row_binds["8R"] = "4A"
row_binds["9R"] = "4Y"

# LEFT SIDE OF NAND
row_binds["12L"] = "1A"
row_binds["13L"] = "1B"
row_binds["14L"] = "1Y"
row_binds["15L"] = "2A"
row_binds["16L"] = "2B"
row_binds["17L"] = "2Y"
row_binds["18L"] = "GND"
# RIGHT SIDE OF NAND
row_binds["12R"] = "VCC"
row_binds["13R"] = "4B"
row_binds["14R"] = "4A"
row_binds["15R"] = "4Y"
row_binds["16R"] = "3B"
row_binds["17R"] = "3A"
row_binds["18R"] = "3Y"

# given input: endpoints + row bindings
# created output: relationships
# take coords and map coordinate to pin 