import type { ReactNode } from "react";

interface PageHeaderProps {
  breadcrumb?: string;
  title: string;
  description?: string;
  icon?: ReactNode;
  actions?: ReactNode;
}

export function PageHeader({
  breadcrumb,
  title,
  description,
  icon,
  actions,
}: PageHeaderProps) {
  return (
    <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 border-b border-slate-800 pb-5 mb-6">
      <div className="space-y-1">
        {breadcrumb && (
          <div className="text-[11px] font-mono font-medium text-slate-400 uppercase tracking-wider">
            {breadcrumb}
          </div>
        )}
        <div className="flex items-center gap-3">
          {icon && (
            <div className="p-2 rounded-lg bg-slate-900 border border-slate-800 text-sky-400 flex-shrink-0">
              {icon}
            </div>
          )}
          <h1 className="text-2xl sm:text-3xl font-semibold tracking-tight text-white font-sans">
            {title}
          </h1>
        </div>
        {description && (
          <p className="text-xs sm:text-sm text-slate-400 max-w-3xl leading-relaxed">
            {description}
          </p>
        )}
      </div>

      {actions && (
        <div className="flex items-center gap-2.5 flex-wrap flex-shrink-0">
          {actions}
        </div>
      )}
    </div>
  );
}
