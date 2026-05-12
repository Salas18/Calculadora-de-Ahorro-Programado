class ErrorMetaInvalida(Exception):
    def __init__(self, meta):
        super().__init__(f"La meta ingresada ({meta}) debe ser mayor a 0.")

class ErrorPlazoInvalido(Exception):
    def __init__(self, plazo):
        super().__init__(f"El plazo ingresado ({plazo}) debe ser mayor a 0 meses.")

class ErrorAbonoInvalido(Exception):
    def __init__(self, abono):
        super().__init__(f"El abono extra ({abono}) no puede ser un valor negativo.")

class ErrorAbonoSuperaMeta(Exception):
    def __init__(self, abono, meta):
        super().__init__(f"El abono extra ({abono}) supera la meta total ({meta}).")

class ErrorMesExtraFueraDeRango(Exception):
    def __init__(self, mes, plazo):
        super().__init__(f"El mes del abono ({mes}) debe estar entre 1 y el plazo máximo ({plazo}).")


class AhorroProgramado:

    TASA_INTERES_MENSUAL = 0.0075

    def __init__(self, meta: float, plazo: int, abono_extra: float = 0.0, mes_abono_extra: int = 0):
        self.meta = meta
        self.plazo = plazo
        self.abono_extra = abono_extra
        self.mes_abono_extra = mes_abono_extra

    def _validar_datos(self) -> None:
        """Función privada con Responsabilidad Única: Solo validar datos."""
        if self.meta <= 0:
            raise ErrorMetaInvalida(self.meta)
        if self.plazo <= 0:
            raise ErrorPlazoInvalido(self.plazo)
        if self.abono_extra < 0:
            raise ErrorAbonoInvalido(self.abono_extra)
        if self.abono_extra > self.meta:
            raise ErrorAbonoSuperaMeta(self.abono_extra, self.meta)
        if self.mes_abono_extra > self.plazo:
            raise ErrorMesExtraFueraDeRango(self.mes_abono_extra, self.plazo)

    def calcular_cuota_mensual(self) -> float:
        """Función con Responsabilidad Única: Solo aplicar matemáticas."""
        self._validar_datos()

        if self.mes_abono_extra > 0:
            periodos_restantes = self.plazo - self.mes_abono_extra
            valor_futuro_abono = self.abono_extra * ((1 + self.TASA_INTERES_MENSUAL) ** periodos_restantes)
        else:
            valor_futuro_abono = 0.0

        factor_acumulacion = ((1 + self.TASA_INTERES_MENSUAL) ** self.plazo - 1) / self.TASA_INTERES_MENSUAL
        cuota = (self.meta - valor_futuro_abono) / factor_acumulacion

        return max(0.0, round(cuota, 2))