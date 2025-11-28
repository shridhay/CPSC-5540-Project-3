import sys
import copy
import random

Clause = list[int]
LiteralIdx = int
DecisionLevel = int

class SAT:
    def __init__(self, numOfVars, numOfClauses):
        self.nbvars = numOfVars
        self.nbclauses = numOfClauses
        self.nbunassigned = numOfVars
        self.clauses: list[Clause] = []
        self.stack: list[tuple[LiteralIdx, bool, DecisionLevel, Clause | None]] = []
        self.d: dict[LiteralIdx, bool | None] = {i: None for i in range(1, self.nbvars + 1)}
        self.level: dict[LiteralIdx, int] = {i: 0 for i in range(1, self.nbvars+1)}
        self.reason: dict[LiteralIdx, Clause | None] = {i: None for i in range(1, self.nbvars+1)}
        self.decision_level: DecisionLevel = 0
        self.unassigned_keys = set(self.d.keys())
        self.stack_size = len(self.stack)
        self.blank_slate = {i: None for i in range(1, self.nbvars + 1)}

    def cold_restart(self):
        self.d = {i: None for i in range(1, self.nbvars + 1)}
        self.unassigned_keys = set(self.d.keys())
        self.nbunassigned = len(self.unassigned_keys)

    def update(self):
        self.unassigned_keys = {key for key in self.d.keys() if self.d[key] is None}
        self.nbunassigned = len(self.unassigned_keys)
    
    def parse_line(self, line):
        self.clauses.append(list(map(int, line.split()))[:-1])

    def increment(self):
        self.nbunassigned += 1

    def decrement(self):
        self.nbunassigned -= 1

    def parse_idx(self, idx):
        val = self.d.get(abs(idx), None)
        if val is None:
            return None
        if idx > 0:
            return val
        else:
            return not(val)
        
    def all_assigned(self):
        # self.update()
        return self.nbunassigned == 0
        
    def print_clauses(self):
        print(self.clauses)
    
    def print_nbvars(self):
        print(self.nbvars)

    def print_nbclauses(self):
        print(self.nbclauses)

    def print_unassigned_keys(self):
        # self.update()
        print(self.unassigned_keys)

    def print_nbunassigned(self):
        # self.update()
        print(self.nbunassigned)

    def get_clauses(self):
        return copy.deepcopy(self.clauses)
        
    def get_unassigned_keys(self):
        return copy.deepcopy(self.unassigned_keys)

    def get_nbunassigned(self):
        return self.nbunassigned
    
    def get_size(self):
        return len(self.stack)

    def display(self):
        print(self.pretty())

    def pretty(self):
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

    def choose_random_key(self):
        return random.choice(list(self.unassigned_keys))
            
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
            # self.update()
            return True
        else:
            # self.update()
            return False        

    def stack_push(self, idx, value, decision):
        self.stack.append((idx, value, self.nbunassigned, decision))

    def stack_pop(self):
        if not(self.stack_empty()):
            return self.stack.pop()
        else:
            raise IndexError("Cannot pop empty stack")

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
        sol = self.cdcl()
        if sol:
            self.print_assignment()
        else:
            print("UNSAT")
        return sol
    
    def backtrack(self, n):
        while len(self.stack) > n:
            idx, _, _, _= self.stack_pop()
            self.d[idx] = None
            self.unassigned_keys.add(idx)
            self.nbunassigned += 1
        # self.update()

    def dpll(self):
        if not(self.unit_propagation()):
            return False
        self.update()
        self.pure_literal_elimination()
        self.update()
        if self.all_assigned():
            return self.check_sat()
        # idx = random.choice(list(self.unassigned_keys))
        idx = self.choose_random_key()
        size = self.get_size()
        self.stack_push(idx, True, True)
        self.set_assignment(idx, True)
        self.update()
        if self.dpll():
            return True
        self.backtrack(size)
        self.stack_push(idx, False, True)
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
                    if self.d[idx] is None:
                        self.stack_push(idx, (literal > 0), False)
                        self.set_assignment(idx, (literal > 0))
                        modified = True
        return True
    
    def clauses_containing(self, literal: int) -> list[Clause]:
        """
        Return all clauses that contain the given literal.
        """
        result = []
        for clause in self.clauses:
            if literal in clause:
                result.append(clause)
        return result

    
    def unit_prop_cdcl(self) -> Clause | None:
        """
        Propagates all consequences of assigned literals.
        Returns a conflicting clause if any, otherwise None.
        """
        #print(f"\n[Unit Propagation] decision_level={self.decision_level}")
        #print("Current assignment:", {k: self.d[k] for k in self.d})

        # Start with all assigned variables
        propagation_queue = [(var if val else -var) for var, val, lvl, reason in self.stack]


        processed = set()

        while propagation_queue:
            literal = propagation_queue.pop()
            if literal in processed:
                continue
            processed.add(literal)

            for clause in self.clauses:
                # Skip if clause already satisfied
                if any(self.parse_idx(lit) is True for lit in clause):
                    continue

                # Collect unassigned literals
                unassigned = [l for l in clause if self.d[abs(l)] is None]

                if len(unassigned) == 0:
                    # Clause is falsified. 
                    # Check if *any* falsified literal is from the current decision level.
                    has_current_level = False
                    for lit in clause:
                        var = abs(lit)
                        # Literal is false if:
                        #   - var assigned False and lit > 0
                        #   - var assigned True  and lit < 0
                        if self.d[var] is not None:
                            false_literal = (self.d[var] is False and lit > 0) or \
                                            (self.d[var] is True  and lit < 0)
                            if false_literal and self.level[var] == self.decision_level:
                                has_current_level = True
                                break

                    if has_current_level:
                        #print(f"Conflict found in clause {clause}")
                        return clause

                    # Otherwise: clause is falsified but NOT due to current level → 
                    # NOT a real conflict for this level. Ignore it.
                    continue


                if len(unassigned) == 1:
                    # Unit clause found
                    unit = unassigned[0]
                    idx = abs(unit)
                    value = unit > 0

                    if self.d[idx] is None:
                        self.d[idx] = value
                        self.level[idx] = self.decision_level
                        self.reason[idx] = clause
                        self.stack.append((idx, value, self.decision_level, clause))
                        propagation_queue.append(idx)  # propagate new assignment

        return None


    def pure_literal_elim_cdcl(self):
        positive, negative = set(), set()
        
        # Scan all clauses
        for clause in self.clauses:
            for literal in clause:
                idx = abs(literal)
                if self.d[idx] is None:
                    if literal > 0:
                        positive.add(idx)
                    else:
                        negative.add(idx)
        
        # Assign pure literals
        for idx in range(1, self.nbvars + 1):
            if self.d[idx] is None:
                if (idx in positive) and not (idx in negative):
                    self.stack.append((idx, True, 0, None))
                    self.d[idx] = True
                    self.level[idx] = 0
                    self.reason[idx] = None
                elif (idx in negative) and not (idx in positive):
                    self.stack.append((idx, False, 0, None))
                    self.d[idx] = False
                    self.level[idx] = 0
                    self.reason[idx] = None

        return True
    
    def cdcl(self) -> bool:
        self.decision_level = 0
        self.pure_literal_elim_cdcl()
        conflict = self.unit_prop_cdcl()
        #print("MEGA CONFLICT")
        #print(conflict)
        if conflict:
            return False

        while True:
            if all(self.d[var] is not None for var in self.d):
                return True

            self.decision_level += 1
            var = self.pick_unassigned_variable()
            value = True
            self.d[var] = value
            self.level[var] = self.decision_level
            self.reason[var] = None
            self.stack.append((var, value, self.decision_level, None))

            while True:
                conflict = self.unit_prop_cdcl()
                # conflict handling inside cdcl(), replace current block with this
                if conflict:
                    #print(">>> CONFLICT handler entry")
                    #print(" conflict clause:", conflict)
                    # analyze
                    learned_clause, backjump_level = self.analyze_conflict(conflict)
                    #print(" learned_clause (post-analyze):", learned_clause)
                    #print(" levels (learned):", {lit: self.level[abs(lit)] for lit in learned_clause})
                    #print(" decision_level (old):", self.decision_level, " backjump_level:", backjump_level)

                    # defensive check for UIP
                    old_level = self.decision_level
                    candidates = [lit for lit in learned_clause if self.level[abs(lit)] == old_level]
                    #print(" candidates at old level:", candidates)

                    # if not the expected single candidate, dump stack + recent assignments
                    if len(candidates) != 1:
                        #print("STACK (top 20):", self.stack[-20:])
                        #print("ASSIGNMENTS (vars in learned):", {abs(l): (self.d[abs(l)], self.level[abs(l)], self.reason[abs(l)]) for l in learned_clause})
                        raise RuntimeError(f"ANALYSIS FAILURE: Expected 1 UIP literal, got {candidates}")

                    asserting_literal = candidates[0]
                    #print(" asserting_literal:", asserting_literal)

                    # now backjump once
                    self.backjump(backjump_level)
                    #print(" backjumped to", backjump_level, "current decision_level:", self.decision_level)

                    # If we are at root level, check if the learned clause is immediately contradictory
                    if backjump_level == 0:
                        # If every literal is already false or becomes false at root,
                        # the formula is UNSAT.
                        if all(self.d[abs(lit)] is not None and self.parse_idx(lit) is False
                            for lit in learned_clause):
                            #print("UNSAT at root")
                            return False


                    # assert UIP
                    idx = abs(asserting_literal); val = asserting_literal > 0
                    if self.d[idx] is not None:
                        #print("Warning: asserting literal already assigned after backjump:", idx, self.d[idx])
                        pass
                    else:
                        self.d[idx] = val
                        self.level[idx] = backjump_level
                        self.reason[idx] = learned_clause
                        self.stack.append((idx, val, backjump_level, learned_clause))
                    continue

                else:
                    break

    def pick_unassigned_variable(self) -> LiteralIdx:
        """
        Return an unassigned variable. 
        For now, simple heuristic: pick the first unassigned.
        """
        for var in self.unassigned_keys:
            if self.d[var] is None:
                return var
        raise RuntimeError("No unassigned variables left")  # should not happen
    
    def analyze_conflict(self, conflict_clause: Clause) -> tuple[Clause, DecisionLevel]:
        #print("Decision level:", self.decision_level)
        #print("Assignments:")
        for v in conflict_clause:
            v = abs(v)
            #print(v, "value:", self.d[v], "level:", self.level[v], "reason:", self.reason[v])

        learned = conflict_clause.copy()
        current_level = self.decision_level

        while True:
            # Count literals at current level
            curr_level_lits = [lit for lit in learned if self.level[abs(lit)] == current_level]

            # Stop when 1-UIP reached
            if len(curr_level_lits) <= 1:
                num_curr_level = sum(1 for lit in learned if self.level[abs(lit)] == current_level)
                #print("CLAUSE:", learned)
                #print("LEVELS:", {lit: self.level[abs(lit)] for lit in learned})
                #print("current_level:", current_level, "num_curr_level:", num_curr_level)
                break

            # Pick literal at current level with a reason
            for lit in curr_level_lits:
                idx = abs(lit)
                if self.reason[idx] is not None:
                    assert self.reason[idx] is not None
                    learned = self.resolve(learned, self.reason[idx], idx)
                    break
            else:
                # No literal with reason found => cannot reduce further
                break

        # Backjump level: highest level among other literals
        backjump_level = max((self.level[abs(lit)] for lit in learned if self.level[abs(lit)] != current_level), default=0)
        return learned, backjump_level

    
    def resolve(self, clause1: Clause, clause2: Clause, pivot: int) -> Clause:
        """
        Resolve two clauses on the pivot variable.
        """
        res = set(clause1).union(clause2)
        res.discard(pivot)
        res.discard(-pivot)
        return list(res)

    def backjump(self, level):
        while self.stack and self.stack[-1][2] > level:
            var, _, _, _ = self.stack.pop()
            self.d[var] = None
            self.level[var] = 0
            self.reason[var] = None
            self.unassigned_keys.add(var)
        self.decision_level = level

        



if __name__ == "__main__":
    if len(sys.argv) > 1:
        path = str(sys.argv[1])        
        try:
            solver = None
            with open(path, 'r') as f:
                for line in f:
                    line = line.strip()
                    if not(line) or (line[0] in {'c', '%', '0'}):
                        continue
                    elif line[0] == 'p':
                        args = line.split()
                        solver = SAT(int(args[2]), int(args[3]))
                    else:
                        assert solver is not None, "Reading valid line before 'p' line read"
                        solver.parse_line(line)
            if solver is not None:
                solver.display()
                solver.solve()
        except FileNotFoundError:
            print(f"Error: File '{path}' not found.")
    else:
        print("Usage: python solver.py <path_to_cnf_file>")
