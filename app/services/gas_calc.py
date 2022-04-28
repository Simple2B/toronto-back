import os
import pandas as pd

from app.config import settings


def get_gas_cost(gas_file_name: str, town_name: str):
    file_path = os.path.join(settings.DATA_DIR, gas_file_name)
    data = pd.read_excel(os.path.join(settings.DATA_DIR, gas_file_name))
    # assert data
    town_price = {}
    HORIZON_OFFSET = 1
    VERTICAL_TOWN_OFFSET = 2
    TOWN_OFFSET = 4

    town_num = (len(data.columns) - HORIZON_OFFSET) // TOWN_OFFSET
    last_date_line_index = len(data) - 2
    for town_index in range(town_num):
        town_column = data[data.columns[HORIZON_OFFSET + (town_index * TOWN_OFFSET)]]
        name = town_column[VERTICAL_TOWN_OFFSET]
        price = town_column[last_date_line_index]
        town_price[name] = price

    if town_name in town_price:
        return town_price[town_name]


def get_gas_mileage(model: str, make: str, year: int):
    FILE_NAME = os.path.join("vehicle", "vehicles.xlsx")
    data = pd.read_excel(os.path.join(settings.DATA_DIR, FILE_NAME))
    assert len(data)
    lines = data.loc[
        (data["Make"] == make) & (data["Model"] == model) & (data["Year"] == year)
    ]
    if not len(lines):
        return None
    mean = lines[["City", "Highway"]].mean()
    return (mean.City + mean.Highway) / 2
