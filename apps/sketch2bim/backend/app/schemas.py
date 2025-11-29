"""
Pydantic schemas for request/response validation
"""
from __future__ import annotations
from pydantic import BaseModel, EmailStr, Field, validator
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum


# ============================================================================
# Enums
# ============================================================================

class JobStatus(str, Enum):
    QUEUED = "queued"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"
    REVIEW = "review"


class SubscriptionTier(str, Enum):
    TRIAL = "trial"
    WEEK = "week"
    MONTH = "month"
    YEAR = "year"


class ProjectType(str, Enum):
    ARCHITECTURE = "architecture"


# ============================================================================
# User Schemas
# ============================================================================

class UserBase(BaseModel):
    email: EmailStr
    name: Optional[str] = None


class UserCreate(UserBase):
    google_id: str


class UserResponse(UserBase):
    id: int
    credits: int  # Historical field (no longer used for access control)
    subscription_tier: str
    subscription_status: str
    subscription_expires_at: Optional[datetime] = None
    created_at: datetime
    last_login: Optional[datetime]
    
    class Config:
        from_attributes = True


class UserUpdate(BaseModel):
    name: Optional[str] = None
    credits: Optional[int] = None
    subscription_tier: Optional[str] = None


# ============================================================================
# Job Schemas
# ============================================================================

class JobCreate(BaseModel):
    sketch_filename: str
    sketch_format: str


class JobResponse(BaseModel):
    id: str
    status: JobStatus
    progress: int
    sketch_filename: str
    project_type: Optional[ProjectType] = ProjectType.ARCHITECTURE
    detection_confidence: Optional[float]
    ifc_url: Optional[str]
    dwg_url: Optional[str]
    rvt_url: Optional[str]
    sketchup_url: Optional[str]  # OBJ format for SketchUp
    preview_image_url: Optional[str]
    error_message: Optional[str]
    legend_data: Optional[Dict[str, Any]] = None
    legend_detected: Optional[bool] = False
    created_at: datetime
    completed_at: Optional[datetime]
    expires_at: Optional[datetime]
    symbol_summary: Optional["SymbolSummary"] = None
    
    class Config:
        from_attributes = True


class JobStatusResponse(BaseModel):
    id: str
    status: JobStatus
    progress: int
    message: Optional[str] = None
    error: Optional[str] = None


class BatchJobResponse(BaseModel):
    batch_id: str
    jobs: List[JobResponse]
    total_jobs: int
    completed_jobs: int
    failed_jobs: int


# ============================================================================
# Upload Schemas
# ============================================================================

class UploadResponse(BaseModel):
    job_id: str
    message: str


class BatchUploadResponse(BaseModel):
    batch_id: str
    job_ids: List[str]
    total_jobs: int


class BatchJobResponse(BaseModel):
    """Batch job status response with aggregated statistics"""
    batch_id: str
    total_jobs: int
    completed: int
    failed: int
    processing: int
    queued: int
    review: int
    jobs: List[JobResponse]  # List of jobs in batch


# ============================================================================
# Plan Data Schemas
# ============================================================================

class Point(BaseModel):
    x: float
    y: float


class Polygon(BaseModel):
    points: List[Point]


class Room(BaseModel):
    id: int
    polygon: List[List[float]]
    room_type: Optional[str] = None
    area: Optional[float] = None


class Opening(BaseModel):
    type: str  # door|window
    position: List[float]
    width: Optional[float] = None


class SymbolDetection(BaseModel):
    label: str
    display_name: Optional[str] = None
    category: Optional[str] = None
    ifc_type: Optional[str] = None
    bbox: List[float]
    confidence: float
    area_pixels: Optional[float] = None
    source: Optional[str] = "ml_detector"


class SymbolSummary(BaseModel):
    total_detected: int
    categories: Dict[str, int]
    sample_labels: List[str] = []
    enabled: bool = False
    inference_ms: Optional[float] = None
    model_path: Optional[str] = None


class PlanData(BaseModel):
    rooms: List[Room]
    walls: List[Dict[str, Any]]
    openings: List[Opening]
    symbols: Optional[List[SymbolDetection]] = None
    symbol_metadata: Optional[Dict[str, Any]] = None
    confidence: float


