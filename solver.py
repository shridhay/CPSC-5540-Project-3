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
    elif bool(l[0]) == False:
        return False
    elif bool(l[0]) == True:
        return bool(l[0]) and bool(and_(l[1:]))

def or_(l):
    if len(l) == 0:
        return False
    elif len(l) == 1:
        return bool(l[0])
    elif bool(l[0]) == True:
        return True
    elif bool(l[0]) == False:
        return bool(l[0]) or bool(or_(l[1:]))
    
def not_(l):
    if l is None:
        return None
    else:
        if l == True:
            return False
        elif l == False:
            return True

class SAT:
    def __init__(self, numOfVars, numOfClauses):
        self.nbvar = numOfVars
        self.nbclauses = numOfClauses
        self.clauses = []
        self.d = {i + 1: None for i in range(self.nbvar)}
    
    def parse_line(self, line):
        self.clauses.append(list(map(int, line.split()))[:-1])

    def parse_idx(self, idx):
        if idx > 0:
            return self.d[idx]
        elif idx < 0:
            return not_(self.d[-idx])
        else:
            return None
        
    def print_clauses(self):
        print(self.clauses)

    def pretty(self) -> str:
        clause_strs = []
        for clause in self.clauses:
            literals = []
            for var in clause:
                if var < 0:
                    literals.append(f"~x{-var}")
                else:
                    literals.append(f"x{var}")
            clause_strs.append("(" + " \\/ ".join(literals) + ")")
        return " /\\ ".join(clause_strs)
    
    def display(self):
        print(self.pretty())

    def random_assignment(self):
        pass

    def print_assignment(self):
        pass
    
    def getVars(self) -> list[str]:
        pass

    def solve(self):
        pass
    
    def check_sat(self):
        """
        Prints a satisfying solution. Does not return anything.
        """
        pass

if __name__ == "__main__":
    if len(sys.argv) > 1:
        path = str(sys.argv[1])        
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
                        c = SAT(nbvar, nbclauses)
                    else:
                        print(line)
                        c.parse_line(line)
            c.display()
        except FileNotFoundError:
            print(f"Error: File '{path}' not found.")
    else:
        print("Usage: python solver.py <path_to_text_file>")
