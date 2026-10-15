"""Semana 10 - Mini-proyecto de datos (cierre del Corte 2).

Autor: Juan David Caviedes Cortes (davidcaviedes499-ship-it)

Integra lo del corte en un solo flujo:
    EXTRAER (CSV crudo)  ->  LIMPIAR (pandas, semana 9)
    ->  CARGAR en el modelo relacional (semana 6)
    ->  ANALIZAR con 2 consultas (SQL y pandas, semana 7)

Uso:
    python pipeline.py

Necesita las carpetas 06-week y 09-week al lado de esta (reutiliza su código).
Escribe todo en salidas/.
"""
from __future__ import annotations

import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

AQUI = Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI.parent / "09-week"))
sys.path.insert(0, str(AQUI.parent / "06-week"))
from limpieza import limpiar, perfilar   # noqa: E402  (semana 9)
from build_db import conteos, construir_db  # noqa: E402  (semana 6)

SALIDAS = AQUI / "salidas"
TEAL = "#0b6e75"

# --- Análisis 1: SQL = filtro (WHERE) + agregación (GROUP BY) ---------------
SQL_ANALISIS_1 = """
SELECT v.marca,
       COUNT(*)                         AS sesiones_con_cobro,
       ROUND(AVG(s.repair_cost_cop), 0) AS costo_promedio_cop,
       ROUND(AVG(s.repair_cost_cop * s.repair_cost_cop)
             - AVG(s.repair_cost_cop) * AVG(s.repair_cost_cop), 0) AS varianza_aprox
FROM sesion_diagnostico AS s
JOIN vehiculo AS v ON v.placa = s.placa
WHERE s.repair_cost_cop > 0
GROUP BY v.marca
ORDER BY costo_promedio_cop DESC, v.marca;
"""


def extraer(ruta: Path) -> pd.DataFrame:
    """E: lee el CSV tal cual (todo como texto, sin interpretar nada)."""
    df = pd.read_csv(ruta, dtype=str)
    print(f"[extraer] {len(df)} filas x {df.shape[1]} columnas desde {ruta.name}")
    return df


def limpiar_datos(raw: pd.DataFrame) -> tuple[pd.DataFrame, dict, dict]:
    """T: aplica la limpieza de la semana 9 y mide antes/después."""
    antes = perfilar(pd.read_csv(AQUI / "data" / "diagnostics_raw.csv"), "antes")
    limpio = limpiar(raw)
    despues = perfilar(limpio, "después")
    print(f"[limpiar] filas {antes['filas']} -> {despues['filas']} | "
          f"nulos {antes['nulos_totales']} -> {despues['nulos_totales']} | "
          f"duplicados {antes['filas_duplicadas']} -> {despues['filas_duplicadas']}")
    return limpio, antes, despues


def cargar(limpio: pd.DataFrame):
    """L: guarda el CSV limpio y lo carga en el modelo relacional normalizado."""
    SALIDAS.mkdir(exist_ok=True)
    csv = SALIDAS / "diagnostics_clean.csv"
    limpio.to_csv(csv, index=False)
    con = construir_db(csv, SALIDAS / "diagnostics.db")
    assert con.execute("PRAGMA foreign_key_check").fetchall() == [], "llaves foráneas rotas"
    print(f"[cargar] {conteos(con)}")
    return con, csv


