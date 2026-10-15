"""Semana 6 - Dibuja el ERD del taller de diagnóstico (genera erd.png).

Autor: Juan David Caviedes Cortes (davidcaviedes499-ship-it)
"""
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Rectangle

AQUI = Path(__file__).resolve().parent
ALTO_FILA = 0.36
COLOR_ENC = "#0b6e75"      # verde azulado institucional
COLOR_PK = "#fff4c2"
COLOR_FK = "#e2f1f3"

TABLAS = {
    "vehiculo": (0.4, 9.4, 3.4, [
        ("PK", "placa", "TEXT"), ("", "marca", "TEXT"), ("", "modelo", "TEXT"),
        ("", "anio", "INTEGER"), ("", "combustible", "TEXT")]),
    "tecnico": (12.2, 9.4, 3.4, [
        ("PK", "tecnico_id", "INTEGER"), ("", "nombre", "TEXT UNIQUE")]),
    "sesion_diagnostico": (6.1, 9.9, 3.8, [
        ("PK", "session_id", "TEXT"), ("", "fecha", "TEXT (ISO)"),
        ("FK", "placa", "-> vehiculo"), ("FK", "tecnico_id", "-> tecnico"),
        ("", "rpm", "REAL"), ("", "coolant_temp_c", "REAL"),
        ("", "battery_v", "REAL"), ("", "map_kpa", "REAL"),
        ("", "mileage_km", "INTEGER"), ("", "repair_cost_cop", "INTEGER")]),
    "codigo_dtc": (0.4, 4.6, 3.4, [
        ("PK", "dtc_code", "TEXT"), ("", "descripcion", "TEXT")]),
    "sesion_dtc": (4.4, 4.6, 3.2, [
        ("PK,FK", "session_id", "-> sesion"), ("PK,FK", "dtc_code", "-> codigo_dtc")]),
    "sesion_sintoma": (8.4, 4.6, 3.2, [
        ("PK,FK", "session_id", "-> sesion"), ("PK,FK", "sintoma_id", "-> sintoma")]),
    "sintoma": (12.2, 4.6, 3.4, [
        ("PK", "sintoma_id", "INTEGER"), ("", "descripcion", "TEXT UNIQUE")]),
}


def dibujar_tabla(ax, nombre, x, y_top, ancho, cols):
    alto = ALTO_FILA * (len(cols) + 1)
    ax.add_patch(Rectangle((x, y_top - alto), ancho, alto, fc="white",
                           ec="#333", lw=1.2, zorder=2))
    ax.add_patch(Rectangle((x, y_top - ALTO_FILA), ancho, ALTO_FILA,
                           fc=COLOR_ENC, ec="#333", lw=1.2, zorder=3))
    ax.text(x + ancho / 2, y_top - ALTO_FILA / 2, nombre, color="white",
            ha="center", va="center", fontsize=10, fontweight="bold", zorder=4)
    for i, (clave, col, tipo) in enumerate(cols):
        yf = y_top - ALTO_FILA * (i + 2)
        if clave:
            ax.add_patch(Rectangle((x, yf), ancho, ALTO_FILA,
                                   fc=COLOR_PK if "PK" in clave else COLOR_FK,
                                   ec="none", zorder=3))
        ax.text(x + 0.08, yf + ALTO_FILA / 2, clave, fontsize=7.5, va="center",
                color="#8a5a00", fontweight="bold", zorder=4)
        ax.text(x + 0.85, yf + ALTO_FILA / 2, col, fontsize=8.5, va="center", zorder=4)
        ax.text(x + ancho - 0.08, yf + ALTO_FILA / 2, tipo, fontsize=7,
                va="center", ha="right", color="#555", zorder=4)
    return {"x": x, "y_top": y_top, "w": ancho, "h": alto}


def main():
    fig, ax = plt.subplots(figsize=(16, 9))
    ax.set_xlim(0, 16)
    ax.set_ylim(2.2, 10.4)
    ax.axis("off")
    caja = {n: dibujar_tabla(ax, n, *t) for n, t in TABLAS.items()}

    def borde(n, lado, frac=0.5):
        c = caja[n]
        if lado == "izq":
            return c["x"], c["y_top"] - c["h"] * frac
        if lado == "der":
            return c["x"] + c["w"], c["y_top"] - c["h"] * frac
        if lado == "arr":
            return c["x"] + c["w"] * frac, c["y_top"]
        return c["x"] + c["w"] * frac, c["y_top"] - c["h"]

    def unir(p, q, a, b, via=None, vertical=False):
        if vertical:
            xs = [p[0]] + [v[0] for v in via] + [q[0]]
            ys = [p[1]] + [v[1] for v in via] + [q[1]]
            ax.plot(xs, ys, color="#333", lw=1.4, zorder=1)
            ax.text(p[0] + 0.12, p[1] - 0.32, a, fontsize=10, fontweight="bold", color=COLOR_ENC)
            ax.text(q[0] + 0.12, q[1] + 0.12, b, fontsize=10, fontweight="bold", color=COLOR_ENC)
            return
        xs = [p[0]] + ([v[0] for v in via] if via else []) + [q[0]]
        ys = [p[1]] + ([v[1] for v in via] if via else []) + [q[1]]
        ax.plot(xs, ys, color="#333", lw=1.4, zorder=1)
        ax.text(p[0] + (0.12 if p[0] <= q[0] else -0.12), p[1] + 0.14, a, fontsize=10,
                fontweight="bold", color=COLOR_ENC, ha="left" if p[0] <= q[0] else "right")
        ax.text(q[0] + (-0.12 if p[0] <= q[0] else 0.12), q[1] + 0.14, b, fontsize=10,
                fontweight="bold", color=COLOR_ENC, ha="right" if p[0] <= q[0] else "left")

    # 1:N hacia sesion_diagnostico (lado "1" primero)
    unir(borde("vehiculo", "der", 0.3), borde("sesion_diagnostico", "izq", 0.3), "1", "N")
    unir(borde("tecnico", "izq", 0.3), borde("sesion_diagnostico", "der", 0.3), "1", "N")
    # sesion -> tablas intermedias (1:N), y catálogo -> intermedias (1:N)
    s_abajo = borde("sesion_diagnostico", "aba", 0.30)
    unir(s_abajo, borde("sesion_dtc", "arr", 0.5), "1", "N",
         via=[(s_abajo[0], 5.3), (borde("sesion_dtc", "arr", 0.5)[0], 5.3)], vertical=True)
    s_abajo2 = borde("sesion_diagnostico", "aba", 0.70)
    unir(s_abajo2, borde("sesion_sintoma", "arr", 0.5), "1", "N",
         via=[(s_abajo2[0], 5.3), (borde("sesion_sintoma", "arr", 0.5)[0], 5.3)], vertical=True)
    unir(borde("codigo_dtc", "der", 0.5), borde("sesion_dtc", "izq", 0.5), "1", "N")
    unir(borde("sintoma", "izq", 0.5), borde("sesion_sintoma", "der", 0.5), "1", "N")

    ax.text(8, 10.25, "ERD - Taller de diagnóstico automotriz (relación N:M resuelta con "
            "sesion_dtc y sesion_sintoma)", ha="center", fontsize=12, fontweight="bold")
    ax.text(8, 2.45, "PK = llave primaria   FK = llave foránea   1:N = uno a muchos   "
            "Autor: Juan David Caviedes Cortes", ha="center", fontsize=8.5, color="#444")
    fig.savefig(AQUI / "erd.png", dpi=150, bbox_inches="tight", facecolor="white")
    print("erd.png generado")


if __name__ == "__main__":
    main()
