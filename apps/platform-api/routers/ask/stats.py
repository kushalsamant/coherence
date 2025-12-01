"""
Statistics API Routes
"""

from fastapi import APIRouter
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from api.models import Stats, Theme
from api.services.csv_service import read_qa_pairs, get_all_themes, get_theme_counts

router = APIRouter()


@router.get("/stats", response_model=Stats)
async def get_stats():
    """
    Get overall statistics about Q&A pairs and themes
    """
    qa_pairs = read_qa_pairs()
    themes_list = get_all_themes()
    theme_counts = get_theme_counts()
    
    # Count questions and answers
    questions = sum(1 for qa in qa_pairs if qa.question)
    answers = sum(1 for qa in qa_pairs if qa.answer)
    
    # Build themes with counts
    themes = [
        Theme(name=theme, count=theme_counts.get(theme, 0))
        for theme in themes_list
    ]
    themes.sort(key=lambda x: (-x.count, x.name))
    
    return Stats(
        total_qa_pairs=len(qa_pairs),
        total_themes=len(themes_list),
        themes=themes,
        total_questions=questions,
        total_answers=answers
    )

