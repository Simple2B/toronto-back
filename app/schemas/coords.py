from pydantic import BaseModel

class Coords(BaseModel):
    start: str
    end: str


class CoordsResults(BaseModel):
    rows: list
