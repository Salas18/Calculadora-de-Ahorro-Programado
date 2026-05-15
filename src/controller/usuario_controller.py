import sys
import os

ruta_raiz = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
sys.path.append(ruta_raiz)
sys.path.append(os.path.join(ruta_raiz, 'src'))

import psycopg2
import secret_config
from src.model.usuario import Usuario

class UsuarioController:
    @staticmethod
    def obtener_conexion():
        return psycopg2.connect(
            host=secret_config.PG_HOST,
            database=secret_config.PG_DATABASE,
            user=secret_config.PG_USER,
            password=secret_config.PG_PASSWORD.strip(),
            port=secret_config.PG_PORT
        )

    @staticmethod
    def insertar(usuario):
        conn = UsuarioController.obtener_conexion()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO usuarios (id_usuario, nombre, email) VALUES (%s, %s, %s)",
            (usuario.id_usuario, usuario.nombre, usuario.email)
        )
        conn.commit()
        cursor.close()
        conn.close()

    @staticmethod
    def buscar(id_usuario):
        conn = UsuarioController.obtener_conexion()
        cursor = conn.cursor()
        cursor.execute("SELECT id_usuario, nombre, email FROM usuarios WHERE id_usuario = %s", (id_usuario,))
        row = cursor.fetchone()
        cursor.close()
        conn.close()
        if row:
            return Usuario(id_usuario=row[0], nombre=row[1], email=row[2])
        return None

    @staticmethod
    def actualizar(usuario):
        conn = UsuarioController.obtener_conexion()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE usuarios SET nombre = %s, email = %s WHERE id_usuario = %s",
            (usuario.nombre, usuario.email, usuario.id_usuario)
        )
        conn.commit()
        cursor.close()
        conn.close()
