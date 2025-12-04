import NextAuth from "next-auth";
import Google from "next-auth/providers/google";
import { UpstashRedisAdapter } from "@auth/upstash-redis-adapter";
import { Redis } from "@upstash/redis";

// Initialize Redis client for NextAuth session storage
const redis = new Redis({
  url: process.env.UPSTASH_REDIS_REST_URL || process.env.PLATFORM_UPSTASH_REDIS_REST_URL || "",
  token: process.env.UPSTASH_REDIS_REST_TOKEN || process.env.PLATFORM_UPSTASH_REDIS_REST_TOKEN || "",
});

export const { handlers, signIn, signOut, auth } = NextAuth({
  // Using JWT strategy without adapter for better session persistence
  providers: [
    Google({
      clientId: process.env.GOOGLE_CLIENT_ID || "",
      clientSecret: process.env.GOOGLE_CLIENT_SECRET || "",
      authorization: {
        params: {
          prompt: "consent",
          access_type: "offline",
          response_type: "code",
        },
      },
    }),
  ],
  session: {
    strategy: "jwt",
    maxAge: 30 * 24 * 60 * 60, // 30 days
  },
  callbacks: {
    async jwt({ token, user, account }) {
      // Initial sign in
      if (account && user) {
        return {
          ...token,
          accessToken: account.access_token,
          userId: user.id,
          email: user.email,
          name: user.name,
        };
      }
      return token;
    },
    async session({ session, token }) {
      return {
        ...session,
        user: {
          ...session.user,
          id: token.userId as string,
          email: token.email as string,
          name: token.name as string,
        },
      };
    },
  },
  basePath: "/api/auth",
  secret: process.env.AUTH_SECRET || process.env.NEXTAUTH_SECRET,
  trustHost: true,
  debug: process.env.NODE_ENV === "development",
});

