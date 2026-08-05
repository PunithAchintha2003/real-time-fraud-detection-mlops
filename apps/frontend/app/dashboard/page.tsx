"use client";

import FraudForm from "@/components/FraudForm";
import { useRouter } from "next/navigation";
import { useEffect, useState } from "react";

type User = {
  id: string;
  name: string;
  email: string;
  role: string;
};

export default function DashboardPage() {
  const router = useRouter();
  const [user, setUser] = useState<User | null>(null);

  useEffect(() => {
    const token = localStorage.getItem("accessToken");
    const savedUser = localStorage.getItem("user");

    if (!token || !savedUser) {
      router.push("/login");
      return;
    }

    setUser(JSON.parse(savedUser));
  }, [router]);

  function handleLogout() {
    localStorage.removeItem("accessToken");
    localStorage.removeItem("user");
    router.push("/login");
  }

  return (
    <main className="relative min-h-screen bg-slate-950 text-white">
      <div className="absolute inset-0 bg-[radial-gradient(circle_at_top_left,rgba(34,211,238,0.18),transparent_35%),radial-gradient(circle_at_bottom_right,rgba(59,130,246,0.16),transparent_35%)]" />

      <section className="relative mx-auto min-h-screen max-w-6xl px-4 py-10">
        <div className="rounded-3xl border border-slate-800 bg-slate-900/80 p-6 shadow-2xl shadow-cyan-950/30 backdrop-blur">
          <div className="flex flex-col gap-4 border-b border-slate-800 pb-6 sm:flex-row sm:items-center sm:justify-between">
            <div>
              <p className="text-sm font-semibold uppercase tracking-[0.25em] text-cyan-300">
                Fraud Detection
              </p>

              <h1 className="mt-2 text-3xl font-bold">
                Transaction Risk Checker
              </h1>

              <p className="mt-2 text-sm text-slate-400">
                Welcome back, {user?.name ?? "User"}. Check transactions using
                the ML-powered fraud detection model.
              </p>
            </div>

            <button
              onClick={handleLogout}
              className="rounded-xl border border-slate-700 bg-slate-950/40 px-4 py-2 text-sm font-semibold text-slate-200 transition hover:bg-slate-800"
            >
              Logout
            </button>
          </div>

          <div className="mt-6">
            <FraudForm dark={true} />
          </div>
        </div>
      </section>
    </main>
  );
}
