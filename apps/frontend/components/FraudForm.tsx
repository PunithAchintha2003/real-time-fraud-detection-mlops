"use client";

import { FormEvent, useState } from "react";

const API_URL = process.env.NEXT_PUBLIC_BACKEND_URL ?? "http://localhost:4000";

type BusinessPredictionResponse = {
  prediction: number;
  is_fraud: boolean;
  fraud_probability: number;
  threshold: number;
  result: string;
  risk_level: string;
  model_type: string;
  model_version: string;
  features_used: number;
  engineered_features: Record<string, number>;
};

type FraudFormProps = {
  dark: boolean;
};

const merchantTypes = [
  { label: "Online Purchase", value: "online_purchase" },
  { label: "Grocery", value: "grocery" },
  { label: "Restaurant", value: "restaurant" },
  { label: "Fuel", value: "fuel" },
  { label: "Electronics", value: "electronics" },
  { label: "Travel", value: "travel" },
  { label: "Digital Goods", value: "digital_goods" },
  { label: "Crypto", value: "crypto" },
  { label: "Gaming", value: "gaming" },
  { label: "Other", value: "other" },
];

const locations = [
  { label: "Sri Lanka", value: "sri_lanka" },
  { label: "India", value: "india" },
  { label: "UAE", value: "uae" },
  { label: "Singapore", value: "singapore" },
  { label: "United Kingdom", value: "united_kingdom" },
  { label: "United States", value: "united_states" },
  { label: "Nigeria", value: "nigeria" },
  { label: "Unknown", value: "unknown" },
  { label: "Other", value: "other" },
];

const paymentMethods = [
  { label: "Card", value: "card" },
  { label: "Bank Transfer", value: "bank_transfer" },
  { label: "Wallet", value: "wallet" },
  { label: "Crypto", value: "crypto" },
  { label: "Cash", value: "cash" },
  { label: "Other", value: "other" },
];

const deviceTypes = [
  { label: "Mobile", value: "mobile" },
  { label: "Desktop", value: "desktop" },
  { label: "Tablet", value: "tablet" },
  { label: "Unknown", value: "unknown" },
  { label: "Other", value: "other" },
];

