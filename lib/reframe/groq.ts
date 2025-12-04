import Groq from "groq-sdk";

/**
 * Groq client configured for Reframe
 * Model: llama-3.1-8b-instant
 * Cost: $0.05/M input tokens, $0.08/M output tokens
 * 
 * Used for AI text reframing with multiple human tones.
 * Tone-specific prompts are managed in lib/tones.ts
 * 
 * IMPORTANT: This uses lazy initialization to avoid build-time errors.
 * The client is only created when getGroqClient() is actually called at runtime.
 */
let groqInstance: Groq | null = null;

/**
 * Get the Groq client instance (lazy initialization)
 * Only creates the client when first called, not during module import
 */
export function getGroqClient(): Groq {
  if (!groqInstance) {
    groqInstance = new Groq({
      apiKey: process.env.REFRAME_GROQ_API_KEY || process.env.GROQ_API_KEY!,
    });
  }
  return groqInstance;
}

