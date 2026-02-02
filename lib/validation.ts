/**
 * Input Validation Schemas using Zod
 * Provides type-safe validation for API requests and user inputs
 */

import { z } from 'zod';

/**
 * Common validation patterns
 */
export const EMAIL_REGEX = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
export const UUID_REGEX = /^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/i;

/**
 * User-related schemas
 */
export const emailSchema = z.string().email('Invalid email address');

export const userIdSchema = z.string().min(1, 'User ID is required');

export const nameSchema = z
  .string()
  .min(1, 'Name is required')
  .max(100, 'Name must be less than 100 characters');

/**
 * Subscription-related schemas
 */
export const subscriptionTierSchema = z.enum(['week', 'month', 'year', 'weekly', 'monthly', 'yearly']);

export const paymentTypeSchema = z.enum(['one_time', 'subscription']);

/**
 * Generation/AI request schemas
 */
export const keywordsSchema = z
  .string()
  .min(3, 'Keywords must be at least 3 characters')
  .max(500, 'Keywords must be less than 500 characters');

export const sessionIdSchema = z.string().uuid('Invalid session ID');

export const themeSchema = z
  .string()
  .min(1, 'Theme is required')
  .max(100, 'Theme must be less than 100 characters');

/**
 * Pagination schemas
 */
export const paginationSchema = z.object({
  page: z.coerce.number().int().positive().default(1),
  pageSize: z.coerce.number().int().positive().max(100).default(20),
});

/**
 * Date range schemas
 */
export const dateRangeSchema = z.object({
  startDate: z.string().datetime().optional(),
  endDate: z.string().datetime().optional(),
  days: z.coerce.number().int().positive().max(365).default(30),
});

/**
 * File upload schemas
 */
export const fileUploadSchema = z.object({
  filename: z.string().min(1, 'Filename is required'),
  filesize: z.number().positive().max(50 * 1024 * 1024, 'File size must be less than 50MB'),
  mimetype: z.string().min(1, 'MIME type is required'),
});

// Removed legacy app schemas - platform now focuses on Sketch2BIM

/**
 * Sketch2BIM-specific schemas
 */
export const sketch2bimJobSchema = z.object({
  project_type: z.enum(['architecture', 'landscape', 'urban_design', 'urban_planning']).default('architecture'),
  detection_confidence: z.coerce.number().min(0).max(1).default(0.5),
});

/**
 * Checkout/Payment schemas
 */
export const checkoutSchema = z.object({
  tier: subscriptionTierSchema,
  paymentType: paymentTypeSchema.default('one_time'),
});

/**
 * Webhook schemas
 */
export const razorpayWebhookSchema = z.object({
  event: z.string(),
  payload: z.object({
    payment: z.object({
      entity: z.object({
        id: z.string(),
        amount: z.number(),
        currency: z.string(),
        status: z.string(),
        order_id: z.string().optional(),
      }),
    }).optional(),
    subscription: z.object({
      entity: z.object({
        id: z.string(),
        plan_id: z.string(),
        status: z.string(),
        customer_id: z.string().optional(),
      }),
    }).optional(),
  }),
});

/**
 * Generic API request validation
 */
export const apiRequestSchema = z.object({
  method: z.enum(['GET', 'POST', 'PUT', 'PATCH', 'DELETE']),
  headers: z.record(z.string(), z.string()).optional(),
  body: z.unknown().optional(),
});

/**
 * Validation helper function
 * Returns validated data or throws error with formatted messages
 */
export function validateInput<T>(schema: z.ZodSchema<T>, data: unknown): T {
  const result = schema.safeParse(data);
  
  if (!result.success) {
    const errors = result.error.issues.map(err => ({
      field: err.path.join('.'),
      message: err.message,
    }));
    
    throw new Error(
      `Validation failed: ${errors.map(e => `${e.field}: ${e.message}`).join(', ')}`
    );
  }
  
  return result.data;
}

/**
 * Validation helper that returns result object instead of throwing
 */
export function safeValidateInput<T>(
  schema: z.ZodSchema<T>,
  data: unknown
): { success: true; data: T } | { success: false; errors: Array<{ field: string; message: string }> } {
  const result = schema.safeParse(data);
  
  if (!result.success) {
    const errors = result.error.issues.map(err => ({
      field: err.path.join('.'),
      message: err.message,
    }));
    
    return { success: false, errors };
  }
  
  return { success: true, data: result.data };
}
