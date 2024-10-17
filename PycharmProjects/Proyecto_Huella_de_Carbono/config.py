# Database configuration
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'huella_de_carbono_universitaria'
}

# Table configuration
TABLE_NAME = "fuentes_emisiones"
COLUMNS = [
    ("ID", "INT AUTO_INCREMENT PRIMARY KEY"),
    ("Nombre", "VARCHAR(255) NOT NULL"),
    ("Unidad_medida", "VARCHAR(255) NOT NULL")
]


