# cython: language_level=3
# Cython file that provides an interface to C++ code

# Authors: Daniel Gribel, Lorenzo Saraiva and Thibaut Vidal
# Contact: dgribel@inf.puc-rio.br

import numpy as np
from libcpp.vector cimport vector

# distutils: language = c++
# distutils: sources = HGMeans.cpp

cdef extern from "HGMeans.h":
    cdef cppclass HGMeans:
        HGMeans()
        vector[vector[int]] Go(vector[vector[double]], vector[int], int, int, int, vector[int], int)
        void GoFile(char*, int, int, int, vector[int], int)

cdef class PyHGMeans:
    cdef HGMeans *thisptr      # hold a C++ instance which we are wrapping
    def __cinit__(self):
        self.thisptr = new HGMeans()
    def __dealloc__(self):
        del self.thisptr
    def Go(self, dataset, y, size_population, max_it, nb_it, list_clusters, w):
        return self.thisptr.Go(dataset, y, size_population, max_it, nb_it, list_clusters, w)
    def GoFile(self, filename, size_population, max_it, nb_it, list_clusters, w):
        self.thisptr.GoFile(filename, size_population, max_it, nb_it, list_clusters, w)
    def run(self, dataset, y, size_population=10, max_it=5000, nb_it=1, list_clusters=[2,3,5], w='0'):
        write = 0
        if w == 'w':
            write = 1
        return self.thisptr.Go(dataset, y, size_population, max_it, nb_it, list_clusters, write)
    def runfile(self, filename, size_population=10, max_it=5000, nb_it=1, list_clusters=[2,3,5], w='0'):
        py_filename = filename.encode('utf-8')
        write = 0
        if w == 'w':
            write = 1
        self.thisptr.GoFile(py_filename, size_population, max_it, nb_it, list_clusters, write)