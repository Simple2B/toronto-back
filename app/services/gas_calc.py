import os
import pandas as pd
import requests
import json

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


def get_make_list():
    FILE_NAME = os.path.join("vehicle", "vehicles.xlsx")
    FILE_INFO = os.path.join("vehicle", "vehicles_year.xlsx")

    data = pd.read_excel(os.path.join(settings.DATA_DIR, FILE_NAME))
    data_two = pd.read_excel(os.path.join(settings.DATA_DIR, FILE_INFO))

    year = data_two["Year"].values.tolist()
    car = data["Make"].values.tolist()
    mod = data["Model"].values.tolist()

    mylist = list(dict.fromkeys(car))
    modList = list(dict.fromkeys(mod))
    yearList = sorted(list(dict.fromkeys(year)))

    li = []
    li2 = []
    list_year = []
    for c in mylist:
        li.append(dict(value=c, label=c))

    for c in modList:
        li2.append(dict(value=c, label=c))

    for c in yearList:
        list_year.append(dict(value=c, label=c))


    return [li, li2, list_year]


def get_coords(start: str, end: str):
    url = f"https://maps.googleapis.com/maps/api/distancematrix/json?origins={start}&destinations={end}&units=imperial&key=Api_key"

    payload={}
    headers = {}

    response = requests.request("GET", url, headers=headers, data=payload)

    json_object = json.loads(response.text)

    # dist = json_object['rows'][0]['elements'][0]['distance']['value'] / 10000
    dist = format(json_object['rows'][0]['elements'][0]['distance']['value'] / 10000, ".2f")
    duration = json_object['rows'][0]['elements'][0]['duration']['value']

    return [dist, duration]
