from fastapi import APIRouter

from app.schemas import CalculationResult
from app.services import get_gas_cost, get_gas_mileage


router = APIRouter()


@router.get("/gas_consumption", response_model=CalculationResult, tags=["Calculation"])
def gas_consumption(year: int, make: str, model: str, town: str):
    """Calculate gas consumption"""
    cost = get_gas_cost(file_name="Regular_Gas.xlsx", town_name=town)
    mileage = get_gas_mileage(model=model, make=make, year=year)
    return CalculationResult(gas_price=cost, mileage=mileage)
