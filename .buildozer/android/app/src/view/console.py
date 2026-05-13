import sys
from pathlib import Path

# Ajuste de ruta para que encuentre la carpeta core
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from src.core.logica import (
    AhorroProgramado,
    ErrorMetaInvalida,
    ErrorPlazoInvalido,
    ErrorAbonoInvalido,
    ErrorAbonoSuperaMeta,
    ErrorMesExtraFueraDeRango
)


def solicitar_entero(mensaje: str) -> int:
    """Función de una sola tarea: Pedir y validar un número."""
    while True:
        try:
            return int(input(mensaje))
        except ValueError:
            print("❌ Error: Debes ingresar un número entero válido.")


def mostrar_encabezado() -> None:
    """Función de una sola tarea: Imprimir la interfaz visual."""
    print("===================================")
    print("   CALCULADORA DE AHORRO PROGRAMADO ")
    print("===================================\n")


def main() -> None:
    mostrar_encabezado()

    try:
        meta = solicitar_entero("Ingrese la meta de ahorro ($): ")
        plazo = solicitar_entero("Ingrese el plazo en meses: ")
        abono_extra = solicitar_entero("Ingrese el abono extra (0 si no hay): ")
        mes_abono_extra = solicitar_entero("Ingrese el mes del abono extra (0 si no hay): ")

        ahorro = AhorroProgramado(
            meta=meta,
            plazo=plazo,
            abono_extra=abono_extra,
            mes_abono_extra=mes_abono_extra
        )

        cuota_mensual = ahorro.calcular_cuota_mensual()

        print("\n✅ Cálculo exitoso")
        print(f"Debes ahorrar mensualmente: ${cuota_mensual:,.2f}")


    except (ErrorMetaInvalida, ErrorPlazoInvalido, ErrorAbonoInvalido, 
            ErrorAbonoSuperaMeta, ErrorMesExtraFueraDeRango) as error_validacion:
        print(f"\n❌ {error_validacion}")

    except Exception as error_inesperado:
        print(f"\n❌ Error crítico inesperado: {error_inesperado}")


if __name__ == "__main__":
    main()