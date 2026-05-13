import psycopg2
import secret_config 

class AhorroController:
    def obtener_cursor(self):
        """Abre la línea telefónica con Render"""
        connection = psycopg2.connect(
            database=secret_config.PG_DATABASE,
            user=secret_config.PG_USER,
            password=secret_config.PG_PASSWORD,
            host=secret_config.PG_HOST,
            port=secret_config.PG_PORT,
            sslmode='require' 
        )
        return connection, connection.cursor()

    def crear_tabla_fixture(self):
        """Crea la tabla si no existe (Punto clave de la rúbrica)"""
        conn, cursor = self.obtener_cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS ahorros (
                id_registro VARCHAR(50) PRIMARY KEY,
                concepto VARCHAR(100),
                monto FLOAT
            )
        """)
        conn.commit() 
        conn.close() 

    def insertar_ahorro(self, ahorro):
        """Manda un objeto Ahorro a la base de datos"""
        conn, cursor = self.obtener_cursor()
        cursor.execute(
            "INSERT INTO ahorros (id_registro, concepto, monto) VALUES (%s, %s, %s)",
            (ahorro.id_registro, ahorro.concepto, ahorro.monto)
        )
        conn.commit()
        conn.close()

    def buscar_ahorro(self, id_registro):
        """Busca un registro por su ID"""
        conn, cursor = self.obtener_cursor()
        cursor.execute("SELECT * FROM ahorros WHERE id_registro = %s", (id_registro,))
        fila = cursor.fetchone()
        conn.close()
        if fila:
            from Model import Ahorro
            return Ahorro(fila[0], fila[1], fila[2])
        return None

    def modificar_ahorro(self, ahorro):
        """Actualiza el concepto y monto de un ID existente"""
        conn, cursor = self.obtener_cursor()
        cursor.execute(
            "UPDATE ahorros SET concepto = %s, monto = %s WHERE id_registro = %s",
            (ahorro.concepto, ahorro.monto, ahorro.id_registro)
        )
        conn.commit()
        conn.close()
    
    def vaciar_tabla_fixture(self):
        conn, cursor = self.obtener_cursor()
        cursor.execute("DELETE FROM ahorros") # Borra todos los registros
        conn.commit()
        conn.close()