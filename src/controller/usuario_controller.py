import sys
import os

ruta_raiz = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
sys.path.append(ruta_raiz)
sys.path.append(os.path.join(ruta_raiz, 'src'))

import psycopg2
import src.secret_config as secret_config
from src.model.usuario import Usuario

class UsuarioController:
    @staticmethod
    def crear_tablas():
        import os
        
        ruta_sql = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../sql'))
        
       
        
        archivos = ['usuarios.sql', 'metas_ahorro.sql', 'historial_calculos.sql', 'inserts_ejemplo.sql']
        
        try:
            connection = psycopg2.connect(
                host=secret_config.PGHOST,
                database=secret_config.PGDATABASE,
                user=secret_config.PGUSER,
                password=secret_config.PGPASSWORD,
                port=secret_config.PGPORT
            )
            cursor = connection.cursor()
            

            for archivo in archivos:
                ruta_archivo = os.path.join(ruta_sql, archivo)
                with open(ruta_archivo, 'r', encoding='utf-8') as f:
                    sql_query = f.read()
                    cursor.execute(sql_query)
                    
            connection.commit()
            connection.close()
            print("\n✅ ¡Tablas creadas exitosamente en Render desde Python!")
            
        except Exception as e:
            print(f"\n❌ Error al crear las tablas: {e}")
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
    
    @staticmethod
    def crear_tablas():
        import os
        
        ruta_sql = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../sql'))
        
        
        archivos = ['usuarios.sql', 'metas_ahorro.sql', 'historial_calculos.sql']
        
        try:
        
            connection = psycopg2.connect(
                host=secret_config.PG_HOST,
                database=secret_config.PG_DATABASE,
                user=secret_config.PG_USER,
                password=secret_config.PG_PASSWORD,
                port=secret_config.PG_PORT
            )
            cursor = connection.cursor()
            
            
            for archivo in archivos:
                ruta_archivo = os.path.join(ruta_sql, archivo)
                with open(ruta_archivo, 'r', encoding='utf-8') as f:
                    sql_query = f.read()
                    cursor.execute(sql_query)
                    
            connection.commit()
            connection.close()
            print("\n✅ ¡Tablas creadas exitosamente en Render desde Python!")
            
        except Exception as e:
            print(f"\n❌ Error al crear las tablas: {e}")

    
