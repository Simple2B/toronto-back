from fastapi import APIRouter

from app.schemas import CalculationResult
from app.schemas.vehicle import MakeList, ModelList, YearList
from app.services import get_gas_cost, get_gas_mileage
from app.services.gas_calc import get_make_list, get_model_list, get_vehicle_year
import re
from app.logger import log


router = APIRouter()


@router.get("/gas_consumption", response_model=CalculationResult, tags=["Calculation"])
def gas_consumption(model: str, make: str, year: int, town: str, distance: str, gasType: str):
    """Calculate gas consumption"""

    # some data in db can be type int but they come like str
    try:
        model = int(model)
    except ValueError:
        pass

    # get distance value from string
    kilometres = float(re.sub('[^0-9.]', "", distance).replace(",", ""))

    # get distance type from string
    if len(distance) > 1:
        # data may not be in English
        try:
            distance_type = re.search(r'[a-zA-Z]+', distance).group()
        except AttributeError:
            log(log.ERROR, "[distance value not in english] distance[%s]", distance)
            distance_type = 'km'
            # convert miles to kilometres
        if distance_type == 'miles':
            kilometres = float(re.findall("[-+]?\d*\.\d+|\d+", distance)[0]) * 1.60934

    cost = get_gas_cost(gas_file_name=gasType, town_name=town) or 0
    mileage = get_gas_mileage(model=model, make=make, year=year) or 0

    # Cents per litre to dollar per litre
    price_per_litr = cost / 100
    result_price = format(kilometres * mileage / 100 * price_per_litr, ".2f")

    # CO2 calculalate
    # 1 liter of petrol weighs 750 grammes. Petrol consists for 87% of carbon,
    # or 652 grammes of carbon per liter of petrol.
    # In order to combust this carbon to CO2, 1740 grammes of oxygen is needed.
    # The sum is then 652 + 1740 = 2392 grammes of CO2/liter of petrol.

    # An average consumption of 5 liters/100 km then corresponds to 5 l x 2392 g/l / 100 (per km) = 120 g CO2/km.
    # https://ecoscore.be/en/info/ecoscore/co2
    # https://www.fleetnews.co.uk/costs/carbon-footprint-calculator/
    c02_kg = format(kilometres * mileage / 100 * 2.392, ".2f")

    return CalculationResult(gas_price=result_price, c02_kg=c02_kg)


@router.get("/make", response_model=MakeList, tags=["Vehicle"])
def get_make():
    """Get all makes"""
    filterer_make_list = get_make_list()
    return MakeList(filterer_make_list=filterer_make_list)


@router.get("/model", response_model=ModelList, tags=["Vehicle"])
def get_model(make: str):
    """Get all models by make"""
    filterer_model_list = get_model_list(make=make)
    return ModelList(filterer_model_list=filterer_model_list)


@router.get("/year", response_model=YearList, tags=["Vehicle"])
def get_year(model):
    """Get years by car model"""
    try:
        model = int(model)
    except ValueError:
        pass

    vehicle_year_list = get_vehicle_year(model)
    return YearList(vehicle_year_list=vehicle_year_list)
