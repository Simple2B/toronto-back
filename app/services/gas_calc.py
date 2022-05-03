import os
import pandas as pd
import requests
import json

from app.config import settings


def get_gas_cost(gas_file_name: str, town_name: str):
    if not len(gas_file_name):
        return ''

    file_path = os.path.join(settings.DATA_DIR, gas_file_name)
    data = pd.read_excel(os.path.join(settings.DATA_DIR, gas_file_name))
    # assert data
    town_price = {}
    HORIZON_OFFSET = 1
    VERTICAL_TOWN_OFFSET = 2
    TOWN_OFFSET = 4
    # 8
    town_num = (len(data.columns) - HORIZON_OFFSET) // TOWN_OFFSET
    last_date_line_index = len(data) - 2

    for town_index in range(town_num):
        town_column = data[data.columns[HORIZON_OFFSET + (town_index * TOWN_OFFSET)]]
        name = town_column[VERTICAL_TOWN_OFFSET]
        price = town_column[last_date_line_index]
        town_price[name] = price

    if town_name == "Average":
        avg = round(sum(town_price.values()) / town_num, 2)
        return avg

    if town_name in town_price:
        return town_price[town_name]


def get_gas_mileage(model: str, make: str, year: int):
    """Get Miles per gallon (MPL)"""
    FILE_NAME = os.path.join("vehicle", "vehicles.xlsx")
    data = pd.read_excel(os.path.join(settings.DATA_DIR, FILE_NAME))
    assert len(data)
    lines = data.loc[
        (data["Make"] == make) & (data["Model"] == model) & (data["Year"] == year)
    ]
    if not len(lines):
        return None
    mean = lines[["City", "Highway"]].mean()

    avg_mileage = (mean.City + mean.Highway) / 2

    # Convert Miles per gallon (MPL) to kilometres per litre (KPL)
    kpl = avg_mileage / 2.352

    return kpl


def get_vehicle_data_list():
    FILE_NAME = os.path.join("vehicle", "vehicles.xlsx")
    FILE_INFO = os.path.join("vehicle", "vehicles_year.xlsx")

    data = pd.read_excel(os.path.join(settings.DATA_DIR, FILE_NAME))
    data_two = pd.read_excel(os.path.join(settings.DATA_DIR, FILE_INFO))

    model = data["Model"].values.tolist()
    make = data["Make"].values.tolist()
    year = data_two["Year"].values.tolist()

    sorted_model = list(dict.fromkeys(model))
    sortec_make = list(dict.fromkeys(make))
    sorted_year = sorted(list(dict.fromkeys(year)), reverse=True)

    model_list = []
    make_list = []
    year_list = []
    for index in sorted_model:
        model_list.append(dict(value=index, label=index))

    for index in sortec_make:
        make_list.append(dict(value=index, label=index))

    for index in sorted_year:
        year_list.append(dict(value=index, label=index))


    return [model_list, make_list, year_list]
