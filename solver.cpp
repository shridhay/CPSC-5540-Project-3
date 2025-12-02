#include <iostream>
#include <fstream>
#include <sstream>
#include <cmath>
#include <vector>
#include <string>
#include <unordered_set>
#include <ctime>
#include <random>

using namespace std;

enum class tribool : char {True, False, None};

class SAT {
    private:
        int nbvars;
        int nbunassigned;
        int nbconflicts = 0;
        int nbrestarts = 0;
        int limit = 4000;
        double alpha = 0.92;
        double alpha_increment = 1.01; 
        double alpha_max = 0.99;
        vector<vector<int> > clauses;
        vector<int> s;
        vector<tribool> umap;
        vector<bool> unassigned_keys;
        vector<double> log;
        vector<bool> polarity;
        mt19937 mt_rand;
        
    public:
        SAT(){mt_rand.seed(time(NULL));}
        void setup(int numOfVars, int numOfClauses){
            nbvars = numOfVars;
            nbunassigned = numOfVars;
            unassigned_keys.assign(nbvars + 1, true);
            umap.assign(nbvars + 1, tribool::None);
            clauses.reserve(numOfClauses);
            log.assign(nbvars + 1, 0.0);
            polarity.assign(nbvars + 1, true);
        }
        void cold_restart(){
            nbrestarts++;
            nbconflicts = 0;
            s.clear();
            umap.clear();
            umap.assign(nbvars + 1, tribool::None);
            unassigned_keys.clear();
            unassigned_keys.assign(nbvars + 1, true);
            nbunassigned = nbvars;
            alpha = min(alpha_max, alpha * alpha_increment);
            decay_keys();
        }
        void update_log(int idx){
            log[idx] = log[idx] + 1;
        }
        void decay_keys(){
            for(int i = 1; i < nbvars + 1; i++){
                log[i] = alpha * log[i];
            }
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
            clauses.push_back(std::move(clause));
        }
        tribool parse_idx(int idx){
            if (umap[abs(idx)] != tribool::None){
                tribool value = umap[abs(idx)];
                if (idx > 0){
                    return value;
                } else if (idx < 0){
                    if (value == tribool::True){
                        return tribool::False;
                    } else if (value == tribool::False){
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
        int choose_key(){
            vector<int> temp;
            double maximum = -1.0;
            for (int i = 1; i < nbvars + 1; i++){
                if ((unassigned_keys[i]) && (log[i] > maximum)){
                    maximum = log[i];
                }
            }
            for (int i = 1; i < nbvars + 1; i++){
                if ((unassigned_keys[i]) && (log[i] == maximum)){
                    temp.push_back(i);
                }
            }
            return temp[getInt(temp.size())];
        }
        bool check_sat(){
            for (const vector<int>& clause : clauses){
                bool satisfied = false;
                for(const int& literal : clause){
                    if (parse_idx(literal) == tribool::True){
                        satisfied = true;
                        break;
                    }
                }
                if (!satisfied) return false;
            }
            return true;
        }
        void set_assignment(int idx, tribool b){
            if (umap[idx] == tribool::None && b != tribool::None){
                nbunassigned--;
            }else if (umap[idx] != tribool::None && b == tribool::None) {
                nbunassigned++;
            }
            umap[idx] = b;
            if (b == tribool::None){ 
                unassigned_keys[idx] = true;
            } else {
                unassigned_keys[idx] = false;
                if (b == tribool::True){
                    polarity[idx] = true;
                } else if (b == tribool::False){
                    polarity[idx] = false;
                }
            }
        }
        bool stack_push(int idx){
            s.push_back(idx);
            return true;
        }
        int stack_pop(){
            if (!s.empty()){
                int t = s[s.size()-1];
                s.pop_back();
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
            bool solution = dpll();
            if (solution){
                print_assignment();
            } else {
                cout << "UNSAT" << endl;
            }
            return solution;
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
                for (const vector<int>& clause : clauses) {
                    bool satisfied = false;
                    int count = 0;
                    int unassigned_literal = 0;
                    for (const int& literal : clause) {
                        tribool val = parse_idx(literal);
                        if (val == tribool::True) {
                            satisfied = true;
                            break;               
                        }
                        else if (val == tribool::None) {
                            count++;
                            unassigned_literal = literal;
                        }
                    }
                    if (!satisfied && count == 0) {
                        nbconflicts += 1;
                        for (const int& literal : clause){
                            update_log(abs(literal));
                        }
                        decay_keys();
                        return false;
                    }
                    if (!satisfied && count == 1) {
                        tribool assignment = tribool::None;
                        if (unassigned_literal > 0){
                            assignment = tribool::True;
                        } else {
                            assignment = tribool::False;
                        }
                        stack_push(abs(unassigned_literal));
                        set_assignment(abs(unassigned_literal), assignment);
                        modified = true;
                    }
                }
            }
            return true; 
        }
        bool pure_literal_elimination(){
            unordered_set<int> positive;
            unordered_set<int> negative;
            for (const vector<int>& clause : clauses) {
                for (const int& literal : clause) {
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
                        set_assignment(idx, tribool::True);
                    } else if (negative.count(idx) && !positive.count(idx)){
                        set_assignment(idx, tribool::False);
                    }
                }
            }
            return true;
        }
        bool dpll(){
            if (nbconflicts >= limit){
                cold_restart();
                return dpll();
            }
            if (!unit_propagation()) return false;
            pure_literal_elimination();
            if (all_assigned()) return check_sat();
            int idx = choose_key();
            int size = s.size();
            stack_push(idx); 
            tribool top = polarity[idx] ? tribool::True : tribool::False;
            set_assignment(idx, top);
            if (dpll()) return true;
            backtrack(size);
            stack_push(idx);
            tribool bottom = polarity[idx] ? tribool::False : tribool::True;
            set_assignment(idx, bottom);
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
        cout << "Unable to open file: " << filename << endl;
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
