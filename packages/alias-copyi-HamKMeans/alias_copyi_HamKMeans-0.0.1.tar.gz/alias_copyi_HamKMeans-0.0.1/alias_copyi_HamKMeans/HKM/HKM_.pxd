from libcpp.vector cimport vector
from libcpp cimport bool

cdef extern from "ham_kmeanspp.cpp":
    pass

cdef extern from "HKM.cpp":
    pass

cdef extern from "HKM.h":
    cdef cppclass HKM:

        vector[vector[int]] Y
        vector[int] n_iter_
        vector[double] time_arr
        vector[int] cal_num_dist

        HKM() except +
        HKM(vector[vector[double]] &X, int c_true, bool debug) except +
        void opt(vector[vector[vector[double]]] &Cen, bool isRing, int ITER)
