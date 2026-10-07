| Metric | Before | After |
|---|---|---|
| Rows | 252 | 240 |
| Null cells | 91 | 0 |
| Duplicate rows | 12 | 0 |

|                 |   nulls_before |   nulls_after | dtype_before   | dtype_after    |
|:----------------|---------------:|--------------:|:---------------|:---------------|
| session_id      |              0 |             0 | str            | str            |
| date            |              0 |             0 | str            | datetime64[us] |
| plate           |              0 |             0 | str            | str            |
| brand           |              0 |             0 | str            | str            |
| model           |              0 |             0 | str            | str            |
| year            |              0 |             0 | int64          | int64          |
| fuel            |              0 |             0 | str            | str            |
| dtc_code        |              0 |             0 | str            | str            |
| symptom         |             10 |             0 | str            | str            |
| rpm             |             26 |             0 | float64        | float64        |
| coolant_temp_c  |             21 |             0 | float64        | float64        |
| battery_v       |             18 |             0 | float64        | float64        |
| map_kpa         |             16 |             0 | float64        | float64        |
| mileage_km      |              0 |             0 | str            | int64          |
| technician      |              0 |             0 | str            | str            |
| repair_cost_cop |              0 |             0 | str            | int64          |

Outliers converted to null before imputation: {'rpm': 6, 'coolant_temp_c': 5}
