import { NextResponse } from "next/server";
import { getInternationalPaymentsEnabled } from "@/lib/app-config";

export const dynamic = 'force-dynamic';

export async function GET() {
  return NextResponse.json({
    enabled: getInternationalPaymentsEnabled()
  });
}

