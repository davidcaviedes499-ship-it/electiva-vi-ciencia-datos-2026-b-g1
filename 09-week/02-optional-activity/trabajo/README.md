# Semana 9 – Modelo, consulta y limpieza de datos
**Caso:** diagnóstico de fallas electrónicas en vehículos (continuación del Corte 1)
**Autor:** FULL_NAME · **GitHub:** GITHUB_USER <!-- completar con el bloque CONFIG -->

## Contenido
| Archivo | Descripción |
|---|---|
| `ERD.md` | Diagrama entidad-relación (5 entidades, cardinalidades) |
| `generate_dataset.py` | Genera el CSV sintético "sucio" (semilla fija) |
| `data/diagnostics_raw.csv` | Dataset original (252 filas) |
| `clean_and_query.py` | Limpieza con pandas + 2 consultas |
| `data/diagnostics_clean.csv` | Dataset limpio (240 filas) |
| `data/cleaning_report.md` | Tabla antes/después |

Ejecución: `pip install pandas tabulate && python generate_dataset.py && python clean_and_query.py`

## 1. ERD
Ver [`ERD.md`](ERD.md): VEHICLE, TECHNICIAN, DIAGNOSTIC_SESSION, DTC y SESSION_DTC (tabla puente N:M). El modelo usa llaves primarias y foráneas, las cardinalidades 1:1, 1:N y N:M y una tabla puente para resolver la relación N:M (CORHUILA, 2026a).

## 2. Limpieza – antes / después
| Métrica | Antes | Después |
|---|---|---|
| Filas | 252 | 240 |
| Celdas nulas | 91 | 0 |
| Filas duplicadas | 12 | 0 |
| Outliers (RPM / temp.) | 6 / 5 | imputados |
| `date`, `mileage_km`, `repair_cost_cop` | texto (3 formatos de fecha, "123,456 km", "$150,000") | `datetime64` / `int` / `int` |

Los métodos aplicados (conteo de nulos, imputación, `drop_duplicates`, conversión de tipos con `to_datetime`/`to_numeric` y normalización con `str.strip().str.title()`) siguen lo visto en la sesión de transformación y calidad de datos (CORHUILA, 2026d). Normalización: marcas y técnicos en `Title Case`, placas `ABC-123`, DTC en mayúsculas, espacios eliminados. Detalle por columna en `data/cleaning_report.md`.

## 3. Consultas y hallazgos
Las consultas usan filtro y agrupación con pandas, equivalentes a `WHERE` y `GROUP BY` en SQL (CORHUILA, 2026b).

**Q1 (agregación por grupo):** número de sesiones y costo promedio de reparación por DTC.
Hallazgo: P0299 (turbo underboost) es el código más frecuente (42 sesiones); P0300 (misfire) y P0171 (mezcla pobre) tienen el costo promedio más alto (~COP 377k y 374k).

**Q2 (filtro + agregación):** sesiones con `battery_v < 12.4` (73 de 240) agrupadas por DTC.
Hallazgo: P0562 (voltaje bajo del sistema) representa solo 11.0 % de las sesiones con batería baja, menos que su 14.2 % global; es decir, no hay relación visible entre voltaje bajo y ese código. Esto muestra por qué un DTC aislado no basta para decidir y se necesitan mediciones (idea central del Corte 1).

> Nota: las descripciones de los códigos DTC (p. ej., P0300 = fallo de encendido aleatorio) son descripciones genéricas de OBD-II escritas por el autor y **no** se verificaron contra una fuente citable; confírmalas con la norma o fuente de tu Corte 1 antes de entregar.
>
> Nota: los datos son **sintéticos** (simulan un export de escáner OBD-II y bitácora de taller), por lo que los hallazgos no deben interpretarse como evidencia mecánica real.

## Data & cleaning
This project uses a synthetic CSV of 252 workshop diagnostic sessions that simulates an OBD-II scanner export, with fields such as plate, brand, DTC code, engine speed, coolant temperature, battery voltage, MAP pressure, mileage and repair cost. The raw file was intentionally messy: it had 91 null cells, 12 exact duplicate rows, three different date formats, numbers stored as text (for example "$150,000" and "123,456 km"), inconsistent capitalization in brands and technicians, and physically impossible values such as 9999 RPM or 250 °C. I removed the duplicates, normalized text and plate formats, converted dates and numeric columns to proper types, turned impossible readings into nulls, and imputed missing sensor values with the median by fuel type (and "Unknown" for missing symptoms), ending with 240 rows and zero nulls. The first question asked which DTC is most frequent and how much its repair costs on average; P0299 was the most common, while P0300 and P0171 were the most expensive. The second question filtered sessions with battery voltage below 12.4 V and counted DTCs, and it showed that the low-voltage code P0562 was not over-represented, so a single code should not drive the repair decision.

## Referencias (APA 7)

CORHUILA. (2026a). *Ciencia de Datos · Semana 6 · Modelamiento de datos* [Material de curso]. Corporación Universitaria del Huila, Facultad de Ingeniería. https://code-corhuila.github.io/ova-web/2026-B/ciencia-datos/06-week/01-session/

CORHUILA. (2026b). *Herramientas y lenguajes (SQL, NoSQL, Python)* [Material de curso]. Corporación Universitaria del Huila, Facultad de Ingeniería. https://code-corhuila.github.io/ova-web/2026-B/ciencia-datos/07-week/01-session/

CORHUILA. (2026c). *Conexión de datos: APIs, ETL y pipelines* [Material de curso]. Corporación Universitaria del Huila, Facultad de Ingeniería. https://code-corhuila.github.io/ova-web/2026-B/ciencia-datos/08-week/01-session/

CORHUILA. (2026d). *Transformación y calidad de datos* [Material de curso]. Corporación Universitaria del Huila, Facultad de Ingeniería. https://code-corhuila.github.io/ova-web/2026-B/ciencia-datos/09-week/01-session/
