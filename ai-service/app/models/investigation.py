from pydantic import BaseModel, Field


class RepositoryContext(BaseModel):
    owner: str
    name: str
    default_branch: str = "main"


class IssueContext(BaseModel):
    number: int
    title: str
    body: str | None = None


class InvestigationRequest(BaseModel):
    repository: RepositoryContext
    issue: IssueContext


class PossibleCause(BaseModel):
    title: str
    explanation: str
    confidence: float = Field(ge=0.0, le=1.0)


class InvestigationStep(BaseModel):
    order: int = Field(ge=1)
    description: str


class SuggestedTest(BaseModel):
    name: str
    description: str


class InvestigationResponse(BaseModel):
    summary: str
    possible_causes: list[PossibleCause]
    investigation_steps: list[InvestigationStep]
    assumptions: list[str]
    suggested_tests: list[SuggestedTest]
