import tkinter as tk
from Database.Conexion_bd import DatabaseConector
from Utils.hashing import check_password
from PIL import Image, ImageTk  # Necesitarás Pillow para manejar imágenes

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("huella_de_carbono_universitaria")
        self.db = DatabaseConector()

        # Cargar la imagen de fondo
        self.background_image = Image.open("background.jpg")
        self.background_image = self.background_image.resize((400, 300), Image.LANCZOS)  # Ajusta el tamaño según necesites
        self.bg_image = ImageTk.PhotoImage(self.background_image)

        # Crear un label para la imagen de fondo
        self.bg_label = tk.Label(self.root, image=self.bg_image)
        self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)  # Colocar la imagen de fondo

        self.create_widgets()

        # Label para mostrar la lista de usuarios
        self.user_display_label = tk.Label(self.root, text="", justify="left", bg="white", anchor="nw", padx=5, pady=5)
        self.user_display_label.grid(row=7, column=0, columnspan=2, sticky="nw", padx=10, pady=10)

    def create_widgets(self):
        # Entradas
        tk.Label(self.root, text="Nombre:").grid(row=0, column=0, sticky="e")
        self.entry_nombre = tk.Entry(self.root)
        self.entry_nombre.grid(row=0, column=1, padx=5)

        tk.Label(self.root, text="Apellido:").grid(row=1, column=0, sticky="e")
        self.entry_apellido = tk.Entry(self.root)
        self.entry_apellido.grid(row=1, column=1, padx=5)

        tk.Label(self.root, text="Usuario:").grid(row=2, column=0, sticky="e")
        self.entry_usuario = tk.Entry(self.root)
        self.entry_usuario.grid(row=2, column=1, padx=5)

        tk.Label(self.root, text="Contraseña:").grid(row=3, column=0, sticky="e")
        self.entry_contrasena = tk.Entry(self.root, show="*")
        self.entry_contrasena.grid(row=3, column=1, padx=5)

        # Botones centrados
        self.button_crear = tk.Button(self.root, text="Crear Usuario", command=self.create_user)
        self.button_crear.grid(row=4, column=2, columnspan=2, pady=5)

        self.button_ver = tk.Button(self.root, text="Ver Usuarios", command=self.show_users)
        self.button_ver.grid(row=5, column=0, columnspan=2, pady=5)

        self.button_login = tk.Button(self.root, text="Iniciar Sesión", command=self.login)
        self.button_login.grid(row=6, column=0, columnspan=2, pady=5)

    def create_user(self):
        nombre = self.entry_nombre.get()
        apellido = self.entry_apellido.get()
        usuario = self.entry_usuario.get()
        contrasena = self.entry_contrasena.get()
        self.db.create_user(nombre, apellido, usuario, contrasena)

    def show_users(self):
        usuarios = self.db.get_users()
        if not usuarios:
            self.user_display_label.config(text="No hay usuarios registrados.")
            return

        user_list = "\n".join([f"ID: {u[0]}, Nombre: {u[1]}, Apellido: {u[2]}, Usuario: {u[3]}" for u in usuarios])
        self.user_display_label.config(text=user_list)

    def login(self):
        usuario = self.entry_usuario.get()
        contrasena = self.entry_contrasena.get()
        resultado = self.db.validate_user(usuario, contrasena)

        if resultado:
            nombre, apellido, contrasena_hasheada = resultado
            if check_password(contrasena, contrasena_hasheada):
                tk.messagebox.showinfo("Bienvenido", f"¡Bienvenido, {nombre} {apellido}!")
            else:
                tk.messagebox.showerror("Error", "Contraseña incorrecta.")
        else:
            tk.messagebox.showerror("Error", "Usuario no encontrado.")

    def run(self):
        """Iniciar la aplicación Tkinter."""
        self.root.mainloop()

    def __del__(self):
        """Cerrar la conexión a la base de datos al finalizar."""
        if hasattr(self, 'db'):
            self.db.close()


if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("400x300")  # Ajusta el tamaño de la ventana
    app = App(root)
    root.mainloop()
