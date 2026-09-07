from typing import Annotated

from fastapi import APIRouter, Depends

from app.api.dependencies import get_investigation_service
from app.models.investigation import (
    InvestigationRequest,
    InvestigationResult,
)
from app.services.investigation import InvestigationService

router = APIRouter(prefix="/ai", tags=["investigation"])


@router.post(
    "/investigate-issue",
    response_model=InvestigationResult,
)
async def investigate_issue(
    request: InvestigationRequest,
    service: Annotated[
        InvestigationService,
        Depends(get_investigation_service),
    ],
) -> InvestigationResult:
    return await service.investigate(request)
