interface SystemStatusProps {
  status?: "online" | "active" | "synced" | "processing" | "offline";
  label?: string;
  showPulse?: boolean;
  className?: string;
}

export function SystemStatus({
  status = "online",
  label,
  showPulse = false,
  className = "",
}: SystemStatusProps) {
  const statusConfig = {
    online: {
      color: "bg-emerald-400",
      textColor: "text-emerald-400",
      label: label || "System Ready",
    },
    active: {
      color: "bg-sky-400",
      textColor: "text-sky-400",
      label: label || "Active",
    },
    synced: {
      color: "bg-blue-400",
      textColor: "text-blue-400",
      label: label || "Synchronized",
    },
    processing: {
      color: "bg-amber-400",
      textColor: "text-amber-400",
      label: label || "Processing",
    },
    offline: {
      color: "bg-slate-500",
      textColor: "text-slate-500",
      label: label || "Offline",
    },
  };

  const config = statusConfig[status] || statusConfig.online;

  return (
    <div className={`inline-flex items-center gap-2 ${className}`}>
      <span className="relative flex h-2 w-2">
        {showPulse && status !== "offline" && (
          <span
            className={`animate-ping absolute inline-flex h-full w-full rounded-full ${config.color} opacity-75`}
          />
        )}
        <span className={`relative inline-flex rounded-full h-2 w-2 ${config.color}`} />
      </span>
      <span className={`text-[12px] font-mono font-medium ${config.textColor}`}>
        {config.label}
      </span>
    </div>
  );
}

export default SystemStatus;
