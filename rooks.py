# Filename: rooks.py
# Author: Zack Fitzsimmons 
# Date: Fall 2020
#
# Description: Implementation of the nrooks problem to be
# solved using the Glucose3 SAT solver.

import sys
from pysat.solvers import Glucose3

def main():
    if len(sys.argv) != 2:
        print('Usage: python3 rooks.py n')
        return

    n = int(sys.argv[1])
    # Create a variable for each square on the board.
    val = 1
    output = {}
    gridVariables = dict()
    for r in range(n):
        for c in range(n):
            gridVariables[(r,c)] = val
            output[val] = (r,c)
            val += 1

    phi = Glucose3()

    allVariables = []
    # Placeholder formula
    for r in range(n):
        for c in range(n):
            allVariables.append(1*gridVariables[(r,c)])
    phi.add_clause(allVariables)
            

    phi.solve()
    m = phi.get_model()
    print("Solution:")
    for r in range(n):
        for c in range(n):
            if(gridVariables[(r,c)] in m):
                print("R",end="")
            else:
                print(".",end="")
        print()
    print()

    count = 0
    for s in phi.enum_models():
        count +=1
    print("Total number of models: %d" %(count))


if __name__ == "__main__":
    main()

