"""
Audit logging for compliance and security
Tracks all user actions and admin operations
"""
from datetime import datetime
from typing import Optional, Dict, Any
import json


class AuditLog:
    """Audit log entry (stored in database or external system)"""
    
    def __init__(self):
        pass
    
    def log_action(
        self,
        user_id: Optional[int],
        action: str,
        resource_type: str,
        resource_id: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None,
        ip_address: Optional[str] = None,
        user_agent: Optional[str] = None
    ):
        """
        Log an audit event
        
        Args:
            user_id: User ID (None for anonymous)
            action: Action performed (create, read, update, delete, approve, reject, etc.)
            resource_type: Type of resource (job, user, payment, etc.)
            resource_id: ID of the resource
            details: Additional details as dict
            ip_address: Client IP address
            user_agent: User agent string
        """
        try:
            # In production, you'd have an AuditLog model
            # For now, we'll use structured logging
            from loguru import logger
            
            log_data = {
                "timestamp": datetime.utcnow().isoformat(),
                "user_id": user_id,
                "action": action,
                "resource_type": resource_type,
                "resource_id": resource_id,
                "details": details or {},
                "ip_address": ip_address,
                "user_agent": user_agent
            }
            
            logger.info(f"AUDIT: {json.dumps(log_data)}")
            
        except Exception as e:
            # Don't fail the request if audit logging fails
            from loguru import logger
            logger.error(f"Audit logging failed: {e}")
    
    def log_job_creation(self, user_id: int, job_id: str, filename: str, ip_address: Optional[str] = None):
        """Log job creation"""
        self.log_action(
            user_id=user_id,
            action="create",
            resource_type="job",
            resource_id=job_id,
            details={"filename": filename},
            ip_address=ip_address
        )
    
    def log_job_download(self, user_id: int, job_id: str, file_type: str, ip_address: Optional[str] = None):
        """Log file download"""
        self.log_action(
            user_id=user_id,
            action="download",
            resource_type="job",
            resource_id=job_id,
            details={"file_type": file_type},
            ip_address=ip_address
        )
    
    def log_payment(self, user_id: int, payment_id: int, amount: int, status: str):
        """Log payment event"""
        self.log_action(
            user_id=user_id,
            action="payment",
            resource_type="payment",
            resource_id=str(payment_id),
            details={"amount": amount, "status": status}
        )
    
    def log_admin_action(self, admin_id: int, action: str, resource_type: str, resource_id: Optional[str] = None, details: Optional[Dict] = None):
        """Log admin action"""
        self.log_action(
            user_id=admin_id,
            action=f"admin_{action}",
            resource_type=resource_type,
            resource_id=resource_id,
            details=details or {}
        )
    
    def log_review_action(self, reviewer_id: int, job_id: str, action: str, reason: Optional[str] = None):
        """Log review action (approve/reject)"""
        self.log_action(
            user_id=reviewer_id,
            action=f"review_{action}",
            resource_type="job",
            resource_id=job_id,
            details={"reason": reason} if reason else {}
        )


# Global audit logger instance
_audit_logger = None

def get_audit_logger() -> AuditLog:
    """Get audit logger instance"""
    global _audit_logger
    if _audit_logger is None:
        _audit_logger = AuditLog()
    return _audit_logger


def log_audit_event(
    user_id: Optional[int],
    action: str,
    resource_type: str,
    resource_id: Optional[str] = None,
    details: Optional[Dict[str, Any]] = None,
    ip_address: Optional[str] = None
):
    """Convenience function for audit logging"""
    logger = get_audit_logger()
    logger.log_action(
        user_id=user_id,
        action=action,
        resource_type=resource_type,
        resource_id=resource_id,
        details=details,
        ip_address=ip_address
    )

