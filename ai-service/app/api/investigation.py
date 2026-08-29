from fastapi import APIRouter, Depends

from app import services
from app.api.dependencies import get_investigation_service
from app.models.investigation import InvestigationResponse, InvestigationRequest
from app.services.investigation import InvestigationService

router = APIRouter(prefix="/ai",tags=["investigation"])

@router.post("/investigate-issue",
             response_model=InvestigationResponse,)
async def investigate_issue(
        request: InvestigationRequest,
        service:InvestigationService=Depends(get_investigation_service)
)->InvestigationResponse:
    return await service.investigate(request)