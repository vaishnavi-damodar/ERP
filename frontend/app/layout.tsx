/**
 * Root layout
 */
import type { Metadata, Viewport } from 'next';
import { Manrope, Space_Grotesk } from 'next/font/google';
import { AuthProvider } from '@/context/AuthContext';
import { Toaster } from 'react-hot-toast';
import '../styles/globals.css';

const manrope = Manrope({
  subsets: ['latin'],
  variable: '--font-manrope',
});

const spaceGrotesk = Space_Grotesk({
  subsets: ['latin'],
  variable: '--font-space-grotesk',
});

export const metadata: Metadata = {
  title: 'EduSync - College ERP System',
  description: 'Smart College Enterprise Resource Planning System',
  icons: {
    icon: '/favicon.ico',
  },
};

export const viewport: Viewport = {
  width: 'device-width',
  initialScale: 1,
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" suppressHydrationWarning>
      <head>
        <meta name="theme-color" content="#0ea5e9" />
      </head>
      <body className={`${manrope.variable} ${spaceGrotesk.variable}`}>
        <AuthProvider>
          <Toaster position="top-right" toastOptions={{ duration: 4000 }} />
          {children}
        </AuthProvider>
      </body>
    </html>
  );
}

