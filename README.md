# CPSC 5540 Project 3: SAT Solver

This implementation was developed by Jonathan Chen and Hridhay Suresh.

## Requirements

This SAT Solver is written in C++17, but may run on previous C++ versions. 

## Running the SAT Solver

To run this SAT solver, run `g++ -std=c++17 -O3 -o solver solver.cpp`, followed by `chmod +x solver` in the terminal.  Finally run `./solver <path_to_cnf_file>` in the terminal.

## Extensions

We implemented 5 extensions in this project:

1) Cold Restart based on an enumeration of variable conflicts.
2) VSIDS heuristic for selecting variables to assign based on the most frequented variables.
3) Polarity saving that remembers the assigment of previously assigned variables.
4) Dynamically adjusting decay for the VSIDS heuristic.
5) Randomized Tie-breaking for the VSIDS heuristic.

## Quick Start

We have provided a benchmark as well as a test script.  To run the test script run `chmod +x testcpp.sh`, followed by `sh testcpp.sh` in the terminal.
