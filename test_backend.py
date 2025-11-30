import neuronet
import sys

try:
    print("iniciando prueba backend")
    g = neuronet.pygrafo()
    print("objeto creado")
    g.cargar_datos("test_graph.txt")
    print("datos cargados")
    
    stats = g.obtener_estadisticas()
    print(f"stats: {stats}")
    
    max_deg = g.max_grado()
    print(f"max degree node: {max_deg}")
    
    bfs_res = g.bfs(0, 2)
    print(f"bfs result: {bfs_res}")
    
except Exception as e:
    print(f"error: {e}")
    sys.exit(1)
