#!/bin/bash

# Run SAT benchmarks
for i in {1..13}; do
    echo "Verifying SAT benchmark $i..."
    python solver.py "benchmarks/sat/bench$i.cnf"
done

# Run UNSAT benchmarks
for i in {1..13}; do
    echo "Verifying UNSAT benchmark $i..."
    python solver.py "benchmarks/unsat/bench$i.cnf"
done
