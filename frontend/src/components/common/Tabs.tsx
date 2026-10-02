import React from "react";

export interface TabItem {
  key: string;
  label: string;
  icon?: React.ReactNode;
  badge?: string | number;
}

export interface TabsProps {
  tabs: TabItem[];
  activeKey: string;
  onChange: (key: string) => void;
  variant?: "pills" | "underline";
  className?: string;
}

export function Tabs({
  tabs,
  activeKey,
  onChange,
  variant = "pills",
  className = "",
}: TabsProps) {
  if (variant === "underline") {
    return (
      <div className={`flex items-center border-b border-slate-800 gap-6 ${className}`}>
        {tabs.map((tab) => {
          const isActive = tab.key === activeKey;
          return (
            <button
              key={tab.key}
              onClick={() => onChange(tab.key)}
              className={`pb-3 text-xs sm:text-sm font-medium transition-colors relative flex items-center gap-2 cursor-pointer focus:outline-none focus-visible:text-sky-400 ${
                isActive
                  ? "text-sky-400 font-semibold"
                  : "text-slate-400 hover:text-slate-200"
              }`}
            >
              {tab.icon && <span className="flex-shrink-0">{tab.icon}</span>}
              <span>{tab.label}</span>
              {tab.badge !== undefined && (
                <span
                  className={`px-1.5 py-0.5 text-[10px] font-mono rounded ${
                    isActive
                      ? "bg-sky-950 text-sky-300 border border-sky-800/60"
                      : "bg-slate-900 text-slate-400"
                  }`}
                >
                  {tab.badge}
                </span>
              )}
              {isActive && (
                <span className="absolute bottom-0 left-0 right-0 h-0.5 bg-sky-500 rounded-t" />
              )}
            </button>
          );
        })}
      </div>
    );
  }

  // Pills variant
  return (
    <div
      className={`inline-flex items-center p-1 rounded-lg bg-slate-900/90 border border-slate-800/90 gap-1 overflow-x-auto max-w-full ${className}`}
    >
      {tabs.map((tab) => {
        const isActive = tab.key === activeKey;
        return (
          <button
            key={tab.key}
            onClick={() => onChange(tab.key)}
            className={`px-3 py-1.5 rounded-md text-xs font-medium transition-all flex items-center gap-1.5 whitespace-nowrap cursor-pointer focus:outline-none focus-visible:ring-2 focus-visible:ring-sky-500 ${
              isActive
                ? "bg-sky-600 !text-white font-semibold shadow-sm"
                : "text-slate-400 hover:text-slate-200 hover:bg-slate-800/50"
            }`}
          >
            {tab.icon && <span className="flex-shrink-0">{tab.icon}</span>}
            <span>{tab.label}</span>
            {tab.badge !== undefined && (
              <span
                className={`px-1.5 py-0.2 text-[10px] font-mono rounded ${
                  isActive ? "bg-sky-700 !text-white" : "bg-slate-800 text-slate-400"
                }`}
              >
                {tab.badge}
              </span>
            )}
          </button>
        );
      })}
    </div>
  );
}

export default Tabs;
