import urllib.request
import time

# flake8: noqa F501


while True:
    urllib.request.urlretrieve(
        "https://www2.nrcan.gc.ca/eneene/sources/pripri/prices_bycity_e.cfm?priceYear=2022&productID=1&locationID=91,92,93,26,94,95,76,17&downloadXLS",
        "Regular Gas.xlsx",
    )
    urllib.request.urlretrieve(
        "https://www2.nrcan.gc.ca/eneene/sources/pripri/prices_bycity_e.cfm?priceYear=2022&productID=2&locationID=91,92,93,26,94,95,76,17&downloadXLS",
        "Mid-Grade Gas.xlsx",
    )
    urllib.request.urlretrieve(
        "https://www2.nrcan.gc.ca/eneene/sources/pripri/prices_bycity_e.cfm?priceYear=2022&productID=3&locationID=91,92,93,26,94,95,76,17&downloadXLS",
        "Premium Gas.xlsx",
    )
    urllib.request.urlretrieve(
        "https://www2.nrcan.gc.ca/eneene/sources/pripri/prices_bycity_e.cfm?priceYear=2022&productID=5&locationID=91,92,93,26,94,95,76,17&downloadXLS",
        "Diesel.xlsx",
    )
    time.sleep(86400)  # 86400 seconds = 24 hours.
