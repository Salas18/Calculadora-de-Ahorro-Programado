class Ahorro:
    def __init__(self, id_registro, concepto, monto):
        self.id_registro = id_registro
        self.concepto = concepto
        self.monto = float(monto) # Lo convertimos a decimal de una vez

    def is_equal(self, otro_ahorro):
        """Este método es clave para que tus tests pasen después"""
        assert self.id_registro == otro_ahorro.id_registro
        assert self.concepto == otro_ahorro.concepto
        assert self.monto == otro_ahorro.monto
        return True