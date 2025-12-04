import { handlers } from "@/lib/auth";

// Log to verify the route is being loaded
console.log("NextAuth route handler loaded, handlers:", typeof handlers);

export const GET = handlers.GET;
export const POST = handlers.POST;
export const runtime = "nodejs";

