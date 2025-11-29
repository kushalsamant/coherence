import type { Metadata } from "next";
import { AppLayout } from "@kushalsamant/design-template";
import "@kushalsamant/design-template/styles/globals.css";
import Link from "next/link";
import HeaderWrapper from "@/components/HeaderWrapper";

export const metadata: Metadata = {
  title: "ASK: Daily Research - Research Q&A Tool",
  description: "Browse and generate research question-answer pairs with photorealistic images. Explore research themes including sustainability science, engineering systems, and more.",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body>
        <AppLayout
          header={<HeaderWrapper />}
          LinkComponent={Link}
        >
          {children}
        </AppLayout>
      </body>
    </html>
  );
}
