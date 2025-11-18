from __future__ import annotations
import sys
import copy
import random

class SAT:
    def __init__(self, numOfVars, numOfClauses):
        self.nbvars = numOfVars
        self.nbclauses = numOfClauses
        self.clauses = []
        self.nbunassigned = numOfVars
        self.d = {i: None for i in range(1, self.nbvars + 1)}
        self.unassignedKeys = list(self.d.keys())
        self.stack = []
        self.stack_size = len(self.stack)
        self.blank_slate = {i: None for i in range(1, self.nbvars + 1)}

    def cold_start(self):
        self.d = {i: None for i in range(1, self.nbvars + 1)}
        self.unassignedKeys = list(self.d.keys())
        self.nbunassigned = len(self.unassignedKeys)

    def update(self):
        self.stack_size = len(self.stack)
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

    def all_assigned(self):
        return self.nbunassigned == 0

    def get_clauses(self):
        return copy.deepcopy(self.clauses)
        
    def get_unassignedKeys(self):
        return copy.deepcopy(self.unassignedKeys)

    def get_nbunassigned(self):
        return self.nbunassigned
    
    def get_size(self):
        return len(self.stack)

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
        return all(any(self.parse_idx(literal) == True for literal in clause) for clause in self.clauses)
    
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
        while len(self.stack) > n:
            idx, _, _ = self.stack_pop()
            self.d[idx] = None
        self.update()

    def dpll(self):
        if not(self.unit_propagation()):
            return False
        self.pure_literal_elimination()
        self.update()
        if self.all_assigned():
            return self.check_sat()
        idx = random.choice(self.unassignedKeys)
        size = self.get_size()
        self.set_assignment(idx, True)
        self.update()
        if self.dpll():
            return True
        self.backtrack(size)
        self.set_assignment(idx, False)
        self.update()
        if self.dpll():
            return True
        self.backtrack(size)
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
        for idx in range(1, self.nbvars + 1):
            if self.d[idx] is None:
                if (idx in positive) and not(idx in negative):
                    self.set_assignment(idx, True)
                elif (idx in negative) and not(idx in positive):
                    self.set_assignment(idx, False)
        return True

    def unit_propagation(self):
        modified = True
        while modified:
            modified = False
            for clause in self.clauses:
                if any(self.parse_idx(literal) is True for literal in clause):
                    continue
                unassigned_literals = [literal for literal in clause if self.parse_idx(literal) is None]
                if len(unassigned_literals) == 0:
                    return False
                if len(unassigned_literals) == 1:
                    literal = unassigned_literals[0]
                    idx = abs(literal) 
                    val = literal > 0
                    if self.d[idx] is None:
                        self.stack_push(idx, val)
                        self.set_assignment(idx, val)
                        modified = True
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
