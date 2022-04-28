from fastapi import APIRouter

from app.schemas import CalculationData, CalculationResult


router = APIRouter()


@router.get("/gas_consumption", response_model=CalculationResult, tags=["Calculation"])
def get_user(year: int, make: str, model: str, town: str):
    """Calculate gas consumption"""

    return CalculationResult(gas=56.7)
