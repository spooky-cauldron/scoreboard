from pydantic import BaseModel, Field


class PostScoreboardBody(BaseModel):
    name: str = Field(min_length=1, max_length=1024)
    teams: list[str] = Field(min_length=1, max_length=1024)


class PostScoreboardResponse(PostScoreboardBody):
    id: str


class PatchTeamScoreBody(BaseModel):
    amount: int


class PatchTeamScoreResponse(BaseModel):
    score: int
