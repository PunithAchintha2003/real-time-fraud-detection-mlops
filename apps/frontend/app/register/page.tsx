"use client";

import Link from "next/link";
import { useRouter } from "next/navigation";
import { useState } from "react";

const API_URL = process.env.NEXT_PUBLIC_BACKEND_URL ?? "http://localhost:4000";

export default function RegisterPage() {
  const router = useRouter();

  const [formData, setFormData] = useState({
    name: "",
    email: "",
    password: "",
  });

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  async function handleSubmit(event: React.FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setLoading(true);
    setError("");

    try {
      const response = await fetch(`${API_URL}/auth/register`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(formData),
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.message ?? "Registration failed");
      }

      router.push("/login");
    } catch (err) {
      setError(err instanceof Error ? err.message : "Registration failed");
    } finally {
      setLoading(false);
    }
  }

  return (
    <main className="min-h-screen bg-slate-950 text-white">
      <div className="absolute inset-0 bg-[radial-gradient(circle_at_top_left,rgba(34,211,238,0.18),transparent_35%),radial-gradient(circle_at_bottom_right,rgba(59,130,246,0.16),transparent_35%)]" />

      <section className="relative flex min-h-screen items-center justify-center px-4 py-10">
        <div className="grid w-full max-w-6xl gap-8 lg:grid-cols-2 lg:items-center">
          <div className="hidden lg:block">
            <p className="mb-4 inline-flex rounded-full border border-cyan-400/30 bg-cyan-400/10 px-4 py-2 text-sm font-medium text-cyan-600 dark:text-cyan-300">
              Real-Time Fraud Detection MLOps
            </p>

            <h1 className="max-w-xl text-5xl font-bold leading-tight">
              Secure access for your{" "}
              <span className="bg-gradient-to-r from-cyan-400 to-blue-500 bg-clip-text text-transparent">
                fraud detection dashboard
              </span>
            </h1>

            <p className="mt-5 max-w-lg text-base leading-7 text-slate-600 dark:text-slate-400">
              Create an account to access ML-powered fraud prediction tools,
              monitoring dashboards, and transaction analysis features.
            </p>

            <div className="mt-8 grid max-w-lg grid-cols-3 gap-3">
              {["JWT", "Prisma", "Postgres"].map((item) => (
                <div
                  key={item}
                  className="rounded-2xl border border-slate-200 bg-white/70 p-4 dark:border-slate-800 dark:bg-slate-900/70"
                >
                  <p className="text-xl font-bold text-cyan-600 dark:text-cyan-300">
                    {item}
                  </p>
                  <p className="mt-1 text-xs text-slate-500 dark:text-slate-400">
                    {item === "JWT" ? "Auth" : item === "Prisma" ? "ORM" : "DB"}
                  </p>
                </div>
              ))}
            </div>
          </div>

          <div className="mx-auto w-full max-w-md rounded-3xl border border-slate-200 bg-white/85 p-8 shadow-2xl shadow-slate-300/40 backdrop-blur dark:border-slate-800 dark:bg-slate-900/80 dark:shadow-cyan-950/30">
            <div className="mb-8">
              <p className="text-sm font-semibold uppercase tracking-[0.25em] text-cyan-600 dark:text-cyan-300">
                Register
              </p>
              <h2 className="mt-3 text-3xl font-bold">Create account</h2>
              <p className="mt-2 text-sm text-slate-600 dark:text-slate-400">
                Start using the fraud detection platform.
              </p>
            </div>

            <form onSubmit={handleSubmit} className="space-y-5">
              <input
                type="text"
                value={formData.name}
                onChange={(event) =>
                  setFormData({ ...formData, name: event.target.value })
                }
                className="w-full rounded-xl border border-slate-300 bg-white px-4 py-3 text-slate-950 outline-none transition placeholder:text-slate-400 focus:border-cyan-500 focus:ring-2 focus:ring-cyan-400/20 dark:border-slate-700 dark:bg-slate-950/70 dark:text-white dark:placeholder:text-slate-600 dark:focus:border-cyan-400"
                placeholder="Full name"
                required
              />

              <input
                type="email"
                value={formData.email}
                onChange={(event) =>
                  setFormData({ ...formData, email: event.target.value })
                }
                className="w-full rounded-xl border border-slate-300 bg-white px-4 py-3 text-slate-950 outline-none transition placeholder:text-slate-400 focus:border-cyan-500 focus:ring-2 focus:ring-cyan-400/20 dark:border-slate-700 dark:bg-slate-950/70 dark:text-white dark:placeholder:text-slate-600 dark:focus:border-cyan-400"
                placeholder="Email address"
                required
              />

              <input
                type="password"
                value={formData.password}
                onChange={(event) =>
                  setFormData({ ...formData, password: event.target.value })
                }
                className="w-full rounded-xl border border-slate-300 bg-white px-4 py-3 text-slate-950 outline-none transition placeholder:text-slate-400 focus:border-cyan-500 focus:ring-2 focus:ring-cyan-400/20 dark:border-slate-700 dark:bg-slate-950/70 dark:text-white dark:placeholder:text-slate-600 dark:focus:border-cyan-400"
                placeholder="Minimum 8 characters"
                minLength={8}
                required
              />

              {error && (
                <p className="rounded-xl border border-red-500/30 bg-red-500/10 px-4 py-3 text-sm text-red-600 dark:text-red-300">
                  {error}
                </p>
              )}

              <button
                type="submit"
                disabled={loading}
                className="w-full rounded-xl bg-gradient-to-r from-cyan-400 to-blue-500 px-4 py-3 font-semibold text-slate-950 shadow-lg shadow-cyan-500/20 transition hover:from-cyan-300 hover:to-blue-400 disabled:cursor-not-allowed disabled:opacity-60"
              >
                {loading ? "Creating account..." : "Create account"}
              </button>
            </form>

            <p className="mt-7 text-center text-sm text-slate-600 dark:text-slate-400">
              Already have an account?{" "}
              <Link href="/login" className="font-semibold text-cyan-600 dark:text-cyan-300">
                Login
              </Link>
            </p>
          </div>
        </div>
      </section>
    </main>
  );
}
