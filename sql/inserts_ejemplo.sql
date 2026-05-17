INSERT INTO usuarios (nombre, email) VALUES
('Miguel Angel', 'miguel.angel@email.com'),
('Jose Angel', 'jose.angel@email.com');

-- Inserción de metas de ahorro con valores diferentes
INSERT INTO metas_ahorro (id_usuario, meta, plazo, extra, mes_extra, cuota_mensual) VALUES
(1, 2500000, 12, 100000, 6, 195000.50),
(2, 8000000, 24, 500000, 12, 310200.75);

-- Inserción del historial con los mismos valores para el registro
INSERT INTO historial_calculos (id_usuario, meta, plazo, extra, mes_extra, cuota_mensual) VALUES
(1, 2500000, 12, 100000, 6, 195000.50),
(2, 8000000, 24, 500000, 12, 310200.75);