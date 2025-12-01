import type { Metadata } from 'next';
export const dynamic = 'force-dynamic';
import { AppLayout } from '@kushalsamant/design-template';
import '@kushalsamant/design-template/styles/globals.css';
import './globals.css';
import Link from 'next/link';
import HeaderWrapper from '@/components/sketch2bim/HeaderWrapper';

export const metadata: Metadata = {
  title: 'Sketch-to-BIM',
  description: 'Convert architectural sketches to editable BIM models using computer vision',
};

export default function Sketch2BIMLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <AppLayout
      header={<HeaderWrapper />}
      LinkComponent={Link}
    >
      {children}
    </AppLayout>
  );
}
