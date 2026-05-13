import unittest
from Model import Ahorro
from Controller import AhorroController

class TestAhorroDB(unittest.TestCase):
    def setUp(self):
        """Se ejecuta antes de cada test"""
        self.ctrl = AhorroController()
        self.ctrl.crear_tabla_fixture()

    def test_insertar_ahorros(self):
        # Caso 1, 2 y 3: Insertar registros diferentes
        for i in range(1, 4):
            nuevo = Ahorro(f"ID-{i}", f"Ahorro {i}", 1000 * i)
            self.ctrl.insertar_ahorro(nuevo)
            buscado = self.ctrl.buscar_ahorro(f"ID-{i}")
            self.assertTrue(nuevo.is_equal(buscado))

    def test_buscar_no_existente(self):
        """Caso de error: Buscar algo que no está"""
        resultado = self.ctrl.buscar_ahorro("ID-QUE-NO-EXISTE")
        self.assertIsNone(resultado)

    def test_modificar_ahorro(self):
        """Caso: Cambiar el monto de un registro existente"""
        original = Ahorro("MOD-1", "Cena", 50000)
        self.ctrl.insertar_ahorro(original)
        
        # Modificación
        actualizado = Ahorro("MOD-1", "Cena Elegante", 80000)
        self.ctrl.modificar_ahorro(actualizado)
        
        buscado = self.ctrl.buscar_ahorro("MOD-1")
        self.assertTrue(actualizado.is_equal(buscado))

    def setUp(self):
        self.ctrl = AhorroController()
        self.ctrl.crear_tabla_fixture()
        self.ctrl.vaciar_tabla_fixture() 

    

if __name__ == "__main__":
    unittest.main()