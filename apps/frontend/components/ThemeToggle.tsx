"use client";

import { Moon, Sun } from "lucide-react";


export default function ThemeToggle() {
  function toggleTheme() {
    const root = document.documentElement;

    const isDark = root.classList.toggle("dark");

    localStorage.setItem(
      "theme",
      isDark ? "dark" : "light"
    );
  }


  return (
    <button
      type="button"
      onClick={toggleTheme}
      aria-label="Toggle theme"
      className="
        flex
        h-11
        w-11
        items-center
        justify-center
        rounded-full

        border
        border-neutral-300
        dark:border-neutral-700

        bg-white/80
        dark:bg-neutral-900/80

        text-neutral-900
        dark:text-neutral-100

        shadow-lg
        backdrop-blur-xl

        transition-all
        duration-300

        hover:scale-110
        active:scale-95
      "
    >
      <Moon
        size={20}
        className="
          block
          dark:hidden
        "
      />

      <Sun
        size={20}
        className="
          hidden
          text-yellow-400
          dark:block
        "
      />
    </button>
  );
}