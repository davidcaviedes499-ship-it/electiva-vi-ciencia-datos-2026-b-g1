-- Semana 7 - Consultas SQL sobre el modelo del taller de diagnóstico
-- Autor: Juan David Caviedes Cortes (davidcaviedes499-ship-it)
-- Base: SQLite, creada con 06-week/build_db.py a partir de diagnostics_clean.csv

-- [Q1] WHERE ---------------------------------------------------------------
-- Pregunta: ¿qué sesiones registraron la batería por debajo de 12 V?
-- (una batería sana en reposo suele estar cerca de 12,6 V; por debajo de 12 V
-- hay descarga o falla de carga y conviene revisarla)
SELECT session_id, fecha, placa, battery_v
FROM sesion_diagnostico
WHERE battery_v < 12.0
ORDER BY battery_v ASC, session_id;

-- [Q2] JOIN ----------------------------------------------------------------
-- Pregunta: ¿cuáles fueron las 10 reparaciones más costosas y a qué vehículo,
-- técnico y falla corresponden? (desempate por session_id)
SELECT s.session_id,
       s.fecha,
       v.placa,
       v.marca || ' ' || v.modelo AS vehiculo,
       t.nombre                   AS tecnico,
       c.dtc_code,
       c.descripcion              AS falla,
       s.repair_cost_cop
FROM sesion_diagnostico AS s
JOIN vehiculo   AS v ON v.placa      = s.placa
JOIN tecnico    AS t ON t.tecnico_id = s.tecnico_id
JOIN sesion_dtc AS d ON d.session_id = s.session_id
JOIN codigo_dtc AS c ON c.dtc_code   = d.dtc_code
ORDER BY s.repair_cost_cop DESC, s.session_id
LIMIT 10;

-- [Q3] GROUP BY ------------------------------------------------------------
-- Pregunta: ¿qué código de falla genera más visitas y cuál cuesta más en
-- promedio reparar?
SELECT d.dtc_code,
       COUNT(*)                            AS sesiones,
       ROUND(AVG(s.repair_cost_cop), 0)    AS costo_promedio_cop,
       SUM(s.repair_cost_cop)              AS costo_total_cop
FROM sesion_diagnostico AS s
JOIN sesion_dtc AS d ON d.session_id = s.session_id
GROUP BY d.dtc_code
ORDER BY costo_promedio_cop DESC, d.dtc_code;
