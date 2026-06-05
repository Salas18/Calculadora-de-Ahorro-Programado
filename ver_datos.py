import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

try:
    from src import secret_config 
    
    conn = psycopg2.connect(
        host=secret_config.PG_HOST,
        database=secret_config.PG_DATABASE,
        user=secret_config.PG_USER,
        password=secret_config.PG_PASSWORD,
        port=secret_config.PG_PORT
    )
    cur = conn.cursor()

    print("--- Contenido de la tabla metas_ahorro ---")
    cur.execute("SELECT id_meta, id_usuario, meta FROM metas_ahorro;")
    rows = cur.fetchall()

    for row in rows:
        print(f"Meta ID: {row[0]} | Usuario ID: {row[1]} | Valor: {row[2]}")

    cur.close()
    conn.close()

except Exception as e:
    print(f"Error al leer: {e}")