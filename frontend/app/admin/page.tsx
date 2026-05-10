import AppShell from '@/components/AppShell';

const approvals = [
  { item: 'New Admission Batch', owner: 'Admissions Office', eta: 'Today' },
  { item: 'Faculty Promotion Cycle', owner: 'HR Team', eta: 'Tomorrow' },
  { item: 'Lab Procurement Request', owner: 'Science Dept', eta: '2 days' },
  { item: 'Transport Vendor Renewal', owner: 'Operations', eta: '3 days' },
];

export default function AdminPage() {
  return (
    <AppShell
      badge="Admin"
      title="Administrative Dashboard"
      subtitle="Monitor institution-wide performance, approvals, compliance, and operational workload from one executive panel."
    >
      <article className="card">
        <p className="text-sm font-semibold uppercase tracking-wide text-primary-700 dark:text-primary-300">Revenue This Month</p>
        <p className="mt-2 text-3xl font-black">$412K</p>
        <p className="mt-2 text-sm text-emerald-600 dark:text-emerald-400">Collected 87% of monthly target</p>
      </article>
      <article className="card">
        <p className="text-sm font-semibold uppercase tracking-wide text-primary-700 dark:text-primary-300">Open Tickets</p>
        <p className="mt-2 text-3xl font-black">29</p>
        <p className="mt-2 text-sm text-amber-600 dark:text-amber-400">12 high-priority issues pending</p>
      </article>
      <article className="card">
        <p className="text-sm font-semibold uppercase tracking-wide text-primary-700 dark:text-primary-300">Policy Compliance</p>
        <p className="mt-2 text-3xl font-black">96.3%</p>
        <p className="mt-2 text-sm text-slate-600 dark:text-slate-300">Audit-ready for this quarter</p>
      </article>
      <article className="card">
        <p className="text-sm font-semibold uppercase tracking-wide text-primary-700 dark:text-primary-300">Events This Week</p>
        <p className="mt-2 text-3xl font-black">8</p>
        <p className="mt-2 text-sm text-slate-600 dark:text-slate-300">3 require administrative confirmation</p>
      </article>

      <article className="card md:col-span-2 xl:col-span-2">
        <h3 className="text-xl font-black">Pending Approvals</h3>
        <div className="mt-4 overflow-x-auto">
          <table>
            <thead>
              <tr>
                <th>Request</th>
                <th>Owner</th>
                <th>ETA</th>
              </tr>
            </thead>
            <tbody>
              {approvals.map((approval) => (
                <tr key={approval.item}>
                  <td>{approval.item}</td>
                  <td>{approval.owner}</td>
                  <td>{approval.eta}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </article>

      <article className="card md:col-span-2 xl:col-span-2">
        <h3 className="text-xl font-black">Quick Actions</h3>
        <div className="mt-4 grid gap-3 sm:grid-cols-2">
          <button className="btn btn-primary">Publish Circular</button>
          <button className="btn btn-secondary">Lock Timetable</button>
          <button className="btn btn-secondary">Export Audit Report</button>
          <button className="btn btn-secondary">Start Fee Reminder Campaign</button>
        </div>
      </article>
    </AppShell>
  );
}
