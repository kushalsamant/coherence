"""
Groq Service for Reframe
Handles Groq API calls for text reframing
"""
import os
import asyncio
from groq import Groq
from typing import Dict, Optional, Any
from .tone_service import ToneName, GenerationId, generate_tone_prompt, get_tone_parameters, get_system_prompt


# Singleton Groq client
_groq_client: Optional[Groq] = None


def get_groq_client() -> Groq:
    """Get Groq client instance (lazy initialization)"""
    global _groq_client
    if _groq_client is None:
        api_key = os.getenv("REFRAME_GROQ_API_KEY", "")
        if not api_key:
            raise ValueError("GROQ_API_KEY environment variable is not set")
        _groq_client = Groq(api_key=api_key)
    return _groq_client


def _reframe_text_sync(
    text: str,
    tone: ToneName,
    generation: GenerationId = "any"
) -> Dict[str, Any]:
    """Synchronous Groq API call (runs in thread pool)"""
    client = get_groq_client()
    
    system_prompt = get_system_prompt()
    user_prompt = generate_tone_prompt(text, tone, generation)
    params = get_tone_parameters(tone)
    
    completion = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        max_tokens=params["max_tokens"],
        temperature=params["temperature"],
    )
    
    output = completion.choices[0].message.content if completion.choices else ""
    usage = {
        "prompt_tokens": completion.usage.prompt_tokens if completion.usage else 0,
        "completion_tokens": completion.usage.completion_tokens if completion.usage else 0,
        "total_tokens": completion.usage.total_tokens if completion.usage else 0,
    }
    
    return {
        "output": output,
        "usage": usage
    }


async def reframe_text(
    text: str,
    tone: ToneName,
    generation: GenerationId = "any"
) -> Dict[str, Any]:
    """
    Reframe text using Groq API with tone-specific prompts (async wrapper)
    
    Returns:
        Dict with 'output' (reframed text) and 'usage' (token usage info)
    """
    # Run synchronous Groq call in thread pool
    return await asyncio.to_thread(_reframe_text_sync, text, tone, generation)

