/**
 * Input Validation Schemas
 * Using Zod for runtime type checking and validation
 */

import { z } from 'zod';

// Common validation schemas

export const EmailSchema = z.string().email('Invalid email address');

export const UserIdSchema = z.string().min(1, 'User ID is required');

export const SubscriptionTierSchema = z.enum(['weekly', 'monthly', 'yearly'], {
  errorMap: () => ({ message: 'Invalid subscription tier. Must be weekly, monthly, or yearly' }),
});

export const PaymentTypeSchema = z.enum(['one_time', 'subscription'], {
  errorMap: () => ({ message: 'Invalid payment type. Must be one_time or subscription' }),
});

// Razorpay webhook validation
export const RazorpayWebhookSchema = z.object({
  event: z.string(),
  payload: z.object({
    payment: z.object({
      entity: z.object({
        id: z.string(),
        amount: z.number(),
        currency: z.string(),
        status: z.string(),
      }),
    }).optional(),
    subscription: z.object({
      entity: z.object({
        id: z.string(),
        status: z.string(),
        customer_id: z.string().optional(),
      }),
    }).optional(),
  }),
});

// Checkout request validation
export const CheckoutRequestSchema = z.object({
  tier: SubscriptionTierSchema,
  paymentType: PaymentTypeSchema.optional().default('one_time'),
});

// Reframe request validation
export const ReframeRequestSchema = z.object({
  text: z.string().min(1, 'Text is required').max(10000, 'Text too long (max 10,000 characters)'),
  tone: z.string().optional(),
  style: z.string().optional(),
});

// ASK generation request validation
export const AskGenerationSchema = z.object({
  theme: z.string().min(1, 'Theme is required'),
  style: z.string().optional(),
  includeImage: z.boolean().optional(),
});

// Sketch2BIM job request validation
export const Sketch2BIMJobSchema = z.object({
  sketchUrl: z.string().url('Invalid sketch URL'),
  options: z.object({
    buildingType: z.enum(['residential', 'commercial', 'mixed']).optional(),
    includeStructure: z.boolean().optional(),
    includeMEP: z.boolean().optional(),
  }).optional(),
});

/**
 * Validate request body against a schema
 * Returns parsed data or throws validation error
 */
export async function validateRequestBody<T>(
  request: Request,
  schema: z.ZodSchema<T>
): Promise<T> {
  const body = await request.json();
  return schema.parse(body);
}

/**
 * Validate request body and return validation result
 * Safe version that returns success/error instead of throwing
 */
export async function safeValidateRequestBody<T>(
  request: Request,
  schema: z.ZodSchema<T>
): Promise<{ success: true; data: T } | { success: false; error: z.ZodError }> {
  try {
    const body = await request.json();
    const data = schema.parse(body);
    return { success: true, data };
  } catch (error) {
    if (error instanceof z.ZodError) {
      return { success: false, error };
    }
    throw error;
  }
}

/**
 * Format Zod validation errors for API response
 */
export function formatValidationError(error: z.ZodError): {
  message: string;
  errors: Array<{ path: string; message: string }>;
} {
  return {
    message: 'Validation failed',
    errors: error.errors.map(err => ({
      path: err.path.join('.'),
      message: err.message,
    })),
  };
}

