import type { Metadata } from 'next';
export const dynamic = 'force-dynamic';
import { Inter } from 'next/font/google';
import { AppLayout } from '@kushalsamant/design-template';
import '@kushalsamant/design-template/styles/globals.css';
import './globals.css';
import Link from 'next/link';
import HeaderWrapper from '@/components/HeaderWrapper';

const inter = Inter({ subsets: ['latin'] });

export const metadata: Metadata = {
  title: 'Sketch-to-BIM',
  description: 'Convert architectural sketches to editable BIM models using computer vision',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" className={inter.className}>
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
