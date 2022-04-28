from app.services import get_gas_cost, get_gas_mileage


def test_gas_cost():
    TOWN_NAME = "Barrie"
    TOWN_NAME = "Toronto"
    FILE_NAME = "Mid-Grade_Gas.xlsx"
    res = get_gas_cost(FILE_NAME, TOWN_NAME)
    assert res


def test_gas_consumption():
    MAKE = "BMW"
    MODEL = "M8 Competition Coupe"
    YEAR = 2022
    res = get_gas_mileage(model=MODEL, make=MAKE, year=YEAR)
    assert res
