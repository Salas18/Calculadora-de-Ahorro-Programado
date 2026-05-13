import unittest
import sys
import psycopg2
import secret_config
from pathlib import Path

# Configuración de rutas para encontrar la carpeta src
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.model.usuario import Usuario
from src.controller.usuario_controller import UsuarioController

class TestUsuarioCompleto(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Configura la conexión una sola vez para todos los tests"""
        try:
            cls.connection = psycopg2.connect(
                host=secret_config.PG_HOST,
                database=secret_config.PG_DATABASE,
                user=secret_config.PG_USER,
                password=secret_config.PG_PASSWORD.strip(),
                port=secret_config.PG_PORT
            )
            cls.connection.autocommit = True
        except Exception as e:
            print(f"\n[ERROR DE CONEXION]: {e}")
            sys.exit(1)

    def setUp(self):
        """Limpia la tabla usuarios y sus dependencias antes de cada test"""
        self.cursor = self.connection.cursor()
        # CASCADE permite borrar aunque existan llaves foraneas en metas_ahorro
        self.cursor.execute("TRUNCATE TABLE usuarios CASCADE")

    def tearDown(self):
        self.cursor.close()

    @classmethod
    def tearDownClass(cls):
        if hasattr(cls, 'connection'):
            cls.connection.close()

    # --- 3 CASOS DE INSERTAR ---
    def test_insertar_basico(self):
        u = Usuario(id_usuario=1, nombre="Luisa", email="luisa@test.com")
        UsuarioController.insertar(u)
        self.assertIsNotNone(UsuarioController.buscar(1))

    def test_insertar_con_acentos(self):
        u = Usuario(id_usuario=2, nombre="Jose Jaramillo", email="jose@test.com")
        UsuarioController.insertar(u)
        self.assertEqual(UsuarioController.buscar(2).nombre, "Jose Jaramillo")

    def test_insertar_nombre_largo(self):
        u = Usuario(id_usuario=3, nombre="A"*50, email="largo@test.com")
        UsuarioController.insertar(u)
        self.assertEqual(len(UsuarioController.buscar(3).nombre), 50)

    # --- 3 CASOS DE BUSCAR ---
    def test_buscar_existente(self):
        UsuarioController.insertar(Usuario(10, "Test", "t@t.com"))
        self.assertIsNotNone(UsuarioController.buscar(10))

    def test_buscar_no_existente(self):
        self.assertIsNone(UsuarioController.buscar(999))

    def test_buscar_datos_correctos(self):
        u = Usuario(20, "Verificar", "v@v.com")
        UsuarioController.insertar(u)
        buscado = UsuarioController.buscar(20)
        self.assertEqual(buscado.email, "v@v.com")

    # --- 3 CASOS DE MODIFICAR ---
    def test_modificar_nombre(self):
        u = Usuario(100, "Original", "o@o.com")
        UsuarioController.insertar(u)
        u.nombre = "Cambiado"
        UsuarioController.actualizar(u)
        self.assertEqual(UsuarioController.buscar(100).nombre, "Cambiado")

    def test_modificar_email(self):
        u = Usuario(101, "User", "viejo@test.com")
        UsuarioController.insertar(u)
        u.email = "nuevo@test.com"
        UsuarioController.actualizar(u)
        self.assertEqual(UsuarioController.buscar(101).email, "nuevo@test.com")

    def test_modificar_completo(self):
        u = Usuario(102, "Nombre1", "email1@t.com")
        UsuarioController.insertar(u)
        u.nombre, u.email = "Nombre2", "email2@t.com"
        UsuarioController.actualizar(u)
        buscado = UsuarioController.buscar(102)
        self.assertEqual(buscado.nombre, "Nombre2")
        self.assertEqual(buscado.email, "email2@t.com")

if __name__ == '__main__':
    unittest.main()
