import AppShell from '@/components/AppShell';

const tasks = [
  { title: 'Database Assignment 4', due: 'Tomorrow, 11:59 PM' },
  { title: 'Cloud Quiz', due: 'May 12, 10:00 AM' },
  { title: 'Project Milestone Demo', due: 'May 14, 02:00 PM' },
];

export default function StudentPage() {
  return (
    <AppShell
      badge="Student"
      title="Student Dashboard"
      subtitle="Keep track of attendance, grades, submissions, and announcements so nothing slips through during the semester."
    >
      <article className="card">
        <p className="text-sm font-semibold uppercase tracking-wide text-primary-700 dark:text-primary-300">Current GPA</p>
        <p className="mt-2 text-3xl font-black">8.72</p>
        <p className="mt-2 text-sm text-emerald-600 dark:text-emerald-400">Up from 8.54 last term</p>
      </article>
      <article className="card">
        <p className="text-sm font-semibold uppercase tracking-wide text-primary-700 dark:text-primary-300">Attendance</p>
        <p className="mt-2 text-3xl font-black">91%</p>
        <p className="mt-2 text-sm text-slate-600 dark:text-slate-300">Safe above minimum threshold</p>
      </article>
      <article className="card">
        <p className="text-sm font-semibold uppercase tracking-wide text-primary-700 dark:text-primary-300">Credits Earned</p>
        <p className="mt-2 text-3xl font-black">94</p>
        <p className="mt-2 text-sm text-slate-600 dark:text-slate-300">Need 26 more credits to graduate</p>
      </article>
      <article className="card">
        <p className="text-sm font-semibold uppercase tracking-wide text-primary-700 dark:text-primary-300">Fee Status</p>
        <p className="mt-2 text-3xl font-black">Due</p>
        <p className="mt-2 text-sm text-amber-600 dark:text-amber-400">Next installment due in 6 days</p>
      </article>

      <article className="card md:col-span-2 xl:col-span-2">
        <h3 className="text-xl font-black">Upcoming Deadlines</h3>
        <div className="mt-4 space-y-3">
          {tasks.map((task) => (
            <div key={task.title} className="rounded-lg border border-slate-200 p-3 dark:border-slate-700">
              <p className="font-semibold">{task.title}</p>
              <p className="text-sm text-slate-600 dark:text-slate-300">Due: {task.due}</p>
            </div>
          ))}
        </div>
      </article>

      <article className="card md:col-span-2 xl:col-span-2">
        <h3 className="text-xl font-black">Today's Timeline</h3>
        <ul className="mt-4 space-y-3 text-sm text-slate-700 dark:text-slate-300">
          <li className="rounded-lg bg-slate-100 p-3 dark:bg-slate-800">08:30 AM - Algorithms lecture, Room A-201</li>
          <li className="rounded-lg bg-slate-100 p-3 dark:bg-slate-800">11:00 AM - Database lab, Lab 3</li>
          <li className="rounded-lg bg-slate-100 p-3 dark:bg-slate-800">03:00 PM - Mini project mentoring, Innovation Hub</li>
        </ul>
      </article>
    </AppShell>
  );
}
