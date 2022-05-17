from typing import Optional
from pydantic import BaseModel


class VehicleData(BaseModel):
    year: int
    make: str
    model: str


class CalculationData(VehicleData):
    town: str


class CalculationResult(BaseModel):
    gas_price: Optional[float]
    c02_kg: Optional[float]
    error: Optional[str]


class MakeList(BaseModel):
    filterer_make_list: list


class ModelList(BaseModel):
    filterer_model_list: list


class YearList(BaseModel):
    vehicle_year_list: list
