"use client";

import { useState } from "react";
import FraudForm from "@/components/FraudForm";

export default function Home() {
  const [dark, setDark] = useState(true);

  return (
    <main
      className={
        dark
          ? "min-h-screen w-full bg-black text-white flex items-center justify-center px-3 py-4 transition-colors duration-300"
          : "min-h-screen w-full bg-white text-black flex items-center justify-center px-3 py-4 transition-colors duration-300"
      }
    >
      <button
        type="button"
        onClick={() => setDark((value) => !value)}
        aria-label="Toggle theme"
        className={
          dark
            ? "fixed right-4 top-4 z-50 h-11 w-11 rounded-full border border-white/20 bg-white/10 text-white shadow-lg backdrop-blur-xl transition-all hover:scale-110"
            : "fixed right-4 top-4 z-50 h-11 w-11 rounded-full border border-black/20 bg-black/5 text-black shadow-lg backdrop-blur-xl transition-all hover:scale-110"
        }
      >
        {dark ? "☀" : "☾"}
      </button>

      <section
        className={
          dark
            ? "w-full max-w-4xl rounded-3xl border border-white/15 bg-white/10 p-4 shadow-2xl backdrop-blur-2xl sm:p-6"
            : "w-full max-w-4xl rounded-3xl border border-black/10 bg-white/80 p-4 shadow-2xl backdrop-blur-2xl sm:p-6"
        }
      >
        <div className="mb-5 text-center">
          <h1 className="text-2xl font-bold tracking-tight sm:text-3xl">
            Fraud Detection AI
          </h1>

          <p
            className={
              dark
                ? "mt-2 text-sm font-medium text-white/70"
                : "mt-2 text-sm font-medium text-black/60"
            }
          >
            Real-time transaction fraud analysis
          </p>
        </div>

        <FraudForm dark={dark} />
      </section>
    </main>
  );
}