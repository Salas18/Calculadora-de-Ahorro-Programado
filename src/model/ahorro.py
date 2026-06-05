class Ahorro:
    def __init__(self, meta: float, plazo: int, extra: float = 0, mes_extra: int = 0):
        self.meta = meta
        self.plazo = plazo
        self.extra = extra
        self.mes_extra = mes_extra

class AhorroProgramado:
    def calcular_ahorro(self, ahorro: Ahorro) -> float:
        tasa = 0.0075 # Tasa fija del 0.75% mensual
        
        # Fórmula de anualidad para calcular la cuota mensual
        if tasa == 0:
            cuota = (ahorro.meta - ahorro.extra) / ahorro.plazo
        else:
            factor_anualidad = ((1 + tasa)**ahorro.plazo - 1) / tasa
            # Descontamos el aporte extra de la meta total
            meta_real = ahorro.meta - ahorro.extra
            cuota = meta_real / factor_anualidad
            
        return round(cuota, 2)