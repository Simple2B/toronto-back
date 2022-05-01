from pydantic import BaseModel


class VehicleData(BaseModel):
    year: int
    make: str
    model: str


class CalculationData(VehicleData):
    town: str


class CalculationResult(BaseModel):
    gas_price: float
    mileage: float
    coords: list
    vehicle_data_list: list