# ============================================================================
# Legend Schemas
# ============================================================================

class LegendData(BaseModel):
    """Parsed legend information from sketch"""
    scale: Optional[str] = None  # Scale text (e.g., "1:100", "1/4\" = 1'-0\"")
    scale_ratio: Optional[float] = None  # Calculated pixels-to-meters ratio
    room_labels: Optional[Dict[str, str]] = None  # Detected room labels and types
    line_types: Optional[Dict[str, str]] = None  # Line type conventions (solid, dashed, dotted)
    symbols: Optional[Dict[str, str]] = None  # Standard architectural symbols detected
    confidence: Optional[float] = None  # Confidence score for legend detection


# ============================================================================
# Payment Schemas
# ============================================================================

class CheckoutSessionCreate(BaseModel):
    price_id: str
    success_url: str
    cancel_url: str


class CheckoutSessionResponse(BaseModel):
    checkout_url: str
    session_id: str


class WebhookEvent(BaseModel):
    type: str
    data: Dict[str, Any]


# ============================================================================
# API Key Schemas
# ============================================================================

class APIKeyCreate(BaseModel):
    name: str
    rate_limit_per_minute: Optional[int] = 10
    rate_limit_per_hour: Optional[int] = 100


class APIKeyResponse(BaseModel):
    id: int
    key: str
    name: str
    rate_limit_per_minute: int
    rate_limit_per_hour: int
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True


# ============================================================================
# Version History Schemas
# ============================================================================

class VersionCreate(BaseModel):
    project_name: str
    job_id: str
    notes: Optional[str] = None


class VersionResponse(BaseModel):
    id: int
    project_name: str
    version_number: int
    job_id: str
    notes: Optional[str]
    created_at: datetime
    
    class Config:
        from_attributes = True


# ============================================================================
# Admin Schemas
# ============================================================================

class AdminStats(BaseModel):
    total_users: int
    total_jobs: int
    total_completed: int
    total_failed: int
    credits_used_today: int
    revenue_today: float
    total_cost: Optional[float] = 0.0
    cost_today: Optional[float] = 0.0
    jobs_requiring_review: Optional[int] = 0


# ============================================================================
# Error Schemas
# ============================================================================

class ErrorResponse(BaseModel):
    error: str
    detail: Optional[str] = None
    code: Optional[str] = None


# ============================================================================
# Iteration Schemas
# ============================================================================

class IterationCreate(BaseModel):
    """Create a new iteration from an existing IFC"""
    parent_iteration_id: Optional[str] = None  # If None, uses job's original IFC
    name: Optional[str] = None
    notes: Optional[str] = None
    changes_json: Optional[Dict[str, Any]] = None  # Changes made in this iteration


class IterationUpdate(BaseModel):
    """Update iteration metadata"""
    name: Optional[str] = None
    notes: Optional[str] = None
    changes_json: Optional[Dict[str, Any]] = None


class IterationResponse(BaseModel):
    """Iteration response"""
    id: str
    job_id: str
    parent_iteration_id: Optional[str]
    ifc_url: Optional[str]
    ifc_filename: Optional[str]
    changes_json: Optional[Dict[str, Any]]
    change_summary: Optional[str]
    name: Optional[str]
    notes: Optional[str]
    created_at: datetime
    
    class Config:
        from_attributes = True


# ============================================================================
# Layout Variation Schemas
# ============================================================================

class VariationGenerateRequest(BaseModel):
    """Request to generate layout variations"""
    num_variations: int = Field(default=3, ge=1, le=10)  # 1-10 variations
    constraints: Optional[Dict[str, Any]] = None  # Optional constraints (room sizes, adjacencies, etc.)


class VariationResponse(BaseModel):
    """Layout variation response"""
    id: str
    job_id: str
    variation_number: int
    plan_data: Optional[Dict[str, Any]]
    confidence: Optional[float]
    ifc_url: Optional[str]
    preview_image_url: Optional[str]
    created_at: datetime
    
    class Config:
        from_attributes = True

