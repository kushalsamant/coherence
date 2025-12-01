"""
Prometheus metrics for monitoring
"""
from prometheus_client import Counter, Histogram, Gauge, generate_latest, CONTENT_TYPE_LATEST
from typing import Optional
import time

# Job metrics
job_count_total = Counter(
    'sketch2bim_jobs_total',
    'Total number of jobs',
    ['status', 'user_tier']
)

job_duration_seconds = Histogram(
    'sketch2bim_job_duration_seconds',
    'Job processing duration in seconds',
    ['status'],
    buckets=[10, 30, 60, 120, 300, 600, 900]
)

job_cost_total = Counter(
    'sketch2bim_job_cost_total',
    'Total cost of jobs in USD',
    ['status']
)

# API metrics
api_requests_total = Counter(
    'sketch2bim_api_requests_total',
    'Total API requests',
    ['method', 'endpoint', 'status_code']
)

api_request_duration_seconds = Histogram(
    'sketch2bim_api_request_duration_seconds',
    'API request duration in seconds',
    ['method', 'endpoint'],
    buckets=[0.01, 0.05, 0.1, 0.5, 1.0, 2.0, 5.0]
)

# Queue metrics
queue_size = Gauge(
    'sketch2bim_queue_size',
    'Current job queue size',
    ['queue_type']
)

# CDN metrics
cdn_uploads_total = Counter(
    'sketch2bim_cdn_uploads_total',
    'Total CDN uploads',
    ['status']
)

cdn_upload_size_bytes = Histogram(
    'sketch2bim_cdn_upload_size_bytes',
    'CDN upload size in bytes',
    buckets=[1024, 10240, 102400, 1048576, 10485760, 104857600]  # 1KB to 100MB
)

# Database metrics
db_query_duration_seconds = Histogram(
    'sketch2bim_db_query_duration_seconds',
    'Database query duration',
    ['operation'],
    buckets=[0.001, 0.005, 0.01, 0.05, 0.1, 0.5, 1.0]
)

# Active users
active_users = Gauge(
    'sketch2bim_active_users',
    'Number of active users',
    ['tier']
)

# Resource limit metrics
database_size_mb = Gauge(
    'sketch2bim_database_size_mb',
    'Current database size in MB'
)

database_size_percentage = Gauge(
    'sketch2bim_database_size_percentage',
    'Percentage of database limit used'
)

redis_commands_today = Gauge(
    'sketch2bim_redis_commands_today',
    'Redis commands executed today'
)

redis_commands_percentage = Gauge(
    'sketch2bim_redis_commands_percentage',
    'Percentage of Redis daily limit used'
)

storage_size_gb = Gauge(
    'sketch2bim_storage_size_gb',
    'Storage size in GB'
)

storage_cost_estimate_usd = Gauge(
    'sketch2bim_storage_cost_estimate_usd',
    'Estimated monthly storage cost in USD'
)


def record_job(status: str, duration: float, cost: float, user_tier: str = "trial"):
    """Record job metrics"""
    job_count_total.labels(status=status, user_tier=user_tier).inc()
    job_duration_seconds.labels(status=status).observe(duration)
    if cost > 0:
        job_cost_total.labels(status=status).inc(cost)


def record_api_request(method: str, endpoint: str, status_code: int, duration: float):
    """Record API request metrics"""
    api_requests_total.labels(
        method=method,
        endpoint=endpoint,
        status_code=status_code
    ).inc()
    api_request_duration_seconds.labels(
        method=method,
        endpoint=endpoint
    ).observe(duration)


def record_cdn_upload(status: str, size_bytes: int):
    """Record CDN upload"""
    cdn_uploads_total.labels(status=status).inc()
    cdn_upload_size_bytes.observe(size_bytes)


def record_db_query(operation: str, duration: float):
    """Record database query"""
    db_query_duration_seconds.labels(operation=operation).observe(duration)


def set_queue_size(queue_type: str, size: int):
    """Set queue size"""
    queue_size.labels(queue_type=queue_type).set(size)


def set_active_users(tier: str, count: int):
    """Set active user count"""
    active_users.labels(tier=tier).set(count)


def get_metrics():
    """Get Prometheus metrics as text"""
    return generate_latest()


def get_metrics_content_type():
    """Get content type for metrics endpoint"""
    return CONTENT_TYPE_LATEST


def update_resource_metrics(db_session=None):
    """
    Update resource limit metrics
    Call this periodically to update Prometheus metrics
    
    Args:
        db_session: Optional database session (if None, database metrics won't be updated)
    """
    try:
        from .database_monitor import get_database_size
        from .redis_monitor import get_redis_usage
        from .storage_monitor import get_storage_usage
        from loguru import logger
        
        # Update database metrics
        if db_session:
            try:
                db_info = get_database_size(db_session)
                database_size_mb.set(db_info.get("size_mb", 0))
                database_size_percentage.set(db_info.get("percentage_used", 0))
            except Exception as e:
                logger.warning(f"Error updating database metrics: {e}")
        
        # Update Redis metrics
        try:
            redis_info = get_redis_usage()
            redis_commands_today.set(redis_info.get("commands_today", 0))
            redis_commands_percentage.set(redis_info.get("percentage_used", 0))
        except Exception as e:
            logger.warning(f"Error updating Redis metrics: {e}")
        
        # Update storage metrics
        try:
            storage_info = get_storage_usage()
            storage_size_gb.set(storage_info.get("size_gb", 0))
            storage_cost_estimate_usd.set(storage_info.get("cost_estimate_usd", 0))
        except Exception as e:
            logger.warning(f"Error updating storage metrics: {e}")
    except Exception as e:
        from loguru import logger
        logger.error(f"Error updating resource metrics: {e}")

