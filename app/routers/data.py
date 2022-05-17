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

    # get distance value (number) from string
    kilometres = float(re.sub('[^0-9.]', "", distance).replace(",", ""))

    # get distance type (string) from string
    if len(distance) > 1:
        # distance data may not be in English
        try:
            distance_type = re.search(r'[a-zA-Z]+', distance).group()
        except AttributeError:
            log(log.ERROR, "[distance value not in english] distance[%s]", distance)
            distance_type = 'km'
            # convert miles to kilometres
        if distance_type == 'miles':
            kilometres = float(re.findall("[-+]?\d*\.\d+|\d+", distance)[0]) * 1.60934

    # get gas price from specific town or country
    cost = get_gas_cost(gas_file_name=gasType, town_name=town) or "wrong_gas_type"
    # if the input data is incorrect, then sends a message to the front about this
    if cost == "wrong_gas_type":
        return CalculationResult(gas_price=0, c02_kg=0, error=cost)

    # get specific car mileage and co2 consumption
    mileage = get_car_mileage(make=make, model=model, year=year) or "wrong_car_options"
    if mileage == "wrong_car_options":
        return CalculationResult(gas_price=0, c02_kg=0, error=mileage)

    # Cents per litre to dollar per litre
    price_per_litr = cost / 100
    litre_consump = kilometres / mileage[0]
    result_price = format(litre_consump * price_per_litr, ".2f")

    # CO2 consumption in grams to kg for the whole route
    c02_kg = format(mileage[1] / 1000 * kilometres, ".2f")

    log(log.INFO, "[CALCULATION RESULTS] result_price[%s], c02_kg[%s]", result_price, c02_kg)
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
