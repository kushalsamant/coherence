"""
CSV Service for reading and parsing log.csv data
"""

import os
import csv
import logging
from typing import List, Optional, Dict
from pathlib import Path
from api.models import QAPair

log = logging.getLogger(__name__)

LOG_CSV_FILE = os.getenv('ASK_LOG_CSV_FILE', os.getenv('LOG_CSV_FILE', 'log.csv'))


def get_csv_path() -> Path:
    """Get the path to the CSV file"""
    base_dir = Path(__file__).parent.parent.parent
    csv_path = base_dir / LOG_CSV_FILE
    return csv_path


def read_qa_pairs() -> List[QAPair]:
    """
    Read all Q&A pairs from log.csv
    
    Returns:
        List of QAPair objects
    """
    csv_path = get_csv_path()
    
    if not csv_path.exists():
        log.warning(f"CSV file not found: {csv_path}")
        return []
    
    qa_pairs = []
    
    try:
        with open(csv_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                try:
                    # Convert question_number to int
                    question_number = int(row.get('question_number', 0))
                    
                    # Parse is_used as boolean
                    is_used = row.get('is_used', 'false').lower() == 'true'
                    
                    # Get image filenames from CSV
                    question_image = row.get('question_image', '').strip() or None
                    answer_image = row.get('answer_image', '').strip() or None
                    
                    qa_pair = QAPair(
                        question_number=question_number,
                        theme=row.get('theme', ''),
                        question=row.get('question', ''),
                        style=row.get('style') if row.get('style') else None,
                        answer=row.get('answer', ''),
                        keywords=row.get('keywords') if row.get('keywords') else None,
                        is_used=is_used,
                        created_timestamp=row.get('created_timestamp'),
                        question_image=question_image,
                        answer_image=answer_image
                    )
                    qa_pairs.append(qa_pair)
                except Exception as e:
                    log.error(f"Error parsing row: {e}, row: {row}")
                    continue
    except Exception as e:
        log.error(f"Error reading CSV file: {e}")
        return []
    
    return qa_pairs


def get_qa_pair_by_id(question_number: int) -> Optional[QAPair]:
    """
    Get a single Q&A pair by question number
    
    Args:
        question_number: The question number to retrieve
        
    Returns:
        QAPair if found, None otherwise
    """
    qa_pairs = read_qa_pairs()
    for qa_pair in qa_pairs:
        if qa_pair.question_number == question_number:
            return qa_pair
    return None


def filter_by_theme(qa_pairs: List[QAPair], theme: str) -> List[QAPair]:
    """
    Filter Q&A pairs by theme
    
    Args:
        qa_pairs: List of Q&A pairs
        theme: Theme to filter by
        
    Returns:
        Filtered list of Q&A pairs
    """
    return [qa for qa in qa_pairs if qa.theme == theme]


def get_all_themes() -> List[str]:
    """
    Get all unique themes from the CSV
    
    Returns:
        List of unique theme names
    """
    qa_pairs = read_qa_pairs()
    themes = set()
    for qa_pair in qa_pairs:
        if qa_pair.theme:
            themes.add(qa_pair.theme)
    return sorted(list(themes))


def get_theme_counts() -> Dict[str, int]:
    """
    Get count of Q&A pairs per theme
    
    Returns:
        Dictionary mapping theme names to counts
    """
    qa_pairs = read_qa_pairs()
    theme_counts = {}
    for qa_pair in qa_pairs:
        theme = qa_pair.theme
        theme_counts[theme] = theme_counts.get(theme, 0) + 1
    return theme_counts

