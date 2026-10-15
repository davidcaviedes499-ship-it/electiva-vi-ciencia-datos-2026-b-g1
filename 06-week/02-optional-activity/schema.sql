-- Semana 6 - Modelo relacional del taller de diagnóstico automotriz
-- Autor: Juan David Caviedes Cortes (davidcaviedes499-ship-it)
-- Motor: SQLite 3 (las llaves foráneas se activan con PRAGMA foreign_keys = ON)

PRAGMA foreign_keys = ON;

-- Un vehículo se describe una sola vez (placa -> marca, modelo, año, combustible)
CREATE TABLE vehiculo (
    placa        TEXT PRIMARY KEY,
    marca        TEXT NOT NULL,
    modelo       TEXT NOT NULL,
    anio         INTEGER NOT NULL CHECK (anio BETWEEN 1990 AND 2030),
    combustible  TEXT NOT NULL CHECK (combustible IN ('gasoline', 'diesel'))
);

CREATE TABLE tecnico (
    tecnico_id   INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre       TEXT NOT NULL UNIQUE
);

-- Catálogo de códigos de falla OBD-II (DTC)
CREATE TABLE codigo_dtc (
    dtc_code     TEXT PRIMARY KEY,
    descripcion  TEXT NOT NULL
);

CREATE TABLE sintoma (
    sintoma_id   INTEGER PRIMARY KEY AUTOINCREMENT,
    descripcion  TEXT NOT NULL UNIQUE
);

-- Hecho central: una visita de diagnóstico
CREATE TABLE sesion_diagnostico (
    session_id        TEXT PRIMARY KEY,
    fecha             TEXT NOT NULL,                     -- ISO aaaa-mm-dd
    placa             TEXT NOT NULL REFERENCES vehiculo(placa),
    tecnico_id        INTEGER NOT NULL REFERENCES tecnico(tecnico_id),
    rpm               REAL,
    coolant_temp_c    REAL,
    battery_v         REAL,
    map_kpa           REAL,
    mileage_km        INTEGER CHECK (mileage_km >= 0),
    repair_cost_cop   INTEGER CHECK (repair_cost_cop >= 0)
);

-- N:M sesión <-> código DTC (una sesión puede registrar varios códigos y
-- un código aparece en muchas sesiones)
CREATE TABLE sesion_dtc (
    session_id  TEXT NOT NULL REFERENCES sesion_diagnostico(session_id),
    dtc_code    TEXT NOT NULL REFERENCES codigo_dtc(dtc_code),
    PRIMARY KEY (session_id, dtc_code)
);

-- N:M sesión <-> síntoma reportado
CREATE TABLE sesion_sintoma (
    session_id  TEXT NOT NULL REFERENCES sesion_diagnostico(session_id),
    sintoma_id  INTEGER NOT NULL REFERENCES sintoma(sintoma_id),
    PRIMARY KEY (session_id, sintoma_id)
);

CREATE INDEX idx_sesion_placa ON sesion_diagnostico(placa);
CREATE INDEX idx_sesion_fecha ON sesion_diagnostico(fecha);
