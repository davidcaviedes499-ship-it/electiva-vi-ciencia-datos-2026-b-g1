"""Semana 6 - Carga el CSV limpio en el modelo relacional normalizado (SQLite).

Autor: Juan David Caviedes Cortes (davidcaviedes499-ship-it)

Uso:
    python build_db.py                 # crea diagnostics.db junto a este archivo

Otras semanas importan `construir_db` para reutilizar el mismo modelo.
"""
from __future__ import annotations

import sqlite3
import sys
from pathlib import Path

import pandas as pd

AQUI = Path(__file__).resolve().parent

# Descripciones genéricas OBD-II (SAE J2012) de los 7 códigos presentes en los datos
DESCRIPCION_DTC = {
    "P0101": "Circuito del sensor de flujo de aire (MAF): rango/desempeño",
    "P0118": "Sensor de temperatura del refrigerante: señal alta",
    "P0171": "Sistema demasiado pobre (mezcla pobre), banco 1",
    "P0299": "Turbo/supercargador: presión de sobrealimentación baja",
    "P0300": "Fallo de encendido aleatorio/múltiple detectado",
    "P0420": "Eficiencia del catalizador por debajo del umbral, banco 1",
    "P0562": "Voltaje del sistema bajo",
}


def construir_db(csv_limpio: Path, db_path: Path | None = None) -> sqlite3.Connection:
    """Crea la base (en archivo, o en memoria si db_path es None) y la llena."""
    df = pd.read_csv(csv_limpio)

    # Comprobación de normalización: la placa determina marca/modelo/año/combustible
    vehiculos = df[["plate", "brand", "model", "year", "fuel"]].drop_duplicates()
    assert vehiculos["plate"].is_unique, "una placa con atributos distintos"
    desconocidos = set(df["dtc_code"]) - set(DESCRIPCION_DTC)
    assert not desconocidos, f"DTC sin descripción: {desconocidos}"

    if db_path is not None and Path(db_path).exists():
        Path(db_path).unlink()
    con = sqlite3.connect(":memory:" if db_path is None else str(db_path))
    con.executescript((AQUI / "schema.sql").read_text(encoding="utf-8"))

    con.executemany(
        "INSERT INTO vehiculo VALUES (?,?,?,?,?)",
        vehiculos.itertuples(index=False, name=None))
    con.executemany(
        "INSERT INTO tecnico(nombre) VALUES (?)",
        [(n,) for n in sorted(df["technician"].unique())])
    con.executemany(
        "INSERT INTO codigo_dtc VALUES (?,?)", sorted(DESCRIPCION_DTC.items()))
    con.executemany(
        "INSERT INTO sintoma(descripcion) VALUES (?)",
        [(s,) for s in sorted(df["symptom"].unique())])

    tec = dict(con.execute("SELECT nombre, tecnico_id FROM tecnico"))
    sin = dict(con.execute("SELECT descripcion, sintoma_id FROM sintoma"))
    con.executemany(
        "INSERT INTO sesion_diagnostico VALUES (?,?,?,?,?,?,?,?,?,?)",
        [(r.session_id, r.date, r.plate, tec[r.technician], r.rpm,
          r.coolant_temp_c, r.battery_v, r.map_kpa, int(r.mileage_km),
          int(r.repair_cost_cop)) for r in df.itertuples()])
    con.executemany("INSERT INTO sesion_dtc VALUES (?,?)",
                    df[["session_id", "dtc_code"]].itertuples(index=False, name=None))
    con.executemany(
        "INSERT INTO sesion_sintoma VALUES (?,?)",
        [(r.session_id, sin[r.symptom]) for r in df.itertuples()])
    con.commit()
    return con


def conteos(con: sqlite3.Connection) -> dict:
    tablas = ["vehiculo", "tecnico", "codigo_dtc", "sintoma",
              "sesion_diagnostico", "sesion_dtc", "sesion_sintoma"]
    return {t: con.execute(f"SELECT COUNT(*) FROM {t}").fetchone()[0] for t in tablas}


if __name__ == "__main__":
    csv = Path(sys.argv[1]) if len(sys.argv) > 1 else AQUI / "data" / "diagnostics_clean.csv"
    destino = AQUI / "diagnostics.db"
    con = construir_db(csv, destino)
    fallas = con.execute("PRAGMA foreign_key_check").fetchall()
    print("Filas por tabla:", conteos(con))
    print("Violaciones de llave foránea:", len(fallas))
