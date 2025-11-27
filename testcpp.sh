#!/bin/bash

# Compile the solver
g++ -std=c++17 -O3 -o solver solver.cpp
chmod +x solver

countFalseNegative=0
countFalsePositive=0

START_TIME=$SECONDS

for i in {1..300}; do
    f="benchmarks/uf50-218/uf50-0${i}.cnf"
    result=$(./solver "$f")
    if [[ "$result" == *UNSAT* ]]; then
        echo "$f: $result"
        ((countFalseNegative++))
    fi
done

for i in {1..300}; do
    f="benchmarks/UUF50.218.1000/uuf50-0${i}.cnf"
    result=$(./solver "$f")
    if [[ ! "$result" == *UNSAT* ]]; then
        echo "$f: $result"
        ((countFalsePositive++))
    fi
done

ELAPSED_TIME=$(($SECONDS - $START_TIME))

echo 
echo "Total UF50 declared UNSAT: $countFalseNegative"
echo "Total UUF50 declared SAT: $countFalsePositive"
echo "Execution time in seconds: $ELAPSED_TIME s"
echo "$(($ELAPSED_TIME/60)) min $(($ELAPSED_TIME%60)) sec"
