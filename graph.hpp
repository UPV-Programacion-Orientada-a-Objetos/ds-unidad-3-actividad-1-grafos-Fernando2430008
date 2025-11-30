#ifndef GRAPH_HPP
#define GRAPH_HPP

#include <vector>
#include <string>
#include <iostream>
#include <fstream>
#include <sstream>
#include <algorithm>
#include <queue>
#include <map>

// clase base abstracta para el grafo
class grafobase {
public:
    virtual ~grafobase() {}
    virtual void cargar_datos(const std::string& archivo) = 0;
    virtual std::vector<int> bfs(int inicio, int profundidad) = 0;
    virtual int max_grado() = 0;
};

// clase concreta que implementa csr
class grafodisperso : public grafobase {
private:
    int num_nodos;
    int num_aristas;
    // vectores para formato csr
    std::vector<int> valores;
    std::vector<int> columnas;
    std::vector<int> fila_ptr;

public:
    grafodisperso();
    ~grafodisperso();

    void cargar_datos(const std::string& archivo) override;
    std::vector<int> bfs(int inicio, int profundidad) override;
    int max_grado() override;
    
    // metodos auxiliares
    int obtener_num_nodos() const { return num_nodos; }
    int obtener_num_aristas() const { return num_aristas; }
};

#endif
