"""Semana 8 - Consume una API pública con `requests` y muestra 3 registros.

Autor: Juan David Caviedes Cortes (davidcaviedes499-ship-it)

API: NHTSA vPIC (gobierno de EE. UU., pública y sin llave).
Endpoint: modelos de una marca para un año.

Uso:
    python consumir_api.py                    # Mazda 2020 (CX-5 del dataset)
    python consumir_api.py toyota 2015

Si no hay conexión (o la API falla), el script usa la muestra guardada en
api_sample.json y lo avisa; así la actividad es reproducible sin internet.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import pandas as pd
import requests

AQUI = Path(__file__).resolve().parent
URL = ("https://vpic.nhtsa.dot.gov/api/vehicles/GetModelsForMakeYear/"
       "make/{marca}/modelyear/{anio}")


def extraer(marca: str, anio: int) -> tuple[dict, str]:
    """E de ETL: pide los datos. Devuelve (json, origen)."""
    try:
        resp = requests.get(URL.format(marca=marca, anio=anio),
                            params={"format": "json"}, timeout=10)
        resp.raise_for_status()
        return resp.json(), "API en vivo"
    except requests.RequestException as err:
        print(f"[aviso] no se pudo consultar la API ({type(err).__name__}); "
              "uso la muestra guardada (api_sample.json).")
        muestra = json.loads((AQUI / "api_sample.json").read_text(encoding="utf-8"))
        return muestra, "muestra guardada (captura del 2026-10-14)"


def transformar(datos: dict) -> pd.DataFrame:
    """T de ETL: de JSON anidado a tabla con nombres de columna del proyecto."""
    df = pd.DataFrame(datos["Results"])
    return df.rename(columns={"Make_Name": "marca", "Model_Name": "modelo",
                              "Make_ID": "marca_id", "Model_ID": "modelo_id"})


def main() -> None:
    marca = sys.argv[1] if len(sys.argv) > 1 else "mazda"
    anio = int(sys.argv[2]) if len(sys.argv) > 2 else 2020
    datos, origen = extraer(marca, anio)
    tabla = transformar(datos)
    print(f"Origen: {origen} | registros que informa la API (Count): {datos.get('Count')}")
    print("Primeros 3 registros:")
    print(tabla.head(3).to_string(index=False))
    # L de ETL: se guarda el resultado para usarlo después
    tabla.head(3).to_csv(AQUI / "muestra_api_3_registros.csv", index=False)


if __name__ == "__main__":
    main()
