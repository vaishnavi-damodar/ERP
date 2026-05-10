import AppShell from '@/components/AppShell';

const modules = [
  { name: 'Admissions', status: 'Operational', owner: 'Admin Office' },
  { name: 'Academics', status: 'Operational', owner: 'Dean Academics' },
  { name: 'Examinations', status: 'Monitoring', owner: 'Exam Cell' },
  { name: 'Finance', status: 'Operational', owner: 'Accounts Team' },
  { name: 'Library', status: 'Operational', owner: 'Knowledge Center' },
  { name: 'Hostel', status: 'Attention', owner: 'Campus Life' },
];

export default function DashboardPage() {
  return (
    <AppShell
      badge="Overview"
      title="Unified ERP Dashboard"
      subtitle="One place to observe module health, recent platform activity, and team ownership across all major campus operations."
    >
      <article className="card">
        <p className="text-sm font-semibold uppercase tracking-wide text-primary-700 dark:text-primary-300">Total Active Users</p>
        <p className="mt-2 text-3xl font-black">2,917</p>
        <p className="mt-2 text-sm text-slate-600 dark:text-slate-300">Across web and mobile sessions</p>
      </article>
      <article className="card">
        <p className="text-sm font-semibold uppercase tracking-wide text-primary-700 dark:text-primary-300">Incidents</p>
        <p className="mt-2 text-3xl font-black">2</p>
        <p className="mt-2 text-sm text-amber-600 dark:text-amber-400">Both are non-critical warnings</p>
      </article>
      <article className="card">
        <p className="text-sm font-semibold uppercase tracking-wide text-primary-700 dark:text-primary-300">Response Time</p>
        <p className="mt-2 text-3xl font-black">142ms</p>
        <p className="mt-2 text-sm text-emerald-600 dark:text-emerald-400">API latency within SLO</p>
      </article>
      <article className="card">
        <p className="text-sm font-semibold uppercase tracking-wide text-primary-700 dark:text-primary-300">Scheduled Jobs</p>
        <p className="mt-2 text-3xl font-black">17</p>
        <p className="mt-2 text-sm text-slate-600 dark:text-slate-300">All nightly jobs completed</p>
      </article>

      <article className="card md:col-span-2 xl:col-span-2">
        <h3 className="text-xl font-black">Module Health</h3>
        <div className="mt-4 overflow-x-auto">
          <table>
            <thead>
              <tr>
                <th>Module</th>
                <th>Status</th>
                <th>Owner</th>
              </tr>
            </thead>
            <tbody>
              {modules.map((module) => (
                <tr key={module.name}>
                  <td>{module.name}</td>
                  <td>{module.status}</td>
                  <td>{module.owner}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </article>

      <article className="card md:col-span-2 xl:col-span-2">
        <h3 className="text-xl font-black">Recent Activity</h3>
        <ul className="mt-4 space-y-3 text-sm text-slate-700 dark:text-slate-300">
          <li className="rounded-lg bg-slate-100 p-3 dark:bg-slate-800">New timetable version published for Semester 6.</li>
          <li className="rounded-lg bg-slate-100 p-3 dark:bg-slate-800">4 departments completed internal mark submission.</li>
          <li className="rounded-lg bg-slate-100 p-3 dark:bg-slate-800">Finance synced payment records from bank gateway.</li>
          <li className="rounded-lg bg-slate-100 p-3 dark:bg-slate-800">Transport route optimization job finished with no errors.</li>
        </ul>
      </article>
    </AppShell>
  );
}
