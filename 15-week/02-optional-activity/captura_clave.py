"""Semana 15 - Gráfico clave del storytelling (acciones frente a valor por segmento).

Autor: Juan David Caviedes Cortes (davidcaviedes499-ship-it)

Datos: stock_list_clean.csv (semana 9), acciones con precio de cierre al 30/12/2021.
Uso:    python captura_clave.py
Genera: captura_clave.png y cifras_clave.txt
"""
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

AQUI = Path(__file__).resolve().parent
df = pd.read_csv(AQUI / "data" / "stock_list_clean.csv")
acc = df[(df["instrument_type"] == "Equity") & df["market_cap"].notna()].copy()
acc["segmento"] = acc["new_market_segment"].str.replace(r" \(Foreign Stock\)", "", regex=True)
acc = acc[acc["segmento"].isin(["Prime Market", "Standard Market", "Growth Market"])]

n = acc.groupby("segmento").size()
cap = acc.groupby("segmento")["market_cap"].sum()
med = acc.groupby("segmento")["market_cap"].median() / 1e9
orden = ["Prime Market", "Standard Market", "Growth Market"]
pct_n, pct_cap = n[orden] / n.sum() * 100, cap[orden] / cap.sum() * 100

AZUL, GRIS = "#1f6f8b", "#b8c0c8"
fig, ax = plt.subplots(figsize=(9, 5))
x = np.arange(3)
b1 = ax.bar(x - 0.2, pct_n.values, 0.38, color=GRIS, label="% de las acciones")
b2 = ax.bar(x + 0.2, pct_cap.values, 0.38, color=AZUL, label="% del valor de mercado")
for b in list(b1) + list(b2):
    ax.text(b.get_x() + b.get_width() / 2, b.get_height() + 1.2, f"{b.get_height():.0f}%", ha="center", fontsize=10)
ax.set_xticks(x); ax.set_xticklabels(["Prime", "Standard", "Growth"])
ax.set_ylim(0, 110); ax.set_ylabel("% del total del mercado")
ax.spines[["top", "right"]].set_visible(False); ax.grid(axis="y", alpha=.25)
ax.legend(frameon=False, loc="upper right")
fig.suptitle(f"El mercado Prime tiene {pct_n['Prime Market']:.0f}% de las acciones y {pct_cap['Prime Market']:.0f}% del valor",
             x=0.01, ha="left", fontsize=13.5, fontweight="bold")
fig.text(0.01, 0.01, f"Fuente: listado de valores de la Bolsa de Tokio, cierre del 30/12/2021. {n.sum():,} acciones con precio.",
         fontsize=8, color="#555")
fig.tight_layout(rect=(0, 0.03, 1, 0.95))
fig.savefig(AQUI / "captura_clave.png", dpi=150)

lineas = [f"Acciones con precio (Prime/Standard/Growth): {n.sum():,}"]
for s in orden:
    lineas.append(f"{s}: {n[s]:,} acciones ({pct_n[s]:.1f}%) = {pct_cap[s]:.1f}% del valor; capitalización mediana ¥{med[s]:.1f} mil millones")
lineas.append(f"Mediana Prime / Standard: {med['Prime Market'] / med['Standard Market']:.1f} veces")
(AQUI / "cifras_clave.txt").write_text("\n".join(lineas) + "\n", encoding="utf-8")
print("\n".join(lineas))
