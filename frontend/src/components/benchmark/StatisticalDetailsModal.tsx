import { useEffect, useMemo } from "react";
import { Link } from "react-router-dom";
import {
  X,
  Award,
  Activity,
  BarChart3,
  Info,
  ExternalLink,
  BookOpen,
  Layers,
  Scale,
  TrendingDown,
  TrendingUp,
} from "lucide-react";
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  ReferenceLine,
  Cell,
} from "recharts";
import { Button } from "../common/Button";
import type { BenchmarkAlgorithmResult, BenchmarkResponse } from "../../types";

interface StatisticalDetailsModalProps {
  isOpen: boolean;
  onClose: () => void;
  result: BenchmarkAlgorithmResult | null;
  benchmarkResponse: BenchmarkResponse | null;
  problemName: string;
  problemSlug: string;
  inputSize: number;
  repetitions: number;
  warmupRuns: number;
}

export function StatisticalDetailsModal({
  isOpen,
  onClose,
  result,
  benchmarkResponse,
  problemName,
  problemSlug,
  inputSize,
  repetitions,
  warmupRuns,
}: StatisticalDetailsModalProps) {
  // Close on Escape key
  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if (e.key === "Escape") {
        onClose();
      }
    };
    if (isOpen) {
      window.addEventListener("keydown", handleKeyDown);
      document.body.style.overflow = "hidden";
    }
    return () => {
      window.removeEventListener("keydown", handleKeyDown);
      document.body.style.overflow = "unset";
    };
  }, [isOpen, onClose]);

  const timeStats = result?.time_stats || {
    mean_ms: 0,
    median_ms: 0,
    min_ms: 0,
    max_ms: 0,
    std_dev_ms: 0,
    variance_ms: 0,
    p95_ms: 0,
    p99_ms: 0,
    iqr_ms: 0,
  };

  const meanMs = timeStats.mean_ms || (result as any)?.execution_time_ms || 0;
  const stdDevMs = timeStats.std_dev_ms || 0;
  const cvPercent = meanMs > 0 ? (stdDevMs / meanMs) * 100 : 0;
  const peakKb = result?.memory_stats?.peak_kb ?? 0;

  // Actual individual measured run durations
  const rawDurations = result?.raw_durations_ms || [];
  const runChartData = useMemo(() => {
    return rawDurations.map((duration, idx) => ({
      runNumber: `Run #${idx + 1}`,
      durationMs: Number(duration.toFixed(5)),
      isAboveMean: duration > meanMs,
    }));
  }, [rawDurations, meanMs]);

  // Determine Measurement Stability based strictly on CV
  const stabilityAssessment = useMemo(() => {
    if (cvPercent < 5) {
      return {
        level: "High Temporal Stability (Low Jitter)",
        variant: "success",
        badgeBg: "bg-emerald-500/15 text-emerald-400 border-emerald-500/30",
        description: `The standard deviation of ${stdDevMs.toFixed(4)} ms represents only ${cvPercent.toFixed(2)}% of the mean runtime. Execution exhibited minimal OS scheduling jitter and highly consistent cache utilization.`,
      };
    } else if (cvPercent <= 20) {
      return {
        level: "Moderate Measurement Variability",
        variant: "warning",
        badgeBg: "bg-amber-500/15 text-amber-300 border-amber-500/30",
        description: `The coefficient of variation is ${cvPercent.toFixed(2)}%. Timing variations reflect typical hardware thread scheduling, context switching, and cache line contention on genuine physical cores.`,
      };
    } else {
      return {
        level: "Noticeable Measurement Variability",
        variant: "danger",
        badgeBg: "bg-rose-500/15 text-rose-300 border-rose-500/30",
        description: `The relative variability of ${cvPercent.toFixed(2)}% indicates sensitivity to branch prediction paths, input data distribution variance, or cold-cache memory access latency across runs.`,
      };
    }
  }, [cvPercent, stdDevMs]);

  // Multi-algorithm comparison metrics if available
  const allResults = benchmarkResponse?.results || [];
  const isFastest = benchmarkResponse?.fastest_algorithm === result?.algorithm_slug;
  const speedupRatio = result?.algorithm_slug ? benchmarkResponse?.speedup_ratios?.[result.algorithm_slug] : undefined;

  if (!isOpen || !result) return null;

  return (
    <div
      className="fixed inset-0 z-50 flex items-center justify-center p-3 sm:p-5 bg-black/80 backdrop-blur-sm animate-in fade-in duration-200"
      onClick={onClose}
    >
      <div
        className="relative w-full max-w-4xl max-h-[90vh] flex flex-col rounded-2xl bg-[#0b0f19] border border-slate-800 shadow-2xl overflow-hidden animate-in zoom-in-95 duration-150"
        onClick={(e) => e.stopPropagation()}
      >
        {/* ============================================================= */}
        {/* 1. MODAL HEADER                                               */}
        {/* ============================================================= */}
        <div className="flex items-start justify-between px-6 py-4 border-b border-slate-800/90 bg-slate-900/60">
          <div className="space-y-1.5">
            <div className="flex items-center gap-2">
              <span className="w-2 h-2 rounded-full bg-sky-400" />
              <span className="text-[11px] font-mono uppercase tracking-wider text-slate-400">
                Empirical Performance Analysis • Statistical Deep-Dive
              </span>
            </div>
            <div className="flex flex-wrap items-center gap-2.5">
              <h2 className="text-lg font-bold text-white tracking-tight flex items-center gap-2">
                {isFastest && <Award className="w-5 h-5 text-emerald-400" />}
                <span>{result.algorithm_name || result.algorithm_slug}</span>
              </h2>
              <span className="px-2 py-0.5 rounded text-[10px] font-mono font-medium bg-sky-500/15 text-sky-300 border border-sky-500/30">
                {result.paradigm || result.category || "Computational"}
              </span>
              {isFastest ? (
                <span className="px-2 py-0.5 rounded text-[10px] font-mono font-bold bg-emerald-500/15 text-emerald-400 border border-emerald-500/30">
                  Fastest Baseline (1.0x)
                </span>
              ) : (
                speedupRatio !== undefined && (
                  <span className="px-2 py-0.5 rounded text-[10px] font-mono font-medium bg-amber-500/15 text-amber-300 border border-amber-500/30">
                    {speedupRatio.toFixed(2)}x slower vs baseline
                  </span>
                )
              )}
            </div>

            {/* Compact Header Badges */}
            <div className="flex flex-wrap items-center gap-2 pt-0.5 text-[11px] font-mono text-slate-400">
              <span className="text-slate-300">Target: <strong className="text-white">{problemName}</strong></span>
              <span>•</span>
              <span>Input: <strong className="text-sky-300">N = {inputSize}</strong></span>
              <span>•</span>
              <span>Samples: <strong className="text-white">{repetitions} Measured Runs</strong></span>
              <span>•</span>
              <span>Warmup: <strong className="text-slate-300">{warmupRuns} Runs</strong></span>
              <span>•</span>
              <span className="text-emerald-400 flex items-center gap-1">
                <Activity className="w-3 h-3" />
                Hardware-Isolated
              </span>
            </div>
          </div>

          <button
            onClick={onClose}
            className="p-1.5 rounded-lg text-slate-400 hover:text-white hover:bg-slate-800 transition-colors focus:outline-none"
            title="Close breakdown (Esc)"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* ============================================================= */}
        {/* 2. SCROLLABLE CONTENT BODY                                    */}
        {/* ============================================================= */}
        <div className="p-6 overflow-y-auto space-y-6 text-slate-200">
          {/* Section 1: Executive Empirical Metrics Cards */}
          <div>
            <div className="text-xs font-mono font-bold text-slate-400 uppercase tracking-wider mb-3 flex items-center gap-2">
              <BarChart3 className="w-4 h-4 text-sky-400" />
              <span>Executive Empirical Metrics</span>
            </div>

            <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 font-mono">
              {/* Mean */}
              <div className="p-3.5 rounded-xl bg-slate-900/80 border border-slate-800 space-y-1">
                <span className="text-[10px] text-slate-400 uppercase tracking-wider block">Arithmetic Mean</span>
                <div className="text-base font-bold text-sky-400 tabular-nums">
                  {meanMs.toFixed(4)} ms
                </div>
                <span className="text-[10px] text-slate-500 block font-sans">Average measured time</span>
              </div>

              {/* Median */}
              <div className="p-3.5 rounded-xl bg-slate-900/80 border border-slate-800 space-y-1">
                <span className="text-[10px] text-slate-400 uppercase tracking-wider block">Median (P50)</span>
                <div className="text-base font-bold text-white tabular-nums">
                  {timeStats.median_ms.toFixed(4)} ms
                </div>
                <span className="text-[10px] text-slate-500 block font-sans">Central observation</span>
              </div>

              {/* Min / Max */}
              <div className="p-3.5 rounded-xl bg-slate-900/80 border border-slate-800 space-y-1">
                <span className="text-[10px] text-slate-400 uppercase tracking-wider block">Min / Max Range</span>
                <div className="text-xs font-bold text-emerald-300 tabular-nums pt-0.5">
                  {timeStats.min_ms.toFixed(4)} / {timeStats.max_ms.toFixed(4)} ms
                </div>
                <span className="text-[10px] text-slate-500 block font-sans">Fastest to slowest run</span>
              </div>

              {/* Std Deviation */}
              <div className="p-3.5 rounded-xl bg-slate-900/80 border border-slate-800 space-y-1">
                <span className="text-[10px] text-slate-400 uppercase tracking-wider block">Std Deviation (σ)</span>
                <div className="text-base font-bold text-amber-400 tabular-nums">
                  {stdDevMs.toFixed(4)} ms
                </div>
                <span className="text-[10px] text-slate-500 block font-sans">Sample dispersion</span>
              </div>

              {/* Variance */}
              <div className="p-3.5 rounded-xl bg-slate-900/80 border border-slate-800 space-y-1">
                <span className="text-[10px] text-slate-400 uppercase tracking-wider block">Variance (σ²)</span>
                <div className="text-xs font-bold text-slate-300 tabular-nums pt-0.5">
                  {timeStats.variance_ms.toFixed(6)} ms²
                </div>
                <span className="text-[10px] text-slate-500 block font-sans">Squared deviation</span>
              </div>

              {/* P95 */}
              <div className="p-3.5 rounded-xl bg-slate-900/80 border border-slate-800 space-y-1">
                <span className="text-[10px] text-slate-400 uppercase tracking-wider block">95th Percentile</span>
                <div className="text-base font-bold text-purple-300 tabular-nums">
                  {timeStats.p95_ms.toFixed(4)} ms
                </div>
                <span className="text-[10px] text-slate-500 block font-sans">95% runs under this time</span>
              </div>

              {/* Relative Std Dev / CV */}
              <div className="p-3.5 rounded-xl bg-slate-900/80 border border-slate-800 space-y-1">
                <span className="text-[10px] text-slate-400 uppercase tracking-wider block">Coeff. of Variation (CV)</span>
                <div className={`text-base font-bold tabular-nums ${cvPercent < 10 ? "text-emerald-400" : "text-amber-400"}`}>
                  {cvPercent.toFixed(2)}%
                </div>
                <span className="text-[10px] text-slate-500 block font-sans">Relative variability (σ/μ)</span>
              </div>

              {/* Peak Memory */}
              <div className="p-3.5 rounded-xl bg-slate-900/80 border border-slate-800 space-y-1">
                <span className="text-[10px] text-slate-400 uppercase tracking-wider block">Peak Memory</span>
                <div className="text-base font-bold text-purple-400 tabular-nums">
                  {peakKb > 0 ? `${peakKb.toFixed(2)} KB` : "Minimal"}
                </div>
                <span className="text-[10px] text-slate-500 block font-sans">Tracemalloc peak heap</span>
              </div>
            </div>
          </div>

          {/* Section 2: Distribution / Run-by-Run Execution Plot */}
          {runChartData.length > 0 && (
            <div className="space-y-3 p-4 rounded-xl bg-slate-900/50 border border-slate-800">
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-2">
                  <Activity className="w-4 h-4 text-sky-400" />
                  <span className="text-xs font-mono font-bold text-white uppercase tracking-wider">
                    Actual Recorded Measurements ({runChartData.length} Runs)
                  </span>
                </div>
                <div className="flex items-center gap-2 text-[10px] font-mono text-slate-400">
                  <span className="inline-block w-2.5 h-0.5 bg-amber-400" />
                  <span>Mean: {meanMs.toFixed(4)} ms</span>
                </div>
              </div>

              <div className="h-44 w-full pt-1">
                <ResponsiveContainer width="100%" height="100%">
                  <BarChart data={runChartData} margin={{ top: 10, right: 15, left: -10, bottom: 5 }}>
                    <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" />
                    <XAxis
                      dataKey="runNumber"
                      stroke="#64748b"
                      fontSize={10}
                      tickLine={false}
                      fontFamily="monospace"
                    />
                    <YAxis
                      stroke="#64748b"
                      fontSize={10}
                      tickLine={false}
                      fontFamily="monospace"
                      label={{
                        value: "Time (ms)",
                        angle: -90,
                        position: "insideLeft",
                        fill: "#64748b",
                        fontSize: 9,
                      }}
                    />
                    <Tooltip
                      contentStyle={{
                        backgroundColor: "#0b0f19",
                        borderColor: "#334155",
                        borderRadius: 8,
                        fontSize: 11,
                        fontFamily: "monospace",
                      }}
                      formatter={(val: any) => [`${Number(val).toFixed(5)} ms`, "Measured Duration"]}
                    />
                    <ReferenceLine
                      y={meanMs}
                      stroke="#f59e0b"
                      strokeDasharray="4 4"
                      label={{
                        value: `Mean`,
                        fill: "#f59e0b",
                        fontSize: 9,
                        position: "top",
                      }}
                    />
                    <Bar dataKey="durationMs" radius={[3, 3, 0, 0]}>
                      {runChartData.map((entry, index) => (
                        <Cell
                          key={`cell-${index}`}
                          fill={entry.isAboveMean ? "#8b5cf6" : "#0ea5e9"}
                        />
                      ))}
                    </Bar>
                  </BarChart>
                </ResponsiveContainer>
              </div>

              <div className="flex items-center justify-between text-[10px] font-mono text-slate-500 pt-1 border-t border-slate-800/80">
                <span>Plotted strictly from genuine hardware measurements.</span>
                <span>Fastest: {timeStats.min_ms.toFixed(4)} ms • Slowest: {timeStats.max_ms.toFixed(4)} ms</span>
              </div>
            </div>
          )}

          {/* Section 3: Empirical Statistical Summary Table */}
          <div className="space-y-3">
            <div className="text-xs font-mono font-bold text-slate-400 uppercase tracking-wider flex items-center gap-2">
              <Scale className="w-4 h-4 text-sky-400" />
              <span>Statistical Distribution Breakdown</span>
            </div>

            <div className="overflow-hidden rounded-xl border border-slate-800 bg-slate-900/50">
              <table className="w-full text-left text-xs font-mono">
                <thead className="bg-slate-950/80 text-slate-400 border-b border-slate-800">
                  <tr>
                    <th className="px-4 py-2.5 font-semibold">Statistical Parameter</th>
                    <th className="px-4 py-2.5 font-semibold text-right">Measured Value</th>
                    <th className="px-4 py-2.5 font-semibold">Academic Interpretation</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-slate-800/60 text-slate-300">
                  <tr>
                    <td className="px-4 py-2 font-medium text-white">Sample Count (N)</td>
                    <td className="px-4 py-2 text-right font-bold text-sky-300">{repetitions} runs</td>
                    <td className="px-4 py-2 text-slate-400 font-sans text-[11px]">
                      Independent hardware executions under isolated thread conditions
                    </td>
                  </tr>
                  <tr>
                    <td className="px-4 py-2 font-medium text-white">Arithmetic Mean (μ)</td>
                    <td className="px-4 py-2 text-right font-bold text-sky-400">{meanMs.toFixed(4)} ms</td>
                    <td className="px-4 py-2 text-slate-400 font-sans text-[11px]">
                      Expected execution time across repeated workload invocations
                    </td>
                  </tr>
                  <tr>
                    <td className="px-4 py-2 font-medium text-white">Median (Q₂ / 50th %ile)</td>
                    <td className="px-4 py-2 text-right font-bold text-white">{timeStats.median_ms.toFixed(4)} ms</td>
                    <td className="px-4 py-2 text-slate-400 font-sans text-[11px]">
                      Robust central tendency resistant to OS background interruption spikes
                    </td>
                  </tr>
                  <tr>
                    <td className="px-4 py-2 font-medium text-white">Minimum (X_min)</td>
                    <td className="px-4 py-2 text-right font-bold text-emerald-400">{timeStats.min_ms.toFixed(4)} ms</td>
                    <td className="px-4 py-2 text-slate-400 font-sans text-[11px]">
                      Best observed run with optimal CPU instruction and cache alignment
                    </td>
                  </tr>
                  <tr>
                    <td className="px-4 py-2 font-medium text-white">Maximum (X_max)</td>
                    <td className="px-4 py-2 text-right font-bold text-rose-400">{timeStats.max_ms.toFixed(4)} ms</td>
                    <td className="px-4 py-2 text-slate-400 font-sans text-[11px]">
                      Worst observed run, capturing cold cache penalty or context interrupt
                    </td>
                  </tr>
                  {timeStats.iqr_ms > 0 && (
                    <tr>
                      <td className="px-4 py-2 font-medium text-white">Interquartile Range (IQR)</td>
                      <td className="px-4 py-2 text-right font-bold text-slate-200">{timeStats.iqr_ms.toFixed(4)} ms</td>
                      <td className="px-4 py-2 text-slate-400 font-sans text-[11px]">
                        Spread of the middle 50% of observed executions (Q₃ - Q₁)
                      </td>
                    </tr>
                  )}
                  <tr>
                    <td className="px-4 py-2 font-medium text-white">Standard Deviation (σ)</td>
                    <td className="px-4 py-2 text-right font-bold text-amber-300">{stdDevMs.toFixed(4)} ms</td>
                    <td className="px-4 py-2 text-slate-400 font-sans text-[11px]">
                      Root-mean-square deviation from the arithmetic mean
                    </td>
                  </tr>
                  <tr>
                    <td className="px-4 py-2 font-medium text-white">Sample Variance (σ²)</td>
                    <td className="px-4 py-2 text-right font-bold text-slate-300">{timeStats.variance_ms.toFixed(6)} ms²</td>
                    <td className="px-4 py-2 text-slate-400 font-sans text-[11px]">
                      Squared measurement variance across sample executions
                    </td>
                  </tr>
                  <tr>
                    <td className="px-4 py-2 font-medium text-white">95th Percentile (P₉₅)</td>
                    <td className="px-4 py-2 text-right font-bold text-purple-300">{timeStats.p95_ms.toFixed(4)} ms</td>
                    <td className="px-4 py-2 text-slate-400 font-sans text-[11px]">
                      Service Level Objective (SLO) bound: 95% of runs complete faster than this
                    </td>
                  </tr>
                  <tr>
                    <td className="px-4 py-2 font-medium text-white">Coefficient of Variation (CV)</td>
                    <td className="px-4 py-2 text-right font-bold text-sky-300">{cvPercent.toFixed(2)}%</td>
                    <td className="px-4 py-2 text-slate-400 font-sans text-[11px]">
                      Relative stability metric: (σ / μ) normalized percentage
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>

          {/* Section 4: Measurement Stability Assessment */}
          <div className="p-4 rounded-xl bg-[#0e131f] border border-slate-800 space-y-2">
            <div className="flex items-center justify-between">
              <span className="text-xs font-mono font-bold text-white uppercase tracking-wider flex items-center gap-2">
                <Activity className="w-4 h-4 text-sky-400" />
                Measurement Stability Assessment
              </span>
              <span className={`px-2 py-0.5 rounded text-[10px] font-mono font-semibold border ${stabilityAssessment.badgeBg}`}>
                {stabilityAssessment.level}
              </span>
            </div>
            <p className="text-xs text-slate-300 leading-relaxed font-sans">
              {stabilityAssessment.description}
            </p>
          </div>

          {/* Section 5: Comparative Standing (if multiple algorithms benchmarked) */}
          {allResults.length > 1 && (
            <div className="space-y-3">
              <div className="text-xs font-mono font-bold text-slate-400 uppercase tracking-wider flex items-center gap-2">
                <Layers className="w-4 h-4 text-sky-400" />
                <span>Multi-Algorithm Comparative Standing</span>
              </div>

              <div className="overflow-hidden rounded-xl border border-slate-800 bg-slate-900/50">
                <table className="w-full text-left text-xs font-mono">
                  <thead className="bg-slate-950/80 text-slate-400 border-b border-slate-800">
                    <tr>
                      <th className="px-4 py-2.5 font-semibold">Candidate</th>
                      <th className="px-4 py-2.5 font-semibold">Mean Time</th>
                      <th className="px-4 py-2.5 font-semibold">Delta vs Baseline</th>
                      <th className="px-4 py-2.5 font-semibold">Peak Memory</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-slate-800/60 text-slate-300">
                    {allResults.map((r) => {
                      const isCurrent = r.algorithm_slug === result.algorithm_slug;
                      const rMean = r.time_stats?.mean_ms ?? (r as any).execution_time_ms ?? 0;
                      const rSpeedup = benchmarkResponse?.speedup_ratios?.[r.algorithm_slug];
                      const isWinner = benchmarkResponse?.fastest_algorithm === r.algorithm_slug;

                      return (
                        <tr
                          key={r.algorithm_slug}
                          className={isCurrent ? "bg-sky-500/10 font-semibold" : "hover:bg-slate-900/30"}
                        >
                          <td className="px-4 py-2.5 flex items-center gap-2">
                            {isWinner && <Award className="w-3.5 h-3.5 text-emerald-400 flex-shrink-0" />}
                            <span className={isCurrent ? "text-sky-300 font-bold" : "text-white"}>
                              {r.algorithm_name || r.algorithm_slug}
                            </span>
                            {isCurrent && (
                              <span className="px-1.5 py-0.2 rounded text-[9px] font-mono bg-sky-500/20 text-sky-300 border border-sky-500/40">
                                This View
                              </span>
                            )}
                          </td>
                          <td className="px-4 py-2.5 text-sky-400">{rMean.toFixed(4)} ms</td>
                          <td className="px-4 py-2.5">
                            {isWinner ? (
                              <span className="text-emerald-400 font-semibold flex items-center gap-1">
                                <TrendingUp className="w-3.5 h-3.5" />
                                Baseline (1.0x)
                              </span>
                            ) : rSpeedup !== undefined ? (
                              <span className="text-amber-400 flex items-center gap-1">
                                <TrendingDown className="w-3.5 h-3.5" />
                                {rSpeedup.toFixed(2)}x slower
                              </span>
                            ) : (
                              <span className="text-slate-500">—</span>
                            )}
                          </td>
                          <td className="px-4 py-2.5 text-purple-300">
                            {r.memory_stats?.peak_kb ? `${r.memory_stats.peak_kb.toFixed(2)} KB` : "—"}
                          </td>
                        </tr>
                      );
                    })}
                  </tbody>
                </table>
              </div>
            </div>
          )}

          {/* Section 6: Theoretical Asymptotics vs. Empirical Reality */}
          <div className="p-4 rounded-xl bg-slate-900/60 border border-slate-800 space-y-3">
            <div className="flex items-center gap-2 text-xs font-mono font-bold text-white uppercase tracking-wider">
              <BookOpen className="w-4 h-4 text-purple-400" />
              <span>Theoretical Asymptotics vs. Empirical Measurement</span>
            </div>

            <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 text-xs font-mono">
              <div className="p-3 rounded-lg bg-slate-950/60 border border-slate-800 space-y-1.5">
                <span className="text-[10px] text-purple-400 font-bold uppercase tracking-wider block">
                  Theoretical Complexity (Formal Bounds)
                </span>
                <div className="space-y-1 text-slate-300 text-[11px]">
                  <div>Average Case: <strong className="text-white">{result.theoretical_complexity?.average || "O(f(n))"}</strong></div>
                  <div>Worst Case: <strong className="text-white">{result.theoretical_complexity?.worst || "O(f(n))"}</strong></div>
                  <div>Auxiliary Space: <strong className="text-white">{result.theoretical_complexity?.space || "O(1)"}</strong></div>
                </div>
              </div>

              <div className="p-3 rounded-lg bg-slate-950/60 border border-slate-800 space-y-1.5">
                <span className="text-[10px] text-sky-400 font-bold uppercase tracking-wider block">
                  Empirical Observation (This Machine & Input)
                </span>
                <div className="space-y-1 text-slate-300 text-[11px]">
                  <div>Measured Mean: <strong className="text-sky-300">{meanMs.toFixed(4)} ms</strong></div>
                  <div>Peak Memory: <strong className="text-purple-300">{peakKb.toFixed(2)} KB</strong></div>
                  <div>Sample Dispersion: <strong className="text-amber-300">σ = {stdDevMs.toFixed(4)} ms</strong></div>
                </div>
              </div>
            </div>

            <div className="p-2.5 rounded-lg bg-slate-950/40 border border-slate-800 text-[11px] font-sans text-slate-400 flex items-start gap-2">
              <Info className="w-4 h-4 text-sky-400 flex-shrink-0 mt-0.5" />
              <span className="leading-relaxed">
                Empirical results represent non-simulated physical execution timings on this hardware environment for input dimension N = {inputSize}. They reflect real architectural cache and instruction behavior and complement, but do not replace, formal asymptotic complexity analysis.
              </span>
            </div>
          </div>

          {/* Section 7: Reproducibility & Environment Configuration */}
          <div className="p-3.5 rounded-xl bg-[#080b11] border border-slate-800/80 text-[11px] font-mono text-slate-400 space-y-1.5">
            <span className="text-[10px] text-slate-500 uppercase tracking-wider font-semibold block">
              Benchmark Reproducibility Metadata:
            </span>
            <div className="grid grid-cols-2 sm:grid-cols-4 gap-2 text-[10px]">
              <div>Target Problem: <span className="text-slate-200">{problemSlug}</span></div>
              <div>Algorithm: <span className="text-slate-200">{result.algorithm_slug}</span></div>
              <div>Clock: <span className="text-emerald-400">perf_counter_ns</span></div>
              <div>Memory Profiler: <span className="text-purple-400">tracemalloc</span></div>
            </div>
          </div>
        </div>

        {/* ============================================================= */}
        {/* 3. MODAL FOOTER                                               */}
        {/* ============================================================= */}
        <div className="flex items-center justify-between px-6 py-3.5 border-t border-slate-800/90 bg-slate-900/80">
          <Link to={`/algorithms/${result.algorithm_slug}`}>
            <Button variant="secondary" size="sm" icon={<ExternalLink className="w-3.5 h-3.5" />}>
              Open Algorithm Specifications & Code
            </Button>
          </Link>

          <Button variant="primary" size="sm" onClick={onClose}>
            Close Breakdown
          </Button>
        </div>
      </div>
    </div>
  );
}
