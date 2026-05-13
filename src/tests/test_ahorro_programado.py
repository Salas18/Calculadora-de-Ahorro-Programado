import unittest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

# Importamos los nombres limpios que definimos en la lógica
from core.logica import (
    AhorroProgramado,
    ErrorMetaInvalida,
    ErrorPlazoInvalido,
    ErrorAbonoInvalido,
    ErrorAbonoSuperaMeta,
    ErrorMesExtraFueraDeRango
)

class TestAhorroProgramado(unittest.TestCase):

    def test_calculo_cuota_sin_abonos_a_doce_meses(self):
        ahorro = AhorroProgramado(meta=1200000, plazo=12, abono_extra=0, mes_abono_extra=0)
        self.assertAlmostEqual(ahorro.calcular_cuota_mensual(), 95941.77, places=2)

    def test_calculo_cuota_meta_alta_a_largo_plazo(self):
        ahorro = AhorroProgramado(meta=5000000, plazo=20, abono_extra=0, mes_abono_extra=0)
        self.assertAlmostEqual(ahorro.calcular_cuota_mensual(), 232653.16, places=2)

    def test_calculo_cuota_meta_baja_a_corto_plazo(self):
        ahorro = AhorroProgramado(meta=450000, plazo=3, abono_extra=0, mes_abono_extra=0)
        self.assertAlmostEqual(ahorro.calcular_cuota_mensual(), 148880.60, places=2)

    def test_calculo_cuota_con_abono_parcial(self):
        ahorro = AhorroProgramado(meta=2000000, plazo=10, abono_extra=1000000, mes_abono_extra=5)
        self.assertAlmostEqual(ahorro.calcular_cuota_mensual(), 92991.27, places=2)

    def test_calculo_cuota_con_abono_total_cubre_meta(self):
        ahorro = AhorroProgramado(meta=8000000, plazo=24, abono_extra=8000000, mes_abono_extra=12)
        self.assertAlmostEqual(ahorro.calcular_cuota_mensual(), 0.00, places=2)

    def test_calculo_cuota_micro_ahorro(self):
        ahorro = AhorroProgramado(meta=60000, plazo=2, abono_extra=0, mes_abono_extra=0)
        self.assertAlmostEqual(ahorro.calcular_cuota_mensual(), 29887.92, places=2)

    def test_falla_al_ingresar_meta_negativa(self):
        with self.assertRaises(ErrorMetaInvalida):
            ahorro = AhorroProgramado(meta=-500000, plazo=12, abono_extra=0, mes_abono_extra=0)
            ahorro.calcular_cuota_mensual()

    def test_falla_al_ingresar_meta_cero(self):
        with self.assertRaises(ErrorMetaInvalida):
            ahorro = AhorroProgramado(meta=0, plazo=6, abono_extra=0, mes_abono_extra=0)
            ahorro.calcular_cuota_mensual()

    def test_falla_al_ingresar_plazo_cero(self):
        with self.assertRaises(ErrorPlazoInvalido):
            ahorro = AhorroProgramado(meta=1000000, plazo=0, abono_extra=0, mes_abono_extra=0)
            ahorro.calcular_cuota_mensual()

    def test_falla_cuando_abono_supera_meta(self):
        with self.assertRaises(ErrorAbonoSuperaMeta):
            ahorro = AhorroProgramado(meta=1500000, plazo=12, abono_extra=2000000, mes_abono_extra=6)
            ahorro.calcular_cuota_mensual()

    def test_falla_cuando_mes_abono_supera_plazo(self):
        with self.assertRaises(ErrorMesExtraFueraDeRango):
            ahorro = AhorroProgramado(meta=1000000, plazo=12, abono_extra=500000, mes_abono_extra=15)
            ahorro.calcular_cuota_mensual()

if __name__ == '__main__':
    unittest.main(verbosity=2)