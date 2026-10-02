import { AlertTriangle, RotateCcw } from "lucide-react";
import { Button } from "./Button";

interface ErrorStateProps {
  title?: string;
  message: string;
  onRetry?: () => void;
  className?: string;
}

export function ErrorState({
  title = "Analysis Error Encountered",
  message,
  onRetry,
  className = "",
}: ErrorStateProps) {
  return (
    <div
      className={`rounded-xl bg-[#0e131f] border border-rose-800/40 p-6 sm:p-8 text-center max-w-md mx-auto space-y-4 ${className}`}
    >
      <div className="w-10 h-10 rounded-full bg-rose-950/60 border border-rose-800/50 text-rose-400 mx-auto flex items-center justify-center">
        <AlertTriangle className="w-5 h-5" />
      </div>

      <div className="space-y-1.5">
        <h3 className="text-sm sm:text-base font-semibold text-slate-100 font-sans">
          {title}
        </h3>
        <p className="text-xs text-slate-400 font-mono bg-slate-900/80 p-3 rounded-lg border border-slate-800 break-words text-left">
          {message}
        </p>
      </div>

      {onRetry && (
        <Button
          variant="secondary"
          size="sm"
          onClick={onRetry}
          icon={<RotateCcw className="w-3.5 h-3.5" />}
        >
          Retry Operation
        </Button>
      )}
    </div>
  );
}

export default ErrorState;
