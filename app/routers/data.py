from fastapi import APIRouter

from app.schemas import CalculationResult
from app.schemas.vehicle import MakeList, ModelList, YearList
from app.services import get_gas_cost, get_car_mileage
from app.services.gas_calc import get_make_list, get_model_list, get_vehicle_year
import re
from app.logger import log


router = APIRouter()


@router.get("/gas_consumption", response_model=CalculationResult, tags=["Calculation"])
def gas_consumption(make: str, model: str, year: int, gasType: str, distance: str, town: str):
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

    cost = get_gas_cost(gas_file_name=gasType, town_name=town) or "wrong_gas_type"
    if cost == "wrong_gas_type":
        return CalculationResult(gas_price=0, c02_kg=0, error=cost)

    mileage = get_car_mileage(make=make, model=model, year=year) or "wrong_car_options"
    if mileage == "wrong_car_options":
        return CalculationResult(gas_price=0, c02_kg=0, error=mileage)

    # Cents per litre to dollar per litre
    price_per_litr = cost / 100
    litre_consump = kilometres / mileage[0]
    result_price = format(litre_consump * price_per_litr, ".2f")

    # CO2 calculalate
    # 1 liter of petrol weighs 750 grammes. Petrol consists for 87% of carbon,
    # or 652 grammes of carbon per liter of petrol.
    # In order to combust this carbon to CO2, 1740 grammes of oxygen is needed.
    # The sum is then 652 + 1740 = 2392 grammes of CO2/liter of petrol.

    # An average consumption of 5 liters/100 km then corresponds to 5 l x 2392 g/l / 100 (per km) = 120 g CO2/km.
    # https://ecoscore.be/en/info/ecoscore/co2
    # https://www.fleetnews.co.uk/costs/carbon-footprint-calculator/
    c02_kg = format(mileage[1] / 1000 * kilometres, ".2f")

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
def get_year(model, make):
    """Get years by car model"""
    try:
        model = int(model)
    except ValueError:
        pass

    vehicle_year_list = get_vehicle_year(model=model, make=make)
    return YearList(vehicle_year_list=vehicle_year_list)
