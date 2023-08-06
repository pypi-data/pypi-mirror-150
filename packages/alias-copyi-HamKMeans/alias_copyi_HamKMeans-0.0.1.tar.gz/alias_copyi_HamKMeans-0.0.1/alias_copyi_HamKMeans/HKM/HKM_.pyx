cimport numpy as np
import numpy as np
np.import_array()

from .HKM_ cimport HKM

cdef class PyHKM:
    cdef HKM c_HKM

    def __cinit__(self, np.ndarray[double, ndim=2] X, int c_true, bool debug=False):
        self.c_HKM = HKM(X, c_true, debug)

    def opt(self, Cen, bool isRing, int ITER=300):

        self.c_HKM.opt(Cen, isRing, ITER)

    @property
    def y_pre(self):
        return np.array(self.c_HKM.Y)
    
    @property
    def n_iter_(self):
        return np.array(self.c_HKM.n_iter_)

    @property
    def cal_num_dist(self):
        return np.array(self.c_HKM.cal_num_dist)

    @property
    def time_arr(self):
        return np.array(self.c_HKM.time_arr)