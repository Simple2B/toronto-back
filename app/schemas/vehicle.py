from pydantic import BaseModel


class VehicleData(BaseModel):
    year: int
    make: str
    model: str


class CalculationData(VehicleData):
    town: str


class CalculationResult(BaseModel):
    gas_price: float
    c02_kg: float


class MakeList(BaseModel):
    filterer_make_list: list


class ModelList(BaseModel):
    filterer_model_list: list


class YearList(BaseModel):
    vehicle_year_list: list
