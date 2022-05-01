from fastapi import APIRouter

from app.schemas import CalculationResult
from app.services import get_gas_cost, get_gas_mileage
from app.services.gas_calc import get_coords, get_vehicle_data_list


router = APIRouter()


@router.get("/gas_consumption", response_model=CalculationResult, tags=["Calculation"])
def gas_consumption(year: int, make: str, model: str, town: str, start: str, end: str):
    """Calculate gas consumption"""

    cost = get_gas_cost(gas_file_name="Regular_Gas.xlsx", town_name=town) or 0
    mileage = get_gas_mileage(model=model, make=make, year=year) or 0
    coords = get_coords(start=start, end=end)
    vehicle_data_list = get_vehicle_data_list()

    return CalculationResult(gas_price=cost, mileage=mileage, coords=coords, vehicle_data_list=vehicle_data_list)
