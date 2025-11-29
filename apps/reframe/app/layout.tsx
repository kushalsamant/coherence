import "./globals.css";
import { AppLayout } from "@kushalsamant/design-template";
import "@kushalsamant/design-template/styles/globals.css";
import { Toaster } from "@/components/ui/toaster";
import { CookieBanner } from "@/components/cookie-banner";
import Link from "next/link";
import HeaderWrapper from "@/components/HeaderWrapper";

export const metadata = {
  title: "Reframe - Reframe text with authentic human voices",
  description: "Reframe text with authentic human voices and tones. Choose from 6 distinct voices: Conversational, Professional, Academic, Enthusiastic, Empathetic, and Witty.",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body>
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
      </body>
    </html>
  );
}
