import AppShell from '@/components/AppShell';

const classes = [
  { course: 'Database Systems', room: 'B-204', time: '09:00 AM' },
  { course: 'Web Technologies', room: 'C-110', time: '11:00 AM' },
  { course: 'Project Mentoring', room: 'Innovation Lab', time: '02:00 PM' },
];

export default function FacultyPage() {
  return (
    <AppShell
      badge="Faculty"
      title="Faculty Dashboard"
      subtitle="Track teaching schedule, attendance trends, assessment queues, and communication tasks in one teaching cockpit."
    >
      <article className="card">
        <p className="text-sm font-semibold uppercase tracking-wide text-primary-700 dark:text-primary-300">Classes Today</p>
        <p className="mt-2 text-3xl font-black">6</p>
        <p className="mt-2 text-sm text-slate-600 dark:text-slate-300">3 completed, 3 upcoming</p>
      </article>
      <article className="card">
        <p className="text-sm font-semibold uppercase tracking-wide text-primary-700 dark:text-primary-300">Average Attendance</p>
        <p className="mt-2 text-3xl font-black">89.6%</p>
        <p className="mt-2 text-sm text-emerald-600 dark:text-emerald-400">+2.1% since last week</p>
      </article>
      <article className="card">
        <p className="text-sm font-semibold uppercase tracking-wide text-primary-700 dark:text-primary-300">Pending Evaluations</p>
        <p className="mt-2 text-3xl font-black">42</p>
        <p className="mt-2 text-sm text-amber-600 dark:text-amber-400">Due before Friday 6:00 PM</p>
      </article>
      <article className="card">
        <p className="text-sm font-semibold uppercase tracking-wide text-primary-700 dark:text-primary-300">Doubt Sessions</p>
        <p className="mt-2 text-3xl font-black">3</p>
        <p className="mt-2 text-sm text-slate-600 dark:text-slate-300">Booked by final-year students</p>
      </article>

      <article className="card md:col-span-2 xl:col-span-2">
        <h3 className="text-xl font-black">Today's Teaching Plan</h3>
        <div className="mt-4 space-y-3">
          {classes.map((session) => (
            <div
              key={session.course}
              className="rounded-lg border border-slate-200 bg-slate-50 p-3 dark:border-slate-700 dark:bg-slate-800"
            >
              <p className="font-semibold">{session.course}</p>
              <p className="text-sm text-slate-600 dark:text-slate-300">{session.room} | {session.time}</p>
            </div>
          ))}
        </div>
      </article>

      <article className="card md:col-span-2 xl:col-span-2">
        <h3 className="text-xl font-black">Action Queue</h3>
        <ul className="mt-4 space-y-3 text-sm text-slate-700 dark:text-slate-300">
          <li className="rounded-lg bg-slate-100 p-3 dark:bg-slate-800">Submit internal marks for Semester 5 by tomorrow.</li>
          <li className="rounded-lg bg-slate-100 p-3 dark:bg-slate-800">Publish assignment feedback for Web Technologies.</li>
          <li className="rounded-lg bg-slate-100 p-3 dark:bg-slate-800">Review attendance anomalies for Section C.</li>
        </ul>
      </article>
    </AppShell>
  );
}
