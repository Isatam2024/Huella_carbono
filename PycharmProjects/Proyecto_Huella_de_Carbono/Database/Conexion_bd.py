import mysql.connector
from mysql.connector import Error
from config import DB_CONFIG, TABLE_NAME, COLUMNS

class DatabaseConector:
    def __init__(self):
        try:
            self.connection = mysql.connector.connect(**DB_CONFIG)
            if self.connection.is_connected():
                self.cursor = self.connection.cursor()
                print("Conectado a la base de datos MySQL")
                self.create_table()
        except Error as e:
            print(f"Error al conectarse a MySQL: {e}")
            raise
    def create_table(self):
        columns = ", ".join([f"{name} {data_type}" for name, data_type in COLUMNS])
        create_table_query = f"""
        CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
            {columns}
        )
        """
        try:
            self.cursor.execute(create_table_query)
            self.connection.commit()
            print(f"Table {TABLE_NAME} created successfully")
        except Error as e:
            print(f"Error al crear la tabla: {e}")
            raise

    def insert_emission(self,ID,Nombre,Unidad_medida):
        insert_query = f"""
        INSERT INTO {TABLE_NAME} (ID, Nombre, Unidad_medida)
        VALUES (%s, %s, %s)
        """
        try:
            self.cursor.execute(insert_query, (ID, Nombre, Unidad_medida))
            self.connection.commit()
            print("Fuente insertada exitosamente")
        except Error as e:
            print(f"Error al insertar fuente: {e}")
            raise

    def get_all_emissions(self):
        select_query = f"SELECT * FROM {TABLE_NAME}"
        try:
            self.cursor.execute(select_query)
            return self.cursor.fetchall()
        except Error as e:
            print(f"Error al recuperar emisiones: {e}")
            raise
    def create_user(self, nombre, apellido, usuario, contrasena):
        try:
            cursor = self.connection.cursor()
            cursor.execute("SELECT * FROM usuarios WHERE usuario = %s", (usuario,))
            if cursor.fetchone():
                print("Error: El nombre de usuario ya existe.")
                return

            from Utils.hashing import hash_password
            contrasena_hasheada = hash_password(contrasena)

            query = """INSERT INTO usuarios (nombre, apellido, usuario, contrasena) 
                       VALUES (%s, %s, %s, %s)"""
            valores = (nombre, apellido, usuario, contrasena_hasheada)
            cursor.execute(query, valores)
            self.connection.commit()
            print("Usuario creado exitosamente")
        except Error as e:
            print(f"Error al crear usuario: {e}")

    def get_users(self):
        try:
            cursor = self.connection.cursor()
            cursor.execute("SELECT id, nombre, apellido, usuario FROM usuarios")
            return cursor.fetchall()
        except Error as e:
            print(f"Error al obtener usuarios: {e}")
            return []

    def validate_user(self, usuario, contrasena):
        try:
            cursor = self.connection.cursor()
            cursor.execute("SELECT nombre, apellido, contrasena FROM usuarios WHERE usuario = %s", (usuario,))
            resultado = cursor.fetchone()
            return resultado
        except Error as e:
            print(f"Error al validar usuario: {e}")
            return None

    def close(self):
        if self.connection.is_connected():
            self.cursor.close()
            self.connection.close()
            print("La conexión MySQL está cerrada")
