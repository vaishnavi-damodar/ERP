import AppShell from '@/components/AppShell';

export default function HomePage() {
  return (
    <AppShell
      badge="EduSync ERP"
      title="College Operations Command Center"
      subtitle="Manage admissions, academics, attendance, finance, and communication from a unified interface designed for administrators, faculty, and students."
    >
      <article className="card border border-primary-100 dark:border-primary-900/40">
        <p className="text-sm font-semibold uppercase tracking-wide text-primary-700 dark:text-primary-300">Total Students</p>
        <p className="mt-3 text-4xl font-black">3,482</p>
        <p className="mt-2 text-sm text-emerald-600 dark:text-emerald-400">+4.8% compared to last semester</p>
      </article>
      <article className="card border border-primary-100 dark:border-primary-900/40">
        <p className="text-sm font-semibold uppercase tracking-wide text-primary-700 dark:text-primary-300">Faculty Strength</p>
        <p className="mt-3 text-4xl font-black">224</p>
        <p className="mt-2 text-sm text-slate-600 dark:text-slate-300">19 departments with active workload balancing</p>
      </article>
      <article className="card border border-primary-100 dark:border-primary-900/40">
        <p className="text-sm font-semibold uppercase tracking-wide text-primary-700 dark:text-primary-300">Attendance Today</p>
        <p className="mt-3 text-4xl font-black">92.4%</p>
        <p className="mt-2 text-sm text-emerald-600 dark:text-emerald-400">On track for monthly attendance target</p>
      </article>
      <article className="card border border-primary-100 dark:border-primary-900/40">
        <p className="text-sm font-semibold uppercase tracking-wide text-primary-700 dark:text-primary-300">Pending Actions</p>
        <p className="mt-3 text-4xl font-black">37</p>
        <p className="mt-2 text-sm text-amber-600 dark:text-amber-400">Admissions, fee approvals, and timetable drafts</p>
      </article>

      <article className="card md:col-span-2 xl:col-span-3">
        <h3 className="text-xl font-black">Platform Highlights</h3>
        <ul className="mt-4 space-y-3 text-sm text-slate-700 dark:text-slate-300">
          <li className="rounded-lg bg-slate-100 p-3 dark:bg-slate-800">Role-based panels for Admin, Faculty, and Student users.</li>
          <li className="rounded-lg bg-slate-100 p-3 dark:bg-slate-800">Unified attendance, assignment, and exam visibility from one workflow.</li>
          <li className="rounded-lg bg-slate-100 p-3 dark:bg-slate-800">Fast API-backed architecture ready for live integration.</li>
        </ul>
      </article>
      <article className="card">
        <h3 className="text-xl font-black">System Status</h3>
        <div className="mt-4 space-y-3 text-sm">
          <p className="rounded-lg border border-emerald-200 bg-emerald-50 px-3 py-2 text-emerald-700 dark:border-emerald-900/40 dark:bg-emerald-950/40 dark:text-emerald-300">Frontend services: healthy</p>
          <p className="rounded-lg border border-emerald-200 bg-emerald-50 px-3 py-2 text-emerald-700 dark:border-emerald-900/40 dark:bg-emerald-950/40 dark:text-emerald-300">Backend health endpoint: reachable</p>
          <p className="rounded-lg border border-primary-200 bg-primary-50 px-3 py-2 text-primary-700 dark:border-primary-900/40 dark:bg-primary-950/40 dark:text-primary-300">Routing map: fully configured</p>
        </div>
      </article>
    </AppShell>
  );
}
