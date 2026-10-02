import type { ReactNode } from "react";

interface MetricCardProps {
  title: string;
  value: string | number;
  subtitle?: string;
  icon?: ReactNode;
  color?: "blue" | "green" | "purple" | "orange" | "red" | "teal" | "slate";
  trend?: {
    value: string;
    isPositive?: boolean;
  };
}

export function MetricCard({
  title,
  value,
  subtitle,
  icon,
  color = "blue",
  trend,
}: MetricCardProps) {
  const colorMap = {
    blue: {
      border: "border-slate-800 hover:border-sky-800/60",
      iconBg: "bg-sky-950/50 text-sky-400 border-sky-800/40",
      textAccent: "text-sky-400",
    },
    green: {
      border: "border-slate-800 hover:border-emerald-800/60",
      iconBg: "bg-emerald-950/50 text-emerald-400 border-emerald-800/40",
      textAccent: "text-emerald-400",
    },
    purple: {
      border: "border-slate-800 hover:border-purple-800/60",
      iconBg: "bg-purple-950/50 text-purple-400 border-purple-800/40",
      textAccent: "text-purple-400",
    },
    orange: {
      border: "border-slate-800 hover:border-amber-800/60",
      iconBg: "bg-amber-950/50 text-amber-400 border-amber-800/40",
      textAccent: "text-amber-400",
    },
    red: {
      border: "border-slate-800 hover:border-rose-800/60",
      iconBg: "bg-rose-950/50 text-rose-400 border-rose-800/40",
      textAccent: "text-rose-400",
    },
    teal: {
      border: "border-slate-800 hover:border-teal-800/60",
      iconBg: "bg-teal-950/50 text-teal-400 border-teal-800/40",
      textAccent: "text-teal-400",
    },
    slate: {
      border: "border-slate-800 hover:border-slate-700",
      iconBg: "bg-slate-900 text-slate-300 border-slate-700",
      textAccent: "text-slate-300",
    },
  };

  const scheme = colorMap[color] || colorMap.blue;

  return (
    <div
      className={`rounded-xl bg-[#0e131f] border ${scheme.border} p-4 sm:p-5 transition-all duration-150 group`}
    >
      <div className="flex items-start justify-between gap-3">
        <div className="space-y-1">
          <p className="text-[11px] font-mono font-medium uppercase tracking-wider text-slate-400">
            {title}
          </p>
          <div className="text-2xl sm:text-3xl font-semibold text-white tracking-tight font-mono tabular-nums">
            {value}
          </div>
          {subtitle && (
            <p className="text-[12px] text-slate-400 font-sans">{subtitle}</p>
          )}
          {trend && (
            <div className="flex items-center gap-1 text-[11px] font-mono pt-0.5">
              <span className={trend.isPositive ? "text-emerald-400" : "text-rose-400"}>
                {trend.value}
              </span>
            </div>
          )}
        </div>

        {icon && (
          <div className={`p-2.5 rounded-lg border ${scheme.iconBg} flex-shrink-0`}>
            {icon}
          </div>
        )}
      </div>
    </div>
  );
}

export default MetricCard;
