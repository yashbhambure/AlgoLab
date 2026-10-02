import React from "react";

export interface BadgeProps extends React.HTMLAttributes<HTMLSpanElement> {
  variant?: "default" | "primary" | "success" | "warning" | "danger" | "purple" | "outline";
  size?: "sm" | "md";
  mono?: boolean;
}

export function Badge({
  children,
  variant = "default",
  size = "sm",
  mono = false,
  className = "",
  ...props
}: BadgeProps) {
  const baseStyles = "inline-flex items-center font-medium rounded border transition-colors";

  const sizeStyles = {
    sm: "px-2 py-0.5 text-[11px]",
    md: "px-2.5 py-1 text-xs",
  };

  const variantStyles = {
    default: "bg-slate-900 text-slate-300 border-slate-800",
    primary: "bg-sky-950/60 text-sky-400 border-sky-800/50",
    success: "bg-emerald-950/60 text-emerald-400 border-emerald-800/50",
    warning: "bg-amber-950/60 text-amber-400 border-amber-800/50",
    danger: "bg-rose-950/60 text-rose-400 border-rose-800/50",
    purple: "bg-purple-950/60 text-purple-400 border-purple-800/50",
    outline: "bg-transparent text-slate-400 border-slate-700",
  };

  const fontStyle = mono ? "font-mono" : "font-sans";

  return (
    <span
      className={`${baseStyles} ${sizeStyles[size]} ${variantStyles[variant]} ${fontStyle} ${className}`}
      {...props}
    >
      {children}
    </span>
  );
}

export default Badge;
