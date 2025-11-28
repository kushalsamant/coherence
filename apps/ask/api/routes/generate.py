"""
Content Generation API Routes
"""

import uuid
import logging
from fastapi import APIRouter, BackgroundTasks, Depends
from sqlalchemy.orm import Session

log = logging.getLogger(__name__)
from api.models import (
    GenerateRequest, GenerateResponse,
    GenerateStartRequest, GenerateStartResponse,
    GenerateNextRequest, GenerateNextResponse,
    UpdateKeywordsRequest, UpdateKeywordsResponse,
    GenerationState
)
from api.services.generation_service import trigger_generation
from api.services.chained_generation_service import (
    validate_keywords,
    generate_question_from_keywords,
    generate_answer_from_question,
    generate_question_from_answer,
    get_generation_state,
    set_generation_state,
    update_keywords,
    add_to_chain
)
from api.services.csv_service import read_qa_pairs
from api.services.groq_service import is_groq_available
from api.routes.qa_pairs import convert_to_response
from api.database import get_db
from research_csv_manager import log_qa_pair

router = APIRouter()


@router.post("/generate/start", response_model=GenerateStartResponse)
async def start_generation(
    request: GenerateStartRequest,
    db: Session = Depends(get_db)
):
    """
    Start generation with keywords
    
    Flow: Keywords → Question
    """
    try:
        # Validate Groq API availability
        if not is_groq_available():
            return GenerateStartResponse(
                success=False,
                message="Groq API is not available. Please check GROQ_API_KEY environment variable.",
                session_id="",
                error="Groq API not configured"
            )
        
        # Validate keywords
        is_valid, error_msg = validate_keywords(request.keywords)
        if not is_valid:
            return GenerateStartResponse(
                success=False,
                message=error_msg or "Invalid keywords",
                session_id="",
                error=error_msg
            )
        
        # Generate session ID if not provided
        session_id = request.session_id or str(uuid.uuid4())
        
        # Generate question from keywords (with usage tracking)
        question = generate_question_from_keywords(request.keywords, db=db)
        
        if not question:
            return GenerateStartResponse(
                success=False,
                message="Failed to generate question from keywords",
                session_id=session_id,
                error="Question generation failed"
            )
        
        # Initialize generation state
        set_generation_state(session_id, request.keywords, last_question=question)
        
        state = get_generation_state(session_id)
        state_model = GenerationState(
            session_id=state['session_id'],
            keywords=state['keywords'],
            last_question=state['last_question'],
            last_answer=state['last_answer'],
            qa_chain=state['qa_chain']
        )
        
        return GenerateStartResponse(
            success=True,
            message="Question generated successfully",
            session_id=session_id,
            question=question,
            state=state_model
        )
        
    except Exception as e:
        return GenerateStartResponse(
            success=False,
            message=f"Error starting generation: {str(e)}",
            session_id=request.session_id or "",
            error=str(e)
        )


