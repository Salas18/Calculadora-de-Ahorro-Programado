import psycopg2
import sys
import os

# Forzamos las rutas para que Python no se pierda buscando los módulos
ruta_raiz = os.path.abspath(os.path.dirname(__file__))
sys.path.append(ruta_raiz)
sys.path.append(os.path.join(ruta_raiz, 'src'))

try:
    from src import secret_config
except ImportError:
    import src.secret_config as secret_config

try:
    print("Conectando directo a Render...")
    conn = psycopg2.connect(
        host=secret_config.PG_HOST,
        database=secret_config.PG_DATABASE,
        user=secret_config.PG_USER,
        password=secret_config.PG_PASSWORD,
        port=secret_config.PG_PORT
    )
    cur = conn.cursor()
    
    print("Guardando usuario y meta de prueba...")
    cur.execute("""
        INSERT INTO usuarios (id_usuario, nombre, email) 
        VALUES (1, 'Miguel Angel', 'miguel@email.com') 
        ON CONFLICT (id_usuario) DO NOTHING;
    """)
    
    cur.execute("""
        INSERT INTO metas_ahorro (id_meta, id_usuario, meta, plazo, extra, mes_extra, tasa, cuota_mensual) 
        VALUES (1, 1, 10000000.00, 12, 500000.00, 6, 0.0075, 750000.00) 
        ON CONFLICT (id_meta) DO NOTHING;
    """)
    
    conn.commit() # El seguro de vida definitivo para confirmar los cambios en la nube
    cur.close()
    conn.close()
    print("✅ ¡Datos guardados con éxito directamente en Render!")

except Exception as e:
    print(f"❌ Error al guardar datos: {e}")