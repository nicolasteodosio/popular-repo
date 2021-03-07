from pydantic import BaseModel


class GitHupApiResponse(BaseModel):
    stars: int
    forks: int
    owner: str
    name: str
