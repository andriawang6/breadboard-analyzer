from schemdraw.parsing import logicparse
import os

def reformat_expr(logic_expr):
    replace = { "*" : "&",
                "+" : "|",
                "^" : "xor",
                "'" : "~",
                "(" : ")",
                ")" : "(" }
    result = ""
    for i in range(len(logic_expr) - 3, -1, -1):
        if logic_expr[i] in replace:
            result += replace[logic_expr[i]]
        else:
            result += logic_expr[i]
    output_label = logic_expr[-1]
    return result, output_label

def gen_schematic(raw_expr, i):
    formatted_expr, output_label = reformat_expr(raw_expr)
    drawing = logicparse(formatted_expr, gateW=2.5, gateH=2, outlabel=output_label)
    drawing.save(f"static/schematics/schematic{i}.svg")    


