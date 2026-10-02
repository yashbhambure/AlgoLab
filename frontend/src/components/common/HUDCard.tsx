import type { ReactNode } from "react";

export interface CardProps {
  children: ReactNode;
  className?: string;
  glow?: boolean;
  glowColor?: "cyan" | "blue" | "violet" | "teal" | "emerald" | "amber" | "rose" | "slate";
  corners?: boolean;
  scanline?: boolean;
  headerTag?: string;
  headerRight?: ReactNode;
  title?: string;
  subtitle?: string;
  interactive?: boolean;
}

export function Card({
  children,
  className = "",
  glow = false,
  glowColor = "cyan",
  headerTag,
  headerRight,
  title,
  subtitle,
  interactive = false,
}: CardProps) {
  const accentBorderMap: Record<string, string> = {
    cyan: "border-sky-800/40 hover:border-sky-700/60",
    blue: "border-blue-800/40 hover:border-blue-700/60",
    violet: "border-purple-800/40 hover:border-purple-700/60",
    teal: "border-teal-800/40 hover:border-teal-700/60",
    emerald: "border-emerald-800/40 hover:border-emerald-700/60",
    amber: "border-amber-800/40 hover:border-amber-700/60",
    rose: "border-rose-800/40 hover:border-rose-700/60",
    slate: "border-slate-800 hover:border-slate-700",
  };

  const borderClass = glow && glowColor ? accentBorderMap[glowColor] || "border-slate-800" : "border-slate-800/90";

  return (
    <div
      className={`relative overflow-hidden rounded-xl bg-[#0e131f] border ${borderClass} transition-all duration-150 ${
        interactive ? "hover:bg-[#141b2d] hover:border-slate-700 cursor-pointer" : ""
      } ${className}`}
    >
      {/* Optional Top Section Tag / Header */}
      {(headerTag || headerRight) && (
        <div className="flex items-center justify-between px-5 py-2.5 border-b border-slate-800/70 bg-slate-900/40 text-[11px] font-mono tracking-wider text-slate-400">
          <div className="flex items-center gap-2">
            <span className="w-1.5 h-1.5 rounded-full bg-sky-400" />
            <span className="font-semibold text-slate-300 uppercase">{headerTag}</span>
          </div>
          {headerRight && <div className="text-slate-400">{headerRight}</div>}
        </div>
      )}

      {/* Optional Card Title & Subtitle */}
      {(title || subtitle) && (
        <div className="px-5 pt-5 pb-1">
          {title && <h3 className="text-base font-semibold text-white tracking-tight">{title}</h3>}
          {subtitle && <p className="text-xs text-slate-400 mt-0.5">{subtitle}</p>}
        </div>
      )}

      {/* Card Body */}
      <div className="p-5 sm:p-6">{children}</div>
    </div>
  );
}

// Backward-compatible export
export const HUDCard = Card;
export default Card;
