from __future__ import annotations
# from abc import ABC, abstractmethod
# from dataclasses import dataclass
# import re
# from typing import Self, Union
# import numpy as np
# from fractions import Fraction
# from functools import reduce
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
        self.blank_slate = {i: None for i in range(1, self.nbvars + 1)}

    def cold_start(self):
        self.d = {i: None for i in range(1, self.nbvars + 1)}
        self.unassignedKeys = list(self.d.keys())
        self.nbunassigned = len(self.unassignedKeys)

    def update(self):
        self.unassignedKeys = [key for key in self.d.keys() if self.d[key] is None]
        self.nbunassigned = len(self.unassignedKeys)
    
    def parse_line(self, line):
        self.clauses.append(list(map(int, line.split()))[:-1])

    # def parse_idx(self, idx):
    #     if idx > 0:
    #         return self.d[idx] if idx in self.d.keys() else None
    #     elif idx < 0:
    #         return not(self.d[-idx]) if -idx in self.d.keys() else None
    #     elif idx == 0:
    #         return None
    #     else:
    #         return None

    def parse_idx(self, idx):
        val = self.d.get(abs(idx), None)
        if val is None:
            return None
        if idx > 0:
            return val
        else:
            return not(val)
        
    def all_assigned(self):
        return all(value is not None for value in self.d.values())
        
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

    def get_nbunassigned(self):
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
            clause_strs.append("(" + " ∨ ".join(literals) + ")")
        return " ∧ ".join(clause_strs)

    # def choose_random_literal(self):
    #     self.update()
    #     if self.nbunassigned == 0:
    #         return None
    #     return random.choice(self.unassignedKeys)
            
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
            return all(any(self.parse_idx(literal) is True for literal in clause) for clause in self.clauses)
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

    def stack_push(self, idx, value):
        self.stack.append((idx, value, self.nbunassigned))

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
    
    def backtrack(self, n):
        while not(self.stack_empty()) and (self.nbunassigned != n):
            idx, _, _ = self.stack_pop()
            self.d[idx] = None
            self.update()

    def dpll(self):
        # 1. UNIT PROPAGATION
        if not self.unit_propagation():
            return False
        # 2. PURE LITERAL ELIMINATION
        self.pure_literal_elimination()
        self.update()
        # 3. If all variables assigned, check clauses
        if self.nbunassigned == 0:
            return all(any(self.parse_idx(literal) == True for literal in clause) for clause in self.clauses)
        # 4. Choose a branching variable
        idx = random.choice(self.unassignedKeys)
        # Store backtracking target (before decision)
        decision_unassigned = self.nbunassigned
        # First branch: True
        self.stack_push(idx, True)
        self.set_assignment(idx, True)
        if self.dpll():
            return True
        # Backtrack
        self.backtrack(decision_unassigned)
        # Second branch: False
        self.stack_push(idx, False)
        self.set_assignment(idx, False)
        if self.dpll():
            return True
        # Backtrack again
        self.backtrack(decision_unassigned)
        return False

    def pure_literal_elimination(self):
        positive, negative = set(), set()
        for clause in self.clauses:
            for literal in clause:
                if self.parse_idx(literal) is None:
                    if literal > 0:
                        positive.add(literal)
                    else:
                        negative.add(-literal)
        for variable in range(1, self.nbvars + 1):
            if self.d[variable] is None:
                if (variable in positive) and not(variable in negative):
                    self.set_assignment(variable, True)
                elif (variable in negative) and not(variable in positive):
                    self.set_assignment(variable, False)
        return True

    def unit_propagation(self):
        """
        Repeatedly apply unit propagation until no more forced literals exist.
        Returns False if a contradiction is found.
        """
        changed = True
        while changed:
            changed = False
            for clause in self.clauses:
                # Clause satisfied -> skip
                if any(self.parse_idx(literal) is True for literal in clause):
                    continue
                # Find unassigned literals
                unassigned_literals = [literal for literal in clause if self.parse_idx(literal) is None]
                # Clause conflict: all false
                if len(unassigned_literals) == 0:
                    return False
                # Unit clause
                if len(unassigned_literals) == 1:
                    literal = unassigned_literals[0]
                    idx = abs(literal) 
                    val = literal > 0
                    if self.d[idx] is None:
                        self.stack_push(idx, val)
                        self.set_assignment(idx, val)
                        changed = True
        return True

if __name__ == "__main__":
    if len(sys.argv) > 1:
        path = str(sys.argv[1])        
        try:
            with open(path, 'r') as f:
                for line in f:
                    line = line.strip()
                    if not(line) or line[0] == 'c':
                        continue
                    elif line[0] == 'p':
                        print(line)
                        lst = line.split()
                        solver = SAT(int(lst[2]), int(lst[3]))
                    else:
                        print(line)
                        solver.parse_line(line)
            solver.display()
            solver.solve()
        except FileNotFoundError:
            print(f"Error: File '{path}' not found.")
    else:
        print("Usage: python solver.py <path_to_cnf_file>")
