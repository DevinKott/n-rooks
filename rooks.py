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


    # Rows
    for row in range(n):
        # First, or together the row and add it as a clause
        row_ord = []
        for col in range(n):
            row_ord.append(gridVariables[(row,col)])
        phi.add_clause(row_ord)

        # Now, we take every index from the row and enumerate
        # all possibilities between each index. We want
        # implication, so we negate each index before adding
        # to the clause.
        more_ord = []
        for j in range(n - 1):
            for k in range(j + 1, n):
                more_ord.append(-row_ord[j])
                more_ord.append(-row_ord[k])
                phi.add_clause(more_ord)
                more_ord = []

    # Columns (we can just switch row/col indices)
    for row in range(n):
        row_ord = []
        for col in range(n):
            row_ord.append(gridVariables[(col,row)])
        phi.add_clause(row_ord)

        more_ord = []
        for j in range(n - 1):
            for k in range(j + 1, n):
                more_ord.append(-row_ord[j])
                more_ord.append(-row_ord[k])
                phi.add_clause(more_ord)
                more_ord = []

    phi.solve()
    m = phi.get_model()
    print("Solution:")
    print_model(m, n, gridVariables)
    

    count = 0
    for s in phi.enum_models():
        #print(s)
        print_model(s, n, gridVariables)
        count +=1
    print("Total number of models: %d" %(count))

def print_model(m, n, gridVariables):
    for r in range(n):
        for c in range(n):
            if(gridVariables[(r,c)] in m):
                print("R",end="")
            else:
                print(".",end="")
        print()
    print()


if __name__ == "__main__":
    main()

