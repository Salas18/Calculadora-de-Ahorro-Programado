import sys
import os

# 1. Este bloque soluciona el problema de las rutas subiendo solo DOS niveles
ruta_raiz = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
sys.path.append(ruta_raiz)
sys.path.append(os.path.join(ruta_raiz, 'src'))

from model.meta_ahorro import MetaAhorro
from controller.ahorro_controller import AhorroController

try:
    print("\n" + "="*40)
    print("BUSCADOR DE METAS DE AHORRO")
    print("="*40)
    
  
    id_buscar = input("\nIngrese el ID de la meta que desea buscar: ")
    

    meta_encontrada = AhorroController.buscar_meta(int(id_buscar))

    if meta_encontrada is None:
        print(f"\n No hay ninguna meta guardada con el ID {id_buscar}. La base de datos está vacía.")
    else:
        print("\n¡Meta Encontrada!")
        print("-" * 30)
        print(f"Meta: $ {meta_encontrada.meta:,.2f}")
        print(f"Plazo: {meta_encontrada.plazo} meses")
        print(f"Abono Extra: $ {meta_encontrada.extra:,.2f}")
        print(f"Mes del Abono: {meta_encontrada.mes_extra}")
        print(f"Cuota Mensual Fija: $ {meta_encontrada.cuota_mensual:,.2f}")
        print("-" * 30 + "\n")

except Exception as err:
    print("\nError:")
    print(str(err) + "\n")