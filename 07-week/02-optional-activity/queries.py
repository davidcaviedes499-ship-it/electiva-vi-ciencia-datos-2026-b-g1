"""Semana 7 - Ejecuta las 3 consultas SQL y reproduce el GROUP BY en pandas.

Autor: Juan David Caviedes Cortes (davidcaviedes499-ship-it)

Uso:
    python queries.py

Requiere la carpeta 06-week al lado de esta (usa su modelo y su CSV limpio).
Escribe resultados.md con las salidas.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

import pandas as pd

AQUI = Path(__file__).resolve().parent
SEMANA6 = AQUI.parent / "06-week"
sys.path.insert(0, str(SEMANA6))
from build_db import construir_db  # noqa: E402


def cargar_consultas(ruta: Path) -> dict[str, str]:
    """Separa queries.sql en {Q1: sql, Q2: sql, Q3: sql} usando los marcadores [Qn]."""
    texto = ruta.read_text(encoding="utf-8")
    partes = re.split(r"^-- \[(Q\d)\].*$", texto, flags=re.M)
    return {partes[i]: partes[i + 1].strip() for i in range(1, len(partes), 2)}


def tabla_md(df: pd.DataFrame) -> str:
    cab = "| " + " | ".join(df.columns) + " |"
    sep = "|" + "|".join("---" for _ in df.columns) + "|"
    filas = ["| " + " | ".join(str(v) for v in r) + " |" for r in df.itertuples(index=False)]
    return "\n".join([cab, sep, *filas])


def main() -> None:
    csv = SEMANA6 / "data" / "diagnostics_clean.csv"
    con = construir_db(csv)               # base en memoria
    consultas = cargar_consultas(AQUI / "queries.sql")
    plano = pd.read_csv(csv)              # versión plana para pandas

    sql = {k: pd.read_sql_query(q, con) for k, q in consultas.items()}

    # ---- Equivalente pandas de Q1 (WHERE) --------------------------------
    p1 = (plano.loc[plano["battery_v"] < 12.0, ["session_id", "date", "plate", "battery_v"]]
          .rename(columns={"date": "fecha", "plate": "placa"})
          .sort_values(["battery_v", "session_id"]).reset_index(drop=True))
    pd.testing.assert_frame_equal(sql["Q1"], p1, check_dtype=False)

    # ---- Equivalente pandas de Q3 (GROUP BY) -----------------------------
    p3 = (plano.groupby("dtc_code")["repair_cost_cop"]
          .agg(sesiones="count", costo_promedio_cop="mean", costo_total_cop="sum")
          .reset_index())
    p3["costo_promedio_cop"] = p3["costo_promedio_cop"].round(0)
    p3 = p3.sort_values(["costo_promedio_cop", "dtc_code"],
                        ascending=[False, True]).reset_index(drop=True)
    pd.testing.assert_frame_equal(sql["Q3"], p3, check_dtype=False)

    print(f"Q1: {len(sql['Q1'])} sesiones con batería < 12 V  (SQL == pandas)")
    print("Q2: top 10 de reparaciones más costosas")
    print(sql["Q2"].to_string(index=False))
    print("Q3: por código DTC  (SQL == pandas)")
    print(sql["Q3"].to_string(index=False))

    explicacion = {
        "Q1": "Filtra con `WHERE` las visitas con batería baja. Sirve para priorizar revisión del sistema de carga.",
        "Q2": "Une 5 tablas con `JOIN` para mostrar, en lugar de llaves, el vehículo, el técnico y la descripción de la falla.",
        "Q3": "Agrupa con `GROUP BY` por código de falla para comparar frecuencia y costo promedio.",
    }
    md = ["# Resultados de la semana 7", "",
          "Generado por `queries.py`. Las consultas Q1 y Q3 se verificaron contra su "
          "equivalente en pandas con `assert_frame_equal`.", ""]
    for k in ("Q1", "Q2", "Q3"):
        md += [f"## {k}", "", explicacion[k], "", "```sql", consultas[k], "```", "",
               f"Filas devueltas: {len(sql[k])}", "", tabla_md(sql[k]), ""]
    (AQUI / "resultados.md").write_text("\n".join(md), encoding="utf-8")


if __name__ == "__main__":
    main()
