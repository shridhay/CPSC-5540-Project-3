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
import random

# def and_(l):
#     if len(l) == 0 or l is None:
#         return True
#     elif len(l) == 1:
#         return bool(l[0]) 
#     elif bool(l[0]) == False:
#         return False
#     elif bool(l[0]) == True:
#         return bool(l[0]) and bool(and_(l[1:]))

# def or_(l):
#     if len(l) == 0 or l is None:
#         return False
#     elif len(l) == 1:
#         return bool(l[0])
#     elif bool(l[0]) == True:
#         return True
#     elif bool(l[0]) == False:
#         return bool(l[0]) or bool(or_(l[1:]))
    
# def not_(l):
#     if l is None:
#         return None
#     else:
#         if l == True:
#             return False
#         elif l == False:
#             return True

class SAT:
    def __init__(self, numOfVars, numOfClauses):
        self.nbvars = numOfVars
        self.nbclauses = numOfClauses
        self.clauses = []
        self.d = {i: None for i in range(1, self.nbvars + 1)}
        self.stack = []
        self.nbunassigned = numOfVars
        self.unassignedKeys = list(range(1, self.nbvars + 1))

    def update(self):
        self.unassignedKeys = [key for key in self.d.keys() if self.d[key] is None]
        self.nbunassigned = len(self.unassignedKeys)
    
    def parse_line(self, line):
        self.clauses.append(list(map(int, line.split()))[:-1])

    def parse_idx(self, idx):
        if idx > 0:
            return self.d[idx]
        elif idx < 0:
            return not(self.d[-idx])
        else:
            return None
        
    def print_clauses(self):
        print(self.clauses)
    
    def print_nbvars(self):
        print(self.nbvars)

    def print_nbclauses(self):
        print(self.nbclauses)

    def display(self):
        print(self.pretty())

    def pretty(self) -> str:
        clause_strs = []
        for clause in self.clauses:
            literals = []
            for literal in clause:
                if literal < 0:
                    literals.append(f"~x{-literal}")
                else:
                    literals.append(f"x{literal}")
            clause_strs.append("(" + " \\/ ".join(literals) + ")")
        return " /\\ ".join(clause_strs)

    def choose_random_variable(self):
        self.update()
        if self.nbunassigned == 0:
            return None
        else:
            return random.choice(self.unassignedKeys)
        
    # def choose_random_assignment(self):
    #     assign_dict = copy.deepcopy(self.d)
    #     for key in assign_dict:
    #         assign_dict[key] = random.choice([True, False])
    #     return assign_dict
    
    # def set_random_assignment(self, idx):
    #     if idx in self.d.keys():
    #         self.d[idx] = random.choice([True, False])
    #         return True
    #     else:
    #         return False

    def check_sat(self):
        pass

    def set_assignment(self, idx, b):
        if idx in self.d.keys():
            self.d[idx] = b
            return True
        else:
            return False        

    def stack_push(self, idx, b):
        if idx in self.d.keys():
            self.stack.append((idx, b, self.nbunassigned))
            return True
        else:
            return False

    def stack_pop(self):
        if not(self.empty()):
            return self.stack.pop()

    def empty(self):
        if len(self.stack) == 0:
            return True
        else:
            return False
        
    def run_dpll(self):
        pass
    
    def dpll(self):
        pass
        
    def print_assignment(self):
        pass

    def get_assignment(self):
        pass
    
    def getVars(self):
        pass

    def push_literal(self):
        pass

    def push_clause(self):
        pass

    def solve(self):
        pass
    
    def unit_propogation(self):
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
                        c = SAT(int(lst[2]), int(lst[3]))
                    else:
                        print(line)
                        c.parse_line(line)
            c.display()
        except FileNotFoundError:
            print(f"Error: File '{path}' not found.")
    else:
        print("Usage: python solver.py <path_to_text_file>")
