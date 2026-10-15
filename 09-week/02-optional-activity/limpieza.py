"""Semana 9 - Limpieza del dataset de diagnósticos automotrices.

Autor: Juan David Caviedes Cortes (davidcaviedes499-ship-it)

Uso:
    python limpieza.py                      # lee data/diagnostics_raw.csv
    python limpieza.py ruta/raw.csv ruta/salida_dir

Genera:
    data/diagnostics_clean.csv          dataset limpio
    reportes/antes_despues.json         métricas antes/después
    reportes/antes_despues.md           la misma evidencia en tabla
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

AQUI = Path(__file__).resolve().parent

# Rangos físicos plausibles. Un valor fuera de rango se trata como atípico
# (error de captura), se marca como nulo y se imputa.
RANGOS = {
    "rpm": (300, 2000),            # ralentí/diagnóstico en vacío; -50 y 9999 son errores
    "coolant_temp_c": (0, 130),    # 250 °C y -40 °C son imposibles para refrigerante
    "battery_v": (9, 16),
    "map_kpa": (15, 110),
}
COLS_NUM = list(RANGOS)
COLS_TEXTO = ["session_id", "plate", "brand", "model", "fuel", "dtc_code",
              "symptom", "technician"]


def perfilar(df: pd.DataFrame, etiqueta: str) -> dict:
    """Métricas de calidad de un DataFrame (sirve para antes y después)."""
    perfil = {
        "etiqueta": etiqueta,
        "filas": int(len(df)),
        "columnas": int(df.shape[1]),
        "nulos_totales": int(df.isna().sum().sum()),
        "nulos_por_columna": {c: int(n) for c, n in df.isna().sum().items() if n},
        "filas_duplicadas": int(df.duplicated().sum()),
        "session_id_repetidos": int(df["session_id"].duplicated().sum()),
        "tipos": {c: str(t) for c, t in df.dtypes.items()},
        "valores_distintos": {
            "plate": int(df["plate"].nunique()),
            "brand": int(df["brand"].nunique()),
            "technician": int(df["technician"].nunique()),
            "dtc_code": int(df["dtc_code"].nunique()),
        },
    }
    atipicos = {}
    for col, (lo, hi) in RANGOS.items():
        x = pd.to_numeric(df[col], errors="coerce")
        atipicos[col] = int(((x < lo) | (x > hi)).sum())
    perfil["atipicos_fuera_de_rango"] = atipicos
    # formatos de fecha distintos (ISO, dd/mm/aaaa, d-m-aaaa)
    f = df["date"].astype(str).str.strip()
    perfil["formatos_de_fecha"] = {
        "ISO aaaa-mm-dd": int(f.str.fullmatch(r"\d{4}-\d{2}-\d{2}").sum()),
        "dd/mm/aaaa": int(f.str.fullmatch(r"\d{1,2}/\d{1,2}/\d{4}").sum()),
        "d-m-aaaa": int(f.str.fullmatch(r"\d{1,2}-\d{1,2}-\d{4}").sum()),
    }
    return perfil


def _parsear_fechas(s: pd.Series) -> pd.Series:
    """Unifica los tres formatos de fecha. Los no-ISO son día primero."""
    s = s.astype(str).str.strip()
    iso = s.str.fullmatch(r"\d{4}-\d{2}-\d{2}")
    out = pd.Series(pd.NaT, index=s.index, dtype="datetime64[ns]")
    out[iso] = pd.to_datetime(s[iso], format="%Y-%m-%d")
    resto = s[~iso].str.extract(r"^(\d{1,2})[/-](\d{1,2})[/-](\d{4})$")
    resto = resto.astype(float)
    out[~iso] = pd.to_datetime(
        {"year": resto[2], "month": resto[1], "day": resto[0]}, errors="coerce"
    )
    return out


def limpiar(raw: pd.DataFrame) -> pd.DataFrame:
    df = raw.copy()

    # 1) Unicidad: filas idénticas duplicadas (12 en el dataset original)
    df = df.drop_duplicates()

    # 2) Texto: quitar espacios y normalizar mayúsculas/minúsculas
    for c in COLS_TEXTO:
        df[c] = df[c].astype("string").str.strip()
    df["plate"] = df["plate"].str.upper().str.replace(" ", "-", regex=False)
    df["brand"] = df["brand"].str.title()
    df["technician"] = df["technician"].str.title()
    df["dtc_code"] = df["dtc_code"].str.upper()
    df["symptom"] = df["symptom"].fillna("Unknown")   # categoría explícita

    # 3) Tipos: fecha (3 formatos) y números guardados como texto
    df["date"] = _parsear_fechas(df["date"]).dt.strftime("%Y-%m-%d")
    for c in ("mileage_km", "repair_cost_cop"):
        df[c] = (df[c].astype(str).str.replace(r"[^\d]", "", regex=True)
                 .astype("int64"))
    df["year"] = df["year"].astype("int64")

    # 4) Atípicos -> nulos, y 5) imputación con la mediana por combustible
    for col, (lo, hi) in RANGOS.items():
        x = pd.to_numeric(df[col], errors="coerce")
        x = x.mask((x < lo) | (x > hi))
        df[col] = x.fillna(x.groupby(df["fuel"]).transform("median"))
        df[col] = df[col].astype("float64")

    # 6) Red de seguridad: tras normalizar, ¿quedó algún session_id repetido?
    df = df.drop_duplicates(subset="session_id", keep="first")
    return df.reset_index(drop=True)


def _tabla_md(antes: dict, despues: dict) -> str:
    filas = [
        ("Filas", antes["filas"], despues["filas"]),
        ("Celdas nulas", antes["nulos_totales"], despues["nulos_totales"]),
        ("Filas duplicadas", antes["filas_duplicadas"], despues["filas_duplicadas"]),
        ("session_id repetidos", antes["session_id_repetidos"],
         despues["session_id_repetidos"]),
        ("Atípicos fuera de rango (total)",
         sum(antes["atipicos_fuera_de_rango"].values()),
         sum(despues["atipicos_fuera_de_rango"].values())),
        ("Placas distintas (mismo vehículo escrito distinto)",
         antes["valores_distintos"]["plate"], despues["valores_distintos"]["plate"]),
        ("Marcas distintas (mayúsculas/espacios)",
         antes["valores_distintos"]["brand"], despues["valores_distintos"]["brand"]),
        ("Técnicos distintos (mayúsculas)",
         antes["valores_distintos"]["technician"],
         despues["valores_distintos"]["technician"]),
        ("Formatos de fecha en uso",
         sum(1 for v in antes["formatos_de_fecha"].values() if v),
         sum(1 for v in despues["formatos_de_fecha"].values() if v)),
    ]
    out = ["| Métrica | Antes | Después |", "|---|---:|---:|"]
    out += [f"| {m} | {a} | {d} |" for m, a, d in filas]
    out += ["", "Nulos por columna (antes): "
            + ", ".join(f"`{c}`={n}" for c, n in antes["nulos_por_columna"].items())]
    return "\n".join(out)


def main(raw_path: Path, salida: Path) -> pd.DataFrame:
    raw = pd.read_csv(raw_path, dtype=str)
    # los numéricos limpios se perfilan sobre su lectura "natural"
    raw_tipado = pd.read_csv(raw_path)
    antes = perfilar(raw_tipado, "antes")
    limpio = limpiar(raw)
    despues = perfilar(limpio, "después")

    (salida / "data").mkdir(parents=True, exist_ok=True)
    (salida / "reportes").mkdir(parents=True, exist_ok=True)
    limpio.to_csv(salida / "data" / "diagnostics_clean.csv", index=False)
    (salida / "reportes" / "antes_despues.json").write_text(
        json.dumps({"antes": antes, "despues": despues}, indent=2,
                   ensure_ascii=False), encoding="utf-8")
    (salida / "reportes" / "antes_despues.md").write_text(
        _tabla_md(antes, despues) + "\n", encoding="utf-8")
    print(_tabla_md(antes, despues))
    return limpio


if __name__ == "__main__":
    raw_p = Path(sys.argv[1]) if len(sys.argv) > 1 else AQUI / "data" / "diagnostics_raw.csv"
    out_d = Path(sys.argv[2]) if len(sys.argv) > 2 else AQUI
    main(raw_p, out_d)
