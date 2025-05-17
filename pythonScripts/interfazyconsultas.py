from tkinter import ttk, messagebox
import mysql.connector
import pandas as pd
import tkinter as tk
from mysql.connector import Error

class AppTransacciones:
    def __init__(self, ventana):
        self.ventana = ventana
        self.ventana.geometry("1100x650")
        self.ventana.title("Visualizador de Datos")
        self.db_config = {
            'password': '1234',
            'host': 'localhost',
            'user': 'admin',
            'database': 'EmpresaPTNT'
        }
        self.orden_monto = 'DESC'
        self.orden_empresa = None
        self.inicializar_ui()
        self.conectar_db()

    def actualizar_estadisticas(self):
        if hasattr(self, 'datos') and not self.datos.empty:
            maximo = self.datos['total_amount'].max()
            minimo = self.datos['total_amount'].min()
            promedio = self.datos['total_amount'].mean()
            self.etiqueta_max.config(text=f"Máximo: ${maximo:,.2f}")
            self.etiqueta_min.config(text=f"Mínimo: ${minimo:,.2f}")
            self.etiqueta_prom.config(text=f"Promedio: ${promedio:,.2f}")

    def cargar_datos(self):
        try:
            sql = "SELECT * FROM vista_transacciones" #vista hecha en sqll
            ordenes = []
            
            if self.orden_empresa:
                ordenes.append(f"company_name {self.orden_empresa}")
            if self.orden_monto:
                ordenes.append(f"total_amount {self.orden_monto}")
            if ordenes:
                sql += " ORDER BY " + ", ".join(ordenes)
            sql += " LIMIT 10" #limitarlo a 10 para que se alcance a ver
            self.datos = pd.read_sql(sql, self.conexion)
            
            for item in self.tabla.get_children():
                self.tabla.delete(item)
                
            self.tabla["columns"] = list(self.datos.columns)
            self.tabla["show"] = "headings"
            for col in self.datos.columns:
                self.tabla.heading(col, text=col)
                self.tabla.column(col, width=100, anchor=tk.CENTER)
            
            for _, fila in self.datos.iterrows():
                self.tabla.insert("", tk.END, values=list(fila))
            self.actualizar_estadisticas()
            



        except Error as e:
            messagebox.showerror("Error", f"Error en la consulta:\n{e}")

    def cambiar_orden(self):
        self.orden_monto = self.var_monto.get()
        orden_emp = self.var_empresa.get()
        self.orden_empresa = orden_emp if orden_emp != 'None' else None
        self.cargar_datos()

    def conectar_db(self):
        try:
            self.conexion = mysql.connector.connect(**self.db_config)
            if self.conexion.is_connected():
                self.cargar_datos()
        except Error as e:
            messagebox.showerror("Error DB", f"Error de conexión:\n{e}")




    def inicializar_ui(self):
        marco_principal = ttk.Frame(self.ventana, padding="10")
        marco_principal.pack(fill=tk.BOTH, expand=True)
        titulo = ttk.Label(
            marco_principal, 
            text="Transacciones", 
            font=('Helvetica', 22, 'bold')
        )
        titulo.pack(pady=10)
        



        controles = ttk.Frame(marco_principal)
        controles.pack(fill=tk.X, pady=10)
        marco_monto = ttk.LabelFrame(controles, text="Ordenar por Monto", padding=10)
        marco_monto.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        self.var_monto = tk.StringVar(value='DESC')
        
        ttk.Radiobutton(
            marco_monto,
            text="Mayor a menor",
            variable=self.var_monto,
            value='DESC',
            command=self.cambiar_orden
        ).pack(side=tk.LEFT, padx=5)
        


        ttk.Radiobutton(
            marco_monto,
            text="Menor a mayor",
            variable=self.var_monto,
            value='ASC',
            command=self.cambiar_orden
        ).pack(side=tk.LEFT, padx=5)
        


        marco_empresa = ttk.LabelFrame(controles, text="Ordenar por Empresa", padding=10)
        marco_empresa.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        
        self.var_empresa = tk.StringVar(value='None')
        ttk.Radiobutton(
            marco_empresa,
            text="A-Z",
            variable=self.var_empresa,
            value='ASC',
            command=self.cambiar_orden
        ).pack(side=tk.LEFT, padx=5)
        ttk.Radiobutton(
            marco_empresa,
            text="Z-A",
            variable=self.var_empresa,
            value='DESC',
            command=self.cambiar_orden
        ).pack(side=tk.LEFT, padx=5)
        ttk.Radiobutton(
            marco_empresa,
            text="Ninguno",
            variable=self.var_empresa,
            value='None',
            command=self.cambiar_orden
        ).pack(side=tk.LEFT, padx=5)
        


        self.tabla = ttk.Treeview(marco_principal)
        self.tabla.pack(fill=tk.BOTH, expand=True, pady=10)
        scroll = ttk.Scrollbar(self.tabla, orient="vertical", command=self.tabla.yview)
        scroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.tabla.configure(yscrollcommand=scroll.set)
        
        botones = ttk.Frame(marco_principal)
        botones.pack(fill=tk.X, pady=10)
        ttk.Button(
            botones, 
            text="actualizar", 
            command=self.cargar_datos
        ).pack(side=tk.LEFT, padx=5)
        ttk.Button(
            botones, 
            text="Salr", 
            command=self.ventana.quit
        ).pack(side=tk.RIGHT, padx=5)



        marco_stats = ttk.LabelFrame(marco_principal, text="Estadísticas", padding=10)
        marco_stats.pack(fill=tk.X, pady=10)
        self.etiqueta_max = ttk.Label(marco_stats, text="Máximo: $0.00")
        self.etiqueta_max.pack(anchor=tk.W)
        self.etiqueta_min = ttk.Label(marco_stats, text="Mínimo: $0.00")
        self.etiqueta_min.pack(anchor=tk.W)
        self.etiqueta_prom = ttk.Label(marco_stats, text="Promedio: $0.00")
        self.etiqueta_prom.pack(anchor=tk.W)


if __name__ == "__main__":
    root = tk.Tk()
    app = AppTransacciones(root)
    root.mainloop()