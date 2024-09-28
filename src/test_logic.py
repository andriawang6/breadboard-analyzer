import logic_processing
import linearization
import datasheets

MIDDLE = 5.5

chip_coords = {}

chip_coords["chip1"] = ["74HCT04", (5, 3), (5, 4), (5, 5), (5, 6), (5, 7), (5, 8), (5, 9), 
                                   (6, 9), (6, 8), (6, 7), (6, 6), (6, 5), (6, 4), (6, 3)]

chip_coords["chip2"] = ["74HCT00", (5, 12), (5, 13), (5, 14), (5, 15), (5, 16), (5, 17), (5, 18), 
                                   (6, 18), (6, 17), (6, 16), (6, 15), (6, 14), (6, 13), (6, 12)]

chip_info = datasheets.chip_info

# what bind_rows() should output: 
row_binds = {}
# LEFT SIDE OF NOT
row_binds["3L"] = "1A_chip1"
row_binds["4L"] = "1Y_chip1"
row_binds["5L"] = "2A_chip1"
row_binds["6L"] = "2Y_chip1"
row_binds["7L"] = "3A_chip1"
row_binds["8L"] = "3Y_chip1"
row_binds["9L"] = "GND_chip1"
# RIGHT SIDE OF NOT 
row_binds["9R"] = "4Y_chip1"
row_binds["8R"] = "4A_chip1"
row_binds["7R"] = "5Y_chip1"
row_binds["6R"] = "5A_chip1"
row_binds["5R"] = "6Y_chip1"
row_binds["4R"] = "6A_chip1"
row_binds["3R"] = "VCC_chip1"

# LEFT SIDE OF NAND
row_binds["12L"] = "1A_chip2"
row_binds["13L"] = "1B_chip2"
row_binds["14L"] = "1Y_chip2"
row_binds["15L"] = "2A_chip2"
row_binds["16L"] = "2B_chip2"
row_binds["17L"] = "2Y_chip2"
row_binds["18L"] = "GND_chip2"
# RIGHT SIDE OF NAND
row_binds["18R"] = "3Y_chip2"
row_binds["17R"] = "3A_chip2"
row_binds["16R"] = "3B_chip2"
row_binds["15R"] = "4Y_chip2"
row_binds["14R"] = "4A_chip2"
row_binds["13R"] = "4B_chip2"
row_binds["12R"] = "VCC_chip2"

endpoints = [[(4, 0), (4, 3)], 
             [(4, 4), (4, 12)], 
             [(2, 14), (2, 20)],
             [(0, 1), (0, 5)], 
             [(0, 6), [0, 13]]]


print("test bind_rows()")
result = logic_processing.bind_rows(chip_coords, chip_info, MIDDLE)
for key in row_binds:
    if result[key] != row_binds[key]:
        print(f"{result[key]}, {row_binds[key]}, {key}")

print("test create_relationships()")
c, i, o = logic_processing.create_relationships(endpoints, result, MIDDLE)
print(c)
print(list(i))
print(list(o))

# adj = linearization.generate_adjacency_map(c, i, o)
# print(adj)

# linearization = linearization.topological_sort(adj, i)
# print(linearization)