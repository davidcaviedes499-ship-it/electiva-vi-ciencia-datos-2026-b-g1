# Semana 9 · Limpieza del dataset de diagnósticos

```python
FULL_NAME   = "Juan David Caviedes Cortes"
GITHUB_USER = "davidcaviedes499-ship-it"
```

Asignatura: Ciencia de Datos · Ingeniería Industrial · CORHUILA · 2026-B · Corte 2.
Guía de la actividad: *Semana 9 · Limpieza de un dataset* (formativa, opcional).

## Qué se entrega

| Archivo | Contenido |
|---|---|
| [`limpieza.py`](limpieza.py) | Script de limpieza en pandas (función `limpiar`) y generador del reporte antes/después |
| [`data/diagnostics_raw.csv`](data/diagnostics_raw.csv) | Dataset **original**, con errores (252 filas × 16 columnas) |
| [`data/diagnostics_clean.csv`](data/diagnostics_clean.csv) | Dataset **limpio** que produce el script (240 filas × 16 columnas) |
| [`reportes/antes_despues.md`](reportes/antes_despues.md) y [`.json`](reportes/antes_despues.json) | Evidencia antes/después |

```bash
python limpieza.py     # lee data/diagnostics_raw.csv y regenera data/ y reportes/
```

Comprobé que el CSV que genera el script es **idéntico, celda por celda**, al `diagnostics_clean.csv` que recibí como referencia (0 diferencias).

## 1. Evidencia antes/después

| Métrica | Antes | Después |
|---|---:|---:|
| Filas | 252 | 240 |
| Celdas nulas | 91 | 0 |
| Filas duplicadas | 12 | 0 |
| `session_id` repetidos | 12 | 0 |
| Atípicos fuera de rango | 12 | 0 |
| Placas distintas (son 10 vehículos) | 18 | 10 |
| Marcas distintas (son 10 marcas) | 27 | 10 |
| Formatos de fecha en uso | 3 | 1 |

Nulos por columna (antes): `symptom` 10 · `rpm` 26 · `coolant_temp_c` 21 · `battery_v` 18 · `map_kpa` 16.

## 2. Problemas encontrados y cómo los traté

| # | Problema | Cómo lo detecté | Tratamiento |
|---|---|---|---|
| 1 | **12 filas duplicadas exactas** | `df.duplicated()` y `session_id` repetido | `drop_duplicates()`; al final reviso otra vez que `session_id` sea único |
| 2 | **Fechas en 3 formatos** (`2026-05-10`, `20/01/2026`, `24-9-2026`) | Expresiones regulares por formato (97 / 72 / 83 filas) | Convertidas a ISO `aaaa-mm-dd`; los formatos con `/` y `-` los leí como **día primero** |
| 3 | **Placas, marcas y técnicos mal escritos** (`nei 789`, `HYUNDAI`, ` Toyota `, `LUIS PEREZ`) | Conteo de valores distintos: 18 placas y 27 marcas para 10 vehículos | `strip()`, mayúsculas en placas con guion, `title()` en marcas y técnicos |
| 4 | **Números guardados como texto** (`"80,544 km"`, `"$900,000"`) | `dtypes` = texto en `mileage_km` y `repair_cost_cop` | Quité todo lo que no es dígito y convertí a entero |
| 5 | **91 celdas vacías** en 5 columnas | `isna().sum()` | Numéricas: mediana por combustible. `symptom`: categoría explícita `Unknown` |
| 6 | **Atípicos imposibles**: RPM `-50` y `9999`; refrigerante `250 °C` y `-40 °C` | Comparación con rangos físicos plausibles | Los marqué como nulos y los imputé como en el punto 5 |

**Rangos usados** para decidir qué es atípico: RPM 300–2000, refrigerante 0–130 °C, batería 9–16 V, MAP 15–110 kPa. Son criterios míos de plausibilidad física, y es el punto más discutible del proceso: otro criterio cambiaría cuántos valores se imputan.

