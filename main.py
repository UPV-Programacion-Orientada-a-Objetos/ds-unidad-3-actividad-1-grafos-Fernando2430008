import tkinter as tk
from tkinter import filedialog, messagebox
import neuronet
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# clase principal de la interfaz
class app:
    def __init__(self, root):
        self.root = root
        self.root.title("neuronet analisis de grafos")
        self.grafo = None

        # frame de controles
        frame_controles = tk.Frame(root)
        frame_controles.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)

        # boton cargar
        btn_cargar = tk.Button(frame_controles, text="cargar dataset", command=self.cargar_datos)
        btn_cargar.pack(side=tk.LEFT, padx=5)

        # etiquetas de estado
        self.lbl_info = tk.Label(frame_controles, text="sin datos cargados")
        self.lbl_info.pack(side=tk.LEFT, padx=5)

        # controles bfs
        tk.Label(frame_controles, text="nodo inicio").pack(side=tk.LEFT, padx=5)
        self.ent_inicio = tk.Entry(frame_controles, width=10)
        self.ent_inicio.pack(side=tk.LEFT)

        tk.Label(frame_controles, text="profundidad").pack(side=tk.LEFT, padx=5)
        self.ent_prof = tk.Entry(frame_controles, width=5)
        self.ent_prof.pack(side=tk.LEFT)

        btn_bfs = tk.Button(frame_controles, text="ejecutar bfs", command=self.ejecutar_bfs)
        btn_bfs.pack(side=tk.LEFT, padx=5)

        btn_grado = tk.Button(frame_controles, text="max grado", command=self.calc_max_grado)
        btn_grado.pack(side=tk.LEFT, padx=5)

        # area de visualizacion
        self.fig, self.ax = plt.subplots(figsize=(8, 6))
        self.canvas = FigureCanvasTkAgg(self.fig, master=root)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # barra de herramientas para zoom y pan
        from matplotlib.backends.backend_tkagg import NavigationToolbar2Tk
        toolbar = NavigationToolbar2Tk(self.canvas, root)
        toolbar.update()
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def cargar_datos(self):
        archivo = filedialog.askopenfilename()
        if not archivo:
            return
        
        try:
            self.grafo = neuronet.pygrafo()
            self.grafo.cargar_datos(archivo)
            stats = self.grafo.obtener_estadisticas()
            self.lbl_info.config(text=f"nodos {stats['nodos']} aristas {stats['aristas']}")
            messagebox.showinfo("exito", "datos cargados correctamente")
        except Exception as e:
            messagebox.showerror("error", str(e))

    def ejecutar_bfs(self):
        if not self.grafo:
            messagebox.showwarning("atencion", "primero cargue un dataset")
            return
        
        try:
            inicio = int(self.ent_inicio.get())
            prof = int(self.ent_prof.get())
            
            nodos_visitados = self.grafo.bfs(inicio, prof)
            self.visualizar_subgrafo(nodos_visitados)
            
        except ValueError:
            messagebox.showerror("error", "ingrese valores numericos validos")

    def calc_max_grado(self):
        if not self.grafo:
            return
        nodo = self.grafo.max_grado()
        messagebox.showinfo("resultado", f"nodo con mayor grado {nodo}")

    def visualizar_subgrafo(self, nodos):
        self.ax.clear()
        if not nodos:
            self.canvas.draw()
            return

        # crear subgrafo con networkx para visualizar
        g_vis = nx.Graph()
        # aqui podriamos recuperar las aristas reales del c++
        # pero por simplicidad y tiempo solo dibujamos los nodos
        # o conectamos secuencialmente para demo
        # en una implementacion real c++ devolveria aristas tambien
        
        # para visualizacion simple conectamos al nodo raiz con el resto
        # esto es solo una aproximacion visual
        raiz = nodos[0]
        for nodo in nodos:
            g_vis.add_node(nodo)
            if nodo != raiz:
                g_vis.add_edge(raiz, nodo)

        pos = nx.spring_layout(g_vis)
        nx.draw(g_vis, pos, ax=self.ax, with_labels=True, node_size=300, node_color='skyblue')
        self.canvas.draw()

if __name__ == "__main__":
    root = tk.Tk()
    app = app(root)
    root.mainloop()
