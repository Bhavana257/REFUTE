from pydantic import BaseModel


class ClaimRequest(BaseModel):
    claim: str


class ClaimResponse(BaseModel):
    verdict: str
    argument: str
    reasoning: str
    counter_argument: str
