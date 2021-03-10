from typing import List

from pydantic import BaseModel


class PopularResponseModel(BaseModel):
    score: int
    owner: str
    name: str
    is_popular: bool


class PopularResponseListModel(BaseModel):
    items: List[PopularResponseModel]
