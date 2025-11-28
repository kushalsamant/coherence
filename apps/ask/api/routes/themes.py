"""
Themes API Routes
"""

from fastapi import APIRouter
from api.models import Theme, ThemeListResponse
from api.services.csv_service import get_all_themes, get_theme_counts

router = APIRouter()


@router.get("/themes", response_model=ThemeListResponse)
async def get_themes():
    """
    Get all available themes with counts
    """
    themes_list = get_all_themes()
    theme_counts = get_theme_counts()
    
    themes = [
        Theme(name=theme, count=theme_counts.get(theme, 0))
        for theme in themes_list
    ]
    
    # Sort by count (descending), then by name
    themes.sort(key=lambda x: (-x.count, x.name))
    
    return ThemeListResponse(
        themes=themes,
        total=len(themes)
    )

