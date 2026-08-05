import Link from "next/link";

export default function WelcomePage() {
  return (
    <main className="relative min-h-screen overflow-hidden bg-slate-950 text-white">
      <div className="absolute inset-0 bg-[radial-gradient(circle_at_top_left,rgba(34,211,238,0.18),transparent_35%),radial-gradient(circle_at_bottom_right,rgba(59,130,246,0.16),transparent_35%)]" />

      <section className="relative mx-auto flex min-h-screen max-w-7xl flex-col px-4 py-8 sm:px-6 lg:px-8">
        <nav className="flex items-center justify-between rounded-3xl border border-slate-800 bg-slate-900/75 px-5 py-4 shadow-xl shadow-cyan-950/20 backdrop-blur">
          <Link href="/" className="text-lg font-bold tracking-tight">
            Fraud<span className="text-cyan-300">MLOps</span>
          </Link>

          <div className="flex items-center gap-3">
            <Link
              href="/login"
              className="rounded-xl border border-slate-700 bg-slate-950/40 px-4 py-2 text-sm font-semibold text-slate-200 transition hover:bg-slate-800"
            >
              Login
            </Link>

            <Link
              href="/register"
              className="rounded-xl bg-gradient-to-r from-cyan-400 to-blue-500 px-4 py-2 text-sm font-semibold text-slate-950 shadow-lg shadow-cyan-500/20 transition hover:from-cyan-300 hover:to-blue-400"
            >
              Register
            </Link>
          </div>
        </nav>

        <div className="grid flex-1 items-center gap-10 py-16 lg:grid-cols-[1.08fr_0.92fr]">
          <div>
            <p className="mb-5 inline-flex rounded-full border border-cyan-400/30 bg-cyan-400/10 px-4 py-2 text-sm font-semibold text-cyan-300">
              Real-Time Fraud Detection MLOps Platform
            </p>

            <h1 className="max-w-4xl text-5xl font-extrabold leading-tight tracking-tight sm:text-6xl">
              Detect suspicious transactions with an{" "}
              <span className="bg-gradient-to-r from-cyan-300 to-blue-400 bg-clip-text text-transparent">
                ML-powered dashboard
              </span>
            </h1>

            <p className="mt-6 max-w-2xl text-base leading-8 text-slate-400 sm:text-lg">
              A production-oriented fraud detection platform with a Next.js
              frontend, NestJS authentication backend, PostgreSQL database,
              FastAPI ML service, MLflow model tracking, Docker, and monitoring.
            </p>

            <div className="mt-9 flex flex-col gap-3 sm:flex-row">
              <Link
                href="/register"
                className="rounded-2xl bg-gradient-to-r from-cyan-400 to-blue-500 px-6 py-3 text-center font-bold text-slate-950 shadow-xl shadow-cyan-500/20 transition hover:from-cyan-300 hover:to-blue-400"
              >
                Create Account
              </Link>

              <Link
                href="/login"
                className="rounded-2xl border border-slate-700 bg-slate-900/75 px-6 py-3 text-center font-bold text-slate-200 shadow-xl shadow-cyan-950/20 transition hover:bg-slate-800"
              >
                Login to Dashboard
              </Link>
            </div>

            <div className="mt-10 grid max-w-2xl grid-cols-2 gap-3 sm:grid-cols-4">
              {[
                ["Next.js", "Frontend"],
                ["NestJS", "Backend"],
                ["PostgreSQL", "Database"],
                ["FastAPI", "ML API"],
              ].map(([title, subtitle]) => (
                <div
                  key={title}
                  className="rounded-2xl border border-slate-800 bg-slate-900/70 p-4 shadow-lg shadow-cyan-950/10 backdrop-blur"
                >
                  <p className="text-lg font-bold text-cyan-300">{title}</p>
                  <p className="mt-1 text-xs font-medium text-slate-400">
                    {subtitle}
                  </p>
                </div>
              ))}
            </div>
          </div>

          <div className="rounded-[2rem] border border-slate-800 bg-slate-900/80 p-6 shadow-2xl shadow-cyan-950/30 backdrop-blur">
            <div className="rounded-3xl border border-slate-800 bg-slate-950/70 p-5">
              <div className="flex items-center justify-between border-b border-slate-800 pb-4">
                <div>
                  <p className="text-sm font-semibold text-cyan-300">
                    Live Risk Preview
                  </p>
                  <h2 className="mt-1 text-2xl font-bold">
                    Transaction Check
                  </h2>
                </div>

                <span className="rounded-full bg-emerald-500/15 px-3 py-1 text-xs font-bold text-emerald-300">
                  Active
                </span>
              </div>

              <div className="mt-5 space-y-4">
                <div className="rounded-2xl border border-slate-800 bg-slate-900 p-4">
                  <div className="flex items-center justify-between">
                    <p className="text-sm font-semibold text-slate-400">
                      Amount
                    </p>
                    <p className="text-lg font-bold">$1,249.62</p>
                  </div>
                </div>

                <div className="grid grid-cols-2 gap-3">
                  <div className="rounded-2xl border border-slate-800 bg-slate-900 p-4">
                    <p className="text-xs font-semibold text-slate-400">
                      Location
                    </p>
                    <p className="mt-1 font-bold">Sri Lanka</p>
                  </div>

                  <div className="rounded-2xl border border-slate-800 bg-slate-900 p-4">
                    <p className="text-xs font-semibold text-slate-400">
                      Device
                    </p>
                    <p className="mt-1 font-bold">Mobile</p>
                  </div>
                </div>

                <div className="rounded-2xl border border-red-400/30 bg-red-500/10 p-5">
                  <p className="text-sm font-semibold text-red-300">
                    Medium Risk
                  </p>

                  <div className="mt-2 flex items-end justify-between">
                    <div>
                      <h3 className="text-2xl font-bold">Fraud Detected</h3>
                      <p className="mt-1 text-sm text-slate-400">
                        RandomForestClassifier · business-v1
                      </p>
                    </div>

                    <div className="rounded-2xl bg-red-500/15 px-4 py-3 text-center">
                      <p className="text-xs font-semibold text-red-300">
                        Probability
                      </p>
                      <p className="text-2xl font-bold">53.15%</p>
                    </div>
                  </div>
                </div>

                <Link
                  href="/login"
                  className="block rounded-2xl bg-gradient-to-r from-cyan-400 to-blue-500 px-5 py-3 text-center font-bold text-slate-950 shadow-lg shdow-cyan-500/20 transition hover:from-cyan-300 hover:to-blue-400"
                >
                  Try the Fraud Checker
                </Link>
              </div>
            </div>
          </div>
        </div>
      </section>
    </main>
  );
}
