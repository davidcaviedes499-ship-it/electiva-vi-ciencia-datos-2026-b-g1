"""Semana 14 - Opción A (SQL): reescribir una consulta lenta y medir la mejora.

Autora: Juan David Caviedes Cortes (davidcaviedes499-ship-it)

Datos: listado de valores de la Bolsa de Tokio (stock_list_clean.csv, semana 9).
Como el listado real tiene solo ~4.400 filas, la diferencia de tiempo sería
imposible de notar. Para ver el efecto del índice se repite el listado 500 veces
(~2 millones de filas) en una base SQLite temporal. Eso es una simulación de
volumen: los códigos de valor se repiten, pero sirve para comparar las dos consultas.

Uso:  python optimizar_consulta.py
Genera: resultados.txt y comparacion_tiempos.png
"""
import sqlite3
import statistics
import tempfile
import time
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

AQUI = Path(__file__).resolve().parent
REPETICIONES_DATOS = 500     # cuántas veces se copia el listado
CORRIDAS = 5                 # veces que se mide cada consulta (se reporta la mediana)

# 1. Carga: tabla con ~2 millones de filas -------------------------------------
df = pd.read_csv(AQUI / "data" / "stock_list_clean.csv",
                 usecols=["securities_code", "name", "sector17_name", "close", "market_cap"])
grande = pd.concat([df] * REPETICIONES_DATOS, ignore_index=True)

tmp = tempfile.TemporaryDirectory()
con = sqlite3.connect(Path(tmp.name) / "bolsa.db")
grande.to_sql("acciones", con, index=False)
n_filas = con.execute("SELECT COUNT(*) FROM acciones").fetchone()[0]

# 2. Las dos versiones de la consulta -----------------------------------------------
# Pregunta: nombre y capitalización de las empresas del sector Bancos.
ANTES = "SELECT * FROM acciones WHERE UPPER(sector17_name) = 'BANKS'"
DESPUES = ("SELECT name, market_cap FROM acciones "
           "WHERE sector17_name = 'BANKS'")
INDICE = "CREATE INDEX idx_sector ON acciones (sector17_name, name, market_cap)"


def medir(sql):
    tiempos = []
    for _ in range(CORRIDAS):
        t0 = time.perf_counter()
        filas = con.execute(sql).fetchall()
        tiempos.append(time.perf_counter() - t0)
    return statistics.median(tiempos), filas


def plan(sql):
    return " | ".join(r[3] for r in con.execute("EXPLAIN QUERY PLAN " + sql))


# 3. Medición ------------------------------------------------------------------------
t_antes, filas_antes = medir(ANTES)
plan_antes = plan(ANTES)

t_solo_forma, _ = medir(DESPUES)            # nueva forma, todavía sin índice
plan_sin_indice = plan(DESPUES)

con.execute(INDICE)
con.execute("ANALYZE")
t_despues, filas_despues = medir(DESPUES)
plan_despues = plan(DESPUES)

# La mejora solo vale si el resultado es el mismo
col_name = [d[0] for d in con.execute("SELECT * FROM acciones LIMIT 1").description]
i_name, i_cap = col_name.index("name"), col_name.index("market_cap")
igual = sorted((f[i_name], f[i_cap]) for f in filas_antes) == sorted(filas_despues)

# 4. Resultados ---------------------------------------------------------------------
lineas = [
    f"Filas en la tabla: {n_filas:,}  |  filas devueltas: {len(filas_despues):,}  |  "
    f"mismo resultado: {igual}",
    f"Corridas por consulta: {CORRIDAS} (se reporta la mediana)",
    "",
    f"ANTES   (SELECT *, función en el WHERE)      : {t_antes * 1000:8.1f} ms",
    f"   plan : {plan_antes}",
    f"SOLO REESCRITA (columnas + igualdad, sin índice) : {t_solo_forma * 1000:8.1f} ms",
    f"   plan : {plan_sin_indice}",
    f"DESPUÉS (columnas + igualdad + índice)       : {t_despues * 1000:8.1f} ms",
    f"   plan : {plan_despues}",
    "",
    f"Mejora total: {t_antes / t_despues:.0f} veces más rápida",
]
(AQUI / "resultados.txt").write_text("\n".join(lineas) + "\n", encoding="utf-8")
print("\n".join(lineas))

# 5. Gráfico ------------------------------------------------------------------------
fig, ax = plt.subplots(figsize=(8, 4.2))
etq = ["Antes\n(SELECT *, función\nen el WHERE)", "Solo reescrita\n(sin índice)",
       "Después\n(igualdad + índice)"]
vals = [t_antes * 1000, t_solo_forma * 1000, t_despues * 1000]
barras = ax.bar(etq, vals, color=["#c0392b", "#b8c0c8", "#1e8449"])
for b, v in zip(barras, vals):
    ax.text(b.get_x() + b.get_width() / 2, v, f"{v:,.1f} ms", ha="center", va="bottom", fontsize=10)
ax.set_ylabel("Tiempo de la consulta (ms, mediana)")
ax.set_ylim(0, max(vals) * 1.15)
fig.suptitle(f"El índice y el filtro sin función hacen la consulta {t_antes / t_despues:.0f} veces más rápida",
             x=0.01, ha="left", fontsize=12.5, fontweight="bold")
ax.spines[["top", "right"]].set_visible(False)
fig.text(0.01, 0.01, f"SQLite, {n_filas:,} filas (listado de la Bolsa de Tokio repetido {REPETICIONES_DATOS} veces).",
         fontsize=8, color="#555")
fig.tight_layout(rect=(0, 0.03, 1, 0.93))
fig.savefig(AQUI / "comparacion_tiempos.png", dpi=150)
tmp.cleanup()
