#include "graph.hpp"

// constructor por defecto
grafodisperso::grafodisperso() : num_nodos(0), num_aristas(0) {
    // inicializamos fila_ptr con 0
    fila_ptr.push_back(0);
}

// destructor
grafodisperso::~grafodisperso() {}

// carga datos desde archivo
void grafodisperso::cargar_datos(const std::string& archivo) {
    std::ifstream file(archivo);
    if (!file.is_open()) {
        std::cerr << "error al abrir archivo" << std::endl;
        return;
    }

    // lista de adyacencia temporal
    std::map<int, std::vector<int>> adyacencia;
    int u;
    int v;
    int max_id = 0;

    // leer archivo linea por linea
    std::string linea;
    while (std::getline(file, linea)) {
        if (linea.empty() || linea[0] == '#') continue;
        std::stringstream ss(linea);
        ss >> u >> v;
        
        adyacencia[u].push_back(v);
        // grafo no dirigido asi que agregamos v u tambien
        adyacencia[v].push_back(u);

        if (u > max_id) max_id = u;
        if (v > max_id) max_id = v;
    }
    
    num_nodos = max_id + 1;
    
    // construir csr
    fila_ptr.resize(num_nodos + 1, 0);
    valores.clear();
    columnas.clear();
    
    int acumulado = 0;
    for (int i = 0; i < num_nodos; ++i) {
        if (adyacencia.find(i) != adyacencia.end()) {
            std::vector<int>& vecinos = adyacencia[i];
            // ordenar vecinos para consistencia
            std::sort(vecinos.begin(), vecinos.end());
            
            for (int vecino : vecinos) {
                valores.push_back(1); // peso 1 por defecto
                columnas.push_back(vecino);
                acumulado++;
            }
        }
        fila_ptr[i + 1] = acumulado;
    }
    num_aristas = acumulado;
    std::cout << "carga completa nodos " << num_nodos << " aristas " << num_aristas << std::endl;
}

// algoritmo bfs
std::vector<int> grafodisperso::bfs(int inicio, int profundidad) {
    std::vector<int> visitados;
    if (inicio < 0 || inicio >= num_nodos) return visitados;

    std::vector<int> distancias(num_nodos, -1);
    std::queue<int> cola;

    distancias[inicio] = 0;
    cola.push(inicio);
    visitados.push_back(inicio);

    while (!cola.empty()) {
        int actual = cola.front();
        cola.pop();

        if (distancias[actual] >= profundidad) continue;

        // iterar vecinos usando csr
        int inicio_vecinos = fila_ptr[actual];
        int fin_vecinos = fila_ptr[actual + 1];

        for (int i = inicio_vecinos; i < fin_vecinos; ++i) {
            int vecino = columnas[i];
            if (distancias[vecino] == -1) {
                distancias[vecino] = distancias[actual] + 1;
                cola.push(vecino);
                visitados.push_back(vecino);
            }
        }
    }
    return visitados;
}

// calcular nodo con mayor grado
int grafodisperso::max_grado() {
    int max_g = -1;
    int nodo_max = -1;

    for (int i = 0; i < num_nodos; ++i) {
        int grado = fila_ptr[i + 1] - fila_ptr[i];
        if (grado > max_g) {
            max_g = grado;
            nodo_max = i;
        }
    }
    return nodo_max;
}
