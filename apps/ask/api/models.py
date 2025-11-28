"""
Data models for ASK Research Tool API
"""

from pydantic import BaseModel
from typing import List, Optional


class QAPair(BaseModel):
    """Q&A Pair model matching CSV structure"""
    question_number: int
    theme: str
    question: str
    style: Optional[str] = None
    answer: str
    keywords: Optional[str] = None  # Keywords used to generate this Q&A pair
    is_used: bool = False
    created_timestamp: Optional[str] = None
    question_image: Optional[str] = None  # Image filename
    answer_image: Optional[str] = None  # Image filename
    
    class Config:
        from_attributes = True


class QAPairResponse(BaseModel):
    """Q&A Pair response with additional metadata"""
    id: int
    question_number: int
    theme: str
    question: str
    style: Optional[str] = None
    answer: str
    keywords: Optional[str] = None
    is_used: bool
    created_timestamp: Optional[str] = None
    question_image: Optional[str] = None  # Image filename
    answer_image: Optional[str] = None  # Image filename
    question_image_url: Optional[str] = None  # Full URL to question image
    answer_image_url: Optional[str] = None  # Full URL to answer image
    answer_image_urls: List[str] = []  # List of answer image URLs (for backward compatibility)


class QAPairListResponse(BaseModel):
    """Paginated Q&A pairs response"""
    items: List[QAPairResponse]
    total: int
    page: int
    page_size: int
    total_pages: int


class Theme(BaseModel):
    """Theme model"""
    name: str
    count: int


class ThemeListResponse(BaseModel):
    """Themes list response"""
    themes: List[Theme]
    total: int


class Stats(BaseModel):
    """Statistics model"""
    total_qa_pairs: int
    total_themes: int
    themes: List[Theme]
    total_questions: int
    total_answers: int


class GenerateRequest(BaseModel):
    """Request model for content generation (legacy)"""
    theme: Optional[str] = None
    count: int = 1


class GenerateResponse(BaseModel):
    """Response model for content generation (legacy)"""
    success: bool
    message: str
    qa_pairs: Optional[List[QAPairResponse]] = None
    error: Optional[str] = None


class GenerateStartRequest(BaseModel):
    """Request model for starting generation with keywords"""
    keywords: str
    session_id: Optional[str] = None  # Optional session ID for state management


class GenerateNextRequest(BaseModel):
    """Request model for generating next Q&A in chain"""
    session_id: str
    keywords: Optional[str] = None  # Optional: update keywords if provided


class UpdateKeywordsRequest(BaseModel):
    """Request model for updating keywords"""
    session_id: str
    keywords: str


class GenerationState(BaseModel):
    """Model for generation state"""
    session_id: str
    keywords: str
    last_question: Optional[str] = None
    last_answer: Optional[str] = None
    qa_chain: List[dict] = []  # List of {question, answer} pairs


class GenerateStartResponse(BaseModel):
    """Response model for starting generation"""
    success: bool
    message: str
    session_id: str
    question: Optional[str] = None
    state: Optional[GenerationState] = None
    error: Optional[str] = None


class GenerateNextResponse(BaseModel):
    """Response model for generating next Q&A"""
    success: bool
    message: str
    question: Optional[str] = None
    answer: Optional[str] = None
    state: Optional[GenerationState] = None
    error: Optional[str] = None


class UpdateKeywordsResponse(BaseModel):
    """Response model for updating keywords"""
    success: bool
    message: str
    state: Optional[GenerationState] = None
    error: Optional[str] = None

