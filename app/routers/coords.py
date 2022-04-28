# # enter your api key here
# api_key ='AIzaSyBNR4gaeTTLzWBDmBTUF4LLzWbcDrWHBis'

# import requests
# from fastapi import APIRouter
# import json

# from app.schemas.coords import Coords, CoordsResults


# router = APIRouter()

# @router.get("/coords", response_model=CoordsResults)
# def get_coords(start: str, end: str):
#     url = f"https://maps.googleapis.com/maps/api/distancematrix/json?origins={start}&destinations={end}&units=imperial&key=AIzaSyBNR4gaeTTLzWBDmBTUF4LLzWbcDrWHBis"

#     payload={}
#     headers = {}

#     response = requests.request("GET", url, headers=headers, data=payload)

#     json_object = json.loads(response.text)

#     dist = json_object['rows'][0]['elements'][0]['distance']
#     duration = json_object['rows'][0]['elements'][0]['duration']

#     return CoordsResults(rows=json_object['rows'])


# start = "44.5173836,-78.0513245"
# end = "44.0376686,-79.2980807"

