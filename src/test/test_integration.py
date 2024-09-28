import sys
import os

current_dir = os.path.dirname(__file__)
src_dir = os.path.abspath(os.path.join(current_dir, '..'))
sys.path.append(src_dir)

import logicanalysis.logic_processing as logic_processing
import logicanalysis.generate_logic as generate_logic
import datasheets

chip_info = datasheets.chip_info
chip_coords = {'chip1': ["74HCT04", (4, 18), (4, 19), (4, 20), (4, 21), (4, 22), (4, 23), (4, 24), (5, 24), (5, 23), (5, 22), (5, 21), (5, 20), (5, 19), (5, 18)],
               'chip2': ["74HCT08", (4, 6), (4, 7), (4, 8), (4, 9), (4, 10), (4, 11), (4, 12), (5, 12), (5, 11), (5, 10), (5, 9), (5, 8), (5, 7), (5, 6)]}
endpoints = [[(2, 19), (2, 40)], [(2, 8), (2, 18)], [(3, 3), (3, 6)], [(1, 1), (1, 7)]]

middle = 4.5

connections, inputs, outputs = logic_processing.process_logic(endpoints, chip_coords, chip_info, middle)
print(connections, inputs, outputs)
logical_expression = generate_logic.generate_logic(connections, inputs, outputs, chip_info, chip_coords)
print(logical_expression)
