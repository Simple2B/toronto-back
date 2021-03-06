from app.services import get_gas_cost, get_car_mileage
from app.services.gas_calc import get_make_list, get_model_list, get_vehicle_year


def test_gas_cost():
    TOWN_NAME = "Barrie"
    TOWN_NAME = "Toronto"
    FILE_NAME = "Mid-Grade"
    res = get_gas_cost(FILE_NAME, TOWN_NAME)
    assert res


def test_gas_consumption():
    MAKE = "BMW"
    MODEL = "M8 Competition Coupe"
    YEAR = 2022
    res = get_car_mileage(model=MODEL, make=MAKE, year=YEAR)
    assert res[0]
    assert res[1]


def test_make_list():
    res = get_make_list()
    assert res


def test_model_list():
    MAKE = "Acura"
    response = get_model_list(make=MAKE)
    assert response


def test_year_list():
    MAKE = "Ford"
    MODEL = "Transit Connect Van FWD"
    response = get_vehicle_year(make=MAKE, model=MODEL)
    assert response
