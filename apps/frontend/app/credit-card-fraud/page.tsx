"use client";

import { authFetch, logout } from "@/lib/api";
import { FormEvent, useState } from "react";
import { useRouter } from "next/navigation";

const API_URL =
  process.env.NEXT_PUBLIC_BACKEND_URL ?? "http://localhost:4000";

const featureNames = Array.from(
  { length: 28 },
  (_, index) => `V${index + 1}`,
);

const demoValues: Record<string, string> = {
  Time: "7610",
  V1: "0.725645739819857",
  V2: "2.30089443776603",
  V3: "-5.32997618300917",
  V4: "4.007682804682",
  V5: "-1.73041059025206",
  V6: "-1.73219256822244",
  V7: "-3.96859261813707",
  V8: "1.06372815344105",
  V9: "-0.486096552344833",
  V10: "-4.62498495406596",
  V11: "5.5887239146762",
  V12: "-7.14824263637845",
  V13: "1.68045074096412",
  V14: "-6.21025774661028",
  V15: "0.495282117814298",
  V16: "-3.5995402092184",
  V17: "-4.83032424210571",
  V18: "-0.649090120211694",
  V19: "2.2501232487881",
  V20: "0.504646226103286",
  V21: "0.589669127323198",
  V22: "0.109541319229913",
  V23: "0.601045276521079",
  V24: "-0.364700278220039",
  V25: "-1.84307769215194",
  V26: "0.351909298434892",
  V27: "0.594549978086464",
  V28: "0.0993722360416487",
  Amount: "1",
};

type CreditCardPredictionResponse = {
  prediction: number;
  is_fraud: boolean;
  fraud_probability: number;
  threshold: number;
  result: string;
  model_type?: string;
  model_version?: string;
  features_used?: number;
};

