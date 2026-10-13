import os
import tkinter as tk
from tkinter import ttk, messagebox

from dbconnection import DBConnectionManager

CONFIG_PATH = os.path.join(os.path.dirname(__file__), "..", "config", "conexiones.json")

COLUMNAS = 3


class DialogConexiones(tk.Toplevel):
    def __init__(self, parent, manager=None):
        super().__init__(parent)
        self.title("Conexión DBISAM")
        self.resizable(True, True)
        self.manager = manager or DBConnectionManager(CONFIG_PATH)
        self.resultado = None

        marco = ttk.Frame(self, padding=10)
        marco.pack(fill=tk.BOTH, expand=True)

        formulario = ttk.Frame(marco)
        formulario.pack(fill=tk.X)

        ttk.Label(formulario, text="DSN:").grid(row=0, column=0, sticky="w", pady=2)
        self.cbo_dsn = ttk.Combobox(formulario, values=self.manager.get_dsn_list(), state="readonly", width=30)
        self.cbo_dsn.grid(row=0, column=1, pady=2)

        ttk.Label(formulario, text="Usuario:").grid(row=1, column=0, sticky="w", pady=2)
        self.txt_usuario = ttk.Entry(formulario, width=32)
        self.txt_usuario.grid(row=1, column=1, pady=2)

        ttk.Label(formulario, text="Contraseña:").grid(row=2, column=0, sticky="w", pady=2)
        self.txt_password = ttk.Entry(formulario, width=32, show="*")
        self.txt_password.grid(row=2, column=1, pady=2)

        botones = ttk.Frame(marco)
        botones.pack(pady=8)
        ttk.Button(botones, text="Probar conexión", command=self._probar).grid(row=0, column=0, padx=4)
        ttk.Button(botones, text="Guardar", command=self._guardar).grid(row=0, column=1, padx=4)
        ttk.Button(botones, text="Cerrar", command=self.destroy).grid(row=0, column=2, padx=4)

        marco_tree = ttk.LabelFrame(marco, text="Tablas disponibles", padding=5)
        marco_tree.pack(fill=tk.BOTH, expand=True, pady=(5, 0))

        self.tree = ttk.Treeview(
            marco_tree,
            columns=tuple(f"c{i}" for i in range(COLUMNAS)),
            show="headings",
            height=15,
        )
        for i in range(COLUMNAS):
            self.tree.heading(f"c{i}", text="")
            self.tree.column(f"c{i}", width=200, stretch=True)
        vsb = ttk.Scrollbar(marco_tree, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=vsb.set)
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        vsb.pack(side=tk.RIGHT, fill=tk.Y)

        self._cargar_activa()

        self.update_idletasks()
        self.wait_visibility()
        x = parent.winfo_x() + (parent.winfo_width() // 2) - (self.winfo_width() // 2)
        y = parent.winfo_y() + (parent.winfo_height() // 2) - (self.winfo_height() // 2)
        self.geometry(f"+{x}+{y}")

    def _cargar_activa(self):
        activa = self.manager.get_active_connection()
        if activa:
            self.cbo_dsn.set(activa.get("dsn", ""))
            self.txt_usuario.insert(0, activa.get("usuario", ""))
            self.txt_password.insert(0, activa.get("password", ""))

    def _limpiar_tree(self):
        self.tree.delete(*self.tree.get_children())

    def _cargar_tablas(self, conn):
        self._limpiar_tree()
        cursor = conn.cursor()
        tablas = cursor.tables()
        nombres = []
        for tabla in tablas:
            nombre = tabla.table_name
            if nombre not in nombres and nombre.isidentifier():
                nombres.append(nombre)
        cursor.close()
        nombres = sorted(nombres)
        filas = (len(nombres) + COLUMNAS - 1) // COLUMNAS
        for fila in range(filas):
            valores = []
            for col in range(COLUMNAS):
                idx = fila * COLUMNAS + col
                valores.append(nombres[idx] if idx < len(nombres) else "")
            self.tree.insert("", tk.END, values=tuple(valores))

    def _probar(self):
        dsn = self.cbo_dsn.get().strip()
        usuario = self.txt_usuario.get().strip()
        password = self.txt_password.get()
        if not dsn:
            messagebox.showwarning("Atención", "Seleccione un DSN.", parent=self)
            return
        ok, msg, conn = self.manager.connect(dsn, usuario, password)
        if not ok:
            self._limpiar_tree()
            messagebox.showerror("Prueba de conexión", msg, parent=self)
            return
        try:
            self._cargar_tablas(conn)
        finally:
            conn.close()
        messagebox.showinfo("Prueba de conexión", msg, parent=self)

    def _guardar(self):
        dsn = self.cbo_dsn.get().strip()
        usuario = self.txt_usuario.get().strip()
        password = self.txt_password.get()
        if not dsn:
            messagebox.showwarning("Atención", "Seleccione un DSN.", parent=self)
            return
        self.manager.save_connection(dsn, usuario, password)
        messagebox.showinfo("Conexión guardada", "Conexión activa guardada.", parent=self)
        self.destroy()