"""
Pydantic models for Reframe API requests and responses
"""
from typing import Optional, Literal
from pydantic import BaseModel, Field, field_validator


ToneName = Literal["conversational", "professional", "academic", "enthusiastic", "empathetic", "witty"]
GenerationId = Literal["any", "silent", "boomers", "genx", "millennials", "genz", "genalpha", "genbeta", "kids"]


class ReframeRequest(BaseModel):
    """Request model for reframe endpoint"""
    text: str = Field(..., min_length=10, description="Text to reframe (min 10 characters)")
    tone: ToneName = Field(default="conversational", description="Tone to use for reframing")
    generation: GenerationId = Field(default="any", description="Target generation/audience")
    timezone_offset: int = Field(default=0, description="Timezone offset (not used in backend)")
    
    @field_validator("text")
    @classmethod
    def validate_text_length(cls, v: str) -> str:
        MAX_CHARS = 50000  # ~10,000 words
        if len(v) > MAX_CHARS:
            raise ValueError(f"Text exceeds maximum {MAX_CHARS} characters (~10,000 words)")
        return v


class ReframeResponse(BaseModel):
    """Response model for reframe endpoint"""
    output: str = Field(..., description="Reframed text")
    usage: Optional[int] = Field(None, description="Usage count (only for free tier users)")


class ErrorResponse(BaseModel):
    """Error response model"""
    error: str = Field(..., description="Error message")
    usage: Optional[int] = Field(None, description="Current usage count (if applicable)")

