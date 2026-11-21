"""Semana 11 - Análisis de una serie de tiempo (ventas diarias simuladas de una tienda).

Autor: Juan David Caviedes Cortes (davidcaviedes499-ship-it)

La actividad permite una serie "real o simulada". El listado de la Bolsa de Tokio
(stock_list.csv) es una foto de un solo día y no sirve como serie, así que aquí se
simulan las ventas diarias de una tienda durante dos años, con tendencia, pico de
diciembre, más ventas en fin de semana y ruido. Como la simulación es conocida, se
puede comprobar si el análisis recupera lo que se puso.

Uso:    python serie_tiempo.py
Genera: ventas_diarias.csv, ventas_mensuales.png y resumen.txt
"""
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

AQUI = Path(__file__).resolve().parent
rng = np.random.default_rng(7)

# 1. Serie simulada: 2 años de ventas diarias (unidades vendidas) ----------------
dias = pd.date_range("2024-01-01", "2025-12-31", freq="D")
t = np.arange(len(dias))
tendencia = 300 + 0.15 * t                                            # +0.15 unidades por día
navidad = 90 * np.cos(2 * np.pi * (dias.dayofyear - 355) / 365.25)    # pico a finales de diciembre
fin_semana = np.where(dias.dayofweek >= 5, 70, 0)                     # más ventas sáb-dom
ruido = rng.normal(0, 20, len(dias))
unidades = (tendencia + navidad + fin_semana + ruido).round().astype(int)
pd.DataFrame({"fecha": dias, "unidades": unidades}).to_csv(AQUI / "ventas_diarias.csv", index=False)

# 2. Carga con la fecha como índice ------------------------------------------------
df = pd.read_csv(AQUI / "ventas_diarias.csv", parse_dates=["fecha"]).set_index("fecha")

# 3. Agregación mensual y media móvil -----------------------------------------------
mensual = df["unidades"].resample("MS").sum()
movil3 = mensual.rolling(3, center=True).mean()

# 4. Cifras para describir tendencia y estacionalidad ---------------------------------
pendiente = np.polyfit(np.arange(len(mensual)), mensual.values, 1)[0]
prom_diario = mensual / mensual.index.days_in_month
por_mes = prom_diario.groupby(prom_diario.index.month).mean()
anual = df["unidades"].resample("YS").sum()
semana = df[df.index.dayofweek < 5].unidades.mean(), df[df.index.dayofweek >= 5].unidades.mean()

# 5. Gráfico ----------------------------------------------------------------------------
fig, ax = plt.subplots(figsize=(10, 5))
ax.plot(mensual.index, mensual.values, color="#9aa5b1", marker="o", ms=4, lw=1.2, label="Ventas del mes")
ax.plot(movil3.index, movil3.values, color="#1f6f8b", lw=2.8, label="Media móvil de 3 meses")
pico = mensual.idxmax()
ax.annotate(f"Pico: {pico:%m/%Y}\n{mensual.max():,.0f} unidades", xy=(pico, mensual.max()),
            xytext=(-95, -5), textcoords="offset points", fontsize=9, color="#1f6f8b",
            arrowprops=dict(arrowstyle="->", color="#1f6f8b"))
ax.set_title("Las ventas crecen cada año y siempre se disparan en diciembre",
             loc="left", fontsize=13, fontweight="bold")
ax.set_ylabel("Unidades vendidas por mes")
ax.set_xlabel("Mes")
ax.set_ylim(0, mensual.max() * 1.15)
ax.spines[["top", "right"]].set_visible(False)
ax.grid(axis="y", alpha=.25)
ax.legend(frameon=False, loc="lower right")
fig.tight_layout()
fig.savefig(AQUI / "ventas_mensuales.png", dpi=150)

# 6. Resumen -------------------------------------------------------------------------------
lineas = [
    f"Días: {len(df)}  |  meses: {len(mensual)}",
    f"Total 2024: {anual.iloc[0]:,}  |  total 2025: {anual.iloc[1]:,}  (+{(anual.iloc[1] / anual.iloc[0] - 1) * 100:.1f}%)",
    f"Pendiente de la tendencia mensual: {pendiente:+.0f} unidades por mes",
    f"Mes con mayor promedio diario: {por_mes.idxmax()} ({por_mes.max():.0f})  |  menor: {por_mes.idxmin()} ({por_mes.min():.0f})",
    f"Media de lun-vie: {semana[0]:.0f}  |  sáb-dom: {semana[1]:.0f}",
]
(AQUI / "resumen.txt").write_text("\n".join(lineas) + "\n", encoding="utf-8")
print("\n".join(lineas))
