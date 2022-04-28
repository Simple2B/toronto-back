from pydantic import BaseModel


class VehicleData(BaseModel):
    year: int
    make: str
    model: str


class CalculationData(VehicleData):
    town: str


class CalculationResult(BaseModel):
    gas: float
