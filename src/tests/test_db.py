import sys
import os
import unittest
import psycopg2

ruta_raiz = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
sys.path.append(ruta_raiz)
sys.path.append(os.path.join(ruta_raiz, 'src'))

import src.secret_config as secret_config
from src.model.usuario import Usuario
from src.controller.usuario_controller import UsuarioController

class TestUsuarioCompleto(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        try:
            # Añadimos connect_timeout para detectar bloqueos de Red/Firewall
            cls.connection = psycopg2.connect(
                host=secret_config.PG_HOST,
                database=secret_config.PG_DATABASE,
                user=secret_config.PG_USER,
                password=secret_config.PG_PASSWORD.strip(),
                port=secret_config.PG_PORT,
                connect_timeout=5 
            )
            cls.connection.autocommit = True
        except Exception as e:
            print(f"\n[ERROR CRITICO]: No se pudo conectar a Render. Verifica si tu IP esta habilitada en el dashboard. \nDetalle: {e}")
            sys.exit(1)

    def setUp(self):
        self.cursor = self.connection.cursor()
        self.cursor.execute("TRUNCATE TABLE usuarios CASCADE")

    def tearDown(self):
        self.cursor.close()

    @classmethod
    def tearDownClass(cls):
        if hasattr(cls, 'connection'):
            cls.connection.close()

    # --- 9 PRUEBAS ---
    def test_insertar_basico(self):
        u = Usuario(id_usuario=1, nombre="Luisa", email="luisa@test.com")
        UsuarioController.insertar(u)
        self.assertIsNotNone(UsuarioController.buscar(1))

    def test_insertar_con_acentos(self):
        u = Usuario(id_usuario=2, nombre="José Jaramillo", email="jose@test.com")
        UsuarioController.insertar(u)
        self.assertEqual(UsuarioController.buscar(2).nombre, "José Jaramillo")

    def test_insertar_nombre_largo(self):
        u = Usuario(id_usuario=3, nombre="A"*50, email="largo@test.com")
        UsuarioController.insertar(u)
        self.assertEqual(len(UsuarioController.buscar(3).nombre), 50)

    def test_buscar_existente(self):
        UsuarioController.insertar(Usuario(id_usuario=10, nombre="Test", email="t@t.com"))
        self.assertIsNotNone(UsuarioController.buscar(10))

    def test_buscar_no_existente(self):
        self.assertIsNone(UsuarioController.buscar(999))

    def test_buscar_datos_correctos(self):
        u = Usuario(id_usuario=20, nombre="Verificar", email="v@v.com")
        UsuarioController.insertar(u)
        buscado = UsuarioController.buscar(20)
        self.assertEqual(buscado.email, "v@v.com")

    def test_modificar_nombre(self):
        u = Usuario(id_usuario=100, nombre="Original", email="o@o.com")
        UsuarioController.insertar(u)
        u.nombre = "Cambiado"
        UsuarioController.actualizar(u)
        self.assertEqual(UsuarioController.buscar(100).nombre, "Cambiado")

    def test_modificar_email(self):
        u = Usuario(id_usuario=101, nombre="User", email="viejo@test.com")
        UsuarioController.insertar(u)
        u.email = "nuevo@test.com"
        UsuarioController.actualizar(u)
        self.assertEqual(UsuarioController.buscar(101).email, "nuevo@test.com")

    def test_modificar_completo(self):
        u = Usuario(id_usuario=102, nombre="Nombre1", email="email1@t.com")
        UsuarioController.insertar(u)
        u.nombre, u.email = "Nombre2", "email2@t.com"
        UsuarioController.actualizar(u)
        buscado = UsuarioController.buscar(102)
        self.assertEqual(buscado.nombre, "Nombre2")
        self.assertEqual(buscado.email, "email2@t.com")

if __name__ == '__main__':
    unittest.main()