**Por qué la mediana por combustible:** la mediana no se distorsiona con valores extremos y, como los diésel y los de gasolina tienen lecturas típicas distintas (por ejemplo, el refrigerante: 90,3 °C frente a 88,3 °C), imputar por grupo respeta esa diferencia mejor que una mediana global.

## 3. Dos dimensiones de calidad que mejoré

Las dimensiones salen de la sesión de clase: completitud, exactitud, consistencia, unicidad y vigencia (Wang y Strong, 1996; ISO/IEC, 2008).

### a) Consistencia: de 3 formatos de fecha a uno, y de 27 «marcas» a 10

Un mismo vehículo aparecía escrito de varias maneras (`NEI-789` y `nei 789`; `Hyundai`, `HYUNDAI`, `hyundai`) y las fechas venían en tres formatos. Eso rompe cualquier agrupación: un `groupby('brand')` sobre los datos originales habría contado 27 marcas en lugar de 10 y repartido las sesiones de un mismo vehículo en varios grupos. Con la normalización, cada categoría tiene una sola forma de escribirse y las fechas se pueden ordenar y comparar.

### b) Completitud: de 91 celdas nulas a 0

Todas las columnas quedaron llenas. Pero **completo no significa verdadero**, y quiero ser claro con lo que eso implica:

- Imputé **89 celdas numéricas** (78 nulas y 11 atípicas, ya sin las filas duplicadas) con una mediana. Son **estimaciones, no mediciones**.
- Eso afecta a **77 de las 240 filas (32 %)**, que tienen al menos una lectura imputada.
- Imputar con la mediana **encoge la variabilidad**: la desviación estándar del RPM pasó de unos 1 060 (inflada por los valores `9999`) a unos 54. Parte de esa caída es corregir los errores, pero parte es el efecto artificial de rellenar con un mismo número.
- Las 10 filas con síntoma vacío no se inventaron: quedaron como `Unknown`.

Por eso, cualquier análisis que dependa de `rpm`, `coolant_temp_c`, `battery_v` o `map_kpa` debería reportar este límite. Una alternativa más prudente para un análisis delicado sería dejar los nulos y excluir esas filas solo cuando la columna sea relevante.

### Bonus: unicidad y exactitud

Los 12 duplicados eliminados (unicidad) habrían inflado conteos y costos de esas sesiones; y los 11 atípicos corregidos (exactitud) habrían distorsionado promedios, porque un solo RPM de 9 999 pesa mucho en un promedio.

## 4. Limitaciones

- No pude verificar contra los registros físicos del taller qué valor correcto tenía cada celda corregida; el tratamiento es estadístico, no una corrección con la fuente.
- Las fechas con `/` o `-` las interpreté como día/mes/año. Eso es coherente con los datos (hay fechas como `24-9-2026`, que solo pueden ser día primero) y con el CSV de referencia, pero una fecha como `05/09/2026` es ambigua por sí sola.
- Los 32 registros con costo `0` los dejé como están (no sé si son garantía o dato faltante).

## 5. Referencias

CORHUILA. (2026). *Ciencia de Datos · Semana 9 · Transformación y calidad de datos* [Material de clase]. Corporación Universitaria del Huila. https://code-corhuila.github.io/ova-web/2026-B/ciencia-datos/09-week/01-session/

International Organization for Standardization & International Electrotechnical Commission. (2008). *ISO/IEC 25012:2008 Software engineering — Software product Quality Requirements and Evaluation (SQuaRE) — Data quality model*.

McKinney, W. (2022). *Python for data analysis* (3.ª ed.). O'Reilly Media.

pandas. (s. f.). *Working with missing data*. https://pandas.pydata.org/docs/user_guide/missing_data.html

Rahm, E., y Do, H. H. (2000). Data cleaning: Problems and current approaches. *IEEE Data Engineering Bulletin, 23*(4), 3–13.

Wang, R. Y., y Strong, D. M. (1996). Beyond accuracy: What data quality means to data consumers. *Journal of Management Information Systems, 12*(4), 5–33.

Wickham, H. (2014). Tidy data. *Journal of Statistical Software, 59*(10), 1–23.
