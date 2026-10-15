# Semana 7 · Consultas SQL y pandas

```python
FULL_NAME   = "Juan David Caviedes Cortes"
GITHUB_USER = "davidcaviedes499-ship-it"
```

Asignatura: Ciencia de Datos · Ingeniería Industrial · CORHUILA · 2026-B · Corte 2.
Guía de la actividad: *Semana 7 · Consultas SQL y pandas* (formativa, opcional).

## Qué se entrega

| Archivo | Contenido |
|---|---|
| [`queries.sql`](queries.sql) | 3 consultas SQL: `WHERE`, `JOIN` y `GROUP BY`, cada una con su pregunta |
| [`queries.py`](queries.py) | Ejecuta las consultas sobre SQLite y reproduce en pandas el `GROUP BY` (y también el `WHERE`) |
| [`resultados.md`](resultados.md) | Salida completa de las tres consultas |

Las consultas se ejecutan sobre el modelo de la [semana 6](../06-week/README.md), con los 240 registros del CSV limpio.

```bash
python queries.py    # necesita la carpeta 06-week al lado de esta
```

El script **falla si el resultado de SQL y el de pandas no coinciden** (`assert_frame_equal`); con los datos entregados pasa sin diferencias.

## Qué responde cada consulta

### Q1 · `WHERE` — baterías por debajo de 12 V

```sql
SELECT session_id, fecha, placa, battery_v
FROM sesion_diagnostico
WHERE battery_v < 12.0
ORDER BY battery_v ASC, session_id;
```

Devuelve las visitas en las que el voltaje de la batería quedó bajo 12 V, que es una señal de descarga o falla de carga y por eso conviene priorizarlas. Resultado: **18 sesiones** de 240 (7,5 %). El listado completo está en `resultados.md`.

### Q2 · `JOIN` — las 10 reparaciones más costosas

```sql
SELECT s.session_id, s.fecha, v.placa,
       v.marca || ' ' || v.modelo AS vehiculo,
       t.nombre AS tecnico, c.dtc_code, c.descripcion AS falla,
       s.repair_cost_cop
FROM sesion_diagnostico AS s
JOIN vehiculo   AS v ON v.placa      = s.placa
JOIN tecnico    AS t ON t.tecnico_id = s.tecnico_id
JOIN sesion_dtc AS d ON d.session_id = s.session_id
JOIN codigo_dtc AS c ON c.dtc_code   = d.dtc_code
ORDER BY s.repair_cost_cop DESC, s.session_id
LIMIT 10;
```

Une cinco tablas para que el resultado muestre vehículo, técnico y descripción de la falla en lugar de llaves numéricas; es justo lo que la normalización de la semana 6 obliga a hacer con `JOIN`.

> **Ojo con este resultado:** las 10 filas cuestan exactamente 900 000 COP. El costo toma pocos valores (0, 80 000, 150 000, 320 000, 450 000 y 900 000), así que hay muchos empates en el tope y el desempate por `session_id` es solo un criterio para que la salida sea reproducible, no un ranking real.

### Q3 · `GROUP BY` — frecuencia y costo promedio por código de falla

```sql
SELECT d.dtc_code,
       COUNT(*)                         AS sesiones,
       ROUND(AVG(s.repair_cost_cop), 0) AS costo_promedio_cop,
       SUM(s.repair_cost_cop)           AS costo_total_cop
FROM sesion_diagnostico AS s
JOIN sesion_dtc AS d ON d.session_id = s.session_id
GROUP BY d.dtc_code
ORDER BY costo_promedio_cop DESC, d.dtc_code;
```

| dtc_code | sesiones | costo_promedio_cop | costo_total_cop |
|---|---:|---:|---:|
| P0300 | 29 | 376 897 | 10 930 000 |
| P0171 | 37 | 374 054 | 13 840 000 |
| P0299 | 42 | 300 238 | 12 610 000 |
| P0420 | 33 | 297 879 | 9 830 000 |
| P0118 | 37 | 296 216 | 10 960 000 |
| P0562 | 34 | 289 706 | 9 850 000 |
| P0101 | 28 | 256 786 | 7 190 000 |

**Cómo leerla:** P0299 es el código más frecuente (42 sesiones), P0300 (fallo de encendido) tiene el promedio más alto y P0171 (mezcla pobre) deja el mayor gasto total, con 13,84 millones COP.

**Qué no puedo afirmar:** las diferencias entre promedios son modestas frente a la dispersión de los costos (la desviación estándar global es de unos 299 000 COP y cada grupo tiene entre 28 y 42 sesiones). Una estimación rápida indica que, por ejemplo, la diferencia entre P0300 y P0101 está en el orden de 1,5 errores estándar, así que **no es evidencia sólida** de que un código cueste más que otro. Con estos datos describo lo observado, no establezco una causa.

## Equivalente en pandas (para Q3)

```python
p3 = (plano.groupby("dtc_code")["repair_cost_cop"]
      .agg(sesiones="count", costo_promedio_cop="mean", costo_total_cop="sum")
      .reset_index())
p3["costo_promedio_cop"] = p3["costo_promedio_cop"].round(0)
p3 = p3.sort_values(["costo_promedio_cop", "dtc_code"], ascending=[False, True])
```

SQL agrupa con `GROUP BY` y calcula con `COUNT`, `AVG` y `SUM`; pandas lo hace con `groupby` y `agg`. La diferencia práctica es que en SQL el `JOIN` con `sesion_dtc` es necesario porque el código vive en otra tabla, mientras que en pandas el CSV plano ya trae `dtc_code` junto al costo.

## Cuándo usé cada herramienta

- **SQL** cuando el dato está repartido en varias tablas y hay que cruzarlo (Q2, Q3). Filtrar y agrupar en el motor evita traer toda la tabla a Python.
- **pandas** para verificar y para el análisis posterior sobre el CSV plano.

## Limitaciones

- Algunas combinaciones de código y vehículo pueden ser poco plausibles (por ejemplo, P0299, de turbo, en un Suzuki Swift 2013 a gasolina), lo que sugiere que los datos son sintéticos. Las consultas son correctas sobre los datos, pero las conclusiones mecánicas no deben tomarse al pie de la letra.
- El costo 0 aparece en 32 sesiones y entra tal cual en los promedios; si significara "dato faltante" en vez de "sin cargo", los promedios estarían subestimados.

## Referencias

Beaulieu, A. (2020). *Learning SQL* (3.ª ed.). O'Reilly Media.

Codd, E. F. (1970). A relational model of data for large shared data banks. *Communications of the ACM, 13*(6), 377–387.

CORHUILA. (2026). *Ciencia de Datos · Semana 7 · Herramientas y lenguajes (SQL, NoSQL, Python)* [Material de clase]. Corporación Universitaria del Huila. https://code-corhuila.github.io/ova-web/2026-B/ciencia-datos/07-week/01-session/

McKinney, W. (2022). *Python for data analysis* (3.ª ed.). O'Reilly Media.

pandas. (s. f.). *Group by: Split-apply-combine*. https://pandas.pydata.org/docs/user_guide/groupby.html

Python Software Foundation. (s. f.). *sqlite3 — DB-API 2.0 interface for SQLite databases*. https://docs.python.org/3/library/sqlite3.html

SQLite. (s. f.). *SQL as understood by SQLite*. https://www.sqlite.org/lang.html
