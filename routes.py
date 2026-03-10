from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any

from models import get_db
from sqlalchemy.orm import Session
from ai_service import generate_summary, extract_tags, search_embeddings

router = APIRouter()

# ---------------------------------------------------------------------------
# Pydantic request models – simple, no complex validators.
# ---------------------------------------------------------------------------
class SummaryRequest(BaseModel):
    document: str = Field(..., min_length=500, max_length=100000)
    summary_type: Optional[str] = Field(default="condensed")
    include_citations: Optional[bool] = Field(default=True)
    domain: str

class TagsRequest(BaseModel):
    text: str = Field(..., min_length=100)
    domain: str

class SearchRequest(BaseModel):
    query: str = Field(..., min_length=1)
    filters: Optional[Dict[str, Any]] = None

# ---------------------------------------------------------------------------
# AI‑driven endpoints.
# ---------------------------------------------------------------------------
@router.post("/summaries", response_model=dict)
async def post_summary(request: SummaryRequest, db: Session = Depends(get_db)):
    """Generate an academic‑style summary using the DO inference service."""
    result = await generate_summary(
        document=request.document,
        summary_type=request.summary_type,
        include_citations=request.include_citations,
        domain=request.domain,
    )
    # In a full implementation we would persist the summary in the DB.
    return result

@router.post("/semantic-tags", response_model=dict)
async def post_tags(request: TagsRequest, db: Session = Depends(get_db)):
    """Extract domain‑specific tags and relationships from raw text."""
    result = await extract_tags(text=request.text, domain=request.domain)
    return result

@router.post("/search", response_model=dict)
async def post_search(request: SearchRequest, db: Session = Depends(get_db)):
    """Perform a semantic search based on a natural‑language query."""
    result = await search_embeddings(query=request.query, filters=request.filters)
    return result
