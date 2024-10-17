import os
import sys
import tkinter as tk
from GUI.huella_GUI import huellaGUI
from GUI.iniciarsesion import App

# Configuración del directorio del proyecto
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, os.pardir))
sys.path.insert(0, project_root)

def main():
    root = tk.Tk()
    app = huellaGUI(root)
    app.run()  # Llama a run() de huellaGUI

def mainn():
    root = tk.Toplevel()  # Usar Toplevel para abrir una nueva ventana
    app = App(root)
    app.run()  # Llama a run() de App

if __name__ == "__main__":
    # Elige qué GUI ejecutar
    gui_to_run = "App"  # Cambia a "huellaGUI" si deseas ejecutar la otra

    if gui_to_run == "huellaGUI":
        main()
    else:
        main()  # Abre la primera GUI
        mainn()  # Luego abre la segunda ventana
