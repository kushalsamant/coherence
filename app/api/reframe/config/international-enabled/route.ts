import { NextResponse } from "next/server";
import { getInternationalPaymentsEnabled } from "@/lib/reframe/app-config";

export const dynamic = 'force-dynamic';

export async function GET() {
  return NextResponse.json({
    enabled: getInternationalPaymentsEnabled()
  });
}

