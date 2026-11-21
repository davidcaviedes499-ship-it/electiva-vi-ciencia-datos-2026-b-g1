"""Semana 13 - Boceto de un dashboard con 3 KPIs (con cifras reales del dataset).

Autor: Juan David Caviedes Cortes (davidcaviedes499-ship-it)

Proceso elegido: calidad y composición del mercado de acciones de la Bolsa de Tokio
(listado de valores, cierre del 30/12/2021, cifras en yenes).
Uso:    python boceto_dashboard.py
Genera: kpis.csv y dashboard_boceto.png
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
acc["segmento"] = (acc["new_market_segment"].str.replace(r" \(Foreign Stock\)", "", regex=True)
                   .replace({"Unassigned": "Sin asignar"}))
total_cap = acc["market_cap"].sum()

# ---- KPIs y objetivos (los objetivos son una propuesta de diseño) ---------------------
cap_seg = acc.groupby("segmento")["market_cap"].sum().sort_values(ascending=False)
prime = cap_seg["Prime Market"] / total_cap * 100                 # KPI 1
cap_sec = acc.groupby("sector17_name")["market_cap"].sum().sort_values(ascending=False)
sector_lider = cap_sec.iloc[0] / total_cap * 100                   # KPI 2
barato = (acc["close"] < 1000).mean() * 100                        # KPI 3
OBJ_PRIME, OBJ_SECTOR, OBJ_BARATO = 90, 25, 35

kpis = pd.DataFrame([
    ["Peso del mercado Prime en la capitalización (%)", round(prime, 1), f">= {OBJ_PRIME}", prime >= OBJ_PRIME],
    ["Peso del sector líder en la capitalización (%)", round(sector_lider, 1), f"<= {OBJ_SECTOR}", sector_lider <= OBJ_SECTOR],
    ["Acciones con cierre menor a ¥1.000 (%)", round(barato, 1), f"<= {OBJ_BARATO}", barato <= OBJ_BARATO],
], columns=["kpi", "valor", "objetivo", "cumple"])
kpis.to_csv(AQUI / "kpis.csv", index=False)
print(kpis.to_string(index=False))

# ---- Datos de apoyo -------------------------------------------------------------------
n_seg = acc.groupby("segmento").size()
pct_cap_seg = (cap_seg / total_cap * 100)
pct_n_seg = (n_seg / n_seg.sum() * 100).reindex(pct_cap_seg.index)
top_sec = (cap_sec / total_cap * 100).head(8)[::-1]
logp = np.log10(acc["close"])

VERDE, ROJO, GRIS, AZUL = "#1e8449", "#c0392b", "#b8c0c8", "#1f6f8b"
fig = plt.figure(figsize=(13, 8), facecolor="white")
gs = fig.add_gridspec(3, 3, height_ratios=[0.3, 0.9, 2.8], hspace=0.45, wspace=0.6,
                      left=0.09, right=0.97, top=0.95, bottom=0.07)

axf = fig.add_subplot(gs[0, :]); axf.axis("off")
for i, f in enumerate(["Fecha de cierre ▾", "Segmento ▾", "Sector (17 grupos) ▾", "Rango de precio ▾"]):
    axf.text(i * 0.24, 0.45, f, fontsize=10, va="center",
             bbox=dict(boxstyle="round,pad=0.5", fc="#f3f5f7", ec="#9aa5b1"))
axf.text(0, 1.05, "Composición del mercado de acciones de Tokio · cierre 30/12/2021",
         fontsize=15, fontweight="bold", va="bottom")


def tarjeta(ax, titulo, valor, objetivo, cumple):
    ax.axis("off")
    color = VERDE if cumple else ROJO
    ax.add_patch(plt.Rectangle((0, 0), 1, 1, transform=ax.transAxes, fc="#f9fafb", ec=color, lw=2.5))
    ax.text(0.04, 0.8, titulo, fontsize=9.5, va="top")
    ax.text(0.04, 0.2, f"{valor:.1f}%", fontsize=26, fontweight="bold", color=color)
    ax.text(0.96, 0.2, f"objetivo {objetivo}\n{'✔ cumple' if cumple else '✘ no cumple'}",
            fontsize=9.5, ha="right", color=color, va="bottom")


for j, (t, v, o, c) in enumerate(zip(["KPI 1 · Peso de Prime", "KPI 2 · Sector líder", "KPI 3 · Acciones baratas"],
                                      kpis["valor"], kpis["objetivo"], kpis["cumple"])):
    tarjeta(fig.add_subplot(gs[1, j]), t, v, o, c)

a1 = fig.add_subplot(gs[2, 0])
y = np.arange(len(pct_cap_seg))
a1.barh(y + 0.2, pct_n_seg.values, height=0.38, color=GRIS, label="% de las acciones")
a1.barh(y - 0.2, pct_cap_seg.values, height=0.38, color=AZUL, label="% del valor")
a1.set_yticks(y); a1.set_yticklabels(pct_cap_seg.index, fontsize=8); a1.invert_yaxis()
a1.axvline(OBJ_PRIME, color="k", ls="--", lw=1)
a1.set_xlabel("%"); a1.set_xlim(0, 105); a1.legend(frameon=False, fontsize=8, loc="center", bbox_to_anchor=(0.45, 0.3))
a1.set_title("Prime tiene el 49% de las acciones\ny el 96% del valor", loc="left", fontsize=10.5, fontweight="bold")

a2 = fig.add_subplot(gs[2, 1])
nombres = {"ELECTRIC APPLIANCES & PRECISION INSTRUMENTS": "Electrodom. y precisión", "IT & SERVICES, OTHERS": "TI y servicios",
           "AUTOMOBILES & TRANSPORTATION EQUIPMENT": "Automóviles", "RAW MATERIALS & CHEMICALS": "Materias primas",
           "RETAIL TRADE": "Comercio minorista", "MACHINERY": "Maquinaria", "PHARMACEUTICAL": "Farmacéutico",
           "COMMERCIAL & WHOLESALE TRADE": "Comercio mayorista", "BANKS": "Bancos",
           "FINANCIALS (EX BANKS)": "Financieras"}
a2.barh([nombres.get(i, i) for i in top_sec.index], top_sec.values,
        color=[ROJO if i == top_sec.index[-1] else GRIS for i in top_sec.index])
a2.axvline(OBJ_SECTOR, color="k", ls="--", lw=1)
a2.set_xlabel("% de la capitalización"); a2.tick_params(axis="y", labelsize=8); a2.set_xlim(0, 27)
a2.set_title("Ningún sector pasa del 25%,\npero dos están casi empatados", loc="left", fontsize=10.5, fontweight="bold")

a3 = fig.add_subplot(gs[2, 2])
a3.hist(logp, bins=30, color=GRIS, edgecolor="white")
a3.axvline(3, color=ROJO, lw=1.5); a3.text(3.03, a3.get_ylim()[1] * 0.92, "¥1.000", color=ROJO, fontsize=9)
a3.set_xlabel("Precio de cierre (log10 de yenes)"); a3.set_ylabel("N.º de acciones")
a3.set_title(f"{barato:.0f}% de las acciones cierra\npor debajo de ¥1.000", loc="left", fontsize=10.5, fontweight="bold")

for a in (a1, a2, a3):
    a.spines[["top", "right"]].set_visible(False)
fig.savefig(AQUI / "dashboard_boceto.png", dpi=150)
print(pct_cap_seg.round(1).to_string()); print(pct_n_seg.round(1).to_string()); print(top_sec.round(1).tail(3).to_string())
