import sys
import os

ruta_raiz = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
sys.path.append(ruta_raiz)
sys.path.append(os.path.join(ruta_raiz, 'src'))

from controller.ahorro_controller import AhorroController

try:
    id_buscar = input("Ingrese el ID de la meta de ahorro que desea buscar: ")
    
    
    ahorro_buscado = AhorroController.buscar_ahorro(id_buscar)
    
    
    print(f"Meta encontrada para Usuario ID {ahorro_buscado.id_usuario}:")
    print(f"- Meta Total: ${ahorro_buscado.meta}")
    print(f"- Plazo: {ahorro_buscado.plazo} meses")
    print(f"- Cuota Mensual a pagar: ${ahorro_buscado.cuota_mensual}")
    
except Exception as err:
    print("Error : ")
    print(str(err))