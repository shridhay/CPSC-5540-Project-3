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
#include <set>
#include <tuple>
#include <utility>
#include <ctime>
#include <random>

using namespace std;

class SAT {
    private:
    int nbvars;
    int nbclauses;
    int nbunassigned;
    vector<vector<int> > clauses;
    stack<tuple<int, bool, int, bool> > s;
    int stack_size = 0;
    unordered_map<int, pair<bool, bool> > d;
    mt19937 mt_rand;
    set<int> unassigned_keys;
    
    public:
        SAT(){
            mt_rand.seed(time(NULL));
        }
        void setup(int numOfVars, int numOfClauses){
            nbvars = numOfVars;
            nbunassigned = numOfVars;
            nbclauses = numOfClauses;
            for(int i = 1; i < nbvars + 1; i++){
                unassigned_keys.insert(i);
            }
        }
        void parse_line(string line){
            vector<int> clause;
            int n;
            stringstream ss(line);
            while (ss >> n){
                if (n == 0){
                    break;
                } else {
                    clause.push_back(n);
                }
            }
            clauses.push_back(clause);
        }
        void update();
        void increment(){nbunassigned++;}
        void decrement(){nbunassigned--;}
        // bool parse_idx(int idx){
        //     if (d.count(abs(idx))){
        //         if (idx > 0){
        //             return d[idx];
        //         } else if (idx < 0){
        //             return !(d[-1 * idx]);
        //         }
        //     } else {
        //         return NULL;
        //     }
        // }
        bool all_assigned(){return nbunassigned == 0;}
        void print_clauses(){
            for (const auto& clause : clauses) {
                for (const auto& elem : clause) {
                    cout << elem << " ";
                }
                cout << endl; 
            }
        }
        void print_nbvars(){cout << to_string(nbvars) << endl;}
        void print_nbclauses(){cout << to_string(nbclauses) << endl;}
        void print_unassigned_keys();
        void print_nbunassigned(){cout << to_string(nbunassigned) << endl;}
        vector<vector<int> > get_clauses();
        vector<int> get_unassigned_keys();
        int get_nbunassigned();
        int get_size(){return s.size();}
        void display();
        string pretty();
        int choose_random_key();
        bool check_sat();
        bool set_assignment(int idx, bool b);
        void stack_push(int idx, bool value, bool decision){
            s.emplace(idx, value, nbunassigned, decision);
        }
        tuple<int, bool, int, bool> stack_pop();
        bool stack_empty(){return s.empty();}
        void stack_print();
        void print_assignment();
        unordered_map<int, bool> get_assignment();
        bool solve();
        void backtrack(int n);
        bool dpll();
        bool pure_literal_elimination();
        bool unit_propagation();
        int getInt(int min, int max){return ((mt_rand() % max) + min);}
        void reseed(){mt_rand.seed(time(NULL));}

};

int main(int argc, char *argv[]){
    if (argc != 2){
        cout << "Usage: " << endl;
        return 1;
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

