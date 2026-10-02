import { Inbox } from "lucide-react";
import type { ReactNode } from "react";

interface EmptyStateProps {
  icon?: ReactNode;
  title: string;
  message: string;
  action?: ReactNode;
  className?: string;
}

export function EmptyState({
  icon,
  title,
  message,
  action,
  className = "",
}: EmptyStateProps) {
  return (
    <div
      className={`rounded-xl bg-[#0e131f] border border-slate-800 p-8 sm:p-12 text-center max-w-md mx-auto space-y-4 ${className}`}
    >
      <div className="w-12 h-12 rounded-xl bg-slate-900 border border-slate-800 text-slate-400 mx-auto flex items-center justify-center">
        {icon || <Inbox className="w-6 h-6" />}
      </div>

      <div className="space-y-1">
        <h3 className="text-base font-semibold text-white font-sans">
          {title}
        </h3>
        <p className="text-xs sm:text-sm text-slate-400 font-sans leading-relaxed">
          {message}
        </p>
      </div>

      {action && <div className="pt-2">{action}</div>}
    </div>
  );
}

export default EmptyState;
