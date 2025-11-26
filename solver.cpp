#include <iostream>
#include <fstream>
#include <sstream>
#include <cmath>
#include <vector>
#include <string>
#include <algorithm>
#include <unordered_set>
#include <unordered_map>
#include <stack>
#include <tuple>
#include <utility>
#include <random>

using namespace std;

class SAT {
    private:
    int nbvars;
    int nbclauses;
    int nbunassigned;
    vector<vector<int> > clauses;
    stack<tuple<int, bool, int, bool> > unassigned_keys;
    int stack_size = 0;
    unordered_map<int, pair<bool, bool> > d;
    
    public:
        SAT(){}
        void setup(int numOfVars, int numOfClauses){
            nbvars = numOfVars;
            nbunassigned = numOfVars;
            nbclauses = numOfClauses;
        }
        void cold_restart();
        void update();
        void parse_line(string line);
        void increment(){nbunassigned++;}
        void decrement(){nbunassigned--;}
        bool parse_idx(int idx);
        bool all_assigned();
        void print_clauses();
        void print_nbvars();
        void print_nbclauses();
        void print_unassignedKeys();
        void print_nbunassigned();
        vector<vector<int> > get_clauses();
        vector<int> get_unassigned_keys();
        int get_nbunassigned();
        int get_size();
        void display();
        string pretty();
        int choose_random_key();
        bool check_sat();
        bool set_assignment(int idx, bool b);
        void stack_push(int idx, bool value, bool decision);
        tuple<int, bool, int, bool> stack_pop();
        bool stack_empty();
        void stack_print();
        void print_assignment();
        unordered_map<int, bool> get_assignment();
        bool solve();
        void backtrack(int n);
        bool dpll();
        bool pure_literal_elimination();
        bool unit_propagation();
};

int main(int argc, char *argv[]){
    if (argc != 2){
        cout << "Usage: " << endl;
    }
    string filename = argv[1];
    ifstream inputFile(filename);
    SAT solver;
    if (!inputFile.is_open()){
        cout << "Cannot open file: " << filename << endl;
    }
    string currentLine, tok;
    while(getline(inputFile, currentLine)){
        if (currentLine.empty() || currentLine[0] == 'c' || currentLine[0] == '%' || currentLine[0] == '0'){
            continue;
        } else if (currentLine[0] == 'p'){
            stringstream ss(currentLine);
            string p, cnf;
            int numOfVars, numOfClauses;
            ss >> p >> cnf >> numOfVars >> numOfClauses;
            solver.setup(numOfVars, numOfClauses);
        } else {
            solver.parse_line(currentLine);
        }
    }
    inputFile.close();
    return 0;
}

