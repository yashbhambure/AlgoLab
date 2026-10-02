import type { ReactNode } from "react";
import { CheckCircle2, XCircle, Sliders } from "lucide-react";
import { Card } from "../common/Card";

export interface AlgorithmTradeoffsProps {
  advantages?: string[];
  suitableCases?: string[];
  disadvantages?: string[];
  unsuitableCases?: string[];
  className?: string;
}

interface SectionHeaderProps {
  icon: ReactNode;
  title: string;
  colorClass: string;
  badgeBg: string;
}

function SectionHeader({ icon, title, colorClass, badgeBg }: SectionHeaderProps) {
  return (
    <div className="flex items-center gap-2.5 pb-0.5">
      <span className={`p-1 rounded-md ${badgeBg} ${colorClass} flex-shrink-0 flex items-center justify-center`}>
        {icon}
      </span>
      <h4 className={`text-xs sm:text-[13px] font-mono font-bold uppercase tracking-wider ${colorClass}`}>
        {title}
      </h4>
    </div>
  );
}

interface TradeoffListProps {
  items?: string[];
  emptyMessage?: string;
  bulletColor: string;
}

function TradeoffList({ items, emptyMessage = "Not documented in dataset.", bulletColor }: TradeoffListProps) {
  if (!items || items.length === 0) {
    return (
      <div className="text-xs text-slate-500 font-mono italic py-1.5 pl-4">
        {emptyMessage}
      </div>
    );
  }

  return (
    <ul className="space-y-3 text-xs sm:text-[13px] text-slate-300">
      {items.map((item, i) => (
        <li key={i} className="flex items-start gap-3 group">
          <span
            className={`flex-shrink-0 mt-2 w-1.5 h-1.5 rounded-full ${bulletColor}`}
            aria-hidden="true"
          />
          <span className="flex-1 min-w-0 leading-relaxed font-sans text-slate-300 break-words tracking-normal">
            {item}
          </span>
        </li>
      ))}
    </ul>
  );
}

/**
 * Reusable, responsive 2-column tradeoffs component for:
 * - Key Advantages
 * - Suitable Scenarios
 * - Limitations & Disadvantages
 * - Unsuitable Scenarios
 *
 * Implements robust flex bullet alignment, comfortable line-height,
 * word-wrapping safety, and balanced divider spacing.
 */
export function AlgorithmTradeoffs({
  advantages = [],
  suitableCases = [],
  disadvantages = [],
  unsuitableCases = [],
  className = "",
}: AlgorithmTradeoffsProps) {
  return (
    <div className={`grid grid-cols-1 md:grid-cols-2 gap-6 ${className}`}>
      {/* Column 1: Key Advantages & Suitable Scenarios */}
      <Card>
        <div className="space-y-4">
          <SectionHeader
            icon={<CheckCircle2 className="w-3.5 h-3.5" />}
            title="Key Advantages"
            colorClass="text-emerald-400"
            badgeBg="bg-emerald-500/10 border border-emerald-500/20"
          />
          <TradeoffList
            items={advantages}
            bulletColor="bg-emerald-400 ring-2 ring-emerald-500/20"
          />
        </div>

        {/* Balanced section divider with generous breathing room */}
        <div className="my-6 border-t border-slate-800/80" />

        <div className="space-y-4">
          <SectionHeader
            icon={<Sliders className="w-3.5 h-3.5" />}
            title="Suitable Scenarios"
            colorClass="text-sky-400"
            badgeBg="bg-sky-500/10 border border-sky-500/20"
          />
          <TradeoffList
            items={suitableCases}
            bulletColor="bg-sky-400 ring-2 ring-sky-500/20"
          />
        </div>
      </Card>

      {/* Column 2: Limitations & Disadvantages & Unsuitable Scenarios */}
      <Card>
        <div className="space-y-4">
          <SectionHeader
            icon={<XCircle className="w-3.5 h-3.5" />}
            title="Limitations & Disadvantages"
            colorClass="text-amber-400"
            badgeBg="bg-amber-500/10 border border-amber-500/20"
          />
          <TradeoffList
            items={disadvantages}
            bulletColor="bg-amber-400 ring-2 ring-amber-500/20"
          />
        </div>

        {/* Balanced section divider with generous breathing room */}
        <div className="my-6 border-t border-slate-800/80" />

        <div className="space-y-4">
          <SectionHeader
            icon={<XCircle className="w-3.5 h-3.5" />}
            title="Unsuitable Scenarios"
            colorClass="text-purple-400"
            badgeBg="bg-purple-500/10 border border-purple-500/20"
          />
          <TradeoffList
            items={unsuitableCases}
            bulletColor="bg-purple-400 ring-2 ring-purple-500/20"
          />
        </div>
      </Card>
    </div>
  );
}

export default AlgorithmTradeoffs;
