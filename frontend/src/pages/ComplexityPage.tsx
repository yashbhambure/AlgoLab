import { useState, useEffect } from "react";
import { useSearchParams, Link } from "react-router-dom";
import {
  Sigma,
  BarChart2,
  ArrowRight,
  ChevronDown,
  ChevronUp,
  Layers,
  Scale,
  Sparkles,
  CheckCircle2,
  XCircle,
  Play,
  ShieldCheck,
  HelpCircle,
  Zap,
} from "lucide-react";
import { Layout } from "../components/layout/Layout";
import { PageHeader } from "../components/layout/PageHeader";
import { Card } from "../components/common/Card";
import { Button } from "../components/common/Button";
import { Badge } from "../components/common/Badge";
import { Tabs } from "../components/common/Tabs";
import { LoadingState } from "../components/common/LoadingState";
import { api } from "../services/api";
import type {
  MasterTheoremResponse,
  CurveFitResponse,
  CompatibleComparisonGroup,
  BenchmarkResponse,
} from "../types";
import {
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  LineChart,
  Line,
  Legend,
} from "recharts";

// ─────────────── Tab 1: Compatible Algorithm Comparisons ───────────────
function CompatibleComparisonsTab({
  initialProblem,
  initialAlgorithm,
}: {
  initialProblem?: string | null;
  initialAlgorithm?: string | null;
}) {
  const [groups, setGroups] = useState<CompatibleComparisonGroup[]>([]);
  const [loading, setLoading] = useState(true);
  const [selectedProblemSlug, setSelectedProblemSlug] = useState<string>("");
  const [benchmarkResult, setBenchmarkResult] = useState<BenchmarkResponse | null>(null);
  const [benchmarkLoading, setBenchmarkLoading] = useState(false);

  useEffect(() => {
    setLoading(true);
    api.getCompatibleGroups(false)
      .then((data) => {
        setGroups(data);
        if (initialProblem && data.some((g) => g.problem_slug === initialProblem)) {
          setSelectedProblemSlug(initialProblem);
        } else if (
          initialAlgorithm &&
          data.some((g) => g.algorithms.some((a) => a.slug === initialAlgorithm))
        ) {
          const matched = data.find((g) => g.algorithms.some((a) => a.slug === initialAlgorithm));
          if (matched) setSelectedProblemSlug(matched.problem_slug);
        } else if (data.length > 0) {
          setSelectedProblemSlug(data[0].problem_slug);
        }
      })
      .catch((err) => console.error("Failed to load compatible groups:", err))
      .finally(() => setLoading(false));
  }, [initialProblem, initialAlgorithm]);

  const selectedGroup = groups.find((g) => g.problem_slug === selectedProblemSlug) || groups[0];

  const handleRunEmpiricalBenchmark = async () => {
    if (!selectedGroup) return;
    setBenchmarkLoading(true);
    setBenchmarkResult(null);
    try {
      const res = await api.runComparisonBenchmark({
        algorithm_slugs: selectedGroup.algorithms.map((a) => a.slug),
        size: 50,
        repetitions: 5,
      });
      setBenchmarkResult(res);
    } catch (err) {
      console.error("Benchmark error:", err);
    } finally {
      setBenchmarkLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="py-20">
        <LoadingState message="Loading curriculum-aware compatibility groups..." />
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Strict Theoretical vs Empirical Separation Banner */}
      <div className="p-4 rounded-xl bg-slate-900/90 border border-slate-800 flex items-start gap-3">
        <ShieldCheck className="w-5 h-5 text-sky-400 flex-shrink-0 mt-0.5" />
        <div className="text-xs font-sans text-slate-300 space-y-1">
          <div className="font-semibold text-white">
            Authoritative Theoretical Bounds vs Empirical Benchmark Telemetry
          </div>
          <p className="text-slate-400 leading-relaxed">
            Theoretical complexity (<span className="font-mono text-emerald-400">Best</span>,{" "}
            <span className="font-mono text-sky-400">Average</span>,{" "}
            <span className="font-mono text-amber-400">Worst</span>,{" "}
            <span className="font-mono text-purple-400">Space</span>) is mathematically proven via asymptotic analysis, recurrence relations, and Master Theorem derivations. Empirical measurements reflect wall-clock hardware execution on physical CPU architectures.
          </p>
        </div>
      </div>

      {/* Problem Group Selector */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 p-4 rounded-xl bg-[#0e131f] border border-slate-800">
        <div className="flex items-center gap-3">
          <Layers className="w-5 h-5 text-sky-400" />
          <div>
            <div className="text-xs font-mono text-slate-400">Select Compatible Problem Group:</div>
            <div className="text-sm font-semibold text-white">{selectedGroup?.problem_name}</div>
          </div>
        </div>

        <select
          value={selectedProblemSlug}
          onChange={(e) => {
            setSelectedProblemSlug(e.target.value);
            setBenchmarkResult(null);
          }}
          className="px-3 py-2 rounded-lg bg-slate-900 border border-slate-700 text-xs font-mono text-white focus:outline-none focus:border-sky-500 font-medium"
        >
          <optgroup label="Authoritative Curriculum Problem Groups">
            {groups
              .filter((g) => g.is_curriculum)
              .map((g) => (
                <option key={g.problem_slug} value={g.problem_slug}>
                  {g.problem_name} ({g.algorithms.length} Algorithms)
                </option>
              ))}
          </optgroup>
          <optgroup label="Supplementary Educational Groups">
            {groups
              .filter((g) => !g.is_curriculum)
              .map((g) => (
                <option key={g.problem_slug} value={g.problem_slug}>
                  {g.problem_name} ({g.algorithms.length} Algorithms)
                </option>
              ))}
          </optgroup>
        </select>
      </div>

      {selectedGroup && (
        <div className="space-y-5">
          {/* Problem Details & Action Header */}
          <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 p-4 rounded-xl bg-slate-900/60 border border-slate-800">
            <div className="space-y-1">
              <div className="flex items-center gap-2">
                <span className="text-xs font-mono text-slate-400">Category:</span>
                <Badge variant="primary" mono size="sm">
                  {selectedGroup.category}
                </Badge>
                {selectedGroup.is_curriculum ? (
                  <span className="px-2 py-0.5 rounded text-[10px] font-mono font-medium bg-emerald-500/15 text-emerald-400 border border-emerald-500/30">
                    Curriculum Core
                  </span>
                ) : (
                  <span className="px-2 py-0.5 rounded text-[10px] font-mono font-medium bg-slate-800 text-slate-400 border border-slate-700">
                    Supplementary Educational
                  </span>
                )}
              </div>
              {selectedGroup.constraints && (
                <div className="text-xs font-mono text-slate-400">
                  Constraints: <span className="text-slate-300">{selectedGroup.constraints}</span>
                </div>
              )}
            </div>

            <Button
              variant="secondary"
              size="sm"
              onClick={handleRunEmpiricalBenchmark}
              disabled={benchmarkLoading || selectedGroup.algorithms.length < 2}
              loading={benchmarkLoading}
              icon={<Zap className="w-3.5 h-3.5 text-amber-400" />}
            >
              Run Live Empirical Benchmark
            </Button>
          </div>

          {/* Side-by-Side Compatible Algorithm Comparison Matrix */}
          <div
            className={`grid gap-4 ${
              selectedGroup.algorithms.length === 2
                ? "grid-cols-1 md:grid-cols-2"
                : selectedGroup.algorithms.length === 3
                ? "grid-cols-1 md:grid-cols-3"
                : "grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4"
            }`}
          >
            {selectedGroup.algorithms.map((algo) => (
              <Card
                key={algo.slug}
                headerTag={algo.name}
                headerRight={
                  <Badge variant="purple" mono size="sm">
                    {algo.paradigm}
                  </Badge>
                }
              >
                <div className="space-y-3 font-mono text-xs">
                  <p className="text-slate-400 text-[11px] leading-relaxed line-clamp-3">
                    {algo.description}
                  </p>

                  <div className="p-3 rounded-lg bg-[#080b11] border border-slate-800 space-y-2">
                    <div className="flex justify-between items-center text-[11px]">
                      <span className="text-slate-400">Best Case:</span>
                      <span className="text-emerald-400 font-semibold">{algo.best_case}</span>
                    </div>
                    <div className="flex justify-between items-center text-[11px]">
                      <span className="text-slate-400">Average Case:</span>
                      <span className="text-sky-400 font-semibold">{algo.average_case}</span>
                    </div>
                    <div className="flex justify-between items-center text-[11px]">
                      <span className="text-slate-400">Worst Case:</span>
                      <span className="text-amber-400 font-semibold">{algo.worst_case}</span>
                    </div>
                    <div className="flex justify-between items-center text-[11px]">
                      <span className="text-slate-400">Space Complexity:</span>
                      <span className="text-purple-400 font-semibold">{algo.space_complexity}</span>
                    </div>
                  </div>

                  {algo.recurrence_relation && (
                    <div className="p-2.5 rounded-lg bg-slate-900/80 border border-slate-800 text-[11px]">
                      <span className="text-slate-400 block mb-0.5">Recurrence:</span>
                      <span className="text-slate-200 font-semibold">{algo.recurrence_relation}</span>
                    </div>
                  )}

                  <div className="grid grid-cols-2 gap-2 text-[10px] pt-1">
                    <div className="p-1.5 rounded bg-slate-900 border border-slate-800 text-center">
                      <span className="text-slate-400 block">Stable</span>
                      <span className={algo.is_stable ? "text-emerald-400 font-bold" : "text-slate-500"}>
                        {algo.is_stable ? "YES" : "NO"}
                      </span>
                    </div>
                    <div className="p-1.5 rounded bg-slate-900 border border-slate-800 text-center">
                      <span className="text-slate-400 block">In-Place</span>
                      <span className={algo.is_in_place ? "text-emerald-400 font-bold" : "text-slate-500"}>
                        {algo.is_in_place ? "YES" : "NO"}
                      </span>
                    </div>
                  </div>

                  {/* Visualizer & Benchmark Deep Links */}
                  <div className="pt-2 border-t border-slate-800 flex items-center justify-between gap-2">
                    <Link
                      to={`/visualizer?algorithm=${algo.slug}`}
                      className="text-sky-400 hover:text-sky-300 transition-colors text-[11px] flex items-center gap-1"
                    >
                      <Play className="w-3 h-3" />
                      <span>Visualize</span>
                    </Link>
                    <Link
                      to={`/benchmarks?algorithm=${algo.slug}`}
                      className="text-purple-400 hover:text-purple-300 transition-colors text-[11px] flex items-center gap-1"
                    >
                      <span>Benchmark</span>
                    </Link>
                  </div>
                </div>
              </Card>
            ))}
          </div>

          {/* Empirical Benchmark Comparison Results (if triggered) */}
          {benchmarkResult && (
            <Card
              headerTag="Empirical Benchmark Comparison Results"
              headerRight={
                <Badge variant="success" mono size="sm">
                  {benchmarkResult.results.length} Algorithms Tested
                </Badge>
              }
            >
              <div className="space-y-4 font-mono text-xs">
                <div className="overflow-x-auto">
                  <table className="w-full text-left font-mono text-xs">
                    <thead className="border-b border-slate-800 bg-[#141b2d] text-[10px] text-slate-400 uppercase tracking-wider">
                      <tr>
                        <th className="py-2.5 px-3">Algorithm</th>
                        <th className="py-2.5 px-3">Paradigm</th>
                        <th className="py-2.5 px-3 text-sky-400">Mean Time (ms)</th>
                        <th className="py-2.5 px-3 text-purple-400">Peak Heap (KB)</th>
                        <th className="py-2.5 px-3 text-amber-400">Operations</th>
                        <th className="py-2.5 px-3">Theoretical Avg</th>
                      </tr>
                    </thead>
                    <tbody className="divide-y divide-slate-800 text-slate-300">
                      {benchmarkResult.results.map((res) => (
                        <tr key={res.algorithm_slug} className="hover:bg-slate-900/40">
                          <td className="py-2.5 px-3 font-semibold text-white">
                            {res.algorithm_name}
                          </td>
                          <td className="py-2.5 px-3 text-slate-400">{res.paradigm}</td>
                          <td className="py-2.5 px-3 text-sky-300 font-semibold tabular-nums">
                            {res.time_stats.mean_ms.toFixed(4)} ms
                          </td>
                          <td className="py-2.5 px-3 text-purple-300 tabular-nums">
                            {res.memory_stats.peak_kb.toFixed(2)} KB
                          </td>
                          <td className="py-2.5 px-3 text-amber-300 tabular-nums">
                            {res.operations?.operations ?? "—"}
                          </td>
                          <td className="py-2.5 px-3 text-emerald-400">
                            {res.theoretical_complexity?.average ?? "—"}
                          </td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              </div>
            </Card>
          )}
        </div>
      )}
    </div>
  );
}

// ─────────────── Tab 2: Master Theorem Solver ───────────────
function MasterTheoremTab() {
  const [a, setA] = useState(2);
  const [b, setB] = useState(2);
  const [k, setK] = useState(1);
  const [p, setP] = useState(0);
  const [result, setResult] = useState<MasterTheoremResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [stepsExpanded, setStepsExpanded] = useState(true);

  const PRESETS = [
    { label: "Binary Search: T(n) = T(n/2) + O(1)", a: 1, b: 2, k: 0, p: 0 },
    { label: "Merge Sort: T(n) = 2T(n/2) + O(n)", a: 2, b: 2, k: 1, p: 0 },
    { label: "Strassen Matrix: T(n) = 7T(n/2) + O(n²)", a: 7, b: 2, k: 2, p: 0 },
    { label: "Finding Max-Min: T(n) = 2T(n/2) + O(1)", a: 2, b: 2, k: 0, p: 0 },
    { label: "T(n) = 4T(n/2) + O(n² log n)", a: 4, b: 2, k: 2, p: 1 },
  ];

  const handleSolve = async () => {
    setLoading(true);
    setError(null);
    try {
      const res = await api.solveMasterTheorem({ a, b, k, p });
      setResult(res);
    } catch (err: any) {
      setError(err.message || "Failed to solve recurrence.");
    } finally {
      setLoading(false);
    }
  };

  const getCaseBadge = (caseNum: number) => {
    switch (caseNum) {
      case 1:
        return <Badge variant="primary" mono>Case 1: Leaf-Heavy (k &lt; log_b a)</Badge>;
      case 2:
        return <Badge variant="purple" mono>Case 2: Balanced (k = log_b a)</Badge>;
      case 3:
        return <Badge variant="warning" mono>Case 3: Root-Heavy (k &gt; log_b a)</Badge>;
      default:
        return <Badge variant="default" mono>Case {caseNum}</Badge>;
    }
  };

  return (
    <div className="space-y-5">
      {/* Preset Recurrences */}
      <Card headerTag="Canonical DAA Recurrence Presets">
        <div className="flex flex-wrap gap-2">
          {PRESETS.map((preset) => (
            <button
              key={preset.label}
              onClick={() => {
                setA(preset.a);
                setB(preset.b);
                setK(preset.k);
                setP(preset.p);
              }}
              className="px-2.5 py-1.5 rounded-lg bg-slate-900/80 border border-slate-800 text-xs font-mono text-slate-300 hover:text-white hover:border-slate-700 transition-colors"
            >
              {preset.label}
            </button>
          ))}
        </div>
      </Card>

      {/* Recurrence Parameters and Solvers */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-5">
        <div className="lg:col-span-2">
          <Card headerTag="Recurrence Parameters: T(n) = a·T(n/b) + f(n)">
            <div className="space-y-4">
              {/* Formula Display */}
              <div className="p-4 rounded-lg bg-[#080b11] border border-slate-800 text-center">
                <span className="text-base sm:text-lg font-mono text-white tracking-wide">
                  T(n) = <span className="text-sky-400 font-semibold">{a}</span> &middot; T(n /{" "}
                  <span className="text-purple-400 font-semibold">{b}</span>) + &Theta;(n
                  <sup className="text-amber-400 font-semibold">{k}</sup>
                  {p !== 0 && (
                    <>
                      {" "}
                      &middot; log<sup className="text-emerald-400 font-semibold">{p}</sup>(n)
                    </>
                  )}
                  )
                </span>
              </div>

              {/* Parameter Inputs */}
              <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
                <div>
                  <label className="text-[11px] font-mono text-slate-400 block mb-1">
                    a (Subproblems &ge; 1)
                  </label>
                  <input
                    type="number"
                    min="1"
                    step="1"
                    value={a}
                    onChange={(e) => setA(Math.max(1, Number(e.target.value)))}
                    className="w-full px-3 py-1.5 rounded-lg bg-slate-900 border border-slate-800 text-white font-mono text-xs focus:outline-none focus:border-sky-500"
                  />
                </div>
                <div>
                  <label className="text-[11px] font-mono text-slate-400 block mb-1">
                    b (Divisor Factor &ge; 2)
                  </label>
                  <input
                    type="number"
                    min="2"
                    step="1"
                    value={b}
                    onChange={(e) => setB(Math.max(2, Number(e.target.value)))}
                    className="w-full px-3 py-1.5 rounded-lg bg-slate-900 border border-slate-800 text-white font-mono text-xs focus:outline-none focus:border-sky-500"
                  />
                </div>
                <div>
                  <label className="text-[11px] font-mono text-slate-400 block mb-1">
                    k (Poly Exponent &ge; 0)
                  </label>
                  <input
                    type="number"
                    min="0"
                    step="0.5"
                    value={k}
                    onChange={(e) => setK(Math.max(0, Number(e.target.value)))}
                    className="w-full px-3 py-1.5 rounded-lg bg-slate-900 border border-slate-800 text-white font-mono text-xs focus:outline-none focus:border-sky-500"
                  />
                </div>
                <div>
                  <label className="text-[11px] font-mono text-slate-400 block mb-1">
                    p (Log Exponent)
                  </label>
                  <input
                    type="number"
                    step="1"
                    value={p}
                    onChange={(e) => setP(Number(e.target.value))}
                    className="w-full px-3 py-1.5 rounded-lg bg-slate-900 border border-slate-800 text-white font-mono text-xs focus:outline-none focus:border-sky-500"
                  />
                </div>
              </div>

              <Button
                variant="primary"
                onClick={handleSolve}
                disabled={loading}
                loading={loading}
                icon={<Sigma className="w-4 h-4" />}
                className="w-full justify-center"
              >
                {loading ? "Deriving Asymptotic Bound..." : "Solve Recurrence"}
              </Button>
            </div>
          </Card>
        </div>

        {/* Master Theorem Theoretical Reference */}
        <div>
          <Card headerTag="Master Theorem Cases">
            <div className="space-y-2.5 font-mono text-xs">
              <div className="p-2.5 rounded-lg bg-slate-900/80 border border-slate-800 space-y-1">
                <span className="text-sky-400 font-semibold block">Case 1: Leaf-Heavy</span>
                <span className="text-slate-300 text-[11px] block">k &lt; log_b a &rarr; &Theta;(n^(log_b a))</span>
                <span className="text-slate-400 text-[10px] block">Sub-problem tree leaves dominate total work</span>
              </div>
              <div className="p-2.5 rounded-lg bg-slate-900/80 border border-slate-800 space-y-1">
                <span className="text-purple-400 font-semibold block">Case 2: Balanced</span>
                <span className="text-slate-300 text-[11px] block">k = log_b a &rarr; &Theta;(n^k &middot; log^(p+1) n)</span>
                <span className="text-slate-400 text-[10px] block">Work is evenly distributed across tree levels</span>
              </div>
              <div className="p-2.5 rounded-lg bg-slate-900/80 border border-slate-800 space-y-1">
                <span className="text-amber-400 font-semibold block">Case 3: Root-Heavy</span>
                <span className="text-slate-300 text-[11px] block">k &gt; log_b a &rarr; &Theta;(f(n))</span>
                <span className="text-slate-400 text-[10px] block">Root problem dominates (regularity must hold)</span>
              </div>
            </div>
          </Card>
        </div>
      </div>

      {/* Error Banner */}
      {error && (
        <div className="p-4 rounded-xl bg-rose-500/10 border border-rose-500/30 text-rose-300 font-mono text-xs">
          {error}
        </div>
      )}

      {/* Result Display */}
      {result && (
        <div className="space-y-4">
          <Card
            headerTag="Asymptotic Derivation Solution"
            headerRight={getCaseBadge(result.case_number)}
          >
            <div className="space-y-4">
              <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 border-b border-slate-800 pb-4">
                <div>
                  <span className="text-xs font-mono text-slate-400 block mb-1">
                    Closed-Form Asymptotic Bound:
                  </span>
                  <div className="text-2xl sm:text-3xl font-semibold text-white font-mono">
                    T(n) = {result.complexity}
                  </div>
                </div>

                {result.regularity_satisfied !== undefined && (
                  <div className="flex items-center gap-1.5 text-xs font-mono">
                    {result.regularity_satisfied ? (
                      <span className="flex items-center gap-1.5 text-emerald-400">
                        <CheckCircle2 className="w-4 h-4" />
                        Regularity Satisfied
                      </span>
                    ) : (
                      <span className="flex items-center gap-1.5 text-rose-400">
                        <XCircle className="w-4 h-4" />
                        Regularity Violated
                      </span>
                    )}
                  </div>
                )}
              </div>

              <p className="text-sm text-slate-300 leading-relaxed">
                {result.explanation}
              </p>

              {/* Critical Exponent Matrix */}
              <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 text-xs font-mono pt-1">
                <div className="p-2.5 rounded-lg bg-slate-900/80 border border-slate-800">
                  <span className="text-slate-400 block text-[10px]">Critical Exponent</span>
                  <span className="text-sky-400 font-semibold">c = log_{result.b}({result.a}) = {result.critical_exponent}</span>
                </div>
                <div className="p-2.5 rounded-lg bg-slate-900/80 border border-slate-800">
                  <span className="text-slate-400 block text-[10px]">Subproblems</span>
                  <span className="text-white font-semibold">a = {result.a}</span>
                </div>
                <div className="p-2.5 rounded-lg bg-slate-900/80 border border-slate-800">
                  <span className="text-slate-400 block text-[10px]">Division Factor</span>
                  <span className="text-white font-semibold">b = {result.b}</span>
                </div>
                <div className="p-2.5 rounded-lg bg-slate-900/80 border border-slate-800">
                  <span className="text-slate-400 block text-[10px]">Poly / Log Exponent</span>
                  <span className="text-white font-semibold">
                    k = {result.k}{result.p !== 0 ? `, p = ${result.p}` : ""}
                  </span>
                </div>
              </div>
            </div>
          </Card>

          {/* Step-by-Step Derivation */}
          {result.steps && result.steps.length > 0 && (
            <Card
              headerTag="Step-by-Step Mathematical Proof"
              headerRight={
                <button
                  onClick={() => setStepsExpanded(!stepsExpanded)}
                  className="flex items-center gap-1 text-xs font-mono text-sky-400 hover:text-sky-300 transition-colors"
                >
                  {stepsExpanded ? <ChevronUp className="w-3.5 h-3.5" /> : <ChevronDown className="w-3.5 h-3.5" />}
                  <span>{stepsExpanded ? "Collapse Proof" : "Expand Proof"}</span>
                </button>
              }
            >
              {stepsExpanded && (
                <div className="space-y-2 pt-1">
                  {result.steps.map((step, i) => (
                    <div
                      key={i}
                      className="flex items-start gap-3 p-3 rounded-lg bg-slate-900/60 border border-slate-800"
                    >
                      <span className="w-5 h-5 rounded-full bg-sky-500/15 border border-sky-500/30 flex items-center justify-center text-[10px] font-mono font-semibold text-sky-400 flex-shrink-0 mt-0.5">
                        {i + 1}
                      </span>
                      <span className="text-xs font-mono text-slate-200 leading-relaxed">{step}</span>
                    </div>
                  ))}
                </div>
              )}
            </Card>
          )}
        </div>
      )}
    </div>
  );
}

// ─────────────── Tab 3: Big-O Curve Fitting ───────────────
function CurveFittingTab() {
  const [dataPointsText, setDataPointsText] = useState(
    "10, 0.002\n50, 0.015\n100, 0.035\n250, 0.12\n500, 0.40\n1000, 1.20\n2000, 4.50\n5000, 28.0"
  );
  const [result, setResult] = useState<CurveFitResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const PRESETS = [
    { label: "O(n log n) Profile", data: "10, 0.03\n50, 0.28\n100, 0.66\n500, 4.5\n1000, 10\n5000, 62\n10000, 133" },
    { label: "O(n²) Quadratic", data: "10, 0.01\n50, 0.25\n100, 1.0\n200, 4.0\n500, 25\n1000, 100\n2000, 400" },
    { label: "O(n) Linear", data: "100, 0.1\n500, 0.5\n1000, 1.0\n5000, 5.0\n10000, 10.0\n50000, 50.0" },
    { label: "O(log n) Logarithmic", data: "10, 0.03\n100, 0.07\n1000, 0.1\n10000, 0.13\n100000, 0.17\n1000000, 0.2" },
  ];

  const handleFit = async () => {
    setLoading(true);
    setError(null);
    try {
      const points = dataPointsText
        .trim()
        .split("\n")
        .filter((line) => line.trim())
        .map((line) => {
          const parts = line.split(",").map((s) => parseFloat(s.trim()));
          return { n: parts[0], time_ms: parts[1] };
        })
        .filter((p) => !isNaN(p.n) && !isNaN(p.time_ms));

      const res = await api.fitBigOCurve({ data_points: points });
      setResult(res);
    } catch (err: any) {
      setError(err.message || "Curve fitting failed.");
    } finally {
      setLoading(false);
    }
  };

  const MODEL_COLORS = ["#0ea5e9", "#8b5cf6", "#10b981", "#f59e0b", "#ec4899", "#6366f1", "#14b8a6"];

  // Merge chart data by n
  const mergedChart: Record<number, any> = {};
  if (result) {
    result.data_points?.forEach((d: any) => {
      if (!mergedChart[d.n]) mergedChart[d.n] = { n: d.n };
      mergedChart[d.n].measured = d.time_ms ?? d.measured;
    });
    result.fits?.slice(0, 4).forEach((fit) => {
      fit.predicted_curve?.forEach((pt: any) => {
        if (!mergedChart[pt.n]) mergedChart[pt.n] = { n: pt.n };
        mergedChart[pt.n][fit.complexity] = pt.predicted_time_ms ?? pt.pred;
      });
    });
  }
  const mergedChartData = Object.values(mergedChart).sort((a: any, b: any) => a.n - b.n);

  return (
    <div className="space-y-5">
      {/* Notice on Empirical Curve Fitting vs Theoretical Proof */}
      <div className="p-3.5 rounded-lg bg-amber-500/10 border border-amber-500/20 text-amber-300 font-mono text-xs flex items-start gap-2">
        <HelpCircle className="w-4 h-4 flex-shrink-0 mt-0.5" />
        <p className="leading-relaxed">
          <strong>Important Methodology Note:</strong> Empirical curve fitting evaluates goodness of fit (R², RMSE, AIC) against measured benchmark execution samples. While useful for empirical profiling, empirical curve fitting does NOT prove theoretical Big-O complexity bounds.
        </p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-5">
        {/* Input Area */}
        <div className="lg:col-span-2">
          <Card headerTag="Empirical Telemetry Samples (N, Time_ms)">
            <div className="space-y-3">
              <div className="flex flex-wrap gap-2">
                {PRESETS.map((p) => (
                  <button
                    key={p.label}
                    onClick={() => setDataPointsText(p.data)}
                    className="px-2.5 py-1.5 rounded-lg bg-slate-900/80 border border-slate-800 text-xs font-mono text-slate-300 hover:text-white hover:border-slate-700 transition-colors"
                  >
                    {p.label}
                  </button>
                ))}
              </div>

              <textarea
                value={dataPointsText}
                onChange={(e) => setDataPointsText(e.target.value)}
                rows={7}
                placeholder="Enter data points formatted as: N, time_ms (one per line)"
                className="w-full px-3 py-2 rounded-lg bg-slate-900 border border-slate-800 text-xs font-mono text-white placeholder-slate-500 focus:outline-none focus:border-sky-500 resize-none"
              />

              <Button
                variant="primary"
                onClick={handleFit}
                disabled={loading}
                loading={loading}
                icon={<BarChart2 className="w-4 h-4" />}
                className="w-full justify-center"
              >
                {loading ? "Fitting Complexity Models..." : "Fit Big-O Asymptotic Curve"}
              </Button>
            </div>
          </Card>
        </div>

        {/* Info Panel */}
        <div>
          <Card headerTag="Regression Methodology">
            <div className="space-y-3 text-xs font-sans text-slate-300">
              <p className="text-slate-400 text-[12px] leading-relaxed">
                Fits empirical <span className="font-mono text-sky-400">(N, time)</span> data points against 7 canonical Big-O models using weighted least-squares regression.
              </p>
              <div className="space-y-2 pt-1 font-mono text-[11px]">
                <div className="flex items-center justify-between p-2 rounded-lg bg-slate-900/80 border border-slate-800">
                  <span className="text-sky-400 font-semibold">R² Score</span>
                  <span className="text-slate-400">Goodness of fit (&rarr; 1.0)</span>
                </div>
                <div className="flex items-center justify-between p-2 rounded-lg bg-slate-900/80 border border-slate-800">
                  <span className="text-purple-400 font-semibold">RMSE</span>
                  <span className="text-slate-400">Root mean squared error</span>
                </div>
                <div className="flex items-center justify-between p-2 rounded-lg bg-slate-900/80 border border-slate-800">
                  <span className="text-amber-400 font-semibold">AIC</span>
                  <span className="text-slate-400">Akaike Information Criterion</span>
                </div>
              </div>
            </div>
          </Card>
        </div>
      </div>

      {error && (
        <div className="p-4 rounded-xl bg-rose-500/10 border border-rose-500/30 text-rose-300 font-mono text-xs">
          {error}
        </div>
      )}

      {/* Results */}
      {result && (
        <div className="space-y-5">
          {/* Best Fit Banner */}
          <div className="p-5 rounded-xl bg-[#0e131f] border border-slate-800 flex flex-col sm:flex-row sm:items-center justify-between gap-4">
            <div>
              <div className="flex items-center gap-2 text-xs font-mono text-sky-400 mb-1">
                <Sparkles className="w-4 h-4" />
                <span>Optimal Asymptotic Fit</span>
              </div>
              <div className="text-2xl font-semibold text-white font-mono">
                {result.best_fit_complexity}
              </div>
              <div className="text-xs text-slate-400 font-mono mt-0.5">
                {result.best_fit_name} &bull; R² = {result.best_r_squared} &bull; {result.sample_count} samples
              </div>
            </div>

            <Badge variant="success" mono size="md">
              R² = {result.best_r_squared}
            </Badge>
          </div>

          {/* Overlay LineChart */}
          {mergedChartData.length > 0 && (
            <Card headerTag="Theoretical vs Empirical Scaling Curves">
              <div className="h-80 w-full pt-3">
                <ResponsiveContainer width="100%" height="100%">
                  <LineChart data={mergedChartData} margin={{ top: 10, right: 15, left: -10, bottom: 20 }}>
                    <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" vertical={false} />
                    <XAxis
                      dataKey="n"
                      stroke="#64748b"
                      fontSize={11}
                      fontFamily="var(--font-mono)"
                      label={{ value: "Input Size (N)", position: "insideBottom", offset: -10, fill: "#64748b", fontSize: 11 }}
                    />
                    <YAxis
                      stroke="#64748b"
                      fontSize={11}
                      fontFamily="var(--font-mono)"
                      unit=" ms"
                    />
                    <Tooltip
                      contentStyle={{
                        backgroundColor: "#0e131f",
                        borderColor: "#1e293b",
                        borderRadius: "8px",
                        fontFamily: "var(--font-mono)",
                        fontSize: "11px",
                        color: "#f8fafc",
                      }}
                    />
                    <Legend wrapperStyle={{ fontSize: "11px", fontFamily: "var(--font-mono)", paddingTop: "15px" }} />
                    <Line
                      type="monotone"
                      dataKey="measured"
                      stroke="#f8fafc"
                      strokeWidth={2}
                      dot={{ fill: "#f8fafc", r: 4 }}
                      name="Measured Data"
                    />
                    {result.fits?.slice(0, 4).map((fit, i) => (
                      <Line
                        key={fit.complexity}
                        type="monotone"
                        dataKey={fit.complexity}
                        stroke={MODEL_COLORS[i % MODEL_COLORS.length]}
                        strokeWidth={1.5}
                        strokeDasharray="4 4"
                        dot={false}
                        name={`${fit.complexity} (R²=${fit.r_squared})`}
                      />
                    ))}
                  </LineChart>
                </ResponsiveContainer>
              </div>
            </Card>
          )}

          {/* Model Rankings Table */}
          <Card headerTag="Asymptotic Model Rankings">
            <div className="overflow-x-auto -mx-5 -mb-5">
              <table className="w-full text-left font-mono text-xs">
                <thead className="border-b border-slate-800 bg-[#141b2d] text-[10px] text-slate-400 uppercase tracking-wider">
                  <tr>
                    <th className="py-3 px-4">Rank</th>
                    <th className="py-3 px-4">Complexity</th>
                    <th className="py-3 px-4">Model Name</th>
                    <th className="py-3 px-4 text-sky-400">R² Score</th>
                    <th className="py-3 px-4 text-purple-400">RMSE</th>
                    <th className="py-3 px-4 text-amber-400">AIC</th>
                    <th className="py-3 px-4">Coefficient</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-slate-800/60 text-slate-300">
                  {result.fits?.map((fit, i) => (
                    <tr
                      key={fit.complexity}
                      className={`hover:bg-slate-900/40 transition-colors ${
                        i === 0 ? "bg-sky-500/5 font-semibold text-white" : ""
                      }`}
                    >
                      <td className="py-3 px-4">
                        {i === 0 ? (
                          <Badge variant="success" mono size="sm">#1 Best Fit</Badge>
                        ) : (
                          `#${i + 1}`
                        )}
                      </td>
                      <td className="py-3 px-4 font-semibold text-white">{fit.complexity}</td>
                      <td className="py-3 px-4 text-slate-300">{fit.name}</td>
                      <td className="py-3 px-4 text-sky-300 font-semibold tabular-nums">{fit.r_squared}</td>
                      <td className="py-3 px-4 text-purple-300 tabular-nums">{fit.rmse}</td>
                      <td className="py-3 px-4 text-amber-300 tabular-nums">{fit.aic}</td>
                      <td className="py-3 px-4 text-slate-400 tabular-nums">{fit.coefficient}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </Card>
        </div>
      )}
    </div>
  );
}

// ─────────────── Tab 4: Asymptotic Hierarchy Comparator ───────────────
function AsymptoticComparatorTab() {
  const [hierarchy, setHierarchy] = useState<any[]>([]);
  const [loadingHierarchy, setLoadingHierarchy] = useState(false);
  const [compA, setCompA] = useState("O(n log n)");
  const [compB, setCompB] = useState("O(n^2)");
  const [compResult, setCompResult] = useState<any | null>(null);
  const [loadingCompare, setLoadingCompare] = useState(false);

  const COMPLEXITY_OPTIONS = [
    "O(1)", "O(log n)", "O(sqrt(n))", "O(n)", "O(n log n)",
    "O(n^2)", "O(n^3)", "O(2^n)", "O(n!)"
  ];

  const handleLoadHierarchy = async () => {
    setLoadingHierarchy(true);
    try {
      const res = await api.getComplexityHierarchy();
      setHierarchy(res);
    } catch (err) {
      console.error(err);
    } finally {
      setLoadingHierarchy(false);
    }
  };

  const handleCompare = async () => {
    setLoadingCompare(true);
    try {
      const data = await api.compareComplexities({ complexity_a: compA, complexity_b: compB });
      setCompResult(data);
    } catch (err) {
      console.error(err);
    } finally {
      setLoadingCompare(false);
    }
  };

  return (
    <div className="space-y-5">
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-5">
        {/* Canonical Growth Hierarchy */}
        <Card headerTag="Canonical Asymptotic Hierarchy">
          <div className="space-y-3">
            {hierarchy.length === 0 ? (
              <Button
                variant="secondary"
                onClick={handleLoadHierarchy}
                disabled={loadingHierarchy}
                loading={loadingHierarchy}
                icon={<Layers className="w-4 h-4" />}
                className="w-full justify-center"
              >
                {loadingHierarchy ? "Fetching Hierarchy..." : "Load Asymptotic Hierarchy"}
              </Button>
            ) : (
              <div className="space-y-2">
                {hierarchy.map((item: any) => (
                  <div
                    key={item.complexity}
                    className="flex items-center gap-3 p-2.5 rounded-lg bg-slate-900/60 border border-slate-800 hover:border-slate-700 transition-colors"
                  >
                    <span className="w-7 h-7 rounded-lg bg-[#080b11] border border-slate-800 flex items-center justify-center text-xs font-mono font-semibold text-slate-400">
                      {item.rank}
                    </span>
                    <div className="flex-1">
                      <span className="font-semibold font-mono text-sm text-sky-400">
                        {item.complexity}
                      </span>
                      <div className="text-[11px] text-slate-400">{item.description}</div>
                    </div>
                    <ArrowRight className="w-3.5 h-3.5 text-slate-600" />
                  </div>
                ))}
                <div className="text-[11px] text-slate-400 font-mono text-center pt-2">
                  Strictly monotonically increasing asymptotic upper bounds
                </div>
              </div>
            )}
          </div>
        </Card>

        {/* Pairwise Comparator */}
        <Card headerTag="Pairwise Asymptotic Comparator">
          <div className="space-y-4">
            <div className="grid grid-cols-2 gap-3">
              <div>
                <label className="text-[11px] font-mono text-slate-400 block mb-1">
                  Complexity Class A
                </label>
                <select
                  value={compA}
                  onChange={(e) => setCompA(e.target.value)}
                  className="w-full px-3 py-1.5 rounded-lg bg-slate-900 border border-slate-800 text-xs font-mono text-white focus:outline-none focus:border-sky-500"
                >
                  {COMPLEXITY_OPTIONS.map((c) => (
                    <option key={c} value={c}>
                      {c}
                    </option>
                  ))}
                </select>
              </div>
              <div>
                <label className="text-[11px] font-mono text-slate-400 block mb-1">
                  Complexity Class B
                </label>
                <select
                  value={compB}
                  onChange={(e) => setCompB(e.target.value)}
                  className="w-full px-3 py-1.5 rounded-lg bg-slate-900 border border-slate-800 text-xs font-mono text-white focus:outline-none focus:border-sky-500"
                >
                  {COMPLEXITY_OPTIONS.map((c) => (
                    <option key={c} value={c}>
                      {c}
                    </option>
                  ))}
                </select>
              </div>
            </div>

            <Button
              variant="primary"
              onClick={handleCompare}
              disabled={loadingCompare}
              loading={loadingCompare}
              icon={<Scale className="w-4 h-4" />}
              className="w-full justify-center"
            >
              {loadingCompare ? "Comparing..." : "Compare Growth Rates"}
            </Button>

            {compResult && (
              <div className="p-4 rounded-xl bg-slate-900/90 border border-slate-800 space-y-3">
                <div className="text-center">
                  <div className="text-base sm:text-lg font-semibold font-mono text-white mb-1">
                    {compResult.complexity_a}
                    <span
                      className={`mx-3 text-xl font-bold ${
                        compResult.asymptotic_symbol === "<"
                          ? "text-emerald-400"
                          : compResult.asymptotic_symbol === ">"
                          ? "text-rose-400"
                          : "text-amber-400"
                      }`}
                    >
                      {compResult.asymptotic_symbol}
                    </span>
                    {compResult.complexity_b}
                  </div>
                  <div className="text-xs text-slate-400 font-mono">{compResult.relation}</div>
                </div>
                <div className="grid grid-cols-2 gap-2.5 pt-2 border-t border-slate-800 text-xs">
                  <div className="p-2.5 rounded-lg bg-[#080b11] border border-slate-800">
                    <div className="text-[10px] font-mono text-slate-400">Class A: {compResult.complexity_a}</div>
                    <div className="text-slate-300 text-[11px] mt-0.5">{compResult.description_a}</div>
                  </div>
                  <div className="p-2.5 rounded-lg bg-[#080b11] border border-slate-800">
                    <div className="text-[10px] font-mono text-slate-400">Class B: {compResult.complexity_b}</div>
                    <div className="text-slate-300 text-[11px] mt-0.5">{compResult.description_b}</div>
                  </div>
                </div>
              </div>
            )}
          </div>
        </Card>
      </div>
    </div>
  );
}

// ─────────────── Main Page ───────────────
export default function ComplexityPage() {
  const [searchParams, setSearchParams] = useSearchParams();
  const initialTab = searchParams.get("tab") || "comparisons";
  const initialProblem = searchParams.get("problem");
  const initialAlgorithm = searchParams.get("algorithm") || searchParams.get("algo");

  const [activeTab, setActiveTab] = useState<string>(initialTab);

  useEffect(() => {
    const tab = searchParams.get("tab");
    if (tab && tab !== activeTab) {
      setActiveTab(tab);
    }
  }, [searchParams]);

  const handleTabChange = (key: string) => {
    setActiveTab(key);
    const newParams: Record<string, string> = { tab: key };
    if (initialProblem) newParams.problem = initialProblem;
    if (initialAlgorithm) newParams.algorithm = initialAlgorithm;
    setSearchParams(newParams);
  };

  const tabItems = [
    { key: "comparisons", label: "Algorithm Complexity & Problem Comparisons", icon: <Layers className="w-4 h-4" /> },
    { key: "master", label: "Master Theorem Solver", icon: <Sigma className="w-4 h-4" /> },
    { key: "curve", label: "Empirical Big-O Curve Fit", icon: <BarChart2 className="w-4 h-4" /> },
    { key: "compare", label: "Asymptotic Comparator", icon: <Scale className="w-4 h-4" /> },
  ];

  return (
    <Layout>
      <div className="space-y-6 animate-in fade-in duration-200">
        {/* Page Header */}
        <PageHeader
          breadcrumb="Theoretical & Empirical Analysis"
          title="Asymptotic Complexity Analyzer"
          description="Examine authoritative theoretical complexities, compare compatible algorithms for canonical DAA problems, solve Master Theorem recurrences, and analyze asymptotic growth hierarchies."
        />

        {/* Tab Navigation */}
        <Tabs
          tabs={tabItems}
          activeKey={activeTab}
          onChange={handleTabChange}
        />

        {/* Tab Content */}
        {activeTab === "comparisons" && (
          <CompatibleComparisonsTab
            initialProblem={initialProblem}
            initialAlgorithm={initialAlgorithm}
          />
        )}
        {activeTab === "master" && <MasterTheoremTab />}
        {activeTab === "curve" && <CurveFittingTab />}
        {activeTab === "compare" && <AsymptoticComparatorTab />}
      </div>
    </Layout>
  );
}
