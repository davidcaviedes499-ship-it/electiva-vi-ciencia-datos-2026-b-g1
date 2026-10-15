# Resultados de la semana 7

Generado por `queries.py`. Las consultas Q1 y Q3 se verificaron contra su equivalente en pandas con `assert_frame_equal`.

## Q1

Filtra con `WHERE` las visitas con batería baja. Sirve para priorizar revisión del sistema de carga.

```sql
-- Pregunta: ¿qué sesiones registraron la batería por debajo de 12 V?
-- (una batería sana en reposo suele estar cerca de 12,6 V; por debajo de 12 V
-- hay descarga o falla de carga y conviene revisarla)
SELECT session_id, fecha, placa, battery_v
FROM sesion_diagnostico
WHERE battery_v < 12.0
ORDER BY battery_v ASC, session_id;
```

Filas devueltas: 18

| session_id | fecha | placa | battery_v |
|---|---|---|---|
| S0077 | 2026-05-17 | PIT-987 | 11.34 |
| S0150 | 2026-08-26 | NEI-789 | 11.48 |
| S0187 | 2026-03-25 | ABC-111 | 11.5 |
| S0096 | 2026-04-15 | TLM-321 | 11.54 |
| S0120 | 2026-02-28 | HUB-456 | 11.73 |
| S0113 | 2026-03-14 | XYZ-222 | 11.84 |
| S0189 | 2026-05-01 | HUA-123 | 11.87 |
| S0169 | 2026-09-07 | NEI-789 | 11.88 |
| S0021 | 2026-07-28 | XYZ-222 | 11.89 |
| S0095 | 2026-03-24 | QRS-444 | 11.89 |
| S0185 | 2026-09-05 | HUA-123 | 11.89 |
| S0144 | 2026-01-26 | GAR-654 | 11.94 |
| S0107 | 2026-06-04 | TLM-321 | 11.95 |
| S0015 | 2026-09-09 | LMN-333 | 11.97 |
| S0136 | 2026-03-14 | TLM-321 | 11.97 |
| S0058 | 2026-07-24 | HUB-456 | 11.98 |
| S0165 | 2026-05-20 | NEI-789 | 11.98 |
| S0178 | 2026-03-09 | XYZ-222 | 11.99 |

## Q2

Une 5 tablas con `JOIN` para mostrar, en lugar de llaves, el vehículo, el técnico y la descripción de la falla.

```sql
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
```

Filas devueltas: 10

| session_id | fecha | placa | vehiculo | tecnico | dtc_code | falla | repair_cost_cop |
|---|---|---|---|---|---|---|---|
| S0015 | 2026-09-09 | LMN-333 | Suzuki Swift | Marta Soto | P0299 | Turbo/supercargador: presión de sobrealimentación baja | 900000 |
| S0017 | 2026-01-03 | HUA-123 | Chevrolet Spark | Marta Soto | P0299 | Turbo/supercargador: presión de sobrealimentación baja | 900000 |
| S0018 | 2026-07-16 | TLM-321 | Toyota Hilux | Carlos Ruiz | P0562 | Voltaje del sistema bajo | 900000 |
| S0028 | 2026-01-09 | LMN-333 | Suzuki Swift | Ana Gomez | P0171 | Sistema demasiado pobre (mezcla pobre), banco 1 | 900000 |
| S0030 | 2026-05-02 | ABC-111 | Hyundai Tucson | Carlos Ruiz | P0299 | Turbo/supercargador: presión de sobrealimentación baja | 900000 |
| S0036 | 2026-06-03 | PIT-987 | Nissan Frontier | Luis Perez | P0171 | Sistema demasiado pobre (mezcla pobre), banco 1 | 900000 |
| S0039 | 2026-03-26 | LMN-333 | Suzuki Swift | Ana Gomez | P0171 | Sistema demasiado pobre (mezcla pobre), banco 1 | 900000 |
| S0045 | 2026-07-14 | TLM-321 | Toyota Hilux | Marta Soto | P0300 | Fallo de encendido aleatorio/múltiple detectado | 900000 |
| S0049 | 2026-07-25 | PIT-987 | Nissan Frontier | Carlos Ruiz | P0101 | Circuito del sensor de flujo de aire (MAF): rango/desempeño | 900000 |
| S0055 | 2026-09-24 | ABC-111 | Hyundai Tucson | Luis Perez | P0299 | Turbo/supercargador: presión de sobrealimentación baja | 900000 |

## Q3

Agrupa con `GROUP BY` por código de falla para comparar frecuencia y costo promedio.

```sql
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
```

Filas devueltas: 7

| dtc_code | sesiones | costo_promedio_cop | costo_total_cop |
|---|---|---|---|
| P0300 | 29 | 376897.0 | 10930000 |
| P0171 | 37 | 374054.0 | 13840000 |
| P0299 | 42 | 300238.0 | 12610000 |
| P0420 | 33 | 297879.0 | 9830000 |
| P0118 | 37 | 296216.0 | 10960000 |
| P0562 | 34 | 289706.0 | 9850000 |
| P0101 | 28 | 256786.0 | 7190000 |
