"""Semana 12 - Rediseña un gráfico (antes y después).

Autor: Juan David Caviedes Cortes (davidcaviedes499-ship-it)

Datos: acciones del listado de la Bolsa de Tokio (stock_list_clean.csv, semana 9;
cierre del 30/12/2021; cifras en yenes). Se compara cuánto valor de mercado concentra
cada grupo de tamaño del índice TOPIX.
Uso:    python redisenar_grafico.py
Genera: grafico_antes.png y grafico_despues.png
"""
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

AQUI = Path(__file__).resolve().parent
df = pd.read_csv(AQUI / "data" / "stock_list_clean.csv")
acc = df[(df["instrument_type"] == "Equity") & df["market_cap"].notna()]
g = acc.groupby("index_size")["market_cap"].agg(["sum", "count"])
orden = ["TOPIX Core30", "TOPIX Large70", "TOPIX Mid400", "TOPIX Small 1", "TOPIX Small 2",
         "Not in TOPIX size index"]
g = g.loc[orden]
cap = g["sum"] / 1e12                    # billones de yenes
pct = cap / cap.sum() * 100

# ANTES: torta con porción separada, colores brillantes, sombra, sin título ni unidades ---
fig, ax = plt.subplots(figsize=(7, 6))
ax.pie(cap.values, labels=g.index, explode=[0.12, 0, 0, 0, 0.12, 0], shadow=True, startangle=90,
       colors=["#ff00ff", "#00ffff", "#ffff00", "#ff7f00", "#00ff00", "#ff0000"],
       autopct="%1.0f%%", textprops={"fontsize": 8})
fig.tight_layout()
fig.savefig(AQUI / "grafico_antes.png", dpi=150)
plt.close(fig)

# DESPUÉS: barras horizontales ordenadas, un color, resaltando el grupo de las 100 mayores ---
nombres = {"TOPIX Core30": "30 mayores (Core30)", "TOPIX Large70": "Siguientes 70 (Large70)",
           "TOPIX Mid400": "Medianas (Mid400)", "TOPIX Small 1": "Pequeñas 1",
           "TOPIX Small 2": "Pequeñas 2", "Not in TOPIX size index": "Fuera del índice de tamaño"}
c = cap.rename(index=nombres).iloc[::-1]
p = pct.rename(index=nombres).iloc[::-1]
n = g["count"].rename(index=nombres).iloc[::-1]
resaltar = {"30 mayores (Core30)", "Siguientes 70 (Large70)"}
colores = ["#1f6f8b" if i in resaltar else "#b8c0c8" for i in c.index]

fig, ax = plt.subplots(figsize=(9, 5))
barras = ax.barh(c.index, c.values, color=colores)
for b, v, pp, nn in zip(barras, c.values, p.values, n.values):
    ax.text(v + 4, b.get_y() + b.get_height() / 2, f"{v:,.0f} billones ({pp:.0f}%) · {nn:,} acciones",
            va="center", fontsize=9)
top100 = pct.iloc[:2].sum()
fig.suptitle(f"Las 100 empresas más grandes concentran {top100:.0f}% del valor del mercado",
             x=0.01, ha="left", fontsize=13, fontweight="bold")
ax.set_xlabel("Capitalización de mercado (billones de yenes)")
ax.set_xlim(0, cap.max() * 1.75)
ax.spines[["top", "right"]].set_visible(False)
ax.grid(axis="x", alpha=.25)
fig.text(0.01, 0.01, f"Fuente: listado de valores de la Bolsa de Tokio, cierre del 30/12/2021. "
         f"Total: {cap.sum():,.0f} billones de yenes ({int(n.sum()):,} acciones).", fontsize=8, color="#555")
fig.tight_layout(rect=(0, 0.03, 1, 0.95))
fig.savefig(AQUI / "grafico_despues.png", dpi=150)
print(cap.round(1).to_string()); print(pct.round(1).to_string()); print("top100", round(top100, 1))
