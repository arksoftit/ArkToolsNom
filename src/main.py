import os
import tkinter as tk
from tkinter import ttk, messagebox

from dbconnection import DBConnectionManager
from dialog_conexiones import DialogConexiones
from system_info import (
    APP_DATE,
    APP_DEVELOPER,
    get_app_version,
    get_current_user,
    get_date_audit,
    get_machine_name,
)

CONFIG_PATH = os.path.join(os.path.dirname(__file__), "..", "config", "conexiones.json")


class AppArkToolsNom(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("ArkToolsNom")
        self._center_window(900, 550)
        self.manager = DBConnectionManager(CONFIG_PATH)
        self.protocol("WM_DELETE_WINDOW", self._salir)

        barra = tk.Menu(self)

        menu_conexiones = tk.Menu(barra, tearoff=0)
        menu_conexiones.add_command(label="Conexión Local", command=self._abrir_dialogo_local)
        barra.add_cascade(label="Conexiones", menu=menu_conexiones)

        menu_transacciones = tk.Menu(barra, tearoff=0)
        menu_transacciones.add_command(label="Nóminas", command=lambda: self._modulo_pendiente("Nóminas"))
        menu_transacciones.add_command(label="Vacaciones", command=lambda: self._modulo_pendiente("Vacaciones"))
        menu_transacciones.add_command(label="Acumulados", command=lambda: self._modulo_pendiente("Acumulados"))
        barra.add_cascade(label="Transacciones", menu=menu_transacciones)

        menu_mantenimiento = tk.Menu(barra, tearoff=0)
        menu_mantenimiento.add_command(label="Respaldos", command=lambda: self._modulo_pendiente("Respaldos"))
        menu_mantenimiento.add_command(label="Mantenimiento", command=lambda: self._modulo_pendiente("Mantenimiento"))
        barra.add_cascade(label="Mantenimiento", menu=menu_mantenimiento)

        menu_ayuda = tk.Menu(barra, tearoff=0)
        menu_ayuda.add_command(label="Acerca de...", command=self.mostrar_acerca)
        barra.add_cascade(label="Ayuda", menu=menu_ayuda)

        menu_salida = tk.Menu(barra, tearoff=0)
        menu_salida.add_command(label="Cerrar Aplicación", command=self._confirmar_salida)
        barra.add_cascade(label="Salir", menu=menu_salida)

        self.config(menu=barra)

        self._create_status_bar()
        self._refrescar_estado_conexion()

    def _center_window(self, width, height):
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)
        self.geometry(f"{width}x{height}+{x}+{y}")

    def _abrir_dialogo_local(self):
        DialogConexiones(self, manager=self.manager)
        self._refrescar_estado_conexion()

    def _modulo_pendiente(self, nombre):
        messagebox.showinfo("En construcción", f"Módulo: {nombre}", parent=self)

    def _create_status_bar(self):
        self.status_bar = ttk.Frame(self)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        self.status_var = tk.StringVar()
        self.status_var.set("Iniciando...")
        self.status_label = ttk.Label(
            self.status_bar,
            textvariable=self.status_var,
            relief=tk.SUNKEN,
            anchor=tk.CENTER,
            padding=(5, 2),
        )
        self.status_label.pack(fill=tk.X)

    def _refrescar_estado_conexion(self):
        activa = self.manager.get_active_connection()
        estado = activa.get("dsn", "Desconectado") if activa else "Desconectado"
        self._componer_barra_estado(estado)

    def _componer_barra_estado(self, estado_conexion):
        try:
            fecha = get_date_audit()
            user = get_current_user()
            equipo = get_machine_name()
            version = get_app_version()
            info_sesion = (
                f" SESIÓN ACTIVA | Usuario: {user} | "
                f"Equipo: {equipo} | Fecha: {fecha} | Versión: {version} | "
                f"Conexión: {estado_conexion}"
            )
            self.status_var.set(info_sesion)
        except Exception as e:
            self.status_var.set(f"Error al actualizar barra de estado: {e}")

    def mostrar_acerca(self):
        info_acerca = (
            f"ArkToolsNom\n"
            f"Versión: {get_app_version()}\n"
            f"Desarrollador: {APP_DEVELOPER}\n"
            f"Fecha: {APP_DATE}\n\n"
            f"Usuario actual: {get_current_user()}\n"
            f"Equipo: {get_machine_name()}\n"
            f"Fecha de auditoría: {get_date_audit()}"
        )
        messagebox.showinfo("Acerca de ArkToolsNom", info_acerca)

    def _confirmar_salida(self):
        if messagebox.askyesno("Salir", "¿Desea cerrar la aplicación?"):
            self._salir()

    def _salir(self):
        self.manager.disconnect()
        self.destroy()


if __name__ == "__main__":
    app = AppArkToolsNom()
    app.mainloop()