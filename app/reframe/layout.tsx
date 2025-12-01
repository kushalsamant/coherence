import "./globals.css";
import { AppLayout } from "@kushalsamant/design-template";
import "@kushalsamant/design-template/styles/globals.css";
import { Toaster } from "@/components/reframe/ui/toaster";
import { CookieBanner } from "@/components/reframe/cookie-banner";
import Link from "next/link";
import HeaderWrapper from "@/components/reframe/HeaderWrapper";
import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "Reframe - Reframe text with authentic human voices",
  description: "Reframe text with authentic human voices and tones. Choose from 6 distinct voices: Conversational, Professional, Academic, Enthusiastic, Empathetic, and Witty.",
};

export default function ReframeLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <AppLayout
      header={<HeaderWrapper />}
      LinkComponent={Link}
      additionalBodyContent={[
        <Toaster key="toaster" />,
        <CookieBanner key="cookie-banner" />,
      ]}
    >
      {children}
    </AppLayout>
  );
}
