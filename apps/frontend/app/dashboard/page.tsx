"use client";

import FraudForm from "@/components/FraudForm";
import TransactionHistory from "@/components/TransactionHistory";
import { authFetch, logout } from "@/lib/api";
import { useRouter } from "next/navigation";
import { useCallback, useEffect, useState } from "react";

const API_URL =
  process.env.NEXT_PUBLIC_BACKEND_URL ?? "http://localhost:4000";

type User = {
  id: string;
  name: string;
  email: string;
  role: string;
};

type FraudPrediction = {
  id: string;
  prediction: number;
  isFraud: boolean;
  fraudProbability: number;
  threshold: number;
  result: string;
  riskLevel: string;
  modelType: string;
  modelVersion: string;
  featuresUsed: number;
  createdAt: string;
};

type Transaction = {
  id: string;
  amount: number;
  merchantType: string;
  location: string;
  transactionTime: string;
  paymentMethod: string;
  deviceType: string;
  isInternational: boolean;
  previousFailedAttempts: number;
  createdAt: string;
  prediction: FraudPrediction | null;
};

export default function DashboardPage() {
  const router = useRouter();

  const [user, setUser] = useState<User | null>(null);
  const [transactions, setTransactions] = useState<Transaction[]>([]);
  const [historyLoading, setHistoryLoading] = useState(true);
  const [pageLoading, setPageLoading] = useState(true);

  const loadTransactions = useCallback(async () => {
    try {
      setHistoryLoading(true);

      const response = await authFetch(`${API_URL}/transactions`);

      if (response.status === 401) {
        localStorage.removeItem("accessToken");
        localStorage.removeItem("user");
        router.replace("/login");
        return;
      }

      if (!response.ok) {
        throw new Error("Failed to load transaction history");
      }

      const data = (await response.json()) as Transaction[];

      setTransactions(data);
    } catch {
      setTransactions([]);
    } finally {
      setHistoryLoading(false);
    }
  }, [router]);

  useEffect(() => {
    async function loadDashboard() {
      try {
        const response = await authFetch(`${API_URL}/auth/me`);

        if (!response.ok) {
          localStorage.removeItem("accessToken");
          localStorage.removeItem("user");
          router.replace("/login");
          return;
        }

        const data = (await response.json()) as {
          user: User;
        };

        setUser(data.user);
        localStorage.setItem("user", JSON.stringify(data.user));

        await loadTransactions();
      } catch {
        localStorage.removeItem("accessToken");
        localStorage.removeItem("user");
        router.replace("/login");
      } finally {
        setPageLoading(false);
      }
    }

    void loadDashboard();
  }, [loadTransactions, router]);

  async function handleLogout() {
    await logout();
    router.replace("/login");
  }

  if (pageLoading) {
    return (
      <main className="flex min-h-screen items-center justify-center bg-slate-950 text-white">
        <div className="text-center">
          <div className="mx-auto h-8 w-8 animate-spin rounded-full border-2 border-slate-700 border-t-cyan-400" />

          <p className="mt-4 text-sm text-slate-400">
            Loading dashboard...
          </p>
        </div>
      </main>
    );
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

            <div className="flex flex-wrap items-center gap-2">
              <button
                type="button"
                onClick={() => router.push("/credit-card-fraud")}
                className="rounded-xl border border-cyan-500/30 bg-cyan-500/10 px-4 py-2 text-sm font-semibold text-cyan-200 transition hover:bg-cyan-500/20"
              >
                Credit Card Fraud Detection
              </button>

              <button
                type="button"
                onClick={() => void handleLogout()}
                className="rounded-xl border border-slate-700 bg-slate-950/40 px-4 py-2 text-sm font-semibold text-slate-200 transition hover:bg-slate-800"
              >
                Logout
              </button>
            </div>
          </div>

          <div className="mt-6">
            <FraudForm
              dark={true}
              onPredictionComplete={() => {
                void loadTransactions();
              }}
            />
          </div>

          <TransactionHistory
            transactions={transactions}
            loading={historyLoading}
          />
        </div>
      </section>
    </main>
  );
}