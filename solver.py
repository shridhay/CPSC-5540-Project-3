from __future__ import annotations
from abc import ABC, abstractmethod
from dataclasses import dataclass
import re
from typing import Self, Union
import numpy as np
from fractions import Fraction
from functools import reduce
import sys
import time
import copy
import itertools

def and_(l):
    if len(l) == 0:
        return True
    elif len(l) == 1:
        return bool(l[0]) 
    else:   
        return bool(l[0]) and and_(l[1:])

def or_(l):
    if len(l) == 0:
        return False
    elif len(l) == 1:
        return bool(l[0])
    else:
        return bool(l[0]) or or_(l[1:])
    
class SAT:

    def __init__(self, numOfVars, numOfClauses, listOfClauses):
        self.nbvar = numOfVars
        self.nbclauses = numOfClauses
        self.clauses = copy.deepcopy(listOfClauses)
        self.d = {i : True for i in range(self.nbvar)}

    def pretty(self) -> str:
        pass
    
    def getVars(self) -> list[str]:
        pass
    
    def coef(self) -> list[str]:
        pass
    
    def check_sat(self):
        """
        Prints a satisfying solution. Does not return anything.
        """
        pass


if __name__ == "__main__":
    if len(sys.argv) > 1:
        path = str(sys.argv[1])        
        clauses = []
        try:
            with open(path, 'r') as f:
                for line in f:
                    if line[0] == 'c':
                        continue
                    elif line[0] == 'p':
                        print(line)
                        lst = line.split()
                        nbvar = int(lst[2])
                        nbclauses = int(lst[3])
                    else:
                        print(line)
                        clauses.append(list(map(int, line.split())))
            c = SAT(nbvar, nbclauses, clauses)
        except FileNotFoundError:
            print(f"Error: File '{path}' not found.")
    else:
        print("Usage: python solver.py <path_to_text_file>")
