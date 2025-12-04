import { NextResponse } from "next/server";
import { authFunction as auth } from "@/app/reframe/auth";
import { getConsent } from "@/lib/reframe/consent";
import { logger } from "@/lib/logger";

export const dynamic = 'force-dynamic';

/**
 * GET /api/consent/get
 * Get user's consent record
 */
export async function GET() {
  const session = await auth();

  if (!session?.user?.id) {
    return NextResponse.json({ error: "Unauthorized" }, { status: 401 });
  }

  try {
    const consent = await getConsent(session.user.id);
    
    if (!consent) {
      return NextResponse.json({ error: "No consent record found" }, { status: 404 });
    }

    return NextResponse.json(consent);
  } catch (error: any) {
    logger.error("Error fetching consent:", error);
    return NextResponse.json(
      { error: "Failed to fetch consent" },
      { status: 500 }
    );
  }
}

