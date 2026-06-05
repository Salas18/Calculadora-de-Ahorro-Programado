import sys
import os

ruta_raiz = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
sys.path.append(ruta_raiz)
sys.path.append(os.path.join(ruta_raiz, 'src'))

from model.ahorro import Ahorro
from controller.ahorro_controller import AhorroController


meta_ahorro = Ahorro(meta=0.0, plazo=0, extra=0.0, mes_extra=0)

print("Por favor ingrese los datos para su meta de ahorro")


meta_ahorro.id_usuario = int(input("Ingrese el ID del usuario: "))
meta_ahorro.meta = float(input("Ingrese la meta de ahorro ($): "))
meta_ahorro.plazo = int(input("Ingrese el plazo en meses: "))
meta_ahorro.extra = float(input("Ingrese el abono extra (0 si no hay): "))
meta_ahorro.mes_extra = int(input("Ingrese el mes del abono extra (0 si no hay): "))


AhorroController.insertar_ahorro(meta_ahorro)

print("¡Meta de ahorro insertada exitosamente!")