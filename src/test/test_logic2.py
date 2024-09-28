import sys
import os

current_dir = os.path.dirname(__file__)
src_dir = os.path.abspath(os.path.join(current_dir, '..'))
sys.path.append(src_dir)

import logicanalysis.logic_processing as logic_processing
import logicanalysis.linearization as linearization
import datasheets

MIDDLE = 4.5

chip_coords = {}

chip_coords["chip1"] = ["74HCT08", (4, 5), (4, 6), (4, 7), (4, 8), (4, 9), (4, 10), (4, 11), 
                                   (5, 11), (5, 10), (5, 9), (5, 8), (5, 7), (5, 6), (5, 5)]

chip_coords["chip2"] = ["74HCT04", (4, 21), (4, 22), (4, 23), (4, 24), (4, 25), (4, 26), (4, 27), 
                                   (5, 27), (5, 26), (5, 25), (5, 24), (5, 23), (5, 22), (5, 21)]

chip_info = datasheets.chip_info

# what bind_rows() should output: 
row_binds = { # LEFT SIDE OF AND
             "5L" : "1A_chip1", 
             "6L" : "1B_chip1",
             "7L" : "1Y_chip1",
             "8L" : "2A_chip1", 
             "9L" : "2B_chip1",
             "10L" : "2Y_chip1",
             "11L" : "GND_chip1",

             # RIGHT SIDE OF AND 
             "11R" : "3Y_chip1",
             "10R" : "3A_chip1",
             "9R" : "3B_chip1",
             "8R" : "4Y_chip1",
             "7R" : "4A_chip1",
             "6R" : "4B_chip1",
             "5R" : "VCC_chip1",

            # LEFT SIDE OF NOT
            "21L" : "1A_chip2",
            "22L" : "1Y_chip2",
            "23L" : "2A_chip2",
            "24L" : "2Y_chip2",
            "25L" : "3A_chip2",
            "26L" : "3Y_chip2",
            "27L" : "GND_chip2",

            # RIGHT SIDE OF NOT
            "27R" : "4Y_chip2",
            "26R" : "4A_chip2",
            "25R" : "5Y_chip2",
            "24R" : "5A_chip2", 
            "23R" : "6Y_chip2",
            "22R" : "6A_chip2",
            "21R" : "VCC_chip2"}

endpoints = [[(1, 1), (3, 5)], 
             [(3, 7), (4, 21)], 
             [(0, 22), (0, 30)],
             [(1, 2), (1, 6)]]


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

adj = linearization.generate_adjacency_map(c, i, o)
print(adj)

linearization = linearization.topological_sort(adj, i)
print(linearization)