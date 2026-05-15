
CREATE TABLE IF NOT EXISTS usuarios (
    id_usuario SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    email VARCHAR(150) UNIQUE NOT NULL
);

CREATE TABLE IF NOT EXISTS metas_ahorro (
    id_meta SERIAL PRIMARY KEY,
    id_usuario INT REFERENCES usuarios(id_usuario) ON DELETE CASCADE,
    meta DECIMAL(18,2) NOT NULL,
    plazo INT NOT NULL,
    extra DECIMAL(18,2) DEFAULT 0,
    mes_extra INT DEFAULT 0,
    cuota_mensual DECIMAL(18,2)
);
os
CREATE TABLE IF NOT EXISTS historial_calculos (
    id_historial SERIAL PRIMARY KEY,
    id_usuario INT REFERENCES usuarios(id_usuario) ON DELETE CASCADE,
    meta DECIMAL(18,2),
    plazo INT,
    extra DECIMAL(18,2),
    mes_extra INT,
    cuota_mensual DECIMAL(18,2),
    fecha_calculo TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);