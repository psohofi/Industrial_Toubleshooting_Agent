from fastapi import APIRouter, status

from app.schemas.telemetry import (
    SensorEvent,
    TelemetryResponse,
)


router = APIRouter(
    prefix="/api/v1",
    tags=["telemetry"],
)


@router.post(
    "/telemetry",
    response_model=TelemetryResponse,
    status_code=status.HTTP_200_OK,
)
async def receive_telemetry(
    event: SensorEvent,
) -> TelemetryResponse:

    return TelemetryResponse(
        status="processed",
        asset_id=event.asset_id,
        timestamp=event.timestamp,
    )