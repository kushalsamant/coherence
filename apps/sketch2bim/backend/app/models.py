"""
SQLAlchemy database models
"""
from sqlalchemy import Column, Integer, String, DateTime, Boolean, Float, ForeignKey, Text, JSON, UniqueConstraint
from sqlalchemy.orm import relationship
from datetime import datetime
from .database import Base


class User(Base):
    """User model"""
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    name = Column(String)
    google_id = Column(String, unique=True, index=True)
    
    # Credits
    credits = Column(Integer, default=0)  # Start with 0 credits - unlimited during trial, then must upgrade
    subscription_tier = Column(String, default="trial")  # trial|week|month|year
    subscription_status = Column(String, default="inactive")  # inactive|active|cancelled
    stripe_customer_id = Column(String, unique=True, index=True)  # Reused to store Razorpay customer ID
    subscription_expires_at = Column(DateTime)
    
    # Razorpay subscription tracking
    razorpay_subscription_id = Column(String, nullable=True, index=True)  # Active subscription ID
    subscription_auto_renew = Column(Boolean, default=False)  # True if subscription, False if one-time
    
    # Metadata
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_login = Column(DateTime)
    is_active = Column(Boolean, default=True)
    
    # Relationships
    jobs = relationship("Job", back_populates="user", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<User {self.email}>"


class Job(Base):
    """Sketch-to-BIM conversion job"""
    __tablename__ = "jobs"
    
    id = Column(String, primary_key=True, index=True)  # UUID
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Job details
    status = Column(String, default="queued")  # queued|processing|completed|failed|review
    progress = Column(Integer, default=0)  # 0-100
    
    # Input
    sketch_filename = Column(String)
    sketch_url = Column(String)  # Original upload URL
    sketch_format = Column(String)  # png|jpg|pdf
    project_type = Column(String, default="architecture")  # architecture only
    
    # Processing details (reader_type removed - always uses OpenCV)
    detection_confidence = Column(Float)  # 0-100
    plan_data = Column(JSON)  # Detected geometry
    
    # Output
    ifc_url = Column(String)
    dwg_url = Column(String)
    rvt_url = Column(String)
    sketchup_url = Column(String)  # OBJ format for SketchUp
    model_3dm_url = Column(String)
    preview_image_url = Column(String)
    
    # Error handling
    error_message = Column(Text)
    retry_count = Column(Integer, default=0)
    
    # Quality control
    qc_report_path = Column(String)  # Path to QC report
    requires_review = Column(Boolean, default=False)  # Flag for human review
    
    # Legend data
    legend_data = Column(JSON)  # Parsed legend information (scale, room labels, etc.)
    legend_detected = Column(Boolean, default=False)  # Whether legend was detected in sketch
    
    # Cost tracking
    cost_usd = Column(Float, default=0.0)  # Processing cost in USD
    
    # Batch tracking
    batch_id = Column(String, nullable=True, index=True)  # Batch ID for grouping jobs
    
    # Metadata
    created_at = Column(DateTime, default=datetime.utcnow)
    started_at = Column(DateTime)
    completed_at = Column(DateTime)
    expires_at = Column(DateTime)  # Download link expiry
    
    # Relationships
    user = relationship("User", back_populates="jobs")
    
    def __repr__(self):
        return f"<Job {self.id} - {self.status}>"


class Payment(Base):
    """Payment transaction history"""
    __tablename__ = "payments"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Razorpay details (reusing Stripe field names for backward compatibility)
    stripe_payment_intent_id = Column(String, unique=True, index=True)  # Stores Razorpay payment_id
    stripe_checkout_session_id = Column(String, unique=True, index=True)  # Stores Razorpay order_id or subscription_id
    
    # Payment details
    amount = Column(Integer)  # in paise (₹1 = 100 paise)
    currency = Column(String, default="INR")
    status = Column(String)  # succeeded|pending|failed
    
    # Product
    product_type = Column(String)  # single|trial|week|month|year|one_time
    credits_added = Column(Integer, default=0)
    
    # Cost tracking
    processing_fee = Column(Integer, default=0)  # Razorpay fee in paise (2% of amount)
    
    # Metadata
    created_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime)
    
    def __repr__(self):
        return f"<Payment {self.stripe_payment_intent_id}>"


class ProjectVersion(Base):
    """Version history for projects"""
    __tablename__ = "project_versions"
    
    id = Column(Integer, primary_key=True, index=True)
    project_name = Column(String, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    version_number = Column(Integer)
    job_id = Column(String, ForeignKey("jobs.id"))
    
    notes = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f"<Version {self.project_name} v{self.version_number}>"


class Iteration(Base):
    """IFC file iteration - tracks versions and modifications"""
    __tablename__ = "iterations"
    
    id = Column(String, primary_key=True, index=True)  # UUID
    job_id = Column(String, ForeignKey("jobs.id"), nullable=False, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Parent iteration (for version tree)
    parent_iteration_id = Column(String, ForeignKey("iterations.id"), nullable=True)
    
    # IFC file
    ifc_url = Column(String)  # CDN URL to IFC file
    ifc_filename = Column(String)  # Original filename
    
    # Changes made in this iteration
    changes_json = Column(JSON)  # JSON describing modifications (moved walls, resized rooms, etc.)
    change_summary = Column(Text)  # Human-readable summary of changes
    
    # Metadata
    name = Column(String)  # User-defined name for this iteration
    notes = Column(Text)  # User notes about this iteration
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    job = relationship("Job", foreign_keys=[job_id])
    parent = relationship("Iteration", remote_side=[id], backref="children")
    
    def __repr__(self):
        return f"<Iteration {self.id} for job {self.job_id}>"


class LayoutVariation(Base):
    """Layout variation - alternative room arrangements from same sketch"""
    __tablename__ = "layout_variations"
    
    id = Column(String, primary_key=True, index=True)  # UUID
    job_id = Column(String, ForeignKey("jobs.id"), nullable=False, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Variation details
    variation_number = Column(Integer)  # 1, 2, 3, etc.
    plan_data = Column(JSON)  # Modified plan data with different layout
    confidence = Column(Float)  # Confidence score for this variation
    
    # Generated IFC
    ifc_url = Column(String)  # CDN URL to generated IFC
    preview_image_url = Column(String)  # Preview image
    
    # Metadata
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    job = relationship("Job", foreign_keys=[job_id])
    
    def __repr__(self):
        return f"<LayoutVariation {self.id} - variation {self.variation_number}>"


class Referral(Base):
    """Referral system - track referrals and rewards"""
    __tablename__ = "referrals"
    
    id = Column(Integer, primary_key=True, index=True)
    referrer_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    referred_id = Column(Integer, ForeignKey("users.id"), nullable=True, index=True)  # Set when user signs up
    referral_code = Column(String, unique=True, index=True, nullable=False)
    
    # Status
    status = Column(String, default="pending")  # pending|completed|rewarded
    credits_awarded = Column(Integer, default=0)
    
    # Metadata
    created_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime)  # When referred user signs up
    rewarded_at = Column(DateTime)  # When credits were awarded
    
    # Relationships
    referrer = relationship("User", foreign_keys=[referrer_id], backref="referrals_sent")
    referred = relationship("User", foreign_keys=[referred_id], backref="referral_received")
    
    def __repr__(self):
        return f"<Referral {self.referral_code} - {self.status}>"

