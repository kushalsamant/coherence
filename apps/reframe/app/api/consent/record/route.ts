import { NextResponse } from "next/server";
import { auth } from "@/auth";
import { recordConsent, CURRENT_TERMS_VERSION, CURRENT_PRIVACY_VERSION } from "@/lib/consent";

export const dynamic = 'force-dynamic';

/**
 * POST /api/consent/record
 * Record user consent for Terms of Service and Privacy Policy
 */
export async function POST(req: Request) {
  const session = await auth();

  if (!session?.user?.id) {
    return NextResponse.json({ error: "Unauthorized" }, { status: 401 });
  }

  try {
    // Get IP address from headers (if available)
    const forwardedFor = req.headers.get("x-forwarded-for");
    const ipAddress = forwardedFor?.split(",")[0] || req.headers.get("x-real-ip") || undefined;
    
    // Get user agent
    const userAgent = req.headers.get("user-agent") || undefined;

    // Record consent with current versions
    await recordConsent(
      session.user.id,
      CURRENT_TERMS_VERSION,
      CURRENT_PRIVACY_VERSION,
      ipAddress,
      userAgent
    );

    return NextResponse.json({ 
      success: true,
      message: "Consent recorded successfully",
      termsVersion: CURRENT_TERMS_VERSION,
      privacyVersion: CURRENT_PRIVACY_VERSION
    });
  } catch (error: any) {
    console.error("Error recording consent:", error);
    return NextResponse.json(
      { error: "Failed to record consent" },
      { status: 500 }
    );
  }
}

