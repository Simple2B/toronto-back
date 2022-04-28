from pydantic import BaseModel


class UpdateExcel(BaseModel):
    url: str
    file_name: str
