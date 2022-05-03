from fastapi import APIRouter

from app.schemas import CalculationResult
from app.services import get_gas_cost, get_gas_mileage
from app.services.gas_calc import get_vehicle_data_list
import re


router = APIRouter()


@router.get("/gas_consumption", response_model=CalculationResult, tags=["Calculation"])
def gas_consumption(model: str, make: str, year: int, town: str, distance: str, gasType: str):
    """Calculate gas consumption"""

    kilometres = int(re.search(r'\d+', distance).group())

    cost = get_gas_cost(gas_file_name=gasType, town_name=town) or 0
    mileage = get_gas_mileage(model=model, make=make, year=year) or 0
    vehicle_data_list = get_vehicle_data_list()

    # Cents per litre to dollar per litre
    price_per_litr = cost / 100
    result_price = format(kilometres * mileage / 100 * price_per_litr, ".2f")

    # CO2 calculalate
    # 1 liter of petrol weighs 750 grammes. Petrol consists for 87% of carbon, or 652 grammes of carbon per liter of petrol. In order to combust this carbon to CO2, 1740 grammes of oxygen is needed. The sum is then 652 + 1740 = 2392 grammes of CO2/liter of petrol.

    # An average consumption of 5 liters/100 km then corresponds to 5 l x 2392 g/l / 100 (per km) = 120 g CO2/km.
    # https://ecoscore.be/en/info/ecoscore/co2
    # https://www.fleetnews.co.uk/costs/carbon-footprint-calculator/
    c02_kg = format(kilometres * mileage / 100 * 2.392, ".2f")

    return CalculationResult(gas_price=result_price, vehicle_data_list=vehicle_data_list, c02_kg=c02_kg)