def analizar(con, limpio: pd.DataFrame):
    # ---- Análisis 1 (SQL): costo promedio de reparación por marca, solo sesiones con cobro
    a1 = pd.read_sql_query(SQL_ANALISIS_1, con)
    a1["desv_est_aprox"] = a1["varianza_aprox"].clip(lower=0).pow(0.5).round(0)
    a1 = a1.drop(columns="varianza_aprox")

    # ---- Análisis 2 (pandas): frecuencia de refrigerante >= 95 °C por vehículo
    por_vehiculo = (limpio.groupby(["brand", "model"])
                    .agg(sesiones=("session_id", "count"),
                         temp_alta=("coolant_temp_c", lambda s: int((s >= 95).sum())))
                    .reset_index())
    por_vehiculo["pct_sesiones_temp_alta"] = (
        100 * por_vehiculo["temp_alta"] / por_vehiculo["sesiones"]).round(1)
    a2 = (por_vehiculo.rename(columns={"brand": "marca", "model": "modelo"})
          .sort_values(["pct_sesiones_temp_alta", "marca"], ascending=[False, True])
          .reset_index(drop=True))

    # Chequeo cruzado: el análisis 1 en pandas debe dar lo mismo que en SQL
    chk = (limpio[limpio["repair_cost_cop"] > 0].groupby("brand")["repair_cost_cop"]
           .agg(["count", "mean"]).round(0))
    chk_sql = a1.set_index("marca")[["sesiones_con_cobro", "costo_promedio_cop"]]
    assert (chk["count"].sort_index().values == chk_sql["sesiones_con_cobro"].sort_index().values).all()
    assert (chk["mean"].sort_index().values == chk_sql["costo_promedio_cop"].sort_index().values).all()

    a1.to_csv(SALIDAS / "analisis1_costo_por_marca.csv", index=False)
    a2.to_csv(SALIDAS / "analisis2_temperatura_alta_por_vehiculo.csv", index=False)
    print("[analizar] análisis 1 (SQL) y 2 (pandas) listos; verificación cruzada OK")
    return a1, a2


def graficar(a1: pd.DataFrame, a2: pd.DataFrame) -> None:
    fig, ejes = plt.subplots(1, 2, figsize=(14, 5.2))
    d1 = a1.sort_values("costo_promedio_cop")
    ejes[0].barh(d1["marca"], d1["costo_promedio_cop"] / 1000, color=TEAL)
    ejes[0].set_xlabel("Costo promedio de reparación (miles de COP)")
    ejes[0].set_title("Análisis 1 · Costo promedio por marca\n(solo sesiones con costo > 0)", fontsize=11)
    for i, (v, n) in enumerate(zip(d1["costo_promedio_cop"], d1["sesiones_con_cobro"])):
        ejes[0].text(v / 1000 + 4, i, f"{v/1000:,.0f}  (n={n})", va="center", fontsize=8)
    ejes[0].set_xlim(0, d1["costo_promedio_cop"].max() / 1000 * 1.25)

    d2 = a2.assign(vehiculo=a2["marca"] + " " + a2["modelo"]).sort_values("pct_sesiones_temp_alta")
    ejes[1].barh(d2["vehiculo"], d2["pct_sesiones_temp_alta"], color="#c4650a")
    ejes[1].set_xlabel("% de sus sesiones con refrigerante ≥ 95 °C")
    ejes[1].set_title("Análisis 2 · Temperatura alta por vehículo", fontsize=11)
    for i, (p, n) in enumerate(zip(d2["pct_sesiones_temp_alta"], d2["sesiones"])):
        ejes[1].text(p + 0.6, i, f"{p:.1f} %  (n={n})", va="center", fontsize=8)
    ejes[1].set_xlim(0, d2["pct_sesiones_temp_alta"].max() * 1.3)
    for ax in ejes:
        ax.spines[["top", "right"]].set_visible(False)
    fig.suptitle("Mini-proyecto · Taller de diagnóstico · Juan David Caviedes Cortes",
                 fontsize=12, fontweight="bold")
    fig.tight_layout()
    fig.savefig(SALIDAS / "analisis.png", dpi=140, facecolor="white")


def main() -> None:
    raw = extraer(AQUI / "data" / "diagnostics_raw.csv")
    limpio, antes, despues = limpiar_datos(raw)
    con, _ = cargar(limpio)
    a1, a2 = analizar(con, limpio)
    graficar(a1, a2)
    print("\nAnálisis 1 (SQL):\n" + a1.to_string(index=False))
    print("\nAnálisis 2 (pandas):\n" + a2.to_string(index=False))


if __name__ == "__main__":
    main()
