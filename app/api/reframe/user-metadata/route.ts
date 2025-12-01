import { NextResponse } from "next/server";
import { auth } from "@/app/reframe/auth";
import { getUserMetadata } from "@/lib/reframe/user-metadata";

export const dynamic = 'force-dynamic';

/**
 * GET /api/user-metadata
 * Fetch user metadata for the authenticated user
 */
export async function GET(req: Request) {
  const session = await auth();
  
  if (!session?.user?.id) {
    return NextResponse.json({ error: "Unauthorized" }, { status: 401 });
  }

  try {
    const metadata = await getUserMetadata(session.user.id);
    return NextResponse.json(metadata || {});
  } catch (error: any) {
    console.error("Error fetching user metadata:", error);
    return NextResponse.json({ 
      error: "Failed to fetch metadata",
      subscription: undefined
    }, { status: 500 });
  }
}