@router.post("/generate/next", response_model=GenerateNextResponse)
async def generate_next(
    request: GenerateNextRequest,
    db: Session = Depends(get_db)
):
    """
    Generate next Q&A in chain
    
    Flow: Answer → Question (if last was question)
          Question → Answer (if last was answer)
    """
    try:
        # Validate Groq API availability
        if not is_groq_available():
            return GenerateNextResponse(
                success=False,
                message="Groq API is not available",
                error="Groq API not configured"
            )
        
        # Get current state
        state = get_generation_state(request.session_id)
        if not state:
            return GenerateNextResponse(
                success=False,
                message="Session not found. Please start a new generation.",
                error="Session not found"
            )
        
        # Update keywords if provided
        if request.keywords:
            is_valid, error_msg = validate_keywords(request.keywords)
            if not is_valid:
                return GenerateNextResponse(
                    success=False,
                    message=error_msg or "Invalid keywords",
                    error=error_msg
                )
            update_keywords(request.session_id, request.keywords)
            state = get_generation_state(request.session_id)
        
        current_keywords = state['keywords']
        last_question = state['last_question']
        last_answer = state['last_answer']
        
        question = None
        answer = None
        
        # Determine what to generate next
        if last_question and not last_answer:
            # Generate answer from last question (with usage tracking)
            answer = generate_answer_from_question(last_question, db=db)
            if answer:
                add_to_chain(request.session_id, last_question, answer)
                # Save to CSV when we complete a Q&A pair
                try:
                    log_qa_pair(
                        theme=current_keywords,
                        question=last_question,
                        answer=answer,
                        question_image="",
                        answer_image="",
                        question_style="Groq-Generated",
                        answer_style="Groq-Generated",
                        keywords=current_keywords
                    )
                except Exception as e:
                    # Log error but don't fail the request
                    log.error(f"Failed to save Q&A pair to CSV: {e}")
        elif last_answer:
            # Generate next question from last answer (with usage tracking)
            question = generate_question_from_answer(last_answer, db=db)
            if question:
                # Update state with new question
                state = get_generation_state(request.session_id)
                set_generation_state(
                    request.session_id,
                    current_keywords,
                    last_question=question,
                    last_answer=None,
                    qa_chain=state['qa_chain']
                )
        elif not last_question and not last_answer:
            # No previous state, generate question from keywords (with usage tracking)
            question = generate_question_from_keywords(current_keywords, db=db)
            if question:
                state = get_generation_state(request.session_id)
                set_generation_state(
                    request.session_id,
                    current_keywords,
                    last_question=question,
                    last_answer=None,
                    qa_chain=state['qa_chain']
                )
        
        if not question and not answer:
            return GenerateNextResponse(
                success=False,
                message="Failed to generate content",
                error="Generation failed"
            )
        
        # Get updated state
        updated_state = get_generation_state(request.session_id)
        state_model = GenerationState(
            session_id=updated_state['session_id'],
            keywords=updated_state['keywords'],
            last_question=updated_state['last_question'],
            last_answer=updated_state['last_answer'],
            qa_chain=updated_state['qa_chain']
        )
        
        return GenerateNextResponse(
            success=True,
            message="Content generated successfully",
            question=question,
            answer=answer,
            state=state_model
        )
        
    except Exception as e:
        return GenerateNextResponse(
            success=False,
            message=f"Error generating next: {str(e)}",
            error=str(e)
        )


@router.post("/generate/update-keywords", response_model=UpdateKeywordsResponse)
async def update_keywords_endpoint(request: UpdateKeywordsRequest):
    """
    Update keywords for a session
    
    Preserves existing Q&A chain, continues from step 2 (generate question from keywords)
    """
    try:
        # Validate keywords
        is_valid, error_msg = validate_keywords(request.keywords)
        if not is_valid:
            return UpdateKeywordsResponse(
                success=False,
                message=error_msg or "Invalid keywords",
                error=error_msg
            )
        
        # Get current state
        state = get_generation_state(request.session_id)
        if not state:
            return UpdateKeywordsResponse(
                success=False,
                message="Session not found",
                error="Session not found"
            )
        
        # Update keywords (preserves Q&A chain)
        update_keywords(request.session_id, request.keywords)
        
        # Get updated state
        updated_state = get_generation_state(request.session_id)
        state_model = GenerationState(
            session_id=updated_state['session_id'],
            keywords=updated_state['keywords'],
            last_question=updated_state['last_question'],
            last_answer=updated_state['last_answer'],
            qa_chain=updated_state['qa_chain']
        )
        
        return UpdateKeywordsResponse(
            success=True,
            message="Keywords updated successfully. Next generation will use new keywords.",
            state=state_model
        )
        
    except Exception as e:
        return UpdateKeywordsResponse(
            success=False,
            message=f"Error updating keywords: {str(e)}",
            error=str(e)
        )


@router.post("/generate", response_model=GenerateResponse)
async def generate_content(
    request: GenerateRequest,
    background_tasks: BackgroundTasks
):
    """
    Legacy endpoint for content generation (kept for backward compatibility)
    
    Note: Generation runs in the background and may take several minutes
    """
    try:
        # Trigger generation
        result = trigger_generation(theme=request.theme, text_only=True)
        
        if not result["success"]:
            return GenerateResponse(
                success=False,
                message=result.get("message", "Generation failed"),
                error=result.get("error")
            )
        
        # After generation, get the latest Q&A pairs
        qa_pairs = read_qa_pairs()
        if qa_pairs:
            # Get the most recent Q&A pairs (last N items)
            recent_pairs = sorted(qa_pairs, key=lambda x: x.question_number, reverse=True)[:request.count]
            recent_responses = [
                convert_to_response(qa, i) 
                for i, qa in enumerate(recent_pairs)
            ]
            
            return GenerateResponse(
                success=True,
                message=result.get("message", "Content generated successfully"),
                qa_pairs=recent_responses
            )
        else:
            return GenerateResponse(
                success=True,
                message=result.get("message", "Content generated successfully"),
                qa_pairs=[]
            )
            
    except Exception as e:
        return GenerateResponse(
            success=False,
            message="Error during generation",
            error=str(e)
        )

