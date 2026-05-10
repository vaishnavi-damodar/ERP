import Link from 'next/link';
import { ReactNode } from 'react';

type AppShellProps = {
  title: string;
  subtitle: string;
  badge?: string;
  children: ReactNode;
};

const navItems = [
  { href: '/', label: 'Home' },
  { href: '/dashboard', label: 'Dashboard' },
  { href: '/admin', label: 'Admin' },
  { href: '/faculty', label: 'Faculty' },
  { href: '/student', label: 'Student' },
  { href: '/login', label: 'Login' },
  { href: '/signup', label: 'Signup' },
];

export default function AppShell({ title, subtitle, badge, children }: AppShellProps) {
  return (
    <main className="min-h-screen bg-gradient-to-br from-slate-100 via-primary-50 to-slate-200 px-4 py-8 text-slate-900 dark:from-slate-950 dark:via-slate-900 dark:to-slate-950 dark:text-slate-100 md:px-8">
      <div className="mx-auto flex max-w-7xl flex-col gap-6">
        <header className="rounded-2xl border border-slate-200/80 bg-white/90 p-6 shadow-xl backdrop-blur dark:border-slate-800 dark:bg-slate-900/90">
          <div className="flex flex-wrap items-start justify-between gap-4">
            <div className="space-y-3">
              {badge ? (
                <p className="inline-flex rounded-full bg-primary-100 px-3 py-1 text-xs font-semibold uppercase tracking-[0.2em] text-primary-700 dark:bg-primary-900/40 dark:text-primary-300">
                  {badge}
                </p>
              ) : null}
              <h1 className="text-3xl font-black md:text-4xl">{title}</h1>
              <p className="max-w-3xl text-sm text-slate-600 dark:text-slate-300 md:text-base">{subtitle}</p>
            </div>
            <Link
              href="/api/health"
              className="btn btn-secondary h-fit whitespace-nowrap"
            >
              Frontend Health
            </Link>
          </div>
          <nav className="mt-6 flex flex-wrap gap-2">
            {navItems.map((item) => (
              <Link
                key={item.href}
                href={item.href}
                className="rounded-lg border border-slate-200 bg-slate-50 px-3 py-2 text-sm font-semibold text-slate-700 transition hover:border-primary-300 hover:bg-primary-50 hover:text-primary-700 dark:border-slate-700 dark:bg-slate-800 dark:text-slate-100 dark:hover:border-primary-700 dark:hover:bg-slate-700"
              >
                {item.label}
              </Link>
            ))}
          </nav>
        </header>

        <section className="grid gap-4 md:grid-cols-2 xl:grid-cols-4">{children}</section>
      </div>
    </main>
  );
}
