"""
Example API route
Replace this with your app-specific routes
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db

router = APIRouter()


@router.get("/example")
async def example_endpoint(db: Session = Depends(get_db)):
    """
    Example endpoint
    Replace with your app-specific logic
    """
    return {
        "message": "This is an example endpoint",
        "status": "success"
    }


# Add more routes here:
# @router.get("/items")
# async def get_items(db: Session = Depends(get_db)):
#     ...

