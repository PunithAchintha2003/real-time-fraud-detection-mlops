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

type TransactionHistoryProps = {
  transactions: Transaction[];
  loading: boolean;
};

function formatCurrency(amount: number) {
  return new Intl.NumberFormat("en-US", {
    style: "currency",
    currency: "USD",
  }).format(amount);
}

function formatDate(value: string) {
  return new Intl.DateTimeFormat("en-US", {
    dateStyle: "medium",
    timeStyle: "short",
  }).format(new Date(value));
}

function formatLabel(value: string) {
  return value
    .split("_")
    .map((word) => word.charAt(0).toUpperCase() + word.slice(1))
    .join(" ");
}

export default function TransactionHistory({
  transactions,
  loading,
}: TransactionHistoryProps) {
  return (
    <div className="mt-8 rounded-3xl border border-slate-800 bg-slate-950/50 p-5">
      <div className="flex flex-col gap-2 border-b border-slate-800 pb-4 sm:flex-row sm:items-center sm:justify-between">
        <div>
          <p className="text-sm font-semibold uppercase tracking-[0.25em] text-cyan-300">
            History
          </p>

          <h2 className="mt-2 text-2xl font-bold">Recent Transactions</h2>
        </div>

        <p className="text-sm text-slate-400">
          {transactions.length} saved transaction
          {transactions.length === 1 ? "" : "s"}
        </p>
      </div>

      {loading ? (
        <div className="py-10 text-center text-sm font-medium text-slate-400">
          Loading transaction history...
        </div>
      ) : transactions.length === 0 ? (
        <div className="py-10 text-center">
          <p className="text-sm font-semibold text-slate-300">
            No transactions checked yet.
          </p>
          <p className="mt-1 text-sm text-slate-500">
            Submit the fraud detection form to create your first transaction.
          </p>
        </div>
      ) : (
        <div className="mt-5 overflow-hidden rounded-2xl border border-slate-800">
          <div className="hidden grid-cols-[1.2fr_1fr_1fr_1fr_1fr] gap-4 bg-slate-900 px-4 py-3 text-xs font-bold uppercase tracking-wide text-slate-400 md:grid">
            <p>Transaction</p>
            <p>Merchant</p>
            <p>Payment</p>
            <p>Risk</p>
            <p>Created</p>
          </div>

          <div className="divide-y divide-slate-800">
            {transactions.map((transaction) => {
              const prediction = transaction.prediction;
              const isFraud = prediction?.isFraud ?? false;

              return (
                <div
                  key={transaction.id}
                  className="grid gap-4 bg-slate-950/40 px-4 py-4 text-sm transition hover:bg-slate-900/70 md:grid-cols-[1.2fr_1fr_1fr_1fr_1fr] md:items-center"
                >
                  <div>
                    <p className="font-bold text-white">
                      {formatCurrency(transaction.amount)}
                    </p>
                    <p className="mt-1 text-xs text-slate-500">
                      {transaction.location} · {transaction.transactionTime}
                    </p>
                  </div>

                  <div>
                    <p className="font-semibold text-slate-200">
                      {formatLabel(transaction.merchantType)}
                    </p>
                    <p className="mt-1 text-xs text-slate-500">
                      {formatLabel(transaction.deviceType)}
                    </p>
                  </div>
                  <div>
                    <p className="font-semibold text-slate-200">
                      {formatLabel(transaction.paymentMethod)}
                    </p>
                    <p className="mt-1 text-xs text-slate-500">
                      Failed attempts: {transaction.previousFailedAttempts}
                    </p>
                  </div>

                  <div>
                    <span
                      className={
                        isFraud
                          ? "inline-flex rounded-full border border-red-400/30 bg-red-500/10 px-3 py-1 text-xs font-bold text-red-300"
                          : "inline-flex rounded-full border border-emerald-400/30 bg-emerald-500/10 px-3 py-1 text-xs font-bold text-emerald-300"
                      }
                    >
                      {prediction?.riskLevel ?? "Unknown"}
                    </span>

                    <p className="mt-2 text-xs text-slate-500">
                      Probability:{" "}
                      {prediction
                        ? `${(prediction.fraudProbability * 100).toFixed(2)}%`
                        : "-"}
                    </p>
                  </div>

                  <div>
                    <p className="font-medium text-slate-300">
                      {formatDate(transaction.createdAt)}
                    </p>
                    <p className="mt-1 text-xs text-slate-500">
                      {prediction?.modelVersion ?? "No model"}
                    </p>
                  </div>
                </div>
              );
            })}
          </div>
        </div>
      )}
    </div>
  );
}
