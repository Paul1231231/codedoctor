from fastapi import APIRouter

from codedoctor.llm.client import LLMClient
from codedoctor.schemas.analysis import AnalysisRequest, AnalysisResponse
from codedoctor.services.analyzer import Analyzer

router = APIRouter()

llm_client = LLMClient()
analyzer = Analyzer(llm_client)

@router.post(
    "/analyze",
    response_model=AnalysisResponse
)
async def analyze(
    request: AnalysisRequest,

) -> AnalysisResponse:
    return await analyzer.analyze(request)

@router.get("/health")
async def health() ->dict[str, str]:
    return {"status": "ok"}