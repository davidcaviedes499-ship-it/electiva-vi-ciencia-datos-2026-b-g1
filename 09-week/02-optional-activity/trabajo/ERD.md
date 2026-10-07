# ERD – Electronic vehicle fault diagnosis

```mermaid
erDiagram
    VEHICLE ||--o{ DIAGNOSTIC_SESSION : "undergoes (1:N)"
    TECHNICIAN ||--o{ DIAGNOSTIC_SESSION : "performs (1:N)"
    DIAGNOSTIC_SESSION ||--o{ SESSION_DTC : "records (1:N)"
    DTC ||--o{ SESSION_DTC : "appears in (1:N)"

    VEHICLE {
        string plate PK
        string brand
        string model
        int year
        string fuel
    }
    TECHNICIAN {
        int technician_id PK
        string full_name
    }
    DIAGNOSTIC_SESSION {
        string session_id PK
        string plate FK
        int technician_id FK
        date date
        int mileage_km
        string symptom
        int rpm
        float coolant_temp_c
        float battery_v
        float map_kpa
        int repair_cost_cop
    }
    DTC {
        string dtc_code PK
        string description
    }
    SESSION_DTC {
        string session_id PK, FK
        string dtc_code PK, FK
    }
```

## Cardinalities
Notation and cardinality types (1:1, 1:N, N:M with a junction table) follow CORHUILA (2026a); full reference in the README.

| Relationship | Cardinality | Meaning |
|---|---|---|
| VEHICLE – DIAGNOSTIC_SESSION | 1:N | A vehicle can have many sessions; each session belongs to one vehicle. |
| TECHNICIAN – DIAGNOSTIC_SESSION | 1:N | A technician performs many sessions; each session has one technician. |
| DIAGNOSTIC_SESSION – DTC | N:M (via SESSION_DTC) | A session can store several DTCs and a DTC appears in many sessions. |

In the CSV each session carries a single primary DTC, so SESSION_DTC currently holds one row per session; the model already supports several.
