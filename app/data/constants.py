from __future__ import annotations

EXPECTED_COLUMNS = [
    "timestamp",
    "TP2",
    "TP3",
    "H1",
    "DV_pressure",
    "Reservoirs",
    "Motor_current",
    "Oil_temperature",
    "COMP",
    "DV_electric",
    "Towers",
    "MPG",
    "LPS",
    "Pressure_switch",
    "Oil_Level",
    "Caudal_impulse",
]

ANALOG_SENSORS = [
    "TP2",
    "TP3",
    "H1",
    "DV_pressure",
    "Reservoirs",
    "Motor_current",
    "Oil_temperature",
]

DIGITAL_SIGNALS = [
    "COMP",
    "DV_electric",
    "Towers",
    "MPG",
    "LPS",
    "Pressure_switch",
    "Oil_Level",
    "Caudal_impulse",
]

FAILURES = [
    {
        "failure_id": 1,
        "start_time": "2020-04-18 00:00:00",
        "end_time": "2020-04-18 23:59:00",
        "failure_type": "Air Leak",
        "severity": "High stress",
        "maintenance_note": None,
    },
    {
        "failure_id": 2,
        "start_time": "2020-05-29 23:30:00",
        "end_time": "2020-05-30 06:00:00",
        "failure_type": "Air Leak",
        "severity": "High stress",
        "maintenance_note": "Maintenance on 30Apr at 12:00",
    },
    {
        "failure_id": 3,
        "start_time": "2020-06-05 10:00:00",
        "end_time": "2020-06-07 14:30:00",
        "failure_type": "Air Leak",
        "severity": "High stress",
        "maintenance_note": "Maintenance on 8Jun at 16:00",
    },
    {
        "failure_id": 4,
        "start_time": "2020-07-15 14:30:00",
        "end_time": "2020-07-15 19:00:00",
        "failure_type": "Air Leak",
        "severity": "High stress",
        "maintenance_note": "Maintenance on 16Jul at 00:00",
    },
]
