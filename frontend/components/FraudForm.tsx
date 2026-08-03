"use client";

import { FormEvent, useState } from "react";

type PredictionResponse = {
  prediction: number;
  is_fraud: boolean;
  fraud_probability: number;
  threshold: number;
  result: string;
  model_source: string;
  model_version: string;
};

type FraudFormProps = {
  dark: boolean;
};

const featureNames = Array.from({ length: 28 }, (_, index) => `V${index + 1}`);

function createInitialFeatures() {
  const values: Record<string, string> = {};

  featureNames.forEach((feature) => {
    values[feature] = "0";
  });

  return values;
}

export default function FraudForm({ dark }: FraudFormProps) {
  const [time, setTime] = useState("0");
  const [amount, setAmount] = useState("");
  const [features, setFeatures] = useState<Record<string, string>>(
    createInitialFeatures
  );

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [result, setResult] = useState<PredictionResponse | null>(null);

  function updateFeature(name: string, value: string) {
    setFeatures((currentValues) => ({
      ...currentValues,
      [name]: value,
    }));
  }

  function clearForm() {
    setTime("0");
    setAmount("");
    setFeatures(createInitialFeatures());
    setResult(null);
    setError("");
  }

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();

    setLoading(true);
    setError("");
    setResult(null);

    const parsedTime = Number(time);
    const parsedAmount = Number(amount);

    if (Number.isNaN(parsedTime) || Number.isNaN(parsedAmount)) {
      setError("Please enter valid numbers for Time and Amount.");
      setLoading(false);
      return;
    }

    if (parsedAmount < 0) {
      setError("Amount cannot be negative.");
      setLoading(false);
      return;
    }

    const payload: Record<string, number> = {
      Time: parsedTime,
      Amount: parsedAmount,
    };

    for (const feature of featureNames) {
      const value = Number(features[feature]);

      if (Number.isNaN(value)) {
        setError(`${feature} must be a valid number.`);
        setLoading(false);
        return;
      }

      payload[feature] = value;
    }

    try {
      const response = await fetch("/fastapi/predict", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(payload),
      });

      if (!response.ok) {
        throw new Error("Prediction request failed.");
      }

      const data = (await response.json()) as PredictionResponse;

      setResult(data);
    } catch {
      setError("Cannot connect to FastAPI. Make sure the API is running.");
    } finally {
      setLoading(false);
    }
  }

  const inputClass = dark
    ? "h-9 w-full rounded-xl border border-white/10 bg-black/40 px-3 text-sm font-medium text-white outline-none transition placeholder:text-white/40 focus:border-white/40 focus:bg-black/60"
    : "h-9 w-full rounded-xl border border-black/10 bg-white px-3 text-sm font-medium text-black outline-none transition placeholder:text-black/40 focus:border-black/40 focus:bg-white";

  const labelClass = dark
    ? "mb-1 block text-xs font-semibold text-white/70"
    : "mb-1 block text-xs font-semibold text-black/60";

  const panelClass = dark
    ? "rounded-2xl border border-white/10 bg-black/30 p-4 text-white"
    : "rounded-2xl border border-black/10 bg-white/80 p-4 text-black";

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      <div className="grid grid-cols-1 gap-3 sm:grid-cols-2">
        <div>
          <label className={labelClass}>Time</label>
          <input
            type="number"
            step="any"
            value={time}
            onChange={(event) => setTime(event.target.value)}
            className={inputClass}
            placeholder="0"
          />
        </div>

        <div>
          <label className={labelClass}>Amount</label>
          <input
            type="number"
            step="any"
            min="0"
            value={amount}
            onChange={(event) => setAmount(event.target.value)}
            className={inputClass}
            placeholder="149.62"
            required
          />
        </div>
      </div>

      <div
        className="
          grid
          max-h-[42vh]
          grid-cols-2
          gap-3
          overflow-y-auto
          pr-1
          sm:max-h-[45vh]
          sm:grid-cols-4
          lg:max-h-none
          lg:grid-cols-7
          lg:overflow-visible
        "
      >
        {featureNames.map((feature) => (
          <div key={feature}>
            <label className={labelClass}>{feature}</label>
            <input
              type="number"
              step="any"
              value={features[feature]}
              onChange={(event) => updateFeature(feature, event.target.value)}
              className={inputClass}
              placeholder="0"
            />
          </div>
        ))}
      </div>

      <div className="grid grid-cols-1 gap-3 sm:grid-cols-2">
        <button
          type="submit"
          disabled={loading}
          className={
            dark
              ? "h-11 rounded-xl bg-white text-sm font-bold text-black transition hover:bg-white/90 disabled:cursor-not-allowed disabled:opacity-60"
              : "h-11 rounded-xl bg-black text-sm font-bold text-white transition hover:bg-black/90 disabled:cursor-not-allowed disabled:opacity-60"
          }
        >
          {loading ? "Analyzing..." : "Analyze Transaction"}
        </button>

        <button
          type="button"
          onClick={clearForm}
          className={
            dark
              ? "h-11 rounded-xl border border-white/15 bg-transparent text-sm font-semibold text-white/80 transition hover:bg-white/10"
              : "h-11 rounded-xl border border-black/10 bg-transparent text-sm font-semibold text-black/70 transition hover:bg-black/5"
          }
        >
          Clear
        </button>
      </div>

      {error && (
        <div
          className={
            dark
              ? "rounded-2xl border border-red-400/30 bg-red-500/10 p-4 text-sm font-semibold text-red-200"
              : "rounded-2xl border border-red-300 bg-red-50 p-4 text-sm font-semibold text-red-700"
          }
        >
          {error}
        </div>
      )}

      {result && (
        <div className={panelClass}>
          <div className="flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
            <div>
              <p
                className={
                  result.is_fraud
                    ? "text-sm font-semibold text-red-400"
                    : "text-sm font-semibold text-emerald-400"
                }
              >
                {result.is_fraud ? "Fraud Detected" : "Legitimate Transaction"}
              </p>

              <h2 className="mt-1 text-2xl font-bold">{result.result}</h2>
            </div>

            <div
              className={
                result.is_fraud
                  ? "rounded-2xl bg-red-500/15 px-4 py-3 text-center"
                  : "rounded-2xl bg-emerald-500/15 px-4 py-3 text-center"
              }
            >
              <p className="text-xs font-semibold opacity-70">
                Fraud Probability
              </p>

              <p className="text-2xl font-bold">
                {(result.fraud_probability * 100).toFixed(2)}%
              </p>
            </div>
          </div>

          <div
            className={
              dark
                ? "mt-4 grid grid-cols-2 gap-3 text-xs text-white/60 sm:grid-cols-4"
                : "mt-4 grid grid-cols-2 gap-3 text-xs text-black/60 sm:grid-cols-4"
            }
          >
            <div>
              <p className="font-semibold">Prediction</p>
              <p>{result.prediction}</p>
            </div>

            <div>
              <p className="font-semibold">Threshold</p>
              <p>{result.threshold}</p>
            </div>

            <div>
              <p className="font-semibold">Model Source</p>
              <p>{result.model_source}</p>
            </div>

            <div>
              <p className="font-semibold">Model Version</p>
              <p>{result.model_version}</p>
            </div>
          </div>
        </div>
      )}
    </form>
  );
}