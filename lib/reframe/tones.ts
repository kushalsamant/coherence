/**
 * Tone System for Reframe
 * Provides 6 distinct human voices/tones for AI text reframing
 */

export type ToneName =
  | "conversational"
  | "professional"
  | "academic"
  | "enthusiastic"
  | "empathetic"
  | "witty";

export type Tone = {
  id: ToneName;
  name: string;
  icon: string;
  description: string;
  premium: boolean;
  example: {
    before: string;
    after: string;
  };
};

export const TONES: Tone[] = [
  {
    id: "conversational",
    name: "Conversational",
    icon: "💬",
    description: "Friendly, casual, relatable",
    premium: false,
    example: {
      before: "The implementation of this feature requires careful consideration of various factors.",
      after: "Look, adding this feature isn't as simple as it sounds. We've got to think through a bunch of different things first.",
    },
  },
  {
    id: "professional",
    name: "Professional",
    icon: "💼",
    description: "Polished, formal, business-like",
    premium: false,
    example: {
      before: "We need to fix the bug ASAP because users are complaining about it all the time!",
      after: "Addressing this bug is a priority given the recurring customer feedback we've received regarding this issue.",
    },
  },
  {
    id: "academic",
    name: "Academic",
    icon: "🎓",
    description: "Scholarly, analytical, researched",
    premium: false,
    example: {
      before: "Social media makes people less happy because they compare themselves to others.",
      after: "Research indicates that social media engagement correlates with decreased life satisfaction, primarily through mechanisms of social comparison.",
    },
  },
  {
    id: "enthusiastic",
    name: "Enthusiastic",
    icon: "⚡",
    description: "Energetic, exciting, passionate",
    premium: true,
    example: {
      before: "This new feature allows users to complete tasks more efficiently than before.",
      after: "This game-changing feature is going to revolutionize how you work—get ready to breeze through tasks like never before!",
    },
  },
  {
    id: "empathetic",
    name: "Empathetic",
    icon: "💙",
    description: "Warm, understanding, compassionate",
    premium: true,
    example: {
      before: "Learning to code can be difficult and frustrating for beginners.",
      after: "I know learning to code can feel overwhelming at first—those moments of frustration are completely normal, and you're not alone in this journey.",
    },
  },
  {
    id: "witty",
    name: "Witty",
    icon: "😄",
    description: "Clever, humorous, engaging",
    premium: true,
    example: {
      before: "Coffee consumption has been shown to increase productivity in the workplace.",
      after: "Turns out your coffee addiction isn't a problem—it's a productivity strategy. Science says so, and who are we to argue with science?",
    },
  },
];

/**
 * Generation/Audience Targeting System
 * 9 generations for targeted content adaptation
 */
export type GenerationId = 
  | 'any'
  | 'silent'
  | 'boomers'
  | 'genx'
  | 'millennials'
  | 'genz'
  | 'genalpha'
  | 'genbeta'
  | 'kids';

export type Generation = {
  id: GenerationId;
  name: string;
  description: string;
  years: string;
  characteristics: string;
};

export const GENERATIONS: Generation[] = [
  {
    id: 'any',
    name: 'Any Age',
    description: 'Universal audience',
    years: '',
    characteristics: 'No age-specific adaptation, write for general audience',
  },
  {
    id: 'silent',
    name: 'Silent Generation',
    description: 'Traditional, respectful',
    years: '1928-1945',
    characteristics: 'Formal language, detailed explanations, traditional values, respectful tone',
  },
  {
    id: 'boomers',
    name: 'Baby Boomers',
    description: 'Optimistic, thorough',
    years: '1946-1964',
    characteristics: 'Clear structure, comprehensive details, optimistic outlook, moderate formality',
  },
  {
    id: 'genx',
    name: 'Generation X',
    description: 'Skeptical, direct',
    years: '1965-1980',
    characteristics: 'Straightforward, no fluff, pragmatic, slightly skeptical, value authenticity',
  },
  {
    id: 'millennials',
    name: 'Millennials',
    description: 'Tech-savvy, balanced',
    years: '1981-1996',
    characteristics: 'Mix of formal and casual, tech references okay, value efficiency and authenticity',
  },
  {
    id: 'genz',
    name: 'Gen Z',
    description: 'Digital native, casual',
    years: '1997-2012',
    characteristics: 'Very casual, short sentences, internet culture aware, authentic and unfiltered',
  },
  {
    id: 'genalpha',
    name: 'Gen Alpha',
    description: 'Ultra-digital, concise',
    years: '2013-2025',
    characteristics: 'Extremely short attention span, visual thinkers, ultra-casual, emoji-friendly',
  },
  {
    id: 'genbeta',
    name: 'Gen Beta',
    description: 'AI-native generation',
    years: '2025+',
    characteristics: 'AI-literate, expects personalization, conversational AI interaction style',
  },
  {
    id: 'kids',
    name: 'Kids (8-12)',
    description: 'Simple, educational',
    years: 'Any era',
    characteristics: 'Very simple vocabulary, short sentences, clear examples, encouraging tone',
  },
];

// Universal system prompt
const SYSTEM_PROMPT = `You are an expert content rewriter specializing in transforming AI-generated text into authentic human writing. Your goal is to reframe content with specific tones while:
- Preserving all original facts, data, and key information
- Maintaining the original intent and message
- Removing robotic AI patterns (excessive formality, hedging, repetition)
- Using natural human speech patterns and rhythm
- Keeping the same approximate length (±20%)
- Never inventing new facts or information`;

// Tone-specific prompts
const conversationalPrompt = (text: string) => `
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
${text}
`;

const professionalPrompt = (text: string) => `
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
${text}
`;

const academicPrompt = (text: string) => `
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
${text}
`;

const enthusiasticPrompt = (text: string) => `
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
${text}
`;

const empatheticPrompt = (text: string) => `
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
${text}
`;

const wittyPrompt = (text: string) => `
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
${text}
`;

// Tone prompt mapping
const tonePrompts: Record<ToneName, (text: string) => string> = {
  conversational: conversationalPrompt,
  professional: professionalPrompt,
  academic: academicPrompt,
  enthusiastic: enthusiasticPrompt,
  empathetic: empatheticPrompt,
  witty: wittyPrompt,
};

// Tone-specific parameters
type ToneParameters = {
  temperature: number;
  max_tokens: number;
};

const toneParameters: Record<ToneName, ToneParameters> = {
  conversational: { temperature: 0.8, max_tokens: 100000 },
  professional: { temperature: 0.7, max_tokens: 100000 },
  academic: { temperature: 0.65, max_tokens: 100000 },
  enthusiastic: { temperature: 0.85, max_tokens: 100000 },
  empathetic: { temperature: 0.75, max_tokens: 100000 },
  witty: { temperature: 0.9, max_tokens: 100000 },
};

/**
 * Generate a tone-specific prompt for text reframing with optional generation targeting
 */
export const generateTonePrompt = (
  text: string, 
  tone: ToneName, 
  generation: GenerationId = 'any'
): string => {
  const promptFunction = tonePrompts[tone];
  if (!promptFunction) {
    throw new Error(`Invalid tone: ${tone}`);
  }
  
  let basePrompt = promptFunction(text);
  
  // Add generation-specific adaptation if not "any"
  if (generation !== 'any') {
    const gen = GENERATIONS.find(g => g.id === generation);
    if (gen) {
      const generationGuidance = `

IMPORTANT - ADAPT FOR ${gen.name.toUpperCase()} AUDIENCE (${gen.years}):
${gen.characteristics}

Adjust vocabulary, references, examples, and complexity to resonate with this specific generation while maintaining the ${tone} tone.`;
      
      basePrompt = basePrompt + generationGuidance;
    }
  }
  
  return basePrompt;
};

/**
 * Get tone-specific generation parameters
 */
export const getToneParameters = (tone: ToneName): ToneParameters => {
  const params = toneParameters[tone];
  if (!params) {
    throw new Error(`Invalid tone: ${tone}`);
  }
  return params;
};

/**
 * Get system prompt
 */
export const getSystemPrompt = (): string => {
  return SYSTEM_PROMPT;
};

/**
 * Check if a tone is premium (requires paid subscription)
 */
export const isTonePremium = (tone: ToneName): boolean => {
  const toneObj = TONES.find((t) => t.id === tone);
  return toneObj?.premium ?? false;
};

/**
 * Check if user can access a specific tone
 */
export const canUserAccessTone = (
  tone: ToneName,
  subscription?: string
): boolean => {
  if (!isTonePremium(tone)) return true; // Free tones
  return subscription !== undefined; // Any paid tier unlocks premium tones
};

