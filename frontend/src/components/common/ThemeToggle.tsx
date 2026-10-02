import { Sun, Moon } from "lucide-react";
import { useTheme } from "../../hooks/useTheme";

interface ThemeToggleProps {
  className?: string;
  variant?: "pill" | "compact";
  showLabel?: boolean;
}

export function ThemeToggle({
  className = "",
  variant = "pill",
  showLabel = false,
}: ThemeToggleProps) {
  const { theme, toggleTheme } = useTheme();
  const isDark = theme === "dark";

  if (variant === "compact") {
    return (
      <button
        type="button"
        role="switch"
        aria-checked={!isDark}
        aria-label={`Switch to ${isDark ? "light" : "dark"} theme`}
        title={`Current: ${isDark ? "Dark" : "Light"} mode. Click to switch.`}
        onClick={toggleTheme}
        className={`relative p-2 rounded-lg transition-all duration-200 focus:outline-none focus-visible:ring-2 focus-visible:ring-sky-500 cursor-pointer ${
          isDark
            ? "bg-slate-900/80 border border-slate-700/80 text-amber-400 hover:bg-slate-800 hover:border-amber-500/50 hover:text-amber-300"
            : "bg-slate-100 border border-slate-300 text-sky-600 hover:bg-slate-200 hover:border-sky-500/50 hover:text-sky-700"
        } ${className}`}
      >
        <div className="relative w-4 h-4 flex items-center justify-center">
          <Sun
            className={`w-4 h-4 transition-transform duration-300 ${
              isDark ? "rotate-0 scale-100 opacity-100" : "-rotate-90 scale-0 opacity-0"
            }`}
          />
          <Moon
            className={`w-4 h-4 absolute transition-transform duration-300 ${
              isDark ? "rotate-90 scale-0 opacity-0" : "rotate-0 scale-100 opacity-100"
            }`}
          />
        </div>
      </button>
    );
  }

  return (
    <button
      type="button"
      role="switch"
      aria-checked={!isDark}
      aria-label={`Switch to ${isDark ? "light" : "dark"} theme`}
      title={`Current: ${isDark ? "Dark" : "Light"} mode. Click to switch to ${isDark ? "Light" : "Dark"} mode.`}
      onClick={toggleTheme}
      className={`group relative flex items-center gap-2 px-2.5 py-1 rounded-lg text-xs font-mono font-medium transition-all duration-200 focus:outline-none focus-visible:ring-2 focus-visible:ring-sky-500 cursor-pointer border ${
        isDark
          ? "bg-slate-900/80 hover:bg-slate-800/90 border-slate-700/80 hover:border-slate-600 text-slate-300"
          : "bg-slate-100 hover:bg-slate-200/90 border-slate-300 hover:border-slate-400 text-slate-700 shadow-xs"
      } ${className}`}
    >
      {/* Visual Pill Indicator */}
      <div
        className={`relative w-8 h-4.5 rounded-full transition-colors duration-200 flex items-center px-0.5 ${
          isDark ? "bg-slate-800 border border-slate-700" : "bg-sky-100 border border-sky-300"
        }`}
      >
        <div
          className={`w-3.5 h-3.5 rounded-full flex items-center justify-center transition-all duration-200 transform ${
            isDark
              ? "translate-x-0 bg-slate-900 text-amber-400 shadow-xs"
              : "translate-x-3.5 bg-white text-sky-600 shadow-sm"
          }`}
        >
          {isDark ? (
            <Moon className="w-2.5 h-2.5 transition-transform duration-200 group-hover:-rotate-12" />
          ) : (
            <Sun className="w-2.5 h-2.5 transition-transform duration-200 group-hover:rotate-45" />
          )}
        </div>
      </div>

      {/* Text Label */}
      <span className="select-none tracking-tight font-sans text-[11px] font-medium">
        {showLabel ? (isDark ? "Dark Mode" : "Light Mode") : isDark ? "Dark" : "Light"}
      </span>
    </button>
  );
}

export default ThemeToggle;
