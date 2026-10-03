from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_health():
    response = client.get("/health")

    assert response.status_code == 200

    assert response.json() == {
        "status": "healthy"
    }


def test_receive_valid_telemetry():
    payload = {
        "asset_id": "metro-apu-001",

        "timestamp": "2020-06-05T10:01:15Z",

        "sensors": {
            "TP2": 8.41,
            "TP3": 8.08,
            "H1": 8.02,

            "DV_pressure": 0.0,

            "Reservoirs": 8.05,

            "Motor_Current": 7.1,

            "Oil_Temperature": 68.5,

            "COMP": 0,

            "DV_electric": 1,

            "TOWERS": 0,

            "MPG": 0,

            "LPS": 0,

            "Pressure_Switch": 0,

            "Oil_Level": 0,

            "Caudal_Impulse": 1,
        },
    }

    response = client.post(
        "/api/v1/telemetry",
        json=payload,
    )

    print(response.json())

    assert response.status_code == 200

    body = response.json()

    assert body["status"] == "processed"

    assert body["asset_id"] == "metro-apu-001"


def test_invalid_digital_sensor():
    payload = {
        "asset_id": "metro-apu-001",

        "timestamp": "2020-06-05T10:01:15Z",

        "sensors": {
            "TP2": 8.41,
            "TP3": 8.08,
            "H1": 8.02,

            "DV_pressure": 0.0,

            "Reservoirs": 8.05,

            "Motor_Current": 7.1,

            "Oil_Temperature": 68.5,

            "COMP": 5,

            "DV_electric": 1,

            "TOWERS": 0,

            "MPG": 0,

            "LPS": 0,

            "Pressure_Switch": 0,

            "Oil_Level": 0,

            "Caudal_Impulse": 1,
        },
    }

    response = client.post(
        "/api/v1/telemetry",
        json=payload,
    )

    assert response.status_code == 422