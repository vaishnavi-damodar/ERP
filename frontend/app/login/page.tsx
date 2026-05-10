'use client';

import { useState } from 'react';
import Link from 'next/link';
import { useRouter } from 'next/navigation';
import { useAuth } from '@/context/AuthContext';
import { toast } from 'react-hot-toast';

export default function LoginPage() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const { login } = useAuth();
  const router = useRouter();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);
    try {
      await login(email, password);
      toast.success('Login successful!');
      router.push('/dashboard');
    } catch (error: any) {
      console.error('Login error:', error);
      const detail = error.response?.data?.detail;
      if (Array.isArray(detail)) {
        const messages = detail.map((err: any) => `${err.loc[err.loc.length - 1]}: ${err.msg}`).join(', ');
        toast.error(`Validation Error: ${messages}`);
      } else {
        toast.error(error.response?.data?.detail || error.message || 'Login failed.');
      }
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <main className="min-h-screen bg-gradient-to-br from-slate-100 via-primary-50 to-slate-200 px-4 py-10 dark:from-slate-950 dark:via-slate-900 dark:to-slate-950 md:px-8">
      <div className="mx-auto grid max-w-6xl gap-6 lg:grid-cols-2">
        <section className="rounded-2xl border border-slate-200 bg-white p-8 shadow-xl dark:border-slate-800 dark:bg-slate-900">
          <p className="inline-flex rounded-full bg-primary-100 px-3 py-1 text-xs font-semibold uppercase tracking-[0.2em] text-primary-700 dark:bg-primary-900/40 dark:text-primary-300">
            Secure Access
          </p>
          <h1 className="mt-4 text-3xl font-black text-slate-900 dark:text-slate-100">Welcome Back</h1>
          <p className="mt-2 text-slate-600 dark:text-slate-300">Sign in to continue to your personalized ERP dashboard.</p>

          <form className="mt-6 space-y-4" onSubmit={handleSubmit}>
            <div>
              <label className="mb-2 block text-sm font-semibold text-slate-700 dark:text-slate-200">Email</label>
              <input 
                type="email" 
                placeholder="name@college.edu" 
                required
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                className="w-full rounded-lg border border-slate-300 bg-white px-3 py-2 dark:border-slate-700 dark:bg-slate-800" 
              />
            </div>
            <div>
              <label className="mb-2 block text-sm font-semibold text-slate-700 dark:text-slate-200">Password</label>
              <input 
                type="password" 
                placeholder="Enter your password" 
                required
                minLength={6}
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                className="w-full rounded-lg border border-slate-300 bg-white px-3 py-2 dark:border-slate-700 dark:bg-slate-800" 
              />
            </div>
            <button 
              type="submit" 
              disabled={isLoading}
              className="btn btn-primary w-full"
            >
              {isLoading ? 'Logging in...' : 'Login'}
            </button>
          </form>

          <p className="mt-4 text-sm text-slate-600 dark:text-slate-300">
            New here? <Link href="/signup" className="font-semibold">Create an account</Link>
          </p>
        </section>

        <section className="rounded-2xl border border-slate-200 bg-white p-8 shadow-xl dark:border-slate-800 dark:bg-slate-900">
          <h2 className="text-2xl font-black text-slate-900 dark:text-slate-100">Quick Role Access</h2>
          <p className="mt-2 text-slate-600 dark:text-slate-300">Jump to role previews while API auth wiring is in progress.</p>
          <div className="mt-6 grid gap-3">
            <Link href="/admin" className="btn btn-secondary text-center">Admin Dashboard</Link>
            <Link href="/faculty" className="btn btn-secondary text-center">Faculty Dashboard</Link>
            <Link href="/student" className="btn btn-secondary text-center">Student Dashboard</Link>
            <Link href="/dashboard" className="btn btn-secondary text-center">Unified Dashboard</Link>
          </div>
        </section>
      </div>
    </main>
  );
}
