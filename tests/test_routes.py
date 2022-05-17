import pytest
from typing import Generator
from fastapi.testclient import TestClient
from app.schemas.vehicle import MakeList, ModelList, YearList

from app.setup import create_app
from app.schemas import CalculationResult


@pytest.fixture()
def client() -> Generator:
    app = create_app()
    with TestClient(app) as c:
        yield c

# gas_consumption(make: str, model: str, year: int, gasType: str, distance: str, town: str):
def test_input_data(client: TestClient):
    response = client.get(
        "/api/gas_consumption",
        params=dict(
            make="Honda", model="Odyssey", year=2022, gasType="Regular", distance="100 km", town="Toronto"
        ),
    )
    assert response.status_code == 200
    res: CalculationResult = CalculationResult.parse_obj(response.json())
    assert res.gas_price
    assert res.c02_kg

    response = client.get(
        "/api/gas_consumption",
        params=dict(
            make="Acura", model="Odyssey", year=2022, gasType="Regular", distance="100 km", town="Toronto"),
    )
    assert response.status_code == 200
    res: CalculationResult = CalculationResult.parse_obj(response.json())
    assert not res.gas_price
    assert not res.c02_kg
    assert res.error == "wrong_car_options"

    response = client.get(
        "/api/gas_consumption",
        params=dict(
            make="Honda", model="Odyssey", year=2022, gasType="UK Prices", distance="100 km", town="Toronto"),
    )
    assert response.status_code == 200
    res: CalculationResult = CalculationResult.parse_obj(response.json())
    assert not res.gas_price
    assert not res.c02_kg
    assert res.error == "wrong_gas_type"


def test_get_make_list(client: TestClient):
    response = client.get("/api/make")
    assert response.status_code == 200
    res: MakeList = MakeList.parse_obj(response.json())
    assert res.filterer_make_list


def test_get_model_list(client: TestClient):
    response = client.get("/api/model", params=dict(make="Honda"))
    assert response.status_code == 200
    res: ModelList = ModelList.parse_obj(response.json())
    assert res.filterer_model_list


def test_get_year_list(client: TestClient):
    response = client.get("/api/year", params=dict(make="Honda", model="Odyssey"))
    assert response.status_code == 200
    res: YearList = YearList.parse_obj(response.json())
    assert res.vehicle_year_list
