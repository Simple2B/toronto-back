import pytest
from typing import Generator
from fastapi.testclient import TestClient

from app.setup import create_app
from app.schemas import CalculationResult


@pytest.fixture()
def client() -> Generator:
    app = create_app()
    with TestClient(app) as c:
        yield c


def test_auth(client: TestClient):
    response = client.get(
        "/api/gas_consumption",
        params=dict(
            year=2022, make="BMW", model="M8 Competition Coupe", town="Toronto"
        ),
    )
    assert response.status_code == 200
    res: CalculationResult = CalculationResult.parse_obj(response.json())
    assert res.gas_price
    assert res.mileage

    response = client.get(
        "/api/gas_consumption",
        params=dict(year=2022, make="BMW", model="X5", town="Toronto"),
    )
    assert response.status_code == 200
    res: CalculationResult = CalculationResult.parse_obj(response.json())
    assert res.gas_price
    assert not res.mileage

    response = client.get(
        "/api/gas_consumption",
        params=dict(year=2022, make="BMW", model="X5", town="Ternopol"),
    )
    assert response.status_code == 200
    res: CalculationResult = CalculationResult.parse_obj(response.json())
    assert not res.gas_price
    assert not res.mileage
