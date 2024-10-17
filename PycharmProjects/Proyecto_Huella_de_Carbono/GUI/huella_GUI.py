import tkinter as tk
from tkinter import ttk, messagebox
from Database.Conexion_bd import DatabaseConector
from Utils.utils import validate_float, validate_int, format_currency

class huellaGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Fuente de Emisión")
        self.master.geometry("600x400")  # Tamaño de la ventana
        self.master.resizable(False, False)  # No permitir cambiar tamaño

        # Intentar conectar a la base de datos
        try:
            self.db = DatabaseConector()
        except Exception as e:
            messagebox.showerror("Database Error", f"No se pudo conectar a la base de datos: {e}")
            self.master.destroy()
            return

        self.create_widgets()

    def create_widgets(self):
        # Crear un frame principal
        main_frame = ttk.Frame(self.master, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Configurar el grid
        for i in range(6):
            main_frame.grid_columnconfigure(i, weight=1)
        for i in range(8):
            main_frame.grid_rowconfigure(i, weight=1)

        # Campos de entrada
        ttk.Label(main_frame, text="ID:",font=("Helvetica",15)).grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.ID_entry = ttk.Entry(main_frame, width=30)
        self.ID_entry.grid(row=0, column=1, columnspan=2, sticky=(tk.W, tk.E), padx=5, pady=5)

        ttk.Label(main_frame, text="Nombre:",font=("Helvetica",15)).grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        self.Nombre_entry = ttk.Entry(main_frame, width=30)
        self.Nombre_entry.grid(row=1, column=1, columnspan=2, sticky=(tk.W, tk.E), padx=5, pady=5)

        ttk.Label(main_frame, text="Unidad de medida:",font=("Helvetica",15)).grid(row=2, column=0, sticky=tk.W, padx=5, pady=5)
        self.Unidad_medida_entry = ttk.Entry(main_frame, width=30)
        self.Unidad_medida_entry.grid(row=2, column=1, columnspan=2, sticky=(tk.W, tk.E), padx=5, pady=5)

        # Botones
        ttk.Button(main_frame, text="Agregar Fuente de emisión", command=self.add_emission).grid(row=5, column=0, columnspan=3, pady=20)
        ttk.Button(main_frame, text="Mostrar Fuentes de emisión", command=self.show_emissions).grid(row=6, column=0, columnspan=3, pady=10)
        ttk.Button(main_frame, text="Salir", command=self.master.destroy).grid(row=7, column=0, columnspan=3, pady=10)


    def add_emission(self):
        # Obtener valores de las entradas
        ID = self.ID_entry.get()
        Nombre = self.Nombre_entry.get()
        Unidad_medida = self.Unidad_medida_entry.get()

        if ID and Nombre and Unidad_medida:
            ID = validate_float(ID)

            if ID is not None:
                try:
                    self.db.insert_emission(ID, Nombre, Unidad_medida)
                    messagebox.showinfo("Success", "Fuente de emisión agregada exitosamente!")
                except Exception as e:
                    messagebox.showerror("Database Error", f"No se pudo agregar la fuente de emisión: {e}")
            else:
                messagebox.showerror("Error", "ID no válido!")
        else:
            messagebox.showerror("Error", "Todos los campos son obligatorios!")



    def show_emissions(self):
        # Obtener los datos desde la base de datos
        try:
            emissions = self.db.get_all_emissions()
            if emissions:
                # Crear una nueva ventana para mostrar las emisiones
                emission_window = tk.Toplevel(self.master)
                emission_window.title("Lista de Fuentes de Emisión")
                emission_window.geometry("800x400")  # Tamaño de la ventana

                # Crear un Treeview para mostrar los datos
                tree = ttk.Treeview(emission_window, columns=("ID", "Nombre", "Unidad de medida"), show="headings")
                tree.heading("ID", text="ID")
                tree.heading("Nombre", text="Nombre")
                tree.heading("Unidad de medida", text="Unidad de medida")

                # Definir el tamaño de las columnas
                tree.column("ID", width=50)
                tree.column("Nombre", width=150)
                tree.column("Unidad de medida", width=150)

                # Insertar los datos en el Treeview
                for emission in emissions:
                    tree.insert("", "end", values=emission)

                # Empaquetar el Treeview
                tree.pack(expand=True, fill='both', padx=10, pady=10)

                # Añadir una barra de desplazamiento
                scrollbar = ttk.Scrollbar(emission_window, orient="vertical", command=tree.yview)
                scrollbar.pack(side='right', fill='y')
                tree.configure(yscrollcommand=scrollbar.set)
            else:
                messagebox.showinfo("Info", "No se encontraron fuentes de emisión.")
        except Exception as e:
            messagebox.showerror("Database Error", f"No se pudieron recuperar las fuentes de emisión: {e}")

    def clear_entries(self):
        """Función para limpiar las entradas después de agregar un dato."""
        self.ID_entry.delete(0, 'end')
        self.Nombre_entry.delete(0, 'end')
        self.Unidad_medida_entry.delete(0, 'end')

    def run(self):
        """Iniciar la aplicación Tkinter."""
        self.master.mainloop()

    def __del__(self):
        """Cerrar la conexión a la base de datos al finalizar."""
        if hasattr(self, 'db'):
            self.db.close()