export default function CreditCardFraudPage() {
  const router = useRouter();

  const [values, setValues] =
    useState<Record<string, string>>(demoValues);

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [result, setResult] =
    useState<CreditCardPredictionResponse | null>(null);

  function updateValue(name: string, value: string) {
    setValues((current) => ({
      ...current,
      [name]: value,
    }));
  }

  function loadDemoData() {
    setValues(demoValues);
    setError("");
    setResult(null);
  }

  function clearForm() {
    const emptyValues: Record<string, string> = {};

    for (const name of ["Time", ...featureNames, "Amount"]) {
      emptyValues[name] = "";
    }

    setValues(emptyValues);
    setError("");
    setResult(null);
  }

  async function handleLogout() {
    await logout();
    router.replace("/login");
  }

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();

    setLoading(true);
    setError("");
    setResult(null);

    const allFields = ["Time", ...featureNames, "Amount"];

    for (const field of allFields) {
      if (
        values[field] === undefined ||
        values[field].trim() === ""
      ) {
        setError(`${field} is required.`);
        setLoading(false);
        return;
      }

      const parsed = Number(values[field]);

      if (!Number.isFinite(parsed)) {
        setError(`${field} must be a valid number.`);
        setLoading(false);
        return;
      }
    }

    const payload: Record<string, number> = {};

    for (const field of allFields) {
      payload[field] = Number(values[field]);
    }

    if (payload.Time < 0) {
      setError("Time must be greater than or equal to 0.");
      setLoading(false);
      return;
    }

    if (payload.Amount < 0) {
      setError("Amount must be greater than or equal to 0.");
      setLoading(false);
      return;
    }

    try {
      const response = await authFetch(
        `${API_URL}/transactions/check-credit-card`,
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify(payload),
        },
      );

      if (response.status === 401) {
        localStorage.removeItem("accessToken");
        localStorage.removeItem("user");
        router.replace("/login");
        return;
      }

      if (!response.ok) {
        let message = "Credit card fraud prediction failed.";

        try {
          const errorData = (await response.json()) as {
            message?: string | string[];
            detail?: string;
          };

          if (typeof errorData.detail === "string") {
            message = errorData.detail;
          } else if (typeof errorData.message === "string") {
            message = errorData.message;
          } else if (Array.isArray(errorData.message)) {
            message = errorData.message.join(", ");
          }
        } catch {
          // Keep the default message.
        }

        throw new Error(message);
      }

      const data =
        (await response.json()) as CreditCardPredictionResponse;

      setResult(data);
    } catch (err) {
      setError(
        err instanceof Error
          ? err.message
          : "Cannot connect to the fraud detection service.",
      );
    } finally {
      setLoading(false);
    }
  }

  const riskLevel =
    result === null
      ? ""
      : result.fraud_probability >= 0.75
        ? "High Risk"
        : result.fraud_probability >= 0.45
          ? "Medium Risk"
          : "Low Risk";

  return (
    <main className="relative min-h-screen bg-slate-950 text-white">
      <div className="absolute inset-0 bg-[radial-gradient(circle_at_top_left,rgba(34,211,238,0.18),transparent_35%),radial-gradient(circle_at_bottom_right,rgba(59,130,246,0.16),transparent_35%)]" />

      <section className="relative mx-auto min-h-screen max-w-6xl px-4 py-8">
        <div className="rounded-3xl border border-slate-800 bg-slate-900/80 p-6 shadow-2xl shadow-cyan-950/30 backdrop-blur">
          <div className="flex flex-col gap-4 border-b border-slate-800 pb-6 sm:flex-row sm:items-center sm:justify-between">
            <div>
              <button
                type="button"
                onClick={() => router.push("/dashboard")}
                className="mb-4 text-sm font-semibold text-cyan-300 transition hover:text-cyan-200"
              >
                ← Back to Dashboard
              </button>

              <p className="text-sm font-semibold uppercase tracking-[0.25em] text-cyan-300">
                Credit Card Fraud Detection
              </p>

              <h1 className="mt-2 text-3xl font-bold">
                Credit Card Transaction Analyzer
              </h1>

              <p className="mt-2 max-w-2xl text-sm text-slate-400">
                Enter the anonymized crit-card transaction features and
                run the existing FraudDetectionModel.
              </p>
            </div>

            <button
              type="button"
              onClick={() => void handleLogout()}
              className="rounded-xl border border-slate-700 bg-slate-950/40 px-4 py-2 text-sm font-semibold text-slate-200 transition hover:bg-slate-800"
            >
              Logout
            </button>
          </div>

          <form
            onSubmit={handleSubmit}
            className="mt-6 space-y-6"
          >
            <div className="rounded-2xl border border-cyan-500/20 bg-cyan-500/5 p-4">
              <p className="text-sm font-semibold text-cyan-200">
                About these features
              </p>

              <p className="mt-1 text-xs leading-5 text-slate-400">
                V1–V28 are anonymized numerical features from the
                credit-card fraud dataset. They do not represent raw card
                details such as card number or V.
              </p>
            </div>

            <div className="grid grid-cols-1 gap-3 sm:grid-cols-2 lg:grid-cols-3">
              <div>
                <label className="mb-1 block text-xs font-semibold text-white/70">
                  Time (seconds)
                </label>

                <input
                  type="number"
                  step="any"
                  min="0"
                  value={values.Time ?? ""}
                  onChange={(event) =>
                    updateValue("Time", event.target.value)
                  }
                  className="h-11 w-full rounded-xl border border-white/10 bg-black/40 px-3 text-sm font-medium text-white outline-none transition placeholder:text-white/40 focus:border-white/40 focus:bg-black/60"
                />
              </div>

              {featureNames.map((feature) => (
                <div key={feature}>
                  <label className="mb-1 block text-xs font-semibold text-white/70">
                    {feature}
                  </label>

                  <input
                    type="number"
                    step="any"
                    value={values[feature] ?? ""}
                    onChange={(event) =>
                      updateValue(feature, event.target.value)
                    }
                    className="h-11 w-full rounded-xl border border-white/10 bg-black/40 px-3 text-sm font-medium text-white outline-none transition placeholder:text-white/40 focus:border-white/40 focus:bg-black/60"
                  />
                </div>
              ))}

              <div>
                <label className="mb-1 block text-xs font-semibold text-white/70">
                  Amount
                </label>

                <input
                  type="number"
                  step="any"
                  min="0"
                  value={values.Amount ?? ""}
                  onChange={(event) =>
                    updateValue("Amount", event.target.value)
                  }
                  className="h-11 w-full rounded-xl border border-cyan-400/30 bg-black/40 px-3 text-sm font-medium text-white outline-none transition placeholder:text-white/40 focus:border-cyan-300 focus:bg-black/60"
                />
              </div>
            </div>

            <div className="grid grid-cols-1 gap-3 sm:grid-cols-3">
              <button
                type="submit"
                disabled={loading}
                className="h-11 rounded-xl bg-white text-sm font-bold text-black transition hover:bg-white/90 disabled:cursor-not-allowed disabled:opacity-60"
              >
                {loading ? "Detecting..." : "Detect Fraud"}
              </button>

              <button
                type="button"
                onClick={loadDemoData}
                disabled={loading}
                className="h-11 rounded-xl border border-cyan-400/30 bg-cyan-400/10 text-sm font-semibold text-cyan-200 transition hover:bg-cyan-400/20 disabled:cursor-not-allowed disabled:opacity-60"
              >
                Load Fraud Demo
              </button>

              <button
                type="button"
                onClick={clearForm}
                disabled={loading}
                className="h-11 rounded-xl border border-white/15 bg-transparent text-sm font-semibold text-white/80 transition hover:bg-white/10 disabled:cursor-not-allowed disabled:opacity-60"
              >
                Clear
              </button>
            </div>

            {error && (
              <div className="rounded-2xl border border-red-400/30 bg-red-500/10 p-4 text-sm font-semibold text-red-200">
                {error}
              </div>
            )}

            {result && (
              <div className="rounded-2xl border border-white/10 bg-black/30 p-5">
                <div className="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
                  <div>
                    <p
                      className={
                        result.is_fraud
                          ? "text-sm font-semibold text-red-400"
                          : "text-sm font-semibold text-emerald-400"
                      }
                    >
                      {riskLevel}
                    </p>

                    <h2 className="mt-1 text-2xl font-bold">
                      {result.is_fraud
                        ? "Fraud Detected"
                        : "Legitimate Transaction"}
                    </h2>
                  </div>

                  <div
                    className={
                      result.is_fraud
                        ? "rounded-2xl bg-red-500/15 px-5 py-4 text-center"
                        : "rounded-2xl bg-emerald-500/15 px-5 py-4 text-center"
                    }
                  >
                    <p className="text-xs font-semibold opacity-70">
                      Fraud Probability
                    </p>

                    <p className="text-3xl font-bold">
                      {(result.fraud_probability * 100).toFixed(2)}%
                    </p>
                  </div>
                </div>

                <div className="mt-5 grid grid-cols-2 gap-4 text-xs text-white/60 sm:grid-cols-4">
                  <div>
                    <p className="font-semibold">Decision</p>
                    <p>{result.is_fraud ? "Fraud" : "Legitimate"}</p>
                  </div>

                  <div>
                    <p className="font-semibold">Threshold</p>
                    <p>{(result.threshold * 100).toFixed(0)}%</p>
                  </div>

                  <div>
                    <p className="font-semibold">Model</p>
                    <p>{result.model_type ?? "FraudDetectionModel"}</p>
                  </div>

                  <div>
                    <p className="font-semibold">Version</p>
                    <p>{result.model_version ?? "MLflow Champion"}</p>
                  </div>
                </div>
              </div>
            )}
          </form>
        </div>
      </section>
    </main>
  );
}
