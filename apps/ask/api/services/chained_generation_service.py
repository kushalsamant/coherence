"""
Chained Generation Service
Implements keyword → question → answer → question chain using Groq API
"""

import logging
from typing import Optional, Dict, List
from sqlalchemy.orm import Session
from api.services.groq_service import generate_with_groq

log = logging.getLogger(__name__)

# Generation state storage (in-memory, could be moved to database for persistence)
_generation_states: Dict[str, Dict] = {}


def validate_keywords(keywords: str):
    """
    Validate keywords: 1-2 words each, comma-separated
    
    Args:
        keywords: Comma-separated keywords string
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    if not keywords or not keywords.strip():
        return False, "Keywords cannot be empty"
    
    keyword_list = [kw.strip() for kw in keywords.split(',') if kw.strip()]
    
    if not keyword_list:
        return False, "At least one keyword is required"
    
    for keyword in keyword_list:
        word_count = len(keyword.split())
        if word_count > 2:
            return False, f"Keyword '{keyword}' has more than 2 words. Each keyword must be 1-2 words maximum."
        if word_count == 0:
            return False, "Empty keyword found"
    
    return True, None


def generate_question_from_keywords(keywords: str, db: Optional[Session] = None) -> Optional[str]:
    """
    Generate a research question from keywords using Groq API
    
    Args:
        keywords: Comma-separated keywords
        db: Optional database session for usage tracking
        
    Returns:
        Generated question or None if generation failed
    """
    system_prompt = "You are an expert researcher. Generate a single, clear, and insightful research question based on the given keywords. The question should be specific, research-oriented, and suitable for academic or professional research."
    
    prompt = f"Based on these keywords: {keywords}\n\nGenerate a single research question that explores these concepts. The question should be clear, specific, and suitable for research."
    
    question = generate_with_groq(prompt, system_prompt, db=db, request_type="question_generation")
    
    if question:
        # Clean up the question (remove quotes, extra whitespace)
        question = question.strip().strip('"').strip("'")
        # Ensure it ends with a question mark
        if not question.endswith('?'):
            question += '?'
    
    return question


def generate_answer_from_question(question: str, db: Optional[Session] = None) -> Optional[str]:
    """
    Generate an answer from a question using Groq API
    
    Args:
        question: The research question to answer
        db: Optional database session for usage tracking
        
    Returns:
        Generated answer or None if generation failed
    """
    system_prompt = "You are an expert researcher and educator. Provide comprehensive, well-structured answers to research questions. Your answers should be detailed, evidence-based, and suitable for academic or professional contexts."
    
    prompt = f"Answer this research question in detail:\n\n{question}\n\nProvide a comprehensive answer that is well-structured and suitable for research purposes."
    
    answer = generate_with_groq(prompt, system_prompt, db=db, request_type="answer_generation")
    
    if answer:
        answer = answer.strip()
    
    return answer


def generate_question_from_answer(answer: str, db: Optional[Session] = None) -> Optional[str]:
    """
    Generate a follow-up question from an answer using Groq API
    
    Args:
        answer: The previous answer to base the question on
        db: Optional database session for usage tracking
        
    Returns:
        Generated question or None if generation failed
    """
    system_prompt = "You are an expert researcher. Generate a logical follow-up research question based on the given answer. The question should build upon the answer and explore related or deeper aspects of the topic."
    
    prompt = f"Based on this answer:\n\n{answer}\n\nGenerate a logical follow-up research question that builds upon this answer and explores related or deeper aspects of the topic."
    
    question = generate_with_groq(prompt, system_prompt, db=db, request_type="question_generation")
    
    if question:
        # Clean up the question
        question = question.strip().strip('"').strip("'")
        if not question.endswith('?'):
            question += '?'
    
    return question


def get_generation_state(session_id: str) -> Optional[Dict]:
    """
    Get generation state for a session
    
    Args:
        session_id: Unique session identifier
        
    Returns:
        Generation state dictionary or None
    """
    return _generation_states.get(session_id)


def set_generation_state(session_id: str, keywords: str, last_question: Optional[str] = None, last_answer: Optional[str] = None, qa_chain: Optional[List[Dict]] = None):
    """
    Set generation state for a session
    
    Args:
        session_id: Unique session identifier
        keywords: Current keywords
        last_question: Last generated question
        last_answer: Last generated answer
        qa_chain: List of Q&A pairs in the chain
    """
    if qa_chain is None:
        qa_chain = []
    
    _generation_states[session_id] = {
        'keywords': keywords,
        'last_question': last_question,
        'last_answer': last_answer,
        'qa_chain': qa_chain
    }


def update_keywords(session_id: str, new_keywords: str):
    """
    Update keywords for a session (preserves existing Q&A chain)
    
    Args:
        session_id: Unique session identifier
        new_keywords: New keywords to use
    """
    if session_id in _generation_states:
        _generation_states[session_id]['keywords'] = new_keywords
        # Reset last question/answer so next generation uses new keywords
        _generation_states[session_id]['last_question'] = None
        _generation_states[session_id]['last_answer'] = None
    else:
        # Create new state if doesn't exist
        set_generation_state(session_id, new_keywords)


def add_to_chain(session_id: str, question: str, answer: str):
    """
    Add a Q&A pair to the generation chain
    
    Args:
        session_id: Unique session identifier
        question: Generated question
        answer: Generated answer
    """
    if session_id not in _generation_states:
        log.warning(f"Session {session_id} not found when adding to chain")
        return
    
    qa_pair = {
        'question': question,
        'answer': answer
    }
    
    _generation_states[session_id]['qa_chain'].append(qa_pair)
    _generation_states[session_id]['last_question'] = question
    _generation_states[session_id]['last_answer'] = answer

