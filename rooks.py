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

    # We essentially want an XOR of each row and each column,
    # but we build that into CNF. We want x11 or x12 or x13...
    # and so on, but need the negations as well to make sure
    # only one variable in a row/column is active at once.


    cur_list = []
    cur_list_2 = []
    for row in range(n):
        for col in range(n):
            cur_list.append(gridVariables[(row,col)])
            cur_list_2.append(gridVariables[(col,row)])
            if col + 1 != n:
                for j in range(col + 1, n):
                    row_pair_list = []
                    col_pair_list = []
                    row_pair_list.append(-gridVariables[(row,col)])
                    row_pair_list.append(-gridVariables[(row, j)])
                    col_pair_list.append(-gridVariables[(col,row)])
                    col_pair_list.append(-gridVariables[(j,row)])
                    phi.add_clause(row_pair_list)
                    phi.add_clause(col_pair_list)
        phi.add_clause(cur_list)
        phi.add_clause(cur_list_2)
        cur_list = []
        cur_list_2 = []

    phi.solve()
    
    count = 0
    for s in phi.enum_models():
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

