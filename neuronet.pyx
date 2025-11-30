# distutils: language = c++

from libcpp.vector cimport vector
from libcpp.string cimport string
from neuronet cimport grafodisperso

# clase wrapper para python
cdef class pygrafo:
    cdef grafodisperso* c_grafo

    def __cinit__(self):
        self.c_grafo = new grafodisperso()

    def __dealloc__(self):
        del self.c_grafo

    def cargar_datos(self, archivo):
        # convertir string python a c++
        cdef string c_archivo = archivo.encode('utf-8')
        self.c_grafo.cargar_datos(c_archivo)

    def bfs(self, inicio, profundidad):
        cdef vector[int] resultado = self.c_grafo.bfs(inicio, profundidad)
        return resultado

    def max_grado(self):
        return self.c_grafo.max_grado()
        
    def obtener_estadisticas(self):
        return {
            "nodos": self.c_grafo.obtener_num_nodos(),
            "aristas": self.c_grafo.obtener_num_aristas()
        }
