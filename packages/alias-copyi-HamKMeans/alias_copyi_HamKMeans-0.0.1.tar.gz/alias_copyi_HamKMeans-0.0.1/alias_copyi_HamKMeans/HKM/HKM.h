#ifndef HKM_H_
#define HKM_H_
#include "ham_kmeanspp.h"

class HKM{
public:
    int N, dim, c_true;
    bool debug;
    MatrixOur X;
    vector<vector<int>> Y;
    vector<int> n_iter_;
    vector<double> time_arr;
    vector<int> cal_num_dist;

    HKM();
    HKM(vector<vector<double>> &X, int c_true, bool debug);
    ~HKM();

    void opt(vector<vector<vector<double>>> &Cen, bool isRing, int ITER);
    Veci_int opt_once(vector<vector<double>> &Cen_vec, int ITER, bool isRing);

};

#endif // HKM_H_