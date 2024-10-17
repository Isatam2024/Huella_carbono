import bcrypt

def hash_password(contrasena):
    sal = bcrypt.gensalt()
    return bcrypt.hashpw(contrasena.encode('utf-8'), sal)

def check_password(contrasena, contrasena_hasheada):
    return bcrypt.checkpw(contrasena.encode('utf-8'), contrasena_hasheada.encode('utf-8'))