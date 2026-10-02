import { useState, useEffect, useMemo } from "react";
import { useSearchParams, Link } from "react-router-dom";
import {
  Play,
  BarChart3,
  HardDrive,
  Award,
  CheckSquare,
  Square,
  AlertTriangle,
  Layers,
  GraduationCap,
  Sparkles,
  Cpu,
  RefreshCw,
  Activity,
} from "lucide-react";
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  Cell,
} from "recharts";
import { Layout } from "../components/layout/Layout";
import { PageHeader } from "../components/layout/PageHeader";
import { Card } from "../components/common/Card";
import { Button } from "../components/common/Button";
import { LoadingState } from "../components/common/LoadingState";
import { EmptyState } from "../components/common/EmptyState";
import { api } from "../services/api";
import type { Problem, ProblemDetailData, BenchmarkResponse, BenchmarkAlgorithmResult } from "../types";
import { StatisticalDetailsModal } from "../components/benchmark/StatisticalDetailsModal";

const PALETTE = [
  "#0ea5e9", // Sky
  "#8b5cf6", // Violet
  "#10b981", // Emerald
  "#f59e0b", // Amber
  "#06b6d4", // Cyan
  "#ec4899", // Pink
  "#6366f1", // Indigo
  "#14b8a6", // Teal
];

// Problem-appropriate dimension specifications and safe size presets
interface ProblemDimensionConfig {
  label: string;
  unit: string;
  presets: number[];
  defaultSize: number;
  maxSafeSize: number;
  description: string;
}

const PROBLEM_CONFIGS: Record<string, ProblemDimensionConfig> = {
  "0-1-knapsack-problem": {
    label: "Items Count (N)",
    unit: "items",
    presets: [4, 8, 12, 16, 20],
    defaultSize: 8,
    maxSafeSize: 25,
    description: "Number of discrete items with weights and profits. Exponential bound for Branch & Bound.",
  },
  "traveling-salesman-problem": {
    label: "Cities Count (N)",
    unit: "cities",
    presets: [4, 5, 6, 7, 8],
    defaultSize: 5,
    maxSafeSize: 14,
    description: "Number of graph vertices in exact TSP tour. Exponential O(n² 2ⁿ) search space.",
  },
  "minimum-spanning-tree": {
    label: "Graph Vertices (|V|)",
    unit: "vertices",
    presets: [6, 12, 25, 50, 100],
    defaultSize: 15,
    maxSafeSize: 500,
    description: "Number of vertices in connected undirected graph for Kruskal and Prim comparison.",
  },
  "single-source-shortest-path": {
    label: "Graph Vertices (|V|)",
    unit: "vertices",
    presets: [6, 15, 30, 60, 120],
    defaultSize: 15,
    maxSafeSize: 300,
    description: "Number of vertices for Dijkstra non-negative relaxation and Bellman-Ford paths.",
  },
  "all-pairs-shortest-path": {
    label: "Matrix Dimension (|V|)",
    unit: "vertices",
    presets: [4, 8, 16, 32],
    defaultSize: 8,
    maxSafeSize: 64,
    description: "Vertex count for O(V³) Floyd-Warshall dynamic programming distance relaxation.",
  },
  "n-queens-problem": {
    label: "Board Dimension (N)",
    unit: "queens",
    presets: [4, 6, 8, 10, 12],
    defaultSize: 8,
    maxSafeSize: 14,
    description: "N x N chessboard dimension. Exponential backtracking search tree.",
  },
  "subset-sum-problem": {
    label: "Numbers Count (N)",
    unit: "elements",
    presets: [6, 10, 14, 18, 22],
    defaultSize: 10,
    maxSafeSize: 25,
    description: "Integer set size for exact state-space subset sum matching.",
  },
  "hamiltonian-cycle-problem": {
    label: "Graph Vertices (|V|)",
    unit: "vertices",
    presets: [4, 5, 6, 7, 8],
    defaultSize: 5,
    maxSafeSize: 10,
    description: "Vertex count for NP-complete Hamiltonian cycle backtracking.",
  },
  "matrix-multiplication-problem": {
    label: "Matrix Dimension (N x N)",
    unit: "dim",
    presets: [2, 4, 8, 16],
    defaultSize: 4,
    maxSafeSize: 32,
    description: "Power-of-two matrix size for Strassen sub-cubic block decomposition.",
  },
  "max-min-problem": {
    label: "Array Size (N)",
    unit: "numbers",
    presets: [10, 50, 200, 1000, 5000],
    defaultSize: 100,
    maxSafeSize: 50000,
    description: "Number of elements for 3n/2 - 2 divide and conquer min-max extraction.",
  },
  "fractional-knapsack-problem": {
    label: "Items Count (N)",
    unit: "items",
    presets: [10, 50, 200, 1000, 5000],
    defaultSize: 50,
    maxSafeSize: 20000,
    description: "Item count for density-sorted greedy selection.",
  },
  "job-sequencing-problem": {
    label: "Jobs Count (N)",
    unit: "jobs",
    presets: [5, 10, 20, 50, 100],
    defaultSize: 15,
    maxSafeSize: 500,
    description: "Job count for profit-sorted deadline scheduling.",
  },
  "optimal-merge-patterns-problem": {
    label: "Files Count (N)",
    unit: "files",
    presets: [5, 15, 30, 60, 100],
    defaultSize: 20,
    maxSafeSize: 1000,
    description: "File list size for 2-way min-heap merge tree construction.",
  },
  "optimal-storage-tapes-problem": {
    label: "Programs Count (N)",
    unit: "programs",
    presets: [5, 15, 30, 60, 100],
    defaultSize: 20,
    maxSafeSize: 1000,
    description: "Program count for Mean Retrieval Time (MRT) minimization.",
  },
  "defective-chessboard-problem": {
    label: "Board Dimension (2^k x 2^k)",
    unit: "dim",
    presets: [2, 4, 8, 16],
    defaultSize: 4,
    maxSafeSize: 32,
    description: "Tromino tiling on 2^k x 2^k board with 1 defect square.",
  },
  "multistage-graph-problem": {
    label: "Graph Vertices (|V|)",
    unit: "vertices",
    presets: [4, 8, 12, 16],
    defaultSize: 8,
    maxSafeSize: 64,
    description: "Number of vertices in k-stage partitioned directed graph.",
  },
  "optimal-bst-problem": {
    label: "Keys Count (N)",
    unit: "keys",
    presets: [4, 8, 16, 32],
    defaultSize: 8,
    maxSafeSize: 64,
    description: "Number of keys with access probabilities for O(n^3) interval DP.",
  },
  "reliability-design-problem": {
    label: "System Stages (N)",
    unit: "stages",
    presets: [3, 5, 8, 10],
    defaultSize: 3,
    maxSafeSize: 20,
    description: "Number of stages for device redundancy optimization under budget.",
  },
};

const DEFAULT_CONFIG: ProblemDimensionConfig = {
  label: "Problem Size (N)",
  unit: "elements",
  presets: [5, 10, 20, 50],
  defaultSize: 10,
  maxSafeSize: 1000,
  description: "Standard algorithmic problem size.",
};

export default function BenchmarkArenaPage() {
  const [searchParams, setSearchParams] = useSearchParams();
  const queryProblem = searchParams.get("problem");
  const queryAlgos = searchParams.get("algos")?.split(",").filter(Boolean);

  const [allProblems, setAllProblems] = useState<Problem[]>([]);
  const [problemDetailsMap, setProblemDetailsMap] = useState<Record<string, ProblemDetailData>>({});
  const [curriculumSlugs, setCurriculumSlugs] = useState<Set<string>>(new Set());

  const [selectedProblemSlug, setSelectedProblemSlug] = useState<string>("0-1-knapsack-problem");
  const [selectedSlugs, setSelectedSlugs] = useState<string[]>([]);
  const [inputDimensionSize, setInputDimensionSize] = useState<number>(8);
  const [repetitions, setRepetitions] = useState<number>(5);
  const [warmupRuns, setWarmupRuns] = useState<number>(2);

  const [benchmarkResult, setBenchmarkResult] = useState<BenchmarkResponse | null>(null);
  const [selectedDetailResult, setSelectedDetailResult] = useState<BenchmarkAlgorithmResult | null>(null);
  const [isDetailsModalOpen, setIsDetailsModalOpen] = useState<boolean>(false);
  const [activeChartTab, setActiveChartTab] = useState<"time" | "memory">("time");
  const [loading, setLoading] = useState(true);
  const [benchmarking, setBenchmarking] = useState(false);
  const [error, setError] = useState<string | null>(null);

  // 1. Initial Data Fetching
  useEffect(() => {
    Promise.all([
      api.getProblems(),
      api.getApprovedCurriculumSlugs().catch(() => [] as string[]),
    ])
      .then(async ([problems, approvedSlugs]) => {
        setAllProblems(problems);
        setCurriculumSlugs(new Set(approvedSlugs));

        // Fetch problem details for compatible algorithm mappings
        const pMap: Record<string, ProblemDetailData> = {};
        await Promise.all(
          problems.map(async (p) => {
            try {
              const detail = await api.getProblemDetail(p.slug);
              pMap[p.slug] = detail;
            } catch {
              // ignore
            }
          })
        );
        setProblemDetailsMap(pMap);

        // Resolve initial problem & algorithms from URL or defaults
        let initialProblem = "0-1-knapsack-problem";
        if (queryProblem && pMap[queryProblem]) {
          initialProblem = queryProblem;
        } else if (queryAlgos && queryAlgos.length > 0) {
          for (const [pSlug, pDetail] of Object.entries(pMap)) {
            const hasMatch = pDetail.applicable_algorithms?.some((a) =>
              queryAlgos.includes(a.slug)
            );
            if (hasMatch) {
              initialProblem = pSlug;
              break;
            }
          }
        }

        setSelectedProblemSlug(initialProblem);

        const targetDetail = pMap[initialProblem];
        const compatible = targetDetail?.applicable_algorithms || [];
        if (queryAlgos && queryAlgos.length > 0) {
          const validQueryAlgos = compatible
            .map((a) => a.slug)
            .filter((s) => queryAlgos.includes(s));
          setSelectedSlugs(validQueryAlgos.length > 0 ? validQueryAlgos : compatible.map((a) => a.slug));
        } else {
          setSelectedSlugs(compatible.map((a) => a.slug));
        }

        const config = PROBLEM_CONFIGS[initialProblem] || DEFAULT_CONFIG;
        setInputDimensionSize(config.defaultSize);
      })
      .catch((err) => {
        console.error("Failed to initialize benchmark arena:", err);
        setError("Failed to load canonical problems.");
      })
      .finally(() => setLoading(false));
  }, []);

  // 2. When selected problem changes, update compatible algorithms & input dimension defaults
  const handleProblemChange = (newProblemSlug: string) => {
    setSelectedProblemSlug(newProblemSlug);
    setBenchmarkResult(null);
    setSelectedDetailResult(null);
    setIsDetailsModalOpen(false);
    setError(null);

    const detail = problemDetailsMap[newProblemSlug];
    const compatible = detail?.applicable_algorithms || [];
    setSelectedSlugs(compatible.map((a) => a.slug));

    const config = PROBLEM_CONFIGS[newProblemSlug] || DEFAULT_CONFIG;
    setInputDimensionSize(config.defaultSize);

    setSearchParams({ problem: newProblemSlug, algos: compatible.map((a) => a.slug).join(",") });
  };

  const currentProblemDetail = problemDetailsMap[selectedProblemSlug];
  const compatibleAlgorithms = currentProblemDetail?.applicable_algorithms || [];
  const currentConfig = PROBLEM_CONFIGS[selectedProblemSlug] || DEFAULT_CONFIG;

  const getProblemDisplayName = (p: Problem) => {
    if (p.slug === "matrix-multiplication-problem") {
      return "Strassen's Matrix Multiplication";
    }
    return p.name || p.title || p.slug;
  };

  const currentProblemName =
    selectedProblemSlug === "matrix-multiplication-problem"
      ? "Strassen's Matrix Multiplication"
      : currentProblemDetail?.name || selectedProblemSlug;

  const handleToggleAlgo = (slug: string) => {
    if (selectedSlugs.includes(slug)) {
      if (selectedSlugs.length > 1) {
        const next = selectedSlugs.filter((s) => s !== slug);
        setSelectedSlugs(next);
        setSearchParams({ problem: selectedProblemSlug, algos: next.join(",") });
      }
    } else {
      const next = [...selectedSlugs, slug];
      setSelectedSlugs(next);
      setSearchParams({ problem: selectedProblemSlug, algos: next.join(",") });
    }
  };

  const handleSelectAll = () => {
    const all = compatibleAlgorithms.map((a) => a.slug);
    setSelectedSlugs(all);
    setSearchParams({ problem: selectedProblemSlug, algos: all.join(",") });
  };

  // 3. Run Universal Benchmark
  const handleRunBenchmark = async () => {
    if (selectedSlugs.length === 0) return;
    setBenchmarking(true);
    setError(null);

    try {
      const dataset = await api.generateDataset({
        problem_type: selectedProblemSlug,
        size: inputDimensionSize,
      });

      const res = await api.runComparisonBenchmark({
        algorithm_slugs: selectedSlugs,
        input_data: dataset.data_payload,
        repetitions: repetitions,
        warmup_runs: warmupRuns,
        size: inputDimensionSize,
      });

      setBenchmarkResult(res);
    } catch (err: any) {
      console.error("Benchmark error:", err);
      setError(err.message || "Benchmark execution failed.");
    } finally {
      setBenchmarking(false);
    }
  };

  // Prepare chart data
  const chartData = useMemo(() => {
    return (
      benchmarkResult?.results?.map((r) => ({
        name: r.algorithm_name || r.algorithm_slug,
        slug: r.algorithm_slug,
        mean_ms: Number((r.time_stats?.mean_ms ?? (r as any).execution_time_ms ?? 0).toFixed(4)),
        median_ms: Number((r.time_stats?.median_ms ?? 0).toFixed(4)),
        p95_ms: Number((r.time_stats?.p95_ms ?? 0).toFixed(4)),
        min_ms: Number((r.time_stats?.min_ms ?? 0).toFixed(4)),
        max_ms: Number((r.time_stats?.max_ms ?? 0).toFixed(4)),
        std_dev_ms: Number((r.time_stats?.std_dev_ms ?? 0).toFixed(4)),
        peak_kb: Number((r.memory_stats?.peak_kb ?? 0).toFixed(2)),
        allocated_kb: Number((r.memory_stats?.allocated_kb ?? 0).toFixed(2)),
        operations: (r as any).metrics?.operations ?? 0,
        comparisons: (r as any).metrics?.comparisons ?? 0,
        swaps: (r as any).metrics?.swaps ?? 0,
      })) || []
    );
  }, [benchmarkResult]);

  return (
    <Layout>
      <div className="space-y-6 animate-in fade-in duration-200">
        {/* Page Header */}
        <PageHeader
          breadcrumb="Empirical Laboratory"
          title="Universal Benchmark Arena"
          description="Conduct hardware-isolated, non-simulated comparative benchmarks across canonical DAA problem paradigms. Evaluate execution durations, memory allocations, operation counts, and asymptotic scaling."
          actions={
            <div className="flex items-center gap-2.5">
              <Link to="/problems">
                <Button variant="secondary" size="sm" icon={<Layers className="w-3.5 h-3.5" />}>
                  Problems Hub
                </Button>
              </Link>
              <Link to="/curriculum">
                <Button variant="ghost" size="sm" icon={<GraduationCap className="w-3.5 h-3.5" />}>
                  Curriculum Hub
                </Button>
              </Link>
            </div>
          }
        />

        {loading ? (
          <div className="py-24">
            <LoadingState message="Loading benchmark laboratory..." />
          </div>
        ) : (
          <div className="space-y-6">
            {/* ============================================================= */}
            {/* 1. BENCHMARK CONFIGURATION MASTER PANEL                       */}
            {/* ============================================================= */}
            <div className="space-y-4">
              {/* Step 1: Target Problem Selection */}
              <Card
                className="p-5 border-slate-800 bg-[#0e131f]"
                headerTag="1. Target Problem Selection"
                headerRight={
                  <div className="flex items-center gap-2 font-mono text-[11px] text-slate-400">
                    <span className="text-sky-400 font-semibold">{currentProblemName}</span>
                    <span>•</span>
                    <span>{allProblems.length} Canonical Problems</span>
                  </div>
                }
              >
                <div className="space-y-3">
                  <div className="flex items-center justify-between">
                    <span className="text-xs font-mono text-slate-400">
                      Select a problem definition to benchmark compatible algorithm implementations:
                    </span>
                    <span className="text-[11px] font-mono text-slate-400 hidden sm:inline">
                      {currentProblemDetail?.category || "Category"} • {currentProblemDetail?.paradigm || "Paradigm"}
                    </span>
                  </div>

                  <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-2.5">
                    {allProblems.map((p) => {
                      const active = selectedProblemSlug === p.slug;
                      const displayName = getProblemDisplayName(p);
                      const algoCount = problemDetailsMap[p.slug]?.applicable_algorithms?.length || 1;

                      return (
                        <button
                          key={p.slug}
                          onClick={() => handleProblemChange(p.slug)}
                          className={`group p-3 rounded-lg text-left transition-all flex flex-col justify-between min-h-[72px] border ${
                            active
                              ? "bg-sky-500/10 border-sky-500/60 text-white ring-1 ring-sky-500/30 shadow-sm"
                              : "bg-slate-900/50 border-slate-800 text-slate-300 hover:border-slate-700 hover:bg-slate-800/40 hover:text-white"
                          }`}
                        >
                          <div className="flex items-center justify-between gap-1.5 mb-1.5 w-full">
                            <span className={`text-xs font-semibold truncate ${active ? "text-sky-300" : "text-white"}`}>
                              {displayName}
                            </span>
                            {active && <span className="w-1.5 h-1.5 rounded-full bg-sky-400 flex-shrink-0" />}
                          </div>

                          <div className="text-[10px] font-mono text-slate-400 flex items-center justify-between w-full">
                            <span className="truncate pr-1">{p.category}</span>
                            <span
                              className={`px-1.5 py-0.5 rounded text-[9px] font-mono font-medium flex-shrink-0 ${
                                active
                                  ? "bg-sky-500/20 text-sky-300 border border-sky-500/40"
                                  : "bg-slate-800/80 text-slate-400 border border-slate-700/60"
                              }`}
                            >
                              {algoCount} {algoCount === 1 ? "algo" : "algos"}
                            </span>
                          </div>
                        </button>
                      );
                    })}
                  </div>
                </div>
              </Card>

              {/* Step 2: Compatible Algorithms Multi-Select */}
              <Card
                className="p-5 border-slate-800 bg-[#0e131f]"
                headerTag="2. Compatible Candidate Implementations"
                headerRight={
                  <div className="flex items-center gap-3">
                    <span className="text-[11px] font-mono text-slate-400">
                      <strong className="text-white">{selectedSlugs.length}</strong> of {compatibleAlgorithms.length} Selected
                    </span>
                    <button
                      onClick={handleSelectAll}
                      className="text-[11px] font-mono text-sky-400 hover:text-sky-300 transition-colors font-semibold"
                    >
                      Select All Compatible
                    </button>
                  </div>
                }
              >
                <div className="space-y-3">
                  <div className="text-xs font-mono text-slate-400">
                    Toggle candidate implementations to benchmark simultaneously against the generated dataset:
                  </div>

                  <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-3">
                    {compatibleAlgorithms.map((algo) => {
                      const isSelected = selectedSlugs.includes(algo.slug);
                      const isCurriculum = curriculumSlugs.has(algo.slug);

                      return (
                        <div
                          key={algo.slug}
                          onClick={() => handleToggleAlgo(algo.slug)}
                          className={`p-3.5 rounded-lg border transition-all cursor-pointer flex items-start gap-3 select-none ${
                            isSelected
                              ? "bg-slate-900 border-sky-500/50 text-white ring-1 ring-sky-500/20 shadow-sm"
                              : "bg-slate-900/40 border-slate-800 text-slate-400 hover:border-slate-700 hover:text-slate-300"
                          }`}
                        >
                          <div className="mt-0.5 text-sky-400">
                            {isSelected ? (
                              <CheckSquare className="w-4 h-4" />
                            ) : (
                              <Square className="w-4 h-4 text-slate-600" />
                            )}
                          </div>

                          <div className="space-y-1.5 flex-1 min-w-0">
                            <div className="flex items-center justify-between gap-1.5">
                              <span className="font-semibold text-xs text-white truncate">{algo.name}</span>
                              {isCurriculum ? (
                                <span className="px-1.5 py-0.5 rounded text-[9px] font-mono bg-emerald-500/15 text-emerald-400 border border-emerald-500/30 flex-shrink-0">
                                  Curriculum
                                </span>
                              ) : (
                                <span className="px-1.5 py-0.5 rounded text-[9px] font-mono bg-slate-800 text-slate-400 border border-slate-700 flex-shrink-0">
                                  Supplementary
                                </span>
                              )}
                            </div>

                            <div className="text-[10px] font-mono text-slate-400 flex items-center justify-between">
                              <span className="truncate">{algo.paradigm}</span>
                              <span className="text-sky-400 font-semibold flex-shrink-0 pl-1">
                                {algo.time_complexity_average}
                              </span>
                            </div>
                          </div>
                        </div>
                      );
                    })}
                  </div>
                </div>
              </Card>

              {/* Lower Deck: Steps 3, 4, 5 (Input Configuration, Telemetry, and Execution CTA) */}
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                {/* Step 3: Input Configuration */}
                <Card
                  className="p-4 border-slate-800 bg-[#0e131f] flex flex-col justify-between"
                  headerTag="3. Input Configuration"
                >
                  <div className="space-y-3">
                    <div className="flex items-center justify-between">
                      <span className="text-xs font-mono text-slate-300 font-semibold">
                        {currentConfig.label}:
                      </span>
                      <span className="px-2 py-0.5 rounded text-xs font-mono font-bold text-sky-300 bg-sky-500/15 border border-sky-500/30">
                        {inputDimensionSize} {currentConfig.unit}
                      </span>
                    </div>

                    <div className="flex flex-wrap gap-1.5">
                      {currentConfig.presets.map((preset) => (
                        <button
                          key={preset}
                          onClick={() => setInputDimensionSize(preset)}
                          className={`px-2.5 py-1 rounded text-xs font-mono transition-colors ${
                            inputDimensionSize === preset
                              ? "bg-sky-500/20 text-sky-300 border border-sky-500/40 font-bold"
                              : "bg-slate-900 border border-slate-800 text-slate-400 hover:text-white hover:border-slate-700"
                          }`}
                        >
                          {preset}
                        </button>
                      ))}
                    </div>

                    <p className="text-[11px] text-slate-400 font-sans leading-relaxed pt-1">
                      {currentConfig.description}
                    </p>
                  </div>
                </Card>

                {/* Step 4: Telemetry Controls */}
                <Card
                  className="p-4 border-slate-800 bg-[#0e131f] flex flex-col justify-between"
                  headerTag="4. Telemetry Controls"
                >
                  <div className="space-y-3">
                    <div className="grid grid-cols-2 gap-2.5">
                      <div className="p-2.5 rounded-lg bg-slate-900 border border-slate-800 space-y-1">
                        <label className="text-[10px] font-mono text-slate-400 font-semibold block uppercase">
                          Iterations:
                        </label>
                        <select
                          value={repetitions}
                          onChange={(e) => setRepetitions(Number(e.target.value))}
                          className="w-full bg-slate-950 border border-slate-800 rounded px-2 py-1 text-xs font-mono text-white focus:outline-none focus:border-sky-500"
                        >
                          <option value={3}>3 runs</option>
                          <option value={5}>5 runs (std)</option>
                          <option value={10}>10 runs</option>
                          <option value={20}>20 runs (dense)</option>
                        </select>
                        <span className="text-[9px] text-slate-500 font-mono block">Statistical sampling</span>
                      </div>

                      <div className="p-2.5 rounded-lg bg-slate-900 border border-slate-800 space-y-1">
                        <label className="text-[10px] font-mono text-slate-400 font-semibold block uppercase">
                          Warmup:
                        </label>
                        <select
                          value={warmupRuns}
                          onChange={(e) => setWarmupRuns(Number(e.target.value))}
                          className="w-full bg-slate-950 border border-slate-800 rounded px-2 py-1 text-xs font-mono text-white focus:outline-none focus:border-sky-500"
                        >
                          <option value={1}>1 run</option>
                          <option value={2}>2 runs (std)</option>
                          <option value={5}>5 runs</option>
                        </select>
                        <span className="text-[9px] text-slate-500 font-mono block">JIT & cache priming</span>
                      </div>
                    </div>

                    <div className="p-2 rounded bg-slate-900/60 border border-slate-800 text-[10px] font-mono text-slate-400 flex items-center gap-2">
                      <Activity className="w-3.5 h-3.5 text-sky-400 flex-shrink-0" />
                      <span>Garbage collector isolated per run with nanosecond resolution.</span>
                    </div>
                  </div>
                </Card>

                {/* Step 5: Execution Action */}
                <Card
                  className="p-4 border-slate-800 bg-[#0e131f] flex flex-col justify-between"
                  headerTag="5. Execution Action"
                >
                  <div className="space-y-3 flex flex-col justify-between h-full">
                    <div className="space-y-1 text-xs font-mono text-slate-400">
                      <div className="flex items-center justify-between text-slate-300">
                        <span>Target Problem:</span>
                        <span className="text-white font-semibold truncate max-w-[140px]">
                          {currentProblemName}
                        </span>
                      </div>
                      <div className="flex items-center justify-between text-slate-300">
                        <span>Candidates:</span>
                        <span className="text-sky-400 font-semibold">
                          {selectedSlugs.length} selected
                        </span>
                      </div>
                    </div>

                    <div className="pt-2">
                      <Button
                        variant="primary"
                        size="lg"
                        icon={benchmarking ? <RefreshCw className="w-4 h-4 animate-spin" /> : <Play className="w-4 h-4" />}
                        onClick={handleRunBenchmark}
                        disabled={benchmarking || selectedSlugs.length === 0}
                        className="w-full h-11 text-xs font-mono font-bold tracking-wide"
                      >
                        {benchmarking
                          ? "Executing Suite..."
                          : `Run Benchmark (${selectedSlugs.length} Candidate${selectedSlugs.length > 1 ? "s" : ""})`}
                      </Button>
                    </div>
                  </div>
                </Card>
              </div>
            </div>

            {/* Error Display */}
            {error && (
              <div className="p-4 rounded-xl bg-amber-950/30 border border-amber-800/50 flex items-center gap-3 text-amber-300 text-xs font-mono">
                <AlertTriangle className="w-4 h-4 flex-shrink-0 text-amber-400" />
                <span>{error}</span>
              </div>
            )}

            {/* ============================================================= */}
            {/* 2. BENCHMARK RESULTS & TELEMETRY SECTION                      */}
            {/* ============================================================= */}
            {benchmarking ? (
              <div className="py-20">
                <LoadingState
                  message={`Executing hardware-isolated benchmark suite on ${selectedSlugs.length} algorithms with GC suspension and nanosecond precision...`}
                />
              </div>
            ) : benchmarkResult && chartData.length > 0 ? (
              <div className="space-y-6 animate-in fade-in duration-200">
                {/* Metric Highlights */}
                <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
                  <Card className="p-4 bg-slate-900/70 border-slate-800 space-y-1">
                    <span className="text-[11px] font-mono text-slate-400 uppercase tracking-wider block">
                      Fastest Implementation
                    </span>
                    <div className="text-base font-bold font-mono text-emerald-400 flex items-center gap-2">
                      <Award className="w-4 h-4 text-emerald-400 flex-shrink-0" />
                      <span className="truncate">{benchmarkResult.fastest_algorithm || "Not available"}</span>
                    </div>
                    <span className="text-[10px] text-slate-400 block">Lowest empirical mean duration</span>
                  </Card>

                  <Card className="p-4 bg-slate-900/70 border-slate-800 space-y-1">
                    <span className="text-[11px] font-mono text-slate-400 uppercase tracking-wider block">
                      Lowest Peak Memory
                    </span>
                    <div className="text-base font-bold font-mono text-purple-400 flex items-center gap-2">
                      <HardDrive className="w-4 h-4 text-purple-400 flex-shrink-0" />
                      <span className="truncate">{benchmarkResult.most_memory_efficient || "Not available"}</span>
                    </div>
                    <span className="text-[10px] text-slate-400 block">Tracemalloc peak resident KB</span>
                  </Card>

                  <Card className="p-4 bg-slate-900/70 border-slate-800 space-y-1">
                    <span className="text-[11px] font-mono text-slate-400 uppercase tracking-wider block">
                      Evaluated Runs
                    </span>
                    <div className="text-base font-bold font-mono text-sky-400 flex items-center gap-2">
                      <Cpu className="w-4 h-4 text-sky-400 flex-shrink-0" />
                      <span>
                        {benchmarkResult.successful_runs} / {benchmarkResult.total_candidates} Successful
                      </span>
                    </div>
                    <span className="text-[10px] text-slate-400 block">
                      {repetitions} iterations per candidate
                    </span>
                  </Card>
                </div>

                {/* Visual Chart Comparison */}
                <Card className="p-5 space-y-4 border-slate-800">
                  <div className="flex flex-wrap items-center justify-between gap-3 border-b border-slate-800 pb-3">
                    <div className="flex items-center gap-2">
                      <BarChart3 className="w-4 h-4 text-sky-400" />
                      <h3 className="font-semibold text-white text-sm tracking-tight">
                        Head-to-Head Telemetry Comparison ({currentProblemName})
                      </h3>
                    </div>

                    <div className="flex items-center gap-1 bg-slate-900 p-0.5 rounded-lg border border-slate-800">
                      <button
                        onClick={() => setActiveChartTab("time")}
                        className={`px-3 py-1 rounded text-xs font-mono transition-colors ${
                          activeChartTab === "time"
                            ? "bg-sky-500/20 text-sky-300 font-bold border border-sky-500/40"
                            : "text-slate-400 hover:text-white"
                        }`}
                      >
                        Mean Runtime (ms)
                      </button>
                      <button
                        onClick={() => setActiveChartTab("memory")}
                        className={`px-3 py-1 rounded text-xs font-mono transition-colors ${
                          activeChartTab === "memory"
                            ? "bg-purple-500/20 text-purple-300 font-bold border border-purple-500/40"
                            : "text-slate-400 hover:text-white"
                        }`}
                      >
                        Peak Memory (KB)
                      </button>
                    </div>
                  </div>

                  <div className="h-[280px] w-full pt-2">
                    <ResponsiveContainer width="100%" height="100%">
                      <BarChart data={chartData} margin={{ top: 10, right: 30, left: 0, bottom: 20 }}>
                        <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" />
                        <XAxis
                          dataKey="name"
                          stroke="#64748b"
                          fontSize={11}
                          tickLine={false}
                          interval={0}
                        />
                        <YAxis
                          stroke="#64748b"
                          fontSize={11}
                          tickLine={false}
                          label={{
                            value: activeChartTab === "time" ? "Time (ms)" : "Memory (KB)",
                            angle: -90,
                            position: "insideLeft",
                            fill: "#64748b",
                            fontSize: 10,
                          }}
                        />
                        <Tooltip
                          contentStyle={{
                            backgroundColor: "#0b0f19",
                            borderColor: "#334155",
                            borderRadius: 8,
                            fontSize: 12,
                            fontFamily: "monospace",
                          }}
                        />
                        <Bar
                          dataKey={activeChartTab === "time" ? "mean_ms" : "peak_kb"}
                          radius={[4, 4, 0, 0]}
                        >
                          {chartData.map((_, idx) => (
                            <Cell key={`cell-${idx}`} fill={PALETTE[idx % PALETTE.length]} />
                          ))}
                        </Bar>
                      </BarChart>
                    </ResponsiveContainer>
                  </div>
                </Card>

                {/* Statistical Breakdown Table */}
                <Card className="p-0 overflow-hidden border-slate-800">
                  <div className="px-5 py-3.5 bg-slate-900/80 border-b border-slate-800 flex items-center justify-between">
                    <div className="text-xs font-mono font-bold text-white uppercase tracking-wider">
                      Empirical Statistical Breakdown (N = {inputDimensionSize})
                    </div>
                    <span className="text-[11px] font-mono text-slate-400">
                      Calculated over {repetitions} iterations per algorithm
                    </span>
                  </div>

                  <div className="overflow-x-auto">
                    <table className="w-full text-left text-xs font-mono">
                      <thead className="bg-slate-950/60 text-slate-400 border-b border-slate-800">
                        <tr>
                          <th className="px-4 py-3">Algorithm</th>
                          <th className="px-4 py-3">Mean (ms)</th>
                          <th className="px-4 py-3">Median (ms)</th>
                          <th className="px-4 py-3">P95 (ms)</th>
                          <th className="px-4 py-3">Min / Max (ms)</th>
                          <th className="px-4 py-3">Peak Memory</th>
                          <th className="px-4 py-3">Speedup Ratio</th>
                          <th className="px-4 py-3 text-right">Actions</th>
                        </tr>
                      </thead>
                      <tbody className="divide-y divide-slate-800/80 text-slate-200">
                        {chartData.map((row) => {
                          const speedup = benchmarkResult.speedup_ratios?.[row.slug];
                          const isFastest = benchmarkResult.fastest_algorithm === row.slug;

                          return (
                            <tr key={row.slug} className="hover:bg-slate-900/40 transition-colors">
                              <td className="px-4 py-3">
                                <div className="font-semibold text-white flex items-center gap-1.5">
                                  {isFastest && <Award className="w-3.5 h-3.5 text-emerald-400" />}
                                  <span>{row.name}</span>
                                </div>
                                <div className="text-[10px] text-slate-400 font-mono">{row.slug}</div>
                              </td>

                              <td className="px-4 py-3 font-semibold text-sky-400">
                                {row.mean_ms.toFixed(4)} ms
                              </td>

                              <td className="px-4 py-3 text-slate-300">
                                {row.median_ms.toFixed(4)} ms
                              </td>

                              <td className="px-4 py-3 text-slate-300">
                                {row.p95_ms.toFixed(4)} ms
                              </td>

                              <td className="px-4 py-3 text-slate-400 text-[11px]">
                                {row.min_ms.toFixed(4)} / {row.max_ms.toFixed(4)}
                              </td>

                              <td className="px-4 py-3 text-purple-300 font-semibold">
                                {row.peak_kb > 0 ? `${row.peak_kb.toFixed(2)} KB` : "Not available"}
                              </td>

                              <td className="px-4 py-3">
                                {isFastest ? (
                                  <span className="px-2 py-0.5 rounded text-[10px] font-bold bg-emerald-950/60 text-emerald-400 border border-emerald-800/60">
                                    Baseline (1.0x)
                                  </span>
                                ) : speedup !== undefined ? (
                                  <span className="text-amber-400 font-mono">
                                    {speedup.toFixed(2)}x slower
                                  </span>
                                ) : (
                                  <span className="text-slate-500">Not available</span>
                                )}
                              </td>

                              <td className="px-4 py-3 text-right">
                                <Button
                                  variant="secondary"
                                  size="sm"
                                  className="text-sky-400 hover:text-white hover:bg-sky-600/30 border-sky-800/50 text-[11px] h-7 px-2.5 font-mono shadow-sm"
                                  onClick={() => {
                                    const foundResult = benchmarkResult?.results?.find(
                                      (r) => r.algorithm_slug === row.slug
                                    );
                                    if (foundResult) {
                                      setSelectedDetailResult(foundResult);
                                      setIsDetailsModalOpen(true);
                                    }
                                  }}
                                >
                                  Details
                                </Button>
                              </td>
                            </tr>
                          );
                        })}
                      </tbody>
                    </table>
                  </div>
                </Card>

                {/* Data-Driven Head-to-Head Analysis */}
                <div className="p-5 rounded-xl bg-[#0e131f] border border-slate-800 space-y-2 text-xs">
                  <div className="flex items-center gap-2 text-xs font-mono font-bold text-sky-400">
                    <Sparkles className="w-4 h-4" />
                    <span>Empirical Performance Analysis:</span>
                  </div>
                  <p className="text-slate-300 leading-relaxed font-sans">
                    For canonical problem <strong>{currentProblemName}</strong> at input dimension <strong>N = {inputDimensionSize}</strong>,{" "}
                    <strong>{benchmarkResult.fastest_algorithm}</strong> achieved the fastest mean execution time of{" "}
                    <strong>
                      {chartData.find((d) => d.slug === benchmarkResult.fastest_algorithm)?.mean_ms.toFixed(4)} ms
                    </strong>
                    .{" "}
                    {chartData.length > 1 && benchmarkResult.most_memory_efficient && (
                      <>
                        The lowest peak memory profile was measured by{" "}
                        <strong>{benchmarkResult.most_memory_efficient}</strong> at{" "}
                        <strong>
                          {chartData.find((d) => d.slug === benchmarkResult.most_memory_efficient)?.peak_kb.toFixed(2)} KB
                        </strong>
                        .
                      </>
                    )}
                  </p>
                </div>
              </div>
            ) : (
              <EmptyState
                title="Ready for Execution"
                message="Select a canonical problem, choose candidate implementations, and click 'Run Benchmark' to generate empirical telemetry."
              />
            )}
          </div>
        )}

        {/* Empirical Statistical Breakdown Details Modal */}
        {isDetailsModalOpen && selectedDetailResult && (
          <StatisticalDetailsModal
            isOpen={isDetailsModalOpen}
            onClose={() => {
              setIsDetailsModalOpen(false);
              setSelectedDetailResult(null);
            }}
            result={selectedDetailResult}
            benchmarkResponse={benchmarkResult}
            problemName={currentProblemName}
            problemSlug={selectedProblemSlug}
            inputSize={inputDimensionSize}
            repetitions={repetitions}
            warmupRuns={warmupRuns}
          />
        )}
      </div>
    </Layout>
  );
}
