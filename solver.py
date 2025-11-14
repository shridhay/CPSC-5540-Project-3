from __future__ import annotations
from abc import ABC, abstractmethod
from dataclasses import dataclass
# import re
from typing import Self, Union
import numpy as np
from fractions import Fraction
from functools import reduce
import sys
# import time
import copy
# import itertools
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
        self.nbunassigned = numOfVars
        self.d = {i: None for i in range(1, self.nbvars + 1)}
        self.unassignedKeys = list(self.d.keys())
        self.stack = []

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
        elif idx == 0:
            return None
        else:
            return None
        
    def all_assigned(self):
        return {True, False} >= set(self.d.values())
        
    def print_clauses(self):
        print(self.clauses)
    
    def print_nbvars(self):
        print(self.nbvars)

    def print_nbclauses(self):
        print(self.nbclauses)

    def print_unassignedKeys(self):
        self.update()
        print(self.unassignedKeys)

    def print_nbunassigned(self):
        self.update()
        print(self.nbunassigned)

    def get_clauses(self):
        return copy.deepcopy(self.clauses)
        
    def get_unassignedKeys(self):
        return copy.deepcopy(self.unassignedKeys)

    def get_nbunassiggned(self):
        return self.nbunassigned

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

    def choose_random_literal(self):
        self.update()
        if self.stack_empty():
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
        self.update()
        if self.stack_empty():
            return all(any(self.parse_idx(literal) for literal in clause) for clause in self.clauses)
        else:
            return None

    def set_assignment(self, idx, b):
        if idx in self.d.keys():
            self.d[idx] = b
            self.update()
            return True
        else:
            self.update()
            return False        

    def stack_push(self, idx, b):
        self.update()
        if idx in self.d.keys():
            self.stack.append((idx, b, self.nbunassigned))
            return True
        else:
            return False

    def stack_pop(self):
        if not(self.stack_empty()):
            return self.stack.pop()
        else:
            return None

    def stack_empty(self):
        return len(self.stack) == 0
    
    def stack_print(self):
        for idx in range(len(self.stack)-1, -1, -1):
            print(f"{self.stack[idx]}")
        
    def print_assignment(self):
        for key in self.d.keys():
            print(f"x{key} : {self.d[key]}")

    def get_assignment(self):
        return copy.deepcopy(self.d)
    
    def solve(self):
        sol = self.dpll()
        if sol:
            self.print_assignment()
        else:
            print("UNSAT")
        return sol

    def run_dpll(self):
        pass
    
    def dpll(self):
        pass
    
    def getVars(self):
        pass

    def push_literal(self):
        pass

    def push_clause(self):
        pass

    def unit_propogation(self):
        pass

    def pure_literal_elimination(self):
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
