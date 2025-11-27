#include <iostream>
#include <fstream>
#include <sstream>
#include <cmath>
#include <vector>
#include <string>
#include <unordered_set>
#include <unordered_map>
#include <stack>
#include <ctime>
#include <random>

using namespace std;

enum class tribool {True, False, None};

class SAT {
    private:
        int nbvars;
        int nbunassigned;
        vector<vector<int> > clauses;
        stack<int> s;
        vector<tribool> umap;
        vector<bool> unassigned_keys;
        mt19937 mt_rand;
        
    public:
        SAT(){mt_rand.seed(time(NULL));}
        void setup(int numOfVars, int numOfClauses){
            nbvars = numOfVars;
            nbunassigned = numOfVars;
            unassigned_keys.assign(nbvars + 1, true);
            umap.assign(nbvars + 1, tribool::None);
        }
        int getInt(int max){return (mt_rand() % max);}
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
        tribool parse_idx(int idx){
            if (umap.at(abs(idx)) != tribool::None){
                tribool val = umap[abs(idx)];
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
        int choose_random_key(){
            if (all_assigned()) return -1;
            vector<int> v;
            v.reserve(nbunassigned);
            for (int i = 1; i < nbvars + 1; i++){
                if (unassigned_keys.at(i)) v.push_back(i);
            }
            return v.at(getInt(v.size()));
        }
        bool check_sat(){
            for (int i = 0; i < clauses.size(); i++){
                const auto& clause = clauses[i];
                bool satisfied = false;
                for (int j = 0; j < clause.size(); j++){
                    if (parse_idx(clause.at(j)) == tribool::True){
                        satisfied = true;
                        break;
                    }
                }
                if (!satisfied) return false;
            }
            return true;
        }
        void set_assignment(int idx, tribool b){
            if (umap[idx] == tribool::None && b != tribool::None) nbunassigned--;
            else if (umap[idx] != tribool::None && b == tribool::None) nbunassigned++;
            umap[idx] = b;
            if (b == tribool::None){ 
                unassigned_keys[idx] = true;
            } else {
                unassigned_keys[idx] = false;
            }
        }
        bool stack_push(int idx){
            s.push(idx);
            return true;
        }
        int stack_pop(){
            if (!s.empty()){
                int t = s.top();
                s.pop();
                return t;
            }
            return 0;
        }
        void print_assignment(){
            for(int i = 1; i < nbvars + 1; i++){
                if (umap[i] == tribool::True){
                    cout << "Key: " << i << ", Value: True"  << endl;
                } else if (umap[i] == tribool::False){
                    cout << "Key: " << i << ", Value: False"  << endl;
                } else {
                    cout << "Key: " << i << ", Value: None"  << endl;
                }
            }
        }
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
            while (s.size() > n){
                int idx = stack_pop();
                set_assignment(idx, tribool::None);
            }
        }
        bool unit_propagation() {
            bool modified = true;
            while (modified) {
                modified = false;
                for (const auto& clause : clauses) {
                    bool satisfied = false;
                    int unassigned_count = 0;
                    int last_unassigned_literal = 0;
                    for (int literal : clause) {
                        tribool val = parse_idx(literal);
                        if (val == tribool::True) {
                            satisfied = true;
                            break;               
                        }
                        else if (val == tribool::None) {
                            unassigned_count++;
                            last_unassigned_literal = literal;
                        }
                    }
                    if (!satisfied && unassigned_count == 0) {
                        return false;
                    }
                    if (!satisfied && unassigned_count == 1) {
                        tribool assignment = tribool::None;
                        if (last_unassigned_literal > 0){
                            assignment = tribool::True;
                        } else {
                            assignment = tribool::False;
                        }
                        stack_push(abs(last_unassigned_literal));
                        set_assignment(abs(last_unassigned_literal), assignment);
                        modified = true;
                    }
                }
            }
            return true; 
        }
        bool pure_literal_elimination(){
            unordered_set<int> positive;
            unordered_set<int> negative;
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
                if (umap[idx] == tribool::None){
                    if (positive.count(idx) && !negative.count(idx)){
                        // stack_push(idx);
                        set_assignment(idx, tribool::True);
                    } else if (negative.count(idx) && !positive.count(idx)){
                        // stack_push(idx);
                        set_assignment(idx, tribool::False);
                    }
                }
            }
            return true;
        }
        bool dpll(){
            if (!unit_propagation()) return false;
            pure_literal_elimination();
            if (all_assigned()) return check_sat();
            int idx = choose_random_key();
            int size = s.size();
            stack_push(idx); 
            set_assignment(idx, tribool::True);
            if (dpll()) return true;
            backtrack(size);
            stack_push(idx);
            set_assignment(idx, tribool::False);
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
    string currentLine;
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
