# distutils: language = c++

from libcpp.vector cimport vector
from libcpp.string cimport string

cdef extern from "graph.cpp":
    pass

cdef extern from "graph.hpp":
    cdef cppclass grafobase:
        pass

    cdef cppclass grafodisperso(grafobase):
        grafodisperso() except +
        void cargar_datos(string archivo)
        vector[int] bfs(int inicio, int profundidad)
        int max_grado()
        int obtener_num_nodos()
        int obtener_num_aristas()
