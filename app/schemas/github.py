from typing import List

from pydantic import BaseModel


class GitHupApiResponse(BaseModel):
    stars: int
    forks: int
    owner: str
    name: str


class GitHupApiOrgResponse(BaseModel):
    items: List[GitHupApiResponse]
