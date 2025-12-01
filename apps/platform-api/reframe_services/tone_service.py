"""
Tone Service for Reframe
Handles tone-specific prompts and parameters for text reframing
"""
from typing import Dict, Literal, Optional

ToneName = Literal["conversational", "professional", "academic", "enthusiastic", "empathetic", "witty"]
GenerationId = Literal["any", "silent", "boomers", "genx", "millennials", "genz", "genalpha", "genbeta", "kids"]

# Universal system prompt
SYSTEM_PROMPT = """You are an expert content rewriter specializing in transforming AI-generated text into authentic human writing. Your goal is to reframe content with specific tones while:
- Preserving all original facts, data, and key information
- Maintaining the original intent and message
- Removing robotic AI patterns (excessive formality, hedging, repetition)
- Using natural human speech patterns and rhythm
- Keeping the same approximate length (±20%)
- Never inventing new facts or information"""

# Generation definitions
GENERATIONS = {
    "any": {"name": "Any Age", "years": "", "characteristics": "No age-specific adaptation, write for general audience"},
    "silent": {"name": "Silent Generation", "years": "1928-1945", "characteristics": "Formal language, detailed explanations, traditional values, respectful tone"},
    "boomers": {"name": "Baby Boomers", "years": "1946-1964", "characteristics": "Clear structure, comprehensive details, optimistic outlook, moderate formality"},
    "genx": {"name": "Generation X", "years": "1965-1980", "characteristics": "Straightforward, no fluff, pragmatic, slightly skeptical, value authenticity"},
    "millennials": {"name": "Millennials", "years": "1981-1996", "characteristics": "Mix of formal and casual, tech references okay, value efficiency and authenticity"},
    "genz": {"name": "Gen Z", "years": "1997-2012", "characteristics": "Very casual, short sentences, internet culture aware, authentic and unfiltered"},
    "genalpha": {"name": "Gen Alpha", "years": "2013-2025", "characteristics": "Extremely short attention span, visual thinkers, ultra-casual, emoji-friendly"},
    "genbeta": {"name": "Gen Beta", "years": "2025+", "characteristics": "AI-literate, expects personalization, conversational AI interaction style"},
    "kids": {"name": "Kids (8-12)", "years": "Any era", "characteristics": "Very simple vocabulary, short sentences, clear examples, encouraging tone"},
}

# Premium tones (require paid subscription)
PREMIUM_TONES = {"enthusiastic", "empathetic", "witty"}


def _conversational_prompt(text: str) -> str:
    return f"""
Reframe this text in a conversational, friendly tone:

REQUIREMENTS:
- Write as if you're having a casual conversation with a friend
- Use contractions (don't, you're, it's) naturally
- Include personal touches ("you know", "honestly", "here's the thing")
- Break up long sentences into shorter, punchier ones
- Use everyday language instead of jargon
- Add transitional phrases ("by the way", "plus", "and get this")
- Sound relatable and approachable
- Avoid corporate speak and overly formal language

AVOID:
- Slang or overly casual language that seems forced
- Valley girl speak or excessive exclamation marks
- Condescending or patronizing tone
- Starting every sentence with "well" or "so"

TEXT TO REFRAME:
{text}
"""


def _professional_prompt(text: str) -> str:
    return f"""
Reframe this text in a professional, polished tone:

REQUIREMENTS:
- Maintain business-appropriate formality
- Use industry-standard terminology where relevant
- Structure information clearly and logically
- Sound confident and authoritative without arrogance
- Use complete sentences with proper grammar
- Include strategic pauses with em-dashes or semicolons
- Sound like a competent colleague or consultant
- Balance professionalism with accessibility

AVOID:
- Overly stiff or robotic corporate jargon
- Buzzwords and business clichés ("synergy", "leverage", "circle back")
- Hedging language ("perhaps", "maybe", "it seems")
- Excessive formality that feels inhuman
- Passive voice overuse

TEXT TO REFRAME:
{text}
"""


def _academic_prompt(text: str) -> str:
    return f"""
Reframe this text in an academic, scholarly tone:

REQUIREMENTS:
- Use precise, technical language appropriate to the subject
- Structure arguments logically with clear reasoning
- Sound analytical and evidence-based
- Use sophisticated vocabulary naturally
- Include qualifying statements where appropriate
- Employ complex sentence structures when warranted
- Sound like a published researcher or professor
- Maintain objectivity while being engaging

AVOID:
- Unnecessary jargon that obscures meaning
- Overly complex sentences that confuse readers
- Pretentious vocabulary used just to sound smart
- Dry, boring academic writing stereotypes
- Claims without context or nuance
- Starting sentences with "It is important to note that"

TEXT TO REFRAME:
{text}
"""