export default function FraudForm({ dark }: FraudFormProps) {
  const [amount, setAmount] = useState("");
  const [merchantType, setMerchantType] = useState("online_purchase");
  const [location, setLocation] = useState("sri_lanka");
  const [transactionTime, setTransactionTime] = useState("14:30");
  const [paymentMethod, setPaymentMethod] = useState("card");
  const [deviceType, setDeviceType] = useState("mobile");
  const [isInternational, setIsInternational] = useState(false);
  const [failedPaymentAttempts, setFailedPaymentAttempts] = useState("0");

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [result, setResult] = useState<BusinessPredictionResponse | null>(null);

  const labelClass = dark
    ? "mb-1 block text-xs font-semibold text-white/70"
    : "mb-1 block text-xs font-semibold text-black/60";

  const inputClass = dark
    ? "h-11 w-full rounded-xl border border-white/10 bg-black/40 px-3 text-sm font-medium text-white outline-none transition placeholder:text-white/40 focus:border-white/40 focus:bg-black/60"
    : "h-11 w-full rounded-xl border border-black/10 bg-white px-3 text-sm font-medium text-black outline-none transition placeholder:text-black/40 focus:border-black/40 focus:bg-white";

  const selectClass = dark
    ? "h-11 w-full rounded-xl border border-white/10 bg-black/40 px-3 text-sm font-medium text-white outline-none transition focus:border-white/40 focus:bg-black/60"
    : "h-11 w-full rounded-xl border border-black/10 bg-white px-3 text-sm font-medium text-black outline-none transition focus:border-black/40 focus:bg-white";

  const panelClass = dark
    ? "rounded-2xl border border-white/10 bg-black/30 p-4 text-white"
    : "rounded-2xl border border-black/10 bg-white/80 p-4 text-black";

  const checkboxClass = dark
    ? "h-5 w-5 accent-white"
    : "h-5 w-5 accent-black";

  function clearForm() {
    setAmount("");
    setMerchantType("online_purchase");
    setLocation("sri_lanka");
    setTransactionTime("14:30");
    setPaymentMethod("card");
    setDeviceType("mobile");
    setIsInternational(false);
    setFailedPaymentAttempts("0");
    setError("");
    setResult(null);
  }

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();

    setLoading(true);
    setError("");
    setResult(null);

    const parsedAmount = Number(amount);
    const parsedFailedAttempts = Number(failedPaymentAttempts);

    if (Number.isNaN(parsedAmount) || parsedAmount < 0) {
      setError("Please enter a valid transaction amount.");
      setLoading(false);
      return;
    }

    if (Number.isNaN(parsedFailedAttempts) || parsedFailedAttempts < 0) {
      setError("Failed payment attempts must be a valid number.");
      setLoading(false);
      return;
    }

    const payload = {
      amount: parsedAmount,
      merchant_type: merchantType,
      location,
      transaction_time: transactionTime,
      payment_method: paymentMethod,
      device_type: deviceType,
      is_international: isInternational,
      previous_failed_attempts: parsedFailedAttempts,
    };

    try {
      const token = localStorage.getItem("accessToken");

      if (!token) {
        throw new Error("Please login before checking a transaction.");
      }

      const response = await fetch(`${API_URL}/transactions/check`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify(payload),
      });

      if (!response.ok) {
        throw new Error("Prediction request failed.");
      }

      const data = (await response.json()) as BusinessPredictionResponse;

      setResult(data);
    } catch {
      setError("Cannot connect to backend prediction gateway.");
    } finally {
      setLoading(false);
    }
  }

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      <div className="grid grid-cols-1 gap-3 sm:grid-cols-2">
        <div>
          <label className={labelClass}>Transaction Amount</label>
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

        <div>
          <label className={labelClass}>Transaction Time</label>
          <input
            type="time"
            value={transactionTime}
            onChange={(event) => setTransactionTime(event.target.value)}
            className={inputClass}
            required
          />
        </div>

        <div>
          <label className={labelClass}>Merchant Type</label>
          <select
            value={merchantType}
            onChange={(event) => setMerchantType(event.target.value)}
            className={selectClass}
          >
            {merchantTypes.map((item) => (
              <option key={item.value} value={item.value}>
                {item.label}
              </option>
            ))}
          </select>
        </div>

        <div>
          <label className={labelClass}>Location</label>
          <select
            value={location}
            onChange={(event) => setLocation(event.target.value)}
            className={selectClass}
          >
            {locations.map((item) => (
              <option key={item.value} value={item.value}>
                {item.label}
              </option>
            ))}
          </select>
        </div>

        <div>
          <label className={labelClass}>Payment Method</label>
          <select
            value={paymentMethod}
            onChange={(event) => setPaymentMethod(event.target.value)}
            className={selectClass}
          >
            {paymentMethods.map((item) => (
              <option key={item.value} value={item.value}>
                {item.label}
              </option>
            ))}
          </select>
        </div>

        <div>
          <label className={labelClass}>Device Type</label>
          <select
            value={deviceType}
            onChange={(event) => setDeviceType(event.target.value)}
            className={selectClass}
          >
            {deviceTypes.map((item) => (
              <option key={item.value} value={item.value}>
                {item.label}
              </option>
            ))}
          </select>
        </div>

        <div>
          <label className={labelClass}>Failed Payment Attempts</label>
          <input
            type="number"
            min="0"
            value={failedPaymentAttempts}
            onChange={(event) => setFailedPaymentAttempts(event.target.value)}
            className={inputClass}
            placeholder="0"
          />
        </div>

        <div
          className={
            dark
              ? "flex h-17.5 items-center justify-between rounded-xl border border-white/10 bg-black/40 px-4"
              : "flex h-17.5 items-center justify-between rounded-xl border border-black/10 bg-white px-4"
          }
        >
          <div>
            <p className="text-sm font-semibold">International Payment</p>

            <p className={dark ? "text-xs text-white/50" : "text-xs text-black/50"}>
              Payment is outside the customer’s home country
            </p>
          </div>

          <input
            type="checkbox"
            checked={isInternational}
            onChange={(event) => setIsInternational(event.target.checked)}
            className={checkboxClass}
          />
        </div>
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
          {loading ? "Checking..." : "Check Transaction"}
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
                {result.risk_level}
              </p>

              <h2 className="mt-1 text-2xl font-bold">
                {result.is_fraud ? "Fraud Detected" : "Legitimate Transaction"}
              </h2>
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
              <p className="font-semibold">Decision</p>
              <p>{result.is_fraud ? "Fraud" : "Legitimate"}</p>
            </div>

            <div>
              <p className="font-semibold">Risk Threshold</p>
              <p>{(result.threshold * 100).toFixed(0)}%</p>
            </div>

            <div>
              <p className="font-semibold">Model</p>
              <p>{result.model_type}</p>
            </div>

            <div>
              <p className="font-semibold">Version</p>
              <p>{result.model_version}</p>
            </div>
          </div>
        </div>
      )}
    </form>
  );
}