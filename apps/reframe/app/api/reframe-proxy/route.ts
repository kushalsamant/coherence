/**
 * Proxy route for Reframe FastAPI backend
 * Adds JWT token from NextAuth session to requests
 */
import { NextRequest, NextResponse } from "next/server";
import { auth } from "@/auth";
import { encode } from "next-auth/jwt";

const API_URL = process.env.REFRAME_API_URL || process.env.REFRAME_NEXT_PUBLIC_API_URL || process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export const dynamic = 'force-dynamic';

export async function POST(req: NextRequest) {
  try {
    // Get session to verify authentication
    const session = await auth();
    
    if (!session?.user?.id) {
      return NextResponse.json({ error: "Unauthorized" }, { status: 401 });
    }

    // Encode JWT token from session
    const secret = process.env.REFRAME_NEXTAUTH_SECRET || process.env.NEXTAUTH_SECRET || process.env.REFRAME_AUTH_SECRET || process.env.AUTH_SECRET;
    if (!secret) {
      return NextResponse.json({ error: "NEXTAUTH_SECRET not configured" }, { status: 500 });
    }

    // Create JWT token payload from session
    const tokenPayload = {
      sub: session.user.id,
      email: session.user.email,
      name: session.user.name,
      iat: Math.floor(Date.now() / 1000),
      exp: Math.floor(Date.now() / 1000) + (30 * 24 * 60 * 60), // 30 days
    };

    // Encode the JWT token
    const jwtToken = await encode({
      token: tokenPayload,
      secret,
    });

    // Get request body
    const body = await req.json();
    
    // Forward request to FastAPI backend with JWT token
    const response = await fetch(`${API_URL}/api/reframe`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "Authorization": `Bearer ${jwtToken}`,
      },
      body: JSON.stringify({
        text: body.text,
        tone: body.tone || "conversational",
        generation: body.generation || "any",
        timezoneOffset: body.timezoneOffset || 0,
      }),
    });

    const data = await response.json();

    if (!response.ok) {
      return NextResponse.json(data, { status: response.status });
    }

    return NextResponse.json(data);
  } catch (error: any) {
    console.error("Proxy error:", error);
    return NextResponse.json(
      { error: error.message || "Internal server error" },
      { status: 500 }
    );
  }
}

