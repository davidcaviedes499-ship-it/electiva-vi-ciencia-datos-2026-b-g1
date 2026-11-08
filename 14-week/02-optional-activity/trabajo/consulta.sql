-- SQLite: consulta de resumen mensual, leyendo solo columnas necesarias.
-- El índice por fecha facilita búsquedas por intervalos temporales.
CREATE INDEX IF NOT EXISTS idx_produccion_fecha ON produccion(fecha);

SELECT substr(fecha, 1, 7) AS mes,
       ROUND(AVG(produccion_mpcd), 2) AS promedio_diario_mpcd,
       ROUND(SUM(produccion_mpcd), 2) AS suma_registros_diarios
FROM produccion
WHERE fecha >= '2025-01-01' AND fecha < '2026-01-01'
GROUP BY substr(fecha, 1, 7)
ORDER BY mes;
-- Nota: con solo 365 filas no se demuestra una mejora de velocidad.
-- El índice beneficia potencialmente filtros de fechas en tablas grandes;
-- GROUP BY sigue necesitando agrupar los registros filtrados.
