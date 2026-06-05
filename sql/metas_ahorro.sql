CREATE TABLE IF NOT EXISTS metas_ahorro (
    id_meta SERIAL PRIMARY KEY,
    id_usuario INT REFERENCES usuarios(id_usuario) ON DELETE CASCADE,
    meta DECIMAL(18,2) NOT NULL,
    plazo INT NOT NULL,
    extra DECIMAL(18,2) DEFAULT 0,
    mes_extra INT DEFAULT 0,
    tasa DECIMAL(6,4) DEFAULT 0.0075,
    cuota_mensual DECIMAL(18,2),
    fecha_calculo TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);