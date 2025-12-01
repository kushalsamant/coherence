import { NextResponse } from "next/server";
import { auth } from "@/app/reframe/auth";
import { getUserMetadata, deleteAllUserData } from "@/lib/reframe/user-metadata";
import { deleteUserFromDatabase } from "@/lib/reframe/auth-cleanup";
// Razorpay subscription cancellation handled via webhook

export const dynamic = 'force-dynamic';

/**
 * POST /api/account/delete
 * Delete user account and all associated data (GDPR Right to Erasure)
 */
export async function POST(req: Request) {
  const session = await auth();

  if (!session?.user?.id || !session?.user?.email) {
    return NextResponse.json({ error: "Unauthorized" }, { status: 401 });
  }

  const userId = session.user.id;
  const email = session.user.email;

  try {
    // Step 1: Razorpay subscription cancellation handled via webhook
    // Subscriptions will be cancelled automatically when user data is deleted

    // Step 2: Delete all user data from Redis (metadata, consent, usage)
    await deleteAllUserData(userId);

    // Step 3: Delete user from NextAuth database (user, sessions, accounts)
    await deleteUserFromDatabase(userId, email);

    // Step 4: Return success response
    // Note: We don't call signOut() here because the client will handle the redirect
    return NextResponse.json({
      success: true,
      message: "Account successfully deleted",
    });
  } catch (error: any) {
    console.error("Error deleting account:", error);
    return NextResponse.json(
      { error: "Failed to delete account", details: error.message },
      { status: 500 }
    );
  }
}

