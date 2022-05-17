import os
import pandas as pd

from app.config import settings
from app.logger import log

TOWNS_NAME = ["UK", "United Kingdom"]
# Gasoline Prices in the United Kingdom decreased to 2.04 USD/Liter in April from 2.14 USD/Liter in March of 2022
# This info take from https://tradingeconomics.com/united-kingdom/gasoline-prices
# cents per liter
UK_GAS_PRICE = 204

def get_gas_cost(gas_file_name: str, town_name: str):
    log(log.INFO, "[get_gas_cost] with file name [%s], town name[%s]", gas_file_name, town_name)

    if town_name in TOWNS_NAME:
        log(log.INFO, "[if UK or United Kingdom] town name[%s]", town_name)
        if gas_file_name == "UK Prices":
            return UK_GAS_PRICE
        else:
            return 0

    if not len(gas_file_name) or gas_file_name == "UK Prices":
        log(log.INFO, "[if gas_file_name empty or it's UK Prices] gas_file_name[%s]", gas_file_name)
        return ''

    data = pd.read_excel(os.path.join(settings.DATA_DIR, gas_file_name + ".xlsx"))
    # assert data
    town_price = {}
    HORIZON_OFFSET = 1
    VERTICAL_TOWN_OFFSET = 2
    TOWN_OFFSET = 4
    # 8
    town_num = (len(data.columns) - HORIZON_OFFSET) // TOWN_OFFSET
    last_date_line_index = len(data) - 2

    # calculate price for each city
    for town_index in range(town_num):
        town_column = data[data.columns[HORIZON_OFFSET + (town_index * TOWN_OFFSET)]]
        name = town_column[VERTICAL_TOWN_OFFSET]
        price = town_column[last_date_line_index]
        town_price[name] = price

    # if none of the 8 cities is selected, calculate the average price
    # between them for any others on the planet
    if town_name == "Average":
        log(log.INFO, "[if no specified city is selected] town_name[%s]", town_name)
        avg = round(sum(town_price.values()) / town_num, 2)
        return avg

    if town_name in town_price:
        log(log.INFO, "[if town_name in town_price] town_name[%s], town_price[town_name][%s]", town_name, town_price[town_name])
        return town_price[town_name]


def get_car_mileage(make: str, model: str, year: int):
    """Get Miles per gallon (MPL)"""
    # FILE_NAME = os.path.join("vehicle", "vehicles.xlsx")
    # data = pd.read_excel(os.path.join(settings.DATA_DIR, FILE_NAME))
    data_frame = pd.read_pickle('all_vehicles.pkl')

    assert len(data_frame)
    lines = data_frame.loc[
        (data_frame["Make"] == make) & (data_frame["Model"] == model) & (data_frame["Year"] == year)
    ]
    if not len(lines):
        return None
    # get average value from same vehicle with different mileage and emissions
    mean = lines[["City", "Highway"]].mean()
    co2 = lines["co2TailpipeGpm"].mean()

    avg_mileage = (mean.City + mean.Highway) / 2

    # Convert Miles per gallon (MPL) to kilometres per litre (KPL)
    kpl = avg_mileage / 2.352

    return [kpl, co2]


def get_make_list():
    # FILE_NAME = os.path.join("vehicle", "all_vehicles-binary.xlsb")
    # data = pd.read_excel(os.path.join(settings.DATA_DIR, FILE_NAME))

    # data.to_pickle('all_vehicles.pkl')    #to save the dataframe to file.pkl
    data_frame = pd.read_pickle('all_vehicles.pkl') #to load file.pkl back to the dataframe
    make = sorted(data_frame["Make"].values.tolist())

    # remove duplicates
    sorted_make = list(dict.fromkeys(make))

    # this is for the selector on the frontend to display the data
    make_list = []
    for index in sorted_make:
        make_list.append(dict(value=index, label=index))

    return make_list


def get_model_list(make: str):
    # FILE_NAME = os.path.join("vehicle", "vehicles.xlsx")
    # data = pd.read_excel(os.path.join(settings.DATA_DIR, FILE_NAME))
    data_frame = pd.read_pickle('all_vehicles.pkl')

    # Select second and third columns (make, model)
    make_model = data_frame[data_frame.columns[1:3]].values.tolist()

    # remove duplicates from list of lists
    remover_model_dup = [list(tupl) for tupl in { tuple(item) for item in make_model }]

    # get models for a specific car and sort
    filter_by_make = [i for i in remover_model_dup if i[0] == make]

    # this is for the selector on the frontend to display the data
    model_list = []
    for index in filter_by_make:
        model_list.append(dict(value=index[1], label=index[1]))

    return model_list


def get_vehicle_year(model, make):
    # FILE_INFO = os.path.join("vehicle", "vehicles_year.xlsx")
    # data_two = pd.read_excel(os.path.join(settings.DATA_DIR, FILE_INFO))
    # year = data_two["Year"].values.tolist()
    data_frame = pd.read_pickle('all_vehicles.pkl')

    # Select first and third columns (year, model)
    model_year = data_frame[data_frame.columns[0:3]].values.tolist()

    # remove duplicates from list of lists
    remover_model_dup = [list(tupl) for tupl in { tuple(item) for item in model_year }]

    # get car year for a specific model and descending sort
    filter_by_model = sorted([i for i in remover_model_dup if model in i], reverse=True)

    # some models have the same makes
    rid_extra_models = [i for i in filter_by_model if i[1] == make]

    # this is for the selector on the frontend to display the data
    year_list = []
    for index in rid_extra_models:
        year_list.append(dict(value=index[0], label=index[0]))

    return year_list
