from app.services import get_gas_cost


def test_gas_cost():
    TOWN_NAME = "Barrie"
    TOWN_NAME = "Toronto"
    FILE_NAME = "Mid-Grade_Gas.xlsx"
    res = get_gas_cost(FILE_NAME, TOWN_NAME)
    assert res
