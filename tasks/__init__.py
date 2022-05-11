import os
from invoke import task
import urllib.request

from app.config import settings
from app.schemas import UpdateExcel

# flake8: noqa F501
DOWNLOAD_SET = (
    UpdateExcel(
        url="https://www2.nrcan.gc.ca/eneene/sources/pripri/prices_bycity_e.cfm?priceYear=2022&productID=1&locationID=91,92,93,26,94,95,76,17&downloadXLS",
        file_name="Regular.xlsx",
    ),
    UpdateExcel(
        url="https://www2.nrcan.gc.ca/eneene/sources/pripri/prices_bycity_e.cfm?priceYear=2022&productID=2&locationID=91,92,93,26,94,95,76,17&downloadXLS",
        file_name="Mid-Grade.xlsx",
    ),
    UpdateExcel(
        url="https://www2.nrcan.gc.ca/eneene/sources/pripri/prices_bycity_e.cfm?priceYear=2022&productID=3&locationID=91,92,93,26,94,95,76,17&downloadXLS",
        file_name="Premium.xlsx",
    ),
    UpdateExcel(
        url="https://www2.nrcan.gc.ca/eneene/sources/pripri/prices_bycity_e.cfm?priceYear=2022&productID=5&locationID=91,92,93,26,94,95,76,17&downloadXLS",
        file_name="Diesel.xlsx",
    ),
)


@task
def update(c):
    """Update Excel files (command: inv update)"""
    print("Updating...")
    for i in DOWNLOAD_SET:
        urllib.request.urlretrieve(i.url, os.path.join(settings.DATA_DIR, i.file_name))
        print("Updated: ", i.file_name)
    print("Finished")
