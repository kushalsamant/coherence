"""
Q&A Pairs API Routes
"""

import os
from fastapi import APIRouter, Query, HTTPException
from typing import Optional, List
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from models.ask_schemas import QAPairResponse, QAPairListResponse
from services.ask.csv_service import (
    read_qa_pairs,
    get_qa_pair_by_id,
    filter_by_theme
)

router = APIRouter()

# Get API base URL from environment or use default
API_BASE_URL = os.getenv('ASK_API_BASE_URL', os.getenv('ASK_BACKEND_URL', 'http://localhost:8000'))


def get_image_url(filename: Optional[str]) -> Optional[str]:
    """Generate full URL for an image filename"""
    if not filename:
        return None
    # Remove any leading slashes
    filename = filename.lstrip('/')
    return f"{API_BASE_URL}/static/images/{filename}"


def convert_to_response(qa_pair, index: int) -> QAPairResponse:
    """Convert QAPair to QAPairResponse with image URLs"""
    question_image = getattr(qa_pair, 'question_image', None)
    answer_image = getattr(qa_pair, 'answer_image', None)
    
    # Generate image URLs
    question_image_url = get_image_url(question_image)
    answer_image_url = get_image_url(answer_image)
    
    # Create answer_image_urls list
    answer_image_urls = []
    if answer_image_url:
        answer_image_urls.append(answer_image_url)
    
    return QAPairResponse(
        id=index,
        question_number=qa_pair.question_number,
        theme=qa_pair.theme,
        question=qa_pair.question,
        style=qa_pair.style,
        answer=qa_pair.answer,
        keywords=getattr(qa_pair, 'keywords', None),
        is_used=qa_pair.is_used,
        created_timestamp=qa_pair.created_timestamp,
        question_image=question_image,
        answer_image=answer_image,
        question_image_url=question_image_url,
        answer_image_url=answer_image_url,
        answer_image_urls=answer_image_urls
    )


@router.get("/qa-pairs", response_model=QAPairListResponse)
async def get_qa_pairs(
    theme: Optional[str] = Query(None, description="Filter by theme"),
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(20, ge=1, le=100, description="Items per page")
):
    """
    Get all Q&A pairs with optional filtering and pagination
    """
    # Read all Q&A pairs
    qa_pairs = read_qa_pairs()
    
    # Filter by theme if provided
    if theme:
        qa_pairs = filter_by_theme(qa_pairs, theme)
    
    # Sort by question number
    qa_pairs.sort(key=lambda x: x.question_number)
    
    # Calculate pagination
    total = len(qa_pairs)
    total_pages = (total + page_size - 1) // page_size
    start = (page - 1) * page_size
    end = start + page_size
    
    # Get paginated items
    paginated_items = qa_pairs[start:end]
    
    # Convert to response format
    items = [convert_to_response(qa, start + i) for i, qa in enumerate(paginated_items)]
    
    return QAPairListResponse(
        items=items,
        total=total,
        page=page,
        page_size=page_size,
        total_pages=total_pages
    )


@router.get("/qa-pairs/{question_number}", response_model=QAPairResponse)
async def get_qa_pair(question_number: int):
    """
    Get a single Q&A pair by question number
    """
    qa_pair = get_qa_pair_by_id(question_number)
    
    if not qa_pair:
        raise HTTPException(status_code=404, detail=f"Q&A pair with question_number {question_number} not found")
    
    return convert_to_response(qa_pair, question_number - 1)  # Use question_number - 1 as index for consistency

