import type { Metadata } from "next";
import { AppLayout } from "@kushalsamant/design-template";
import "@kushalsamant/design-template/styles/globals.css";
import Link from "next/link";
import HeaderWrapper from "@/components/HeaderWrapper";

export const metadata: Metadata = {
  title: "{{APP_DISPLAY_NAME}}",
  description: "{{APP_DESCRIPTION}}",
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

