from pyeda.inter import exprvars, truthtable, espresso_tts

import pyeda.boolalg.minimization
# from pyeda.boolalg.minimization import _cover2exprs


from typing import Any

def my_modified_function(inputs:list, noutputs:int, cover:Any) -> list[tuple[list[int],list[int]]]:
    """Convert a cover to a tuple of Expression instances."""
    # fs = []
    for i in range(noutputs):
        terms = []
        for invec, outvec in cover:
            if outvec[i]:
                my_term : tuple[list[int],list[int]] = ([],[])
                # term = []
                for j, v in enumerate(inputs):
                    if invec[j] == 1:
                        # term.append(~v)
                        my_term[1].append(j)
                    elif invec[j] == 2:                        
                        my_term[0].append(j)
                        # term.append(v)
                # terms.append(term)
                terms.append(my_term)
                # print(term)
                # print(my_term)
        # fs.append(Or(*[And(*term) for term in terms]))
        # fs.append()
        # print(terms)
    return terms
    # return tuple(fs)

# Monkey-patching
pyeda.boolalg.minimization._cover2exprs = my_modified_function


# Define the variables x[0], x[1], and x[2]
X = exprvars('x', 3)

# Define the truth table
f = truthtable(X, "10010101")
# f = truthtable(X, "1001010111101001")

# Minimize the truth table using Espresso
fm = espresso_tts(f)

# Print the minimized form
print(fm)
print(len(fm))

# print(type(fm[0]))
# print(fm[0])
