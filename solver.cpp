#include <iostream>
#include <fstream>
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

    
    public:
        SAT(int numOfVars, int numOfClauses) : nbvars(numOfVars), nbunassigned(numOfVars), nbclauses(numOfClauses){
            

            
        }
        void cold_restart();
        void update();
        void parse_line();
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
        vector<int> get_unassignedKeys();
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

int main(){

    unordered_set<char> exclusion_chars = {'c', '%', '0'};
    cout << boolalpha;
    cout << "Hello World" << endl;
    return 0;
    
}

