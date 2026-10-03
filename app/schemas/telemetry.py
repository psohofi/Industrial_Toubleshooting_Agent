from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class SensorValues(BaseModel):
    model_config = ConfigDict(extra="forbid")

    # Analog sensors
    TP2: float
    TP3: float
    H1: float
    DV_pressure: float
    Reservoirs: float
    Motor_Current: float
    Oil_Temperature: float

    # Digital sensors
    COMP: int = Field(ge=0, le=1)
    DV_electric: int = Field(ge=0, le=1)
    TOWERS: int = Field(ge=0, le=1)
    MPG: int = Field(ge=0, le=1)
    LPS: int = Field(ge=0, le=1)
    Pressure_Switch: int = Field(ge=0, le=1)
    Oil_Level: int = Field(ge=0, le=1)

    # Pulse counter
    Caudal_Impulse: int = Field(ge=0)


class SensorEvent(BaseModel):
    model_config = ConfigDict(extra="forbid")

    asset_id: str = Field(
        min_length=1,
        json_schema_extra={
            "example": "metro-apu-001"
        },
    )

    timestamp: datetime

    sensors: SensorValues


class TelemetryResponse(BaseModel):
    status: str
    asset_id: str
    timestamp: datetime