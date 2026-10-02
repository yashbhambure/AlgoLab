import { Loader2 } from "lucide-react";

interface LoadingStateProps {
  message?: string;
  subtitle?: string;
  size?: "sm" | "md" | "lg";
}

export function LoadingState({
  message = "Loading benchmark data...",
  subtitle,
  size = "md",
}: LoadingStateProps) {
  const iconSizes = {
    sm: "w-5 h-5",
    md: "w-7 h-7",
    lg: "w-10 h-10",
  };

  return (
    <div className="flex flex-col items-center justify-center p-8 sm:p-12 text-center space-y-3">
      <div className="p-3 rounded-xl bg-slate-900/80 border border-slate-800 text-sky-400">
        <Loader2 className={`${iconSizes[size]} animate-spin`} />
      </div>

      <div className="space-y-1">
        <p className="text-xs sm:text-sm font-medium text-slate-200 font-sans">
          {message}
        </p>
        {subtitle && (
          <p className="text-[12px] text-slate-500 font-sans max-w-sm">
            {subtitle}
          </p>
        )}
      </div>
    </div>
  );
}

export default LoadingState;