def _enthusiastic_prompt(text: str) -> str:
    return f"""
Reframe this text in an enthusiastic, energetic tone:

REQUIREMENTS:
- Express genuine excitement about the topic
- Use dynamic, action-oriented language
- Include power words that energize ("amazing", "breakthrough", "transform")
- Vary sentence length for rhythmic impact
- Show passion without sounding fake
- Use active voice predominantly
- Sound like someone genuinely excited to share this information
- Make the reader feel your energy

AVOID:
- Excessive exclamation marks (max 2-3 per paragraph)
- Over-the-top hype that sounds like a scam
- All caps or unnecessary emphasis
- Repetitive excitement phrases ("so excited", "can't wait")
- Fake enthusiasm that feels forced
- Ignoring actual substance for hype

TEXT TO REFRAME:
{text}
"""


def _empathetic_prompt(text: str) -> str:
    return f"""
Reframe this text in an empathetic, compassionate tone:

REQUIREMENTS:
- Acknowledge the reader's feelings or situation
- Use warm, understanding language
- Show you care about their experience
- Use "you" and "your" to connect personally
- Include reassuring phrases naturally
- Sound like a supportive friend or counselor
- Balance empathy with helpfulness
- Validate concerns while offering perspective

AVOID:
- Being patronizing or talking down to readers
- Over-apologizing or excessive hedging
- Sounding overly emotional or dramatic
- Using therapy-speak that feels clinical
- Empty platitudes without substance
- Toxic positivity or dismissing real concerns

TEXT TO REFRAME:
{text}
"""


def _witty_prompt(text: str) -> str:
    return f"""
Reframe this text in a witty, clever tone:

REQUIREMENTS:
- Use wordplay, clever observations, or light humor
- Include unexpected turns of phrase
- Make smart connections or analogies
- Sound intelligent and entertaining simultaneously
- Use timing and rhythm for comedic effect
- Keep humor relevant to the content
- Sound like a smart friend with a great sense of humor
- Balance wit with clarity (don't sacrifice understanding)

AVOID:
- Forced jokes that fall flat
- Sarcasm that seems mean-spirited
- References that won't age well or are too niche
- Trying too hard to be funny on every line
- Undermining serious points with inappropriate humor
- Dad jokes unless they actually fit
- Pop culture references that distract from the message

TEXT TO REFRAME:
{text}
"""


# Tone prompt mapping
TONE_PROMPTS: Dict[ToneName, callable] = {
    "conversational": _conversational_prompt,
    "professional": _professional_prompt,
    "academic": _academic_prompt,
    "enthusiastic": _enthusiastic_prompt,
    "empathetic": _empathetic_prompt,
    "witty": _witty_prompt,
}

# Tone-specific parameters
TONE_PARAMETERS: Dict[ToneName, Dict[str, float]] = {
    "conversational": {"temperature": 0.8, "max_tokens": 100000},
    "professional": {"temperature": 0.7, "max_tokens": 100000},
    "academic": {"temperature": 0.65, "max_tokens": 100000},
    "enthusiastic": {"temperature": 0.85, "max_tokens": 100000},
    "empathetic": {"temperature": 0.75, "max_tokens": 100000},
    "witty": {"temperature": 0.9, "max_tokens": 100000},
}


def generate_tone_prompt(text: str, tone: ToneName, generation: GenerationId = "any") -> str:
    """Generate a tone-specific prompt for text reframing with optional generation targeting"""
    prompt_function = TONE_PROMPTS.get(tone)
    if not prompt_function:
        raise ValueError(f"Invalid tone: {tone}")
    
    base_prompt = prompt_function(text)
    
    # Add generation-specific adaptation if not "any"
    if generation != "any":
        gen = GENERATIONS.get(generation)
        if gen:
            generation_guidance = f"""

IMPORTANT - ADAPT FOR {gen['name'].upper()} AUDIENCE ({gen['years']}):
{gen['characteristics']}

Adjust vocabulary, references, examples, and complexity to resonate with this specific generation while maintaining the {tone} tone."""
            
            base_prompt = base_prompt + generation_guidance
    
    return base_prompt


def get_tone_parameters(tone: ToneName) -> Dict[str, float]:
    """Get tone-specific generation parameters"""
    params = TONE_PARAMETERS.get(tone)
    if not params:
        raise ValueError(f"Invalid tone: {tone}")
    return params


def get_system_prompt() -> str:
    """Get system prompt"""
    return SYSTEM_PROMPT


def is_tone_premium(tone: ToneName) -> bool:
    """Check if a tone is premium (requires paid subscription)"""
    return tone in PREMIUM_TONES


def can_user_access_tone(tone: ToneName, subscription_tier: Optional[str] = None) -> bool:
    """Check if user can access a specific tone"""
    if not is_tone_premium(tone):
        return True  # Free tones
    # Any paid tier unlocks premium tones
    return subscription_tier is not None and subscription_tier != "trial" and subscription_tier != "expired"

