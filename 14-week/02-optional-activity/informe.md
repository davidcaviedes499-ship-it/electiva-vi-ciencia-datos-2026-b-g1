# Semana 14 · Actividad opcional · Opción A (SQL)

**Estudiante:** Juan David Caviedes Cortes · **Usuario GitHub:** davidcaviedes499-ship-it

## La consulta lenta

La pregunta: *¿cuáles son el nombre y la capitalización de las empresas del sector Bancos?*

```sql
-- ANTES
SELECT * FROM acciones
WHERE UPPER(sector17_name) = 'BANKS';
```

Tiene dos problemas de los que hablamos en la sesión. Trae todas las columnas con `SELECT *` cuando solo necesito dos, y aplica la función `UPPER()` sobre la columna del `WHERE`, así que la base de datos debe transformar cada fila antes de comparar y no puede usar un índice.

## La consulta mejorada

```sql
-- DESPUÉS
CREATE INDEX idx_sector ON acciones (sector17_name, name, market_cap);

SELECT name, market_cap
FROM acciones
WHERE sector17_name = 'BANKS';
```

Cambié tres cosas: pido solo las columnas necesarias, comparo la columna directamente (sin función) y creo un índice sobre la columna que filtro, incluyendo las dos que devuelvo.

## Qué pasó al medirlo

Medí cada versión 5 veces y tomé la mediana. Para que el tiempo se notara repetí el listado de la Bolsa de Tokio 500 veces (unos 2 millones de filas en SQLite); es un volumen simulado, no datos reales distintos. Los tiempos exactos están en `resultados.txt` y varían un poco entre computadores.

| Versión | Plan de ejecución | Tiempo |
|---|---|---|
| Antes | `SCAN acciones` (lee toda la tabla) | ≈ 226 ms |
| Solo reescrita, sin índice | `SCAN acciones` | ≈ 108 ms |
| Después, con índice | `SEARCH ... USING COVERING INDEX` | ≈ 14 ms |

Las dos versiones devuelven exactamente las mismas 40.500 filas (el script lo comprueba).

## Por qué es más eficiente

Quitar `SELECT *` y la función ayudó a la mitad del camino, porque se movieron menos datos, pero la base seguía leyendo toda la tabla. Lo que más pesó fue el índice: con la comparación directa, SQLite va derecho a la parte del índice donde están los bancos (`SEARCH`) en lugar de revisar los 2 millones de filas, y como el índice ya trae `name` y `market_cap`, ni siquiera tiene que volver a la tabla (`COVERING INDEX`).

## Buenas prácticas aplicadas

- Evitar `SELECT *` y traer solo lo necesario.
- No poner funciones sobre la columna filtrada.
- Crear un índice sobre la columna del filtro.
- Medir antes y después, y comprobar que el resultado es el mismo.

Archivos: `optimizar_consulta.py` (reproduce todo), `resultados.txt`, `comparacion_tiempos.png`.
