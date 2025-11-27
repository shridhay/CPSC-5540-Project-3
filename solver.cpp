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

enum class tribool {True, False, None};

class SAT {
    private:
        int nbvars;
        int nbclauses;
        int nbunassigned;
        vector<vector<int> > clauses;
        stack<tuple<int, bool, int, bool> > s;
        int stack_size = 0;
        unordered_map<int, tribool> d;
        mt19937 mt_rand;
        set<int> unassigned_keys;
        
    public:
        SAT(){mt_rand.seed(time(NULL));}
        void setup(int numOfVars, int numOfClauses){
            nbvars = numOfVars;
            nbunassigned = numOfVars;
            nbclauses = numOfClauses;
            for(int i = 1; i < nbvars + 1; i++){
                unassigned_keys.insert(i);
            }
            for(int i = 1; i < nbvars + 1; i++){
                d.insert({i, tribool::None});
            }
        }
        int getInt(int min, int max){
            std::uniform_int_distribution<int> dist(min, max - 1);
            return dist(mt_rand);
        }
        void reseed(){mt_rand.seed(time(NULL));}
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
        void update(){
            unassigned_keys.clear();
            for (const auto& p : d) {
                if (p.second == tribool::None) {  
                    unassigned_keys.insert(p.first);
                }
            }
            nbunassigned = unassigned_keys.size();
        }
        // void increment(){nbunassigned++;}
        // void decrement(){nbunassigned--;}
        tribool parse_idx(int idx){
            if (d.count(abs(idx))){
                tribool val = d[abs(idx)];
                if (idx > 0){
                    return val;
                } else if (idx < 0){
                    if (val == tribool::True){
                        return tribool::False;
                    } else if (val == tribool::False){
                        return tribool::True;
                    } else {
                        return tribool::None;
                    }
                } else {
                    return tribool::None;
                }
            } else {
                return tribool::None;
            }
        }
        bool all_assigned(){return nbunassigned == 0;}
        // void print_clauses(){
        //     for (const auto& clause : clauses) {
        //         for (const auto& literal : clause) {
        //             cout << literal << " ";
        //         }
        //         cout << endl; 
        //     }
        // }
        // void print_nbvars(){cout << to_string(nbvars) << endl;}
        // void print_nbclauses(){cout << to_string(nbclauses) << endl;}
        // void print_unassigned_keys(){
        //     for (const int& key : unassigned_keys) {
        //         cout << key << endl;
        //     }
        // }
        // void print_nbunassigned(){cout << to_string(nbunassigned) << endl;}
        // vector<vector<int> > get_clauses(){
        //     vector<vector<int> > v = clauses;
        //     return v;
        // }
        // set<int> get_unassigned_keys(){
        //     set<int> t;
        //     for (const int& key : unassigned_keys) {
        //         t.insert(key);
        //     }
        //     return t;
        // }
        // int get_nbunassigned(){return nbunassigned;}
        // int get_nbclauses(){return nbclauses;}
        // int get_nbvars(){return nbvars;}
        int get_size(){return s.size();}
        void display(){cout << pretty() << endl;}
        string pretty(){
            vector<string> clause_strs;
            for (const auto& clause : clauses) {
                vector<string> literals;
                for (const auto& literal : clause) {
                    if (literal < 0){
                        literals.push_back("~x" + to_string(-literal));
                    } else {
                        literals.push_back("x" + to_string(literal));
                    }
                }
                string clause_str = "(";
                for (int i = 0; i < literals.size(); i++){
                    clause_str += literals[i];
                    if (i < literals.size() - 1){
                        clause_str += " ∨ ";
                    }
                }
                clause_str += ")";
                clause_strs.push_back(clause_str);
            }
            string result = "";
            for (int i = 0; i < clause_strs.size(); i++){
                result += clause_strs[i];
                if (i < clause_strs.size() - 1){
                    result += " ∧ ";
                }
            }
            return result;
        }
        int choose_random_key(){
            vector<int> v;
            v.reserve(unassigned_keys.size());
            for (const int& key : unassigned_keys) {
                v.push_back(key);
            }
            int idx = getInt(0, v.size());
            int val = v.at(idx);
            v.clear();
            return val;
        }
        bool check_sat(){
            for (int i = 0; i < clauses.size(); i++){
                const auto& clause = clauses[i];
                bool satisfied = false;
                for (int j = 0; j < clause.size(); j++){
                    int literal = clause.at(j);
                    tribool val = parse_idx(literal);
                    if (val == tribool::True){
                        satisfied = true;
                        break;
                    }
                }
                if (!satisfied){
                    return false;
                }
            }
            return true;
        }
        void set_assignment(int idx, tribool b){
            d[idx] = b;
            if (b == tribool::None){
                unassigned_keys.insert(idx);
            } else{
                unassigned_keys.erase(idx);
            }
        }
        bool stack_push(int idx, bool value, bool decision){
            tuple<int, bool, int, bool> t = make_tuple(idx, value, nbunassigned, decision);
            s.push(t);
            return true;
        }
        tuple<int, bool, int, bool> stack_pop(){
            if (!s.empty()){
                tuple<int, bool, int, bool> t = s.top();
                s.pop();
                return t;
            }
            return make_tuple(0, false, 0, false);
        }
        bool stack_empty(){return s.empty();}
        void print_assignment(){
            for(int i = 1; i < nbvars + 1; i++){
                tribool value = d[i];
                if (value == tribool::True){
                    cout << "Key: " << i << ", Value: True"  << endl;
                } else if (value == tribool::False){
                    cout << "Key: " << i << ", Value: False"  << endl;
                } else {
                    cout << "Key: " << i << ", Value: None"  << endl;
                }
            }
        }
        // unordered_map<int, tribool> get_assignment(){
        //     unordered_map<int, tribool> m = d;
        //     return m;
        // }
        bool solve(){
            bool sol = dpll();
            if (sol){
                print_assignment();
            } else {
                cout << "UNSAT" << endl;
            }
            return sol;
        }
        void backtrack(int n){
            while (get_size() > n){
                tuple<int, bool, int, bool> t = stack_pop();
                int idx = get<0>(t);
                d[idx] = tribool::None;
                unassigned_keys.insert(idx);
                nbunassigned++;
            }
        }
        bool unit_propagation() {
            bool modified = true;
            while (modified) {
                modified = false;
                for (const auto& clause : clauses) {
                    bool satisfied = false;
                    int unassigned_count = 0;
                    int last_unassigned_lit = 0;
                    for (int lit : clause) {
                        tribool val = parse_idx(lit);
                        if (val == tribool::True) {
                            satisfied = true;
                            break;               
                        }
                        else if (val == tribool::None) {
                            unassigned_count++;
                            last_unassigned_lit = lit;
                        }
                    }
                    if (!satisfied && unassigned_count == 0) {
                        return false;
                    }
                    if (!satisfied && unassigned_count == 1) {
                        int var = abs(last_unassigned_lit);
                        tribool assign_val = (last_unassigned_lit > 0) 
                                            ? tribool::True 
                                            : tribool::False;
                        stack_push(var, assign_val == tribool::True, false);
                        set_assignment(var, assign_val);
                        modified = true;
                    }
                }
            }
            return true; 
        }
        bool pure_literal_elimination(){
            set<int> positive;
            set<int> negative;
            for (const auto& clause : clauses) {
                for (const auto& literal : clause) {
                    if (parse_idx(literal) == tribool::None){
                        if (literal > 0){
                            positive.insert(literal);
                        } else {
                            negative.insert(-1 * literal);
                        }
                    }
                }
            }
            for(int idx = 1; idx < nbvars + 1; idx++){
                if (d[idx] == tribool::None){
                    if (positive.count(idx) && !negative.count(idx)){
                        set_assignment(idx, tribool::True);
                    } else if (negative.count(idx) && !positive.count(idx)){
                        set_assignment(idx, tribool::False);
                    }
                }
            }
            return true;
        }
        bool dpll(){
            if (!unit_propagation()) return false;
            update();
            pure_literal_elimination();
            update();
            if (all_assigned()) return check_sat();
            int idx = choose_random_key();
            int size = get_size();
            stack_push(idx, true, true); 
            set_assignment(idx, tribool::True);
            update();
            if (dpll()) return true;
            backtrack(size);
            stack_push(idx, false, false);
            set_assignment(idx, tribool::False);
            update();
            if (dpll()) return true;
            backtrack(size);
            return false;
        }
};

int main(int argc, char *argv[]){
    if (argc != 2){
        cout << "Usage: ./solver <path_to_cnf_file>" << endl;
        return 1;
    }
    string filename = argv[1];
    ifstream inputFile(filename);
    SAT solver;
    if (!inputFile.is_open()){
        cout << "Cannot open file: " << filename << endl;
        return 1;
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
    solver.solve();
    return 0;
}

