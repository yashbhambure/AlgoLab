import { useState, useEffect, useRef } from "react";
import { useSearchParams, Link } from "react-router-dom";
import {
  Play,
  Pause,
  RotateCcw,
  SkipForward,
  SkipBack,
  Sliders,
  Info,
  AlertTriangle,
  BookOpen,
  ExternalLink,
  Crown,
} from "lucide-react";
import { Layout } from "../components/layout/Layout";
import { PageHeader } from "../components/layout/PageHeader";
import { Card } from "../components/common/Card";
import { Button } from "../components/common/Button";
import { Badge } from "../components/common/Badge";
import { LoadingState } from "../components/common/LoadingState";
import { useTheme } from "../hooks/useTheme";
import { api } from "../services/api";
import type { Algorithm, AlgorithmExecutionResult, ExecutionStep } from "../types";

// Default input presets for all 23 authoritative curriculum algorithms and supplementary methods
const ALGORITHM_DEFAULT_INPUTS: Record<string, any> = {
  // Module 1: Divide and Conquer
  "defective-chessboard": { size: 4, defect: [0, 0] },
  "max-min-divide-conquer": [22, 13, -5, 88, 41, 7, 95, 3],
  "strassen-matrix-multiplication": {
    matrix_a: [[1, 2], [3, 4]],
    matrix_b: [[5, 6], [7, 8]],
  },

  // Module 2: Backtracking
  "n-queens-backtracking": { n: 4 },
  "subset-sum-backtracking": { numbers: [3, 5, 6, 7], target_sum: 15 },
  "hamiltonian-cycle-backtracking": {
    vertices: ["A", "B", "C", "D"],
    edges: [["A", "B"], ["B", "C"], ["C", "D"], ["D", "A"]],
  },
  "graph-coloring-backtracking": {
    vertices: ["0", "1", "2", "3"],
    edges: [["0", "1"], ["1", "2"], ["2", "3"], ["3", "0"], ["0", "2"]],
    max_colors: 3,
  },

  // Module 3: Dynamic Programming I
  "multistage-graph-dp": {
    num_vertices: 8,
    stages: 4,
    edges: [
      { from: 1, to: 2, weight: 2 }, { from: 1, to: 3, weight: 1 }, { from: 1, to: 4, weight: 3 },
      { from: 2, to: 5, weight: 2 }, { from: 2, to: 6, weight: 3 }, { from: 3, to: 5, weight: 6 },
      { from: 3, to: 6, weight: 7 }, { from: 4, to: 6, weight: 6 }, { from: 4, to: 7, weight: 8 },
      { from: 5, to: 8, weight: 1 }, { from: 6, to: 8, weight: 4 }, { from: 7, to: 8, weight: 2 },
    ],
  },
  "floyd-warshall-apsp": {
    matrix: [
      [0, 3, 999999, 7],
      [8, 0, 2, 999999],
      [5, 999999, 0, 1],
      [2, 999999, 999999, 0],
    ],
  },
  "optimal-bst-dp": {
    keys: ["k1", "k2", "k3", "k4"],
    p: [0.1, 0.2, 0.4, 0.3],
    q: [0.05, 0.1, 0.05, 0.05, 0.05],
  },

  // Module 4: Dynamic Programming II
  "0-1-knapsack-dp": { weights: [2, 3, 4, 5], values: [3, 4, 5, 6], capacity: 5 },
  "traveling-salesman-dp": {
    distance_matrix: [
      [0, 10, 15, 20],
      [10, 0, 35, 25],
      [15, 35, 0, 30],
      [20, 25, 30, 0],
    ],
    cities: ["A", "B", "C", "D"],
  },
  "reliability-design-dp": {
    reliabilities: [0.9, 0.8, 0.5],
    costs: [30, 15, 20],
    budget: 105,
  },

  // Module 5: Greedy Method I
  "optimal-storage-tapes-greedy": {
    lengths: [5, 10, 3, 20, 12, 7],
    tapes: 1,
    programs: ["P1", "P2", "P3", "P4", "P5", "P6"],
  },
  "fractional-knapsack": { weights: [10, 20, 30], values: [60, 100, 120], capacity: 50 },
  "job-sequencing-deadlines": {
    jobs: [
      { id: "J1", deadline: 2, profit: 100 },
      { id: "J2", deadline: 1, profit: 19 },
      { id: "J3", deadline: 2, profit: 27 },
      { id: "J4", deadline: 1, profit: 25 },
      { id: "J5", deadline: 3, profit: 15 },
    ],
  },

  // Module 6: Greedy Method II
  "optimal-merge-patterns-greedy": { files: [20, 30, 10, 5, 30], names: ["F1", "F2", "F3", "F4", "F5"] },
  "kruskal-mst": {
    vertices: ["0", "1", "2", "3"],
    edges: [["0", "1", 10], ["0", "2", 6], ["0", "3", 5], ["1", "3", 15], ["2", "3", 4]],
  },
  "prim-mst": {
    vertices: ["0", "1", "2", "3"],
    edges: [["0", "1", 10], ["0", "2", 6], ["0", "3", 5], ["1", "3", 15], ["2", "3", 4]],
  },
  "dijkstra-sssp": {
    vertices: ["A", "B", "C", "D"],
    edges: [["A", "B", 1], ["B", "C", 2], ["A", "C", 4], ["C", "D", 1]],
    source: "A",
  },
  "bellman-ford-sssp": {
    vertices: ["A", "B", "C", "D"],
    edges: [["A", "B", 4], ["A", "C", 5], ["B", "C", -2], ["C", "D", 3]],
    source: "A",
  },

  // Module 7: Branch and Bound
  "0-1-knapsack-lc-bb": { weights: [2, 4, 6, 9], values: [10, 10, 12, 18], capacity: 15 },
  "0-1-knapsack-fifo-bb": { weights: [2, 4, 6, 9], values: [10, 10, 12, 18], capacity: 15 },
  "traveling-salesman-bb": {
    distance_matrix: [
      [999999, 20, 30, 10, 11],
      [15, 999999, 16, 4, 2],
      [3, 5, 999999, 2, 4],
      [19, 6, 18, 999999, 3],
      [16, 4, 7, 16, 999999],
    ],
    cities: ["A", "B", "C", "D", "E"],
  },

};

// Theoretical non-executable topics guard
const THEORY_ONLY_SLUGS: Record<string, { title: string; module: string; description: string }> = {
  "tractable-problems": {
    title: "Tractable Problems",
    module: "Module 6: P and NP Problems",
    description: "Problems solvable in deterministic polynomial time O(n^k). This is a foundational complexity theory topic and cannot be executed as a standalone step-by-step algorithm.",
  },
  "non-tractable-problems": {
    title: "Non-Tractable Problems",
    module: "Module 6: P and NP Problems",
    description: "Problems with super-polynomial lower bounds Omega(c^n). This is a theoretical classification and has no single step execution.",
  },
  "class-p": {
    title: "Class P (Deterministic Polynomial Time)",
    module: "Module 6: P and NP Problems",
    description: "Complexity class of languages decidable by a Deterministic Turing Machine in polynomial time. Explore reductions and proofs in the Curriculum Hub.",
  },
  "class-np": {
    title: "Class NP (Nondeterministic Polynomial Time)",
    module: "Module 6: P and NP Problems",
    description: "Complexity class of problems verifiable in deterministic polynomial time given a certificate.",
  },
  "np-hard-problems": {
    title: "NP-Hard Problems",
    module: "Module 7: NP-Hard & NP-Complete",
    description: "Class of problems to which every problem in NP can be reduced in polynomial time.",
  },
  "np-complete-problems": {
    title: "NP-Complete Problems",
    module: "Module 7: NP-Hard & NP-Complete",
    description: "Equivalence class of the hardest decision problems in NP (satisfiability, vertex cover, Hamiltonian cycle decision).",
  },
  "cooks-theorem": {
    title: "Cook's Theorem (Cook-Levin Theorem)",
    module: "Module 7: NP-Hard & NP-Complete",
    description: "Landmark 1971 mathematical proof establishing that Boolean Satisfiability (SAT) is NP-Complete.",
  },
};

export default function VisualizerPage() {
  const { theme } = useTheme();
  const isLight = theme === "light";
  const [searchParams, setSearchParams] = useSearchParams();
  const urlAlgo = searchParams.get("algo") || searchParams.get("algorithm") || "defective-chessboard";

  const [availableAlgorithms, setAvailableAlgorithms] = useState<Algorithm[]>([]);
  const [curriculumSlugs, setCurriculumSlugs] = useState<Set<string>>(new Set());
  const [selectedAlgoSlug, setSelectedAlgoSlug] = useState(urlAlgo);
  const [inputJsonText, setInputJsonText] = useState("");
  const [lastExecutedInputText, setLastExecutedInputText] = useState("");
  const [inputError, setInputError] = useState<string | null>(null);

  const [executionResult, setExecutionResult] = useState<AlgorithmExecutionResult | null>(null);
  const [currentStepIndex, setCurrentStepIndex] = useState(0);
  const [isPlaying, setIsPlaying] = useState(false);
  const [speedMs, setSpeedMs] = useState(300);
  const [loading, setLoading] = useState(false);
  const [algoDetails, setAlgoDetails] = useState<Algorithm | null>(null);

  const timerRef = useRef<any>(null);

  // Synchronize URL query params
  useEffect(() => {
    const slug = searchParams.get("algo") || searchParams.get("algorithm");
    if (slug && slug !== selectedAlgoSlug) {
      setSelectedAlgoSlug(slug);
    }
  }, [searchParams]);

  // Load algorithms list & approved curriculum whitelist on mount
  useEffect(() => {
    Promise.all([
      api.getAlgorithms(),
      api.getApprovedCurriculumSlugs().catch(() => [] as string[]),
    ])
      .then(([algos, slugs]) => {
        setAvailableAlgorithms(algos);
        setCurriculumSlugs(new Set(slugs));
      })
      .catch((err) => console.error("Failed to fetch visualizer algorithms:", err));
  }, []);

  // Update default input and load details when algorithm changes
  useEffect(() => {
    if (THEORY_ONLY_SLUGS[selectedAlgoSlug]) {
      setExecutionResult(null);
      setAlgoDetails(null);
      return;
    }

    const defaultVal = ALGORITHM_DEFAULT_INPUTS[selectedAlgoSlug] ?? [64, 34, 25, 12, 22, 11, 90];
    const defaultJson = JSON.stringify(defaultVal, null, 2);
    setInputJsonText(defaultJson);
    setLastExecutedInputText(defaultJson);
    setInputError(null);

    api.getAlgorithm(selectedAlgoSlug)
      .then(setAlgoDetails)
      .catch((err) => console.error("Failed to load algo details:", err));

    handleRunExecution(selectedAlgoSlug, defaultVal);
  }, [selectedAlgoSlug]);

  const handleRunExecution = async (slugToRun = selectedAlgoSlug, inputOverride?: any) => {
    if (THEORY_ONLY_SLUGS[slugToRun]) return;

    if (timerRef.current) clearInterval(timerRef.current);
    setIsPlaying(false);
    setInputError(null);

    let parsedInput: any;
    let rawTextToTrack = inputJsonText;

    if (inputOverride !== undefined) {
      parsedInput = inputOverride;
      rawTextToTrack = typeof inputOverride === "string" ? inputOverride : JSON.stringify(inputOverride, null, 2);
    } else {
      const trimmed = inputJsonText.trim();
      if (!trimmed) {
        setInputError("Input payload cannot be empty. Please provide valid JSON or an array.");
        return;
      }

      try {
        parsedInput = JSON.parse(trimmed);
      } catch {
        // Fallback for 1D array of comma-separated numbers
        const parts = trimmed.split(",").map((s) => s.trim()).filter(Boolean);
        const parsedNums = parts.map(Number);
        if (parts.length > 0 && parsedNums.every((n) => !isNaN(n))) {
          parsedInput = parsedNums;
        } else {
          setInputError("Invalid JSON format. Please provide valid JSON or comma-separated numbers.");
          return;
        }
      }
    }

    // Invalidate previous trace immediately before fetching new trace
    setExecutionResult(null);
    setCurrentStepIndex(0);
    setLoading(true);

    try {
      const res = await api.runStepExecution({
        algorithm_slug: slugToRun,
        input_data: parsedInput,
        max_steps: 500,
      });

      setExecutionResult(res);
      setCurrentStepIndex(0);
      setLastExecutedInputText(rawTextToTrack);
    } catch (err: any) {
      console.error("Execution error:", err);
      setInputError(err.message || "Failed to execute algorithm step tracing.");
      setExecutionResult(null);
    } finally {
      setLoading(false);
    }
  };

  const handleResetDefaultInput = () => {
    const defaultVal = ALGORITHM_DEFAULT_INPUTS[selectedAlgoSlug] ?? [64, 34, 25, 12, 22, 11, 90];
    const defaultJson = JSON.stringify(defaultVal, null, 2);
    setInputJsonText(defaultJson);
    setLastExecutedInputText(defaultJson);
    setInputError(null);
    handleRunExecution(selectedAlgoSlug, defaultVal);
  };

  const isInputDirty = inputJsonText.trim() !== lastExecutedInputText.trim();

  const handleTogglePlay = async () => {
    if (isPlaying) {
      setIsPlaying(false);
      return;
    }

    if (!executionResult || isInputDirty) {
      await handleRunExecution(selectedAlgoSlug);
      setIsPlaying(true);
    } else {
      if (currentStepIndex >= executionResult.steps.length - 1) {
        setCurrentStepIndex(0);
      }
      setIsPlaying(true);
    }
  };

  // Playback loop
  useEffect(() => {
    if (isPlaying && executionResult && executionResult.steps.length > 0) {
      timerRef.current = setInterval(() => {
        setCurrentStepIndex((prev) => {
          if (prev >= executionResult.steps.length - 1) {
            setIsPlaying(false);
            clearInterval(timerRef.current);
            return prev;
          }
          return prev + 1;
        });
      }, speedMs);
    } else {
      if (timerRef.current) clearInterval(timerRef.current);
    }

    return () => {
      if (timerRef.current) clearInterval(timerRef.current);
    };
  }, [isPlaying, executionResult, speedMs]);

  const currentStep: ExecutionStep | null =
    executionResult && executionResult.steps.length > 0
      ? executionResult.steps[currentStepIndex] || null
      : null;

  const isTheoryOnly = Boolean(THEORY_ONLY_SLUGS[selectedAlgoSlug]);

  // Determine state presentation adapter
  const isNQueens = selectedAlgoSlug.includes("n-queen");
  const isChessboard = selectedAlgoSlug === "defective-chessboard";
  const isStrassen = selectedAlgoSlug === "strassen-matrix-multiplication";
  const isStorageOnTapes = selectedAlgoSlug === "optimal-storage-tapes-greedy";
  const isJobSequencing = selectedAlgoSlug === "job-sequencing-deadlines";

  const is1DArray =
    Array.isArray(currentStep?.state_snapshot) &&
    currentStep.state_snapshot.every((v) => typeof v === "number");

  const is2DMatrix =
    Array.isArray(currentStep?.state_snapshot) &&
    currentStep.state_snapshot.length > 0 &&
    Array.isArray(currentStep.state_snapshot[0]);

  const currentArray: number[] = is1DArray
    ? (currentStep?.state_snapshot as number[])
    : Array.isArray(executionResult?.output) && executionResult.output.every((v: any) => typeof v === "number")
    ? (executionResult.output as number[])
    : [];

  const maxVal = Math.max(...(currentArray.length ? currentArray : [100]), 10);

  const getBarColor = (idx: number) => {
    if (!currentStep) {
      return isLight
        ? "bg-sky-500 border-sky-600 text-white shadow-sm"
        : "bg-sky-600/80 border-sky-500 text-sky-300";
    }
    const { action, indices } = currentStep;
    if (action === "swap" && indices?.includes(idx)) {
      return isLight
        ? "bg-rose-500 border-rose-600 text-white shadow-md ring-2 ring-rose-300"
        : "bg-rose-500/80 border-rose-400 text-rose-300";
    }
    if (action === "compare" && indices?.includes(idx)) {
      return isLight
        ? "bg-amber-400 border-amber-500 text-amber-950 shadow-md ring-2 ring-amber-300"
        : "bg-amber-500/80 border-amber-400 text-amber-300";
    }
    if ((action === "select" || action === "pivot") && indices?.includes(idx)) {
      return isLight
        ? "bg-purple-500 border-purple-600 text-white shadow-md ring-2 ring-purple-300"
        : "bg-purple-500/80 border-purple-400 text-purple-300";
    }
    if ((action === "found" || action === "complete" || action === "base_case_1") && indices?.includes(idx)) {
      return isLight
        ? "bg-emerald-500 border-emerald-600 text-white shadow-md ring-2 ring-emerald-300"
        : "bg-emerald-500/80 border-emerald-400 text-emerald-300";
    }
    return isLight
      ? "bg-slate-200 hover:bg-slate-300 border-slate-300 text-slate-700"
      : "bg-slate-800 border-slate-700 text-slate-300";
  };

  const selectedAlgo = availableAlgorithms.find((a) => a.slug === selectedAlgoSlug);

  return (
    <Layout>
      <div className="space-y-6 animate-in fade-in duration-200">
        {/* Page Header */}
        <PageHeader
          breadcrumb="Interactive Execution"
          title="Algorithm Step-by-Step Visualizer"
          description="Trace all 23 authoritative curriculum algorithms and supplementary methods step-by-step with real execution instrumentation, verified state mutations, and telemetry."
          actions={
            <div className="flex items-center gap-3">
              <div className="flex items-center gap-2">
                <span className="text-xs font-mono text-slate-600 dark:text-slate-400 hidden sm:inline">Algorithm:</span>
                <select
                  value={selectedAlgoSlug}
                  onChange={(e) => {
                    setSelectedAlgoSlug(e.target.value);
                    setSearchParams({ algo: e.target.value });
                  }}
                  className="px-3 py-1.5 rounded-lg bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 text-xs font-mono text-slate-900 dark:text-white focus:outline-none focus:border-sky-500 font-medium max-w-[280px] truncate shadow-sm dark:shadow-none transition-colors"
                >
                  <optgroup label="Authoritative Curriculum (23 Algorithms)">
                    {availableAlgorithms
                      .filter((a) => curriculumSlugs.has(a.slug))
                      .map((algo) => (
                        <option key={algo.slug} value={algo.slug}>
                          {algo.name} ({algo.category})
                        </option>
                      ))}
                  </optgroup>
                  <optgroup label="Supplementary Educational Methods">
                    {availableAlgorithms
                      .filter((a) => !curriculumSlugs.has(a.slug))
                      .map((algo) => (
                        <option key={algo.slug} value={algo.slug}>
                          {algo.name} ({algo.category})
                        </option>
                      ))}
                  </optgroup>
                </select>
              </div>
            </div>
          }
        />

        {/* Theory-Only Notice if user selected theoretical topic */}
        {isTheoryOnly && (
          <Card headerTag="Theoretical Concept Notice">
            <div className="p-6 text-center space-y-4 max-w-2xl mx-auto">
              <div className="w-12 h-12 rounded-xl bg-purple-500/10 border border-purple-500/30 flex items-center justify-center mx-auto text-purple-400">
                <BookOpen className="w-6 h-6" />
              </div>
              <h3 className="text-lg font-semibold text-white">
                {THEORY_ONLY_SLUGS[selectedAlgoSlug].title}
              </h3>
              <p className="text-xs text-slate-400 font-mono">
                {THEORY_ONLY_SLUGS[selectedAlgoSlug].module}
              </p>
              <p className="text-sm text-slate-300 leading-relaxed">
                {THEORY_ONLY_SLUGS[selectedAlgoSlug].description}
              </p>
              <div className="pt-2">
                <Link to="/curriculum">
                  <Button variant="primary" icon={<ExternalLink className="w-4 h-4" />}>
                    Explore in Curriculum Hub
                  </Button>
                </Link>
              </div>
            </div>
          </Card>
        )}

        {!isTheoryOnly && (
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-5">
            {/* Main Visualizer Canvas & Controls */}
            <div className="lg:col-span-2 space-y-4">
              {/* Input & Execution Bar */}
              <Card
                headerTag="Input Payload & Tracing Parameters"
                headerRight={
                  <div className="flex items-center gap-2">
                    {curriculumSlugs.has(selectedAlgoSlug) ? (
                      <span className="px-2 py-0.5 rounded text-[10px] font-mono font-medium bg-emerald-500/15 text-emerald-400 border border-emerald-500/30">
                        Curriculum
                      </span>
                    ) : (
                      <span className="px-2 py-0.5 rounded text-[10px] font-mono font-medium bg-slate-800 text-slate-400 border border-slate-700">
                        Supplementary
                      </span>
                    )}
                    <Badge variant="primary" mono size="sm">
                      {selectedAlgo?.name || selectedAlgoSlug}
                    </Badge>
                  </div>
                }
              >
                <div className="space-y-3">
                  <div>
                    <div className="flex items-center justify-between mb-1.5">
                      <div className="flex items-center gap-2">
                        <label className="text-[11px] font-mono text-slate-600 dark:text-slate-400">
                          Execution Input (JSON / Array)
                        </label>
                        {isInputDirty && (
                          <span className="px-1.5 py-0.5 rounded text-[10px] font-mono bg-amber-500/15 text-amber-700 dark:text-amber-300 border border-amber-500/30">
                            Modified
                          </span>
                        )}
                      </div>
                      <div className="flex items-center gap-2">
                        <button
                          onClick={handleResetDefaultInput}
                          className="text-[11px] font-mono text-slate-600 dark:text-slate-400 hover:text-sky-600 dark:hover:text-sky-300 transition-colors"
                        >
                          Reset Default
                        </button>
                        <Button
                          variant="primary"
                          size="sm"
                          onClick={() => handleRunExecution(selectedAlgoSlug)}
                          disabled={loading}
                          loading={loading}
                          icon={<Play className="w-3.5 h-3.5" />}
                        >
                          Run / Visualize
                        </Button>
                      </div>
                    </div>
                    <textarea
                      rows={3}
                      value={inputJsonText}
                      onChange={(e) => {
                        setInputJsonText(e.target.value);
                        setInputError(null);
                      }}
                      className={`w-full px-3 py-2 rounded-lg bg-slate-50 dark:bg-slate-900 border text-xs font-mono text-slate-900 dark:text-white focus:outline-none focus:bg-white dark:focus:bg-slate-900 resize-y shadow-inner transition-colors ${
                        inputError ? "border-rose-500 focus:border-rose-400" : "border-slate-200 dark:border-slate-800 focus:border-sky-500"
                      }`}
                      placeholder="Enter input JSON or comma-separated numbers"
                    />
                  </div>

                  {inputError && (
                    <div className="p-3 rounded-lg bg-rose-50 dark:bg-rose-500/10 border border-rose-200 dark:border-rose-500/30 flex items-start gap-2 text-rose-700 dark:text-rose-300 font-mono text-xs">
                      <AlertTriangle className="w-4 h-4 flex-shrink-0 mt-0.5 text-rose-600 dark:text-rose-400" />
                      <span>{inputError}</span>
                    </div>
                  )}

                  {/* Playback Controls Toolbar */}
                  <div className="flex flex-wrap items-center justify-between gap-3 pt-3 border-t border-slate-200 dark:border-slate-800">
                    <div className="flex items-center gap-2">
                      <Button
                        variant={isPlaying ? "secondary" : "secondary"}
                        size="sm"
                        onClick={handleTogglePlay}
                        disabled={loading}
                        icon={isPlaying ? <Pause className="w-3.5 h-3.5" /> : <Play className="w-3.5 h-3.5" />}
                      >
                        {isPlaying ? "Pause" : "Play"}
                      </Button>

                      <Button
                        variant="ghost"
                        size="sm"
                        onClick={() => {
                          setIsPlaying(false);
                          setCurrentStepIndex((prev) => Math.max(0, prev - 1));
                        }}
                        disabled={currentStepIndex <= 0}
                        icon={<SkipBack className="w-3.5 h-3.5" />}
                      >
                        Back
                      </Button>

                      <Button
                        variant="ghost"
                        size="sm"
                        onClick={() => {
                          setIsPlaying(false);
                          setCurrentStepIndex((prev) =>
                            executionResult ? Math.min(executionResult.steps.length - 1, prev + 1) : 0
                          );
                        }}
                        disabled={!executionResult || currentStepIndex >= executionResult.steps.length - 1}
                        icon={<SkipForward className="w-3.5 h-3.5" />}
                      >
                        Next
                      </Button>

                      <Button
                        variant="ghost"
                        size="sm"
                        onClick={() => {
                          setIsPlaying(false);
                          setCurrentStepIndex(0);
                        }}
                        icon={<RotateCcw className="w-3.5 h-3.5" />}
                        title="Reset trace to step 0"
                      >
                        Reset
                      </Button>
                    </div>

                    {/* Speed Slider & Re-trace */}
                    <div className="flex items-center gap-3">
                      <div className="flex items-center gap-2 text-xs font-mono text-slate-600 dark:text-slate-400">
                        <Sliders className="w-3.5 h-3.5 text-slate-400 dark:text-slate-500" />
                        <span>{speedMs}ms</span>
                        <input
                          type="range"
                          min="50"
                          max="1000"
                          step="50"
                          value={speedMs}
                          onChange={(e) => setSpeedMs(Number(e.target.value))}
                          className="w-20 accent-sky-500 dark:accent-sky-400 cursor-pointer"
                          title="Adjust animation speed"
                        />
                      </div>

                      <Button
                        variant="ghost"
                        size="sm"
                        onClick={() => handleRunExecution(selectedAlgoSlug)}
                        disabled={loading}
                        loading={loading}
                        icon={<RotateCcw className="w-3.5 h-3.5" />}
                        title="Re-execute trace with current input"
                      >
                        Re-trace
                      </Button>
                    </div>
                  </div>

                  {/* Scrubber Progress Bar */}
                  {executionResult && executionResult.steps.length > 0 && (
                    <div className="pt-2">
                      <input
                        type="range"
                        min="0"
                        max={executionResult.steps.length - 1}
                        value={currentStepIndex}
                        onChange={(e) => {
                          setIsPlaying(false);
                          setCurrentStepIndex(Number(e.target.value));
                        }}
                        className="w-full accent-sky-500 dark:accent-sky-400 cursor-pointer h-2 bg-slate-200 dark:bg-slate-800 rounded-lg appearance-none"
                      />
                    </div>
                  )}

                </div>
              </Card>

              {/* Visual Canvas Card */}
              <div className="rounded-xl bg-white dark:bg-[#0e131f] border border-slate-200 dark:border-slate-800 p-5 space-y-4 shadow-sm dark:shadow-none transition-colors duration-200">
                {/* Step Status & Action Marker */}
                <div className="flex items-center justify-between border-b border-slate-200 dark:border-slate-800 pb-3">
                  <div className="flex items-center gap-2 font-mono text-xs text-slate-600 dark:text-slate-300">
                    <span className="w-2 h-2 rounded-full bg-sky-500 dark:bg-sky-400 animate-pulse" />
                    <span>
                      Step <strong className="text-slate-900 dark:text-white font-semibold">{executionResult?.steps.length ? currentStepIndex + 1 : 0}</strong> of{" "}
                      {executionResult?.steps.length || 0}
                    </span>
                  </div>

                  <Badge
                    variant={
                      currentStep?.action === "swap"
                        ? "danger"
                        : currentStep?.action === "compare"
                        ? "warning"
                        : currentStep?.action === "found" || currentStep?.action === "complete" || currentStep?.action === "solution_found"
                        ? "success"
                        : currentStep?.action === "select" || currentStep?.action === "pivot" || currentStep?.action === "place_queen" || currentStep?.action === "place_tromino"
                        ? "purple"
                        : "default"
                    }
                    mono
                    size="sm"
                  >
                    Action: {currentStep?.action ? currentStep.action.toUpperCase() : "READY"}
                  </Badge>
                </div>

                {/* Step Narrative Callout */}
                <div className="p-3.5 rounded-lg bg-sky-50/70 dark:bg-slate-900/80 border border-sky-100 dark:border-slate-800 text-xs font-mono text-slate-700 dark:text-slate-300 flex items-start gap-2.5 shadow-sm dark:shadow-none transition-colors">
                  <Info className="w-4 h-4 text-sky-600 dark:text-sky-400 flex-shrink-0 mt-0.5" />
                  <span className="leading-relaxed">
                    {currentStep?.description ||
                      "Ready to trace execution. Press Play or Next to step through verified state mutations."}
                  </span>
                </div>

                {/* Multi-Paradigm State Visualizer Adapters */}
                {loading ? (
                  <div className="py-20">
                    <LoadingState message="Computing verified execution trace..." />
                  </div>
                ) : isNQueens && Array.isArray(currentStep?.state_snapshot) ? (
                  /* Dedicated N-Queens Board Visualizer */
                  <div className="py-4">
                    <div className="flex flex-col items-center gap-3">
                      <div className="text-xs font-mono text-slate-600 dark:text-slate-400">
                        Board State: {((currentStep?.state_snapshot as number[]) || []).map((col, row) => (
                          <span key={row} className="inline-block mx-1 text-sky-600 dark:text-sky-300 font-semibold">
                            R{row}: {col >= 0 ? `C${col}` : "—"}
                          </span>
                        ))}
                      </div>
                      <div className="inline-block p-3.5 rounded-xl bg-slate-100 dark:bg-slate-950 border border-slate-200 dark:border-slate-800 shadow-md transition-colors">
                        <div
                          className="grid gap-1.5"
                          style={{
                            gridTemplateColumns: `repeat(${currentStep?.state_snapshot?.length || 4}, minmax(0, 1fr))`,
                          }}
                        >
                          {((currentStep?.state_snapshot as number[]) || []).map((queenCol, rIdx) => {
                            const n = (currentStep?.state_snapshot as number[])?.length || 4;
                            return Array.from({ length: n }).map((_, cIdx) => {
                              const isDark = (rIdx + cIdx) % 2 === 1;
                              const hasQueen = queenCol === cIdx;
                              const isCurrentPlaced = currentStep.indices?.[0] === rIdx && currentStep.indices?.[1] === cIdx;

                              return (
                                <div
                                  key={`${rIdx}-${cIdx}`}
                                  className={`w-11 h-11 sm:w-14 sm:h-14 rounded-lg flex items-center justify-center font-mono text-xs transition-all duration-150 ${
                                    hasQueen
                                      ? isCurrentPlaced
                                        ? "bg-purple-600 text-white font-bold ring-2 ring-purple-400 shadow-lg scale-105"
                                        : "bg-emerald-600 text-white font-bold ring-1 ring-emerald-400 shadow-md"
                                      : isDark
                                      ? isLight
                                        ? "bg-slate-200/90 text-slate-400 border border-slate-300/60"
                                        : "bg-slate-800/80 text-slate-500"
                                      : isLight
                                      ? "bg-white text-slate-400 border border-slate-200"
                                      : "bg-slate-900 text-slate-600"
                                  }`}
                                >
                                  {hasQueen ? (
                                    <div className="flex flex-col items-center">
                                      <Crown className="w-5 h-5 text-amber-300 fill-amber-300 drop-shadow" />
                                      <span className="text-[9px] text-white font-bold">Q{rIdx}</span>
                                    </div>
                                  ) : (
                                    <span className="text-[10px] opacity-40 font-mono text-slate-500 dark:text-slate-400">{rIdx},{cIdx}</span>
                                  )}
                                </div>
                              );
                            });
                          })}
                        </div>
                      </div>
                    </div>
                  </div>
                ) : isChessboard && is2DMatrix ? (
                  /* Defective Chessboard Tromino Tiling Visualizer */
                  <div className="py-4 overflow-x-auto">
                    <div className="text-center mb-3 text-xs font-mono text-slate-600 dark:text-slate-400 font-medium">
                      2^k x 2^k Chessboard Tile Grid (Defect in Rose, Tromino IDs color-coded)
                    </div>
                    <div className="flex justify-center">
                      <div className="inline-block p-3 sm:p-4 rounded-xl bg-slate-50 dark:bg-slate-950 border border-slate-200 dark:border-slate-800 shadow-sm dark:shadow-none transition-colors">
                        <table className="border-collapse font-mono text-xs">
                          <tbody>
                            {((currentStep?.state_snapshot as number[][]) || []).map((row, rIdx) => (
                              <tr key={rIdx}>
                                {row.map((cell, cIdx) => {
                                  const isDefect = cell === -1;
                                  const isTiled = cell > 0;
                                  const hue = isTiled ? (cell * 57) % 360 : 0;
                                  return (
                                    <td
                                      key={cIdx}
                                      style={{
                                        backgroundColor: isDefect
                                          ? isLight
                                            ? "rgba(254, 205, 211, 0.9)"
                                            : "rgba(244, 63, 94, 0.4)"
                                          : isTiled
                                          ? isLight
                                            ? `hsla(${hue}, 85%, 90%, 0.95)`
                                            : `hsla(${hue}, 70%, 25%, 0.7)`
                                          : isLight
                                          ? "#ffffff"
                                          : "rgba(15, 23, 42, 0.9)",
                                        borderColor: isDefect
                                          ? "rgba(244, 63, 94, 0.8)"
                                          : isTiled
                                          ? isLight
                                            ? `hsla(${hue}, 80%, 48%, 0.9)`
                                            : `hsla(${hue}, 70%, 55%, 0.85)`
                                          : isLight
                                          ? "rgba(203, 213, 225, 0.8)"
                                          : "rgba(51, 65, 85, 0.6)",
                                      }}
                                      className="border p-2 sm:p-3 text-center min-w-[44px] h-[44px] sm:min-w-[50px] sm:h-[50px] transition-colors rounded-sm"
                                    >
                                      {isDefect ? (
                                        <span className="text-rose-600 dark:text-rose-300 font-bold tracking-wide text-[11px]">DEFECT</span>
                                      ) : isTiled ? (
                                        <span
                                          style={{ color: isLight ? `hsla(${hue}, 90%, 24%, 1)` : "#ffffff" }}
                                          className="font-bold text-xs"
                                        >
                                          T#{cell}
                                        </span>
                                      ) : (
                                        <span className="text-slate-300 dark:text-slate-600 text-lg font-bold">·</span>
                                      )}
                                    </td>
                                  );
                                })}
                              </tr>
                            ))}
                          </tbody>
                        </table>
                      </div>
                    </div>
                  </div>
                ) : isStrassen && currentStep?.state_snapshot?.quadrants ? (
                  /* Strassen Matrix Quadrants Visualizer */
                  <div className="py-3 space-y-4">
                    <div className="text-xs font-mono text-sky-600 dark:text-sky-400 font-semibold text-center">
                      Recursive Strassen Quadrant Partitioning (Level {currentStep.state_snapshot.depth ?? 0})
                    </div>
                    <div className="grid grid-cols-2 gap-4">
                      <div className="p-3 rounded-lg bg-slate-50 dark:bg-slate-900 border border-slate-200 dark:border-slate-800 space-y-2">
                        <span className="text-[11px] font-mono text-slate-600 dark:text-slate-400 font-semibold block">Matrix A Sub-Blocks</span>
                        <div className="grid grid-cols-2 gap-2 text-center font-mono text-xs">
                          <div className="p-2 rounded bg-sky-50 dark:bg-sky-950/40 border border-sky-200 dark:border-sky-800/40 text-sky-800 dark:text-sky-300 font-medium">A11: {JSON.stringify(currentStep.state_snapshot.quadrants.A11)}</div>
                          <div className="p-2 rounded bg-sky-50 dark:bg-sky-950/40 border border-sky-200 dark:border-sky-800/40 text-sky-800 dark:text-sky-300 font-medium">A12: {JSON.stringify(currentStep.state_snapshot.quadrants.A12)}</div>
                          <div className="p-2 rounded bg-sky-50 dark:bg-sky-950/40 border border-sky-200 dark:border-sky-800/40 text-sky-800 dark:text-sky-300 font-medium">A21: {JSON.stringify(currentStep.state_snapshot.quadrants.A21)}</div>
                          <div className="p-2 rounded bg-sky-50 dark:bg-sky-950/40 border border-sky-200 dark:border-sky-800/40 text-sky-800 dark:text-sky-300 font-medium">A22: {JSON.stringify(currentStep.state_snapshot.quadrants.A22)}</div>
                        </div>
                      </div>
                      <div className="p-3 rounded-lg bg-slate-50 dark:bg-slate-900 border border-slate-200 dark:border-slate-800 space-y-2">
                        <span className="text-[11px] font-mono text-slate-600 dark:text-slate-400 font-semibold block">Matrix B Sub-Blocks</span>
                        <div className="grid grid-cols-2 gap-2 text-center font-mono text-xs">
                          <div className="p-2 rounded bg-purple-50 dark:bg-purple-950/40 border border-purple-200 dark:border-purple-800/40 text-purple-800 dark:text-purple-300 font-medium">B11: {JSON.stringify(currentStep.state_snapshot.quadrants.B11)}</div>
                          <div className="p-2 rounded bg-purple-50 dark:bg-purple-950/40 border border-purple-200 dark:border-purple-800/40 text-purple-800 dark:text-purple-300 font-medium">B12: {JSON.stringify(currentStep.state_snapshot.quadrants.B12)}</div>
                          <div className="p-2 rounded bg-purple-50 dark:bg-purple-950/40 border border-purple-200 dark:border-purple-800/40 text-purple-800 dark:text-purple-300 font-medium">B21: {JSON.stringify(currentStep.state_snapshot.quadrants.B21)}</div>
                          <div className="p-2 rounded bg-purple-50 dark:bg-purple-950/40 border border-purple-200 dark:border-purple-800/40 text-purple-800 dark:text-purple-300 font-medium">B22: {JSON.stringify(currentStep.state_snapshot.quadrants.B22)}</div>
                        </div>
                      </div>
                    </div>
                  </div>
                ) : isStorageOnTapes && currentStep?.state_snapshot?.tape_assignments ? (
                  /* Storage on Tapes MRT Timeline Visualizer */
                  <div className="py-3 space-y-3">
                    <span className="text-xs font-mono text-sky-600 dark:text-sky-400 block font-semibold">Magnetic Tape Allocation:</span>
                    {(currentStep.state_snapshot.tape_assignments as any[]).map((tape: any[], tIdx: number) => (
                      <div key={tIdx} className="p-3 rounded-lg bg-slate-50 dark:bg-slate-900 border border-slate-200 dark:border-slate-800 space-y-2">
                        <div className="flex items-center justify-between text-xs font-mono">
                          <span className="text-purple-700 dark:text-purple-300 font-semibold">Tape #{tIdx + 1}</span>
                          <span className="text-slate-500 dark:text-slate-400">{tape.length} programs allocated</span>
                        </div>
                        <div className="flex flex-wrap gap-2">
                          {tape.map((prog: any, pIdx: number) => (
                            <div key={pIdx} className="px-3 py-1.5 rounded bg-white dark:bg-[#080b11] border border-slate-200 dark:border-slate-700 text-xs font-mono text-slate-800 dark:text-white flex items-center gap-2 shadow-sm">
                              <span className="text-sky-600 dark:text-sky-400 font-semibold">{prog.name || `P${prog.id}`}</span>
                              <span className="text-slate-500 dark:text-slate-400 text-[10px]">len={prog.length}</span>
                            </div>
                          ))}
                        </div>
                      </div>
                    ))}
                  </div>
                ) : isJobSequencing && currentStep?.state_snapshot?.time_slots ? (
                  /* Job Sequencing Deadline Slots Visualizer */
                  <div className="py-3 space-y-3">
                    <span className="text-xs font-mono text-sky-600 dark:text-sky-400 block font-semibold">Scheduled Deadline Slots:</span>
                    <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
                      {(currentStep.state_snapshot.time_slots as any[]).map((job: any, slotIdx: number) => (
                        <div
                          key={slotIdx}
                          className={`p-3 rounded-lg border text-xs font-mono transition-colors ${
                            job
                              ? "bg-emerald-50 dark:bg-emerald-950/40 border-emerald-300 dark:border-emerald-500/40 text-emerald-900 dark:text-emerald-200 shadow-sm"
                              : "bg-slate-50 dark:bg-slate-900/60 border-slate-200 dark:border-slate-800 text-slate-400 dark:text-slate-500"
                          }`}
                        >
                          <div className="text-[10px] text-slate-500 dark:text-slate-400 mb-1">Slot #{slotIdx + 1}</div>
                          {job ? (
                            <div>
                              <div className="font-semibold text-slate-900 dark:text-white">{job.id}</div>
                              <div className="text-[11px] text-amber-600 dark:text-amber-300 font-medium">Profit: ${job.profit}</div>
                            </div>
                          ) : (
                            <div className="italic">Empty Slot</div>
                          )}
                        </div>
                      ))}
                    </div>
                  </div>
                ) : is1DArray || currentArray.length > 0 ? (
                  /* Array Bar Chart Canvas */
                  <div className="p-4 rounded-xl bg-slate-50/80 dark:bg-slate-950/60 border border-slate-200 dark:border-slate-800/80 shadow-sm dark:shadow-none transition-colors">
                    <div className="flex items-end justify-center gap-2 sm:gap-3 h-52 pb-2 pt-4 px-2">
                      {currentArray.map((val, idx) => {
                        const heightPercent = Math.max(12, Math.round((val / maxVal) * 100));
                        return (
                          <div key={idx} className="flex flex-col items-center gap-1.5 flex-1 max-w-[48px]">
                            <span className="text-[11px] font-mono font-medium text-slate-800 dark:text-slate-200">
                              {val}
                            </span>
                            <div
                              style={{ height: `${heightPercent}%` }}
                              className={`w-full rounded-t-md border transition-all duration-150 ${getBarColor(
                                idx
                              )}`}
                            />
                            <span className="text-[10px] font-mono text-slate-500">[{idx}]</span>
                          </div>
                        );
                      })}
                    </div>
                    {/* Color Code Legend */}
                    <div className="flex flex-wrap items-center justify-center gap-4 pt-3 border-t border-slate-200 dark:border-slate-800 text-[11px] font-mono text-slate-600 dark:text-slate-400">
                      <div className="flex items-center gap-1.5">
                        <span className="w-2.5 h-2.5 rounded bg-amber-400 ring-1 ring-amber-500" />
                        <span>Comparing</span>
                      </div>
                      <div className="flex items-center gap-1.5">
                        <span className="w-2.5 h-2.5 rounded bg-rose-500 ring-1 ring-rose-600" />
                        <span>Swapping / Pivot</span>
                      </div>
                      <div className="flex items-center gap-1.5">
                        <span className="w-2.5 h-2.5 rounded bg-purple-500 ring-1 ring-purple-600" />
                        <span>Selected</span>
                      </div>
                      <div className="flex items-center gap-1.5">
                        <span className="w-2.5 h-2.5 rounded bg-emerald-500 ring-1 ring-emerald-600" />
                        <span>Optimal / Bound</span>
                      </div>
                    </div>
                  </div>
                ) : is2DMatrix ? (
                  /* 2D Matrix / DP Tabulation Canvas */
                  <div className="py-4 overflow-x-auto">
                    <div className="inline-block min-w-full p-3 rounded-xl bg-slate-50 dark:bg-slate-950 border border-slate-200 dark:border-slate-800 shadow-sm dark:shadow-none transition-colors">
                      <table className="mx-auto border-collapse font-mono text-xs">
                        <tbody>
                          {((currentStep?.state_snapshot as any[][]) || []).map((row, rIdx) => (
                            <tr key={rIdx}>
                              {row.map((cell, cIdx) => {
                                const isCurrentCell =
                                  currentStep?.indices &&
                                  currentStep.indices[0] === rIdx &&
                                  currentStep.indices[1] === cIdx;
                                return (
                                  <td
                                    key={cIdx}
                                    className={`border p-2.5 sm:p-3 text-center min-w-[40px] transition-colors ${
                                      isCurrentCell
                                        ? "bg-sky-500/25 dark:bg-sky-500/40 text-sky-900 dark:text-white font-bold ring-2 ring-sky-500 border-sky-400"
                                        : cell === -1
                                        ? "bg-rose-50 dark:bg-rose-500/30 text-rose-600 dark:text-rose-300 font-bold border-rose-200 dark:border-slate-700"
                                        : cell > 0
                                        ? "bg-white dark:bg-slate-900 text-sky-800 dark:text-sky-200 border-slate-200 dark:border-slate-700 font-semibold"
                                        : "bg-slate-100/70 dark:bg-slate-900/60 text-slate-400 dark:text-slate-500 border-slate-200 dark:border-slate-700"
                                    }`}
                                  >
                                    {cell === 999999 ? "inf" : String(cell)}
                                  </td>
                                );
                              })}
                            </tr>
                          ))}
                        </tbody>
                      </table>
                    </div>
                  </div>
                ) : (
                  /* Structured Telemetry State Snapshot */
                  <div className="py-2">
                    <div className="p-4 rounded-lg bg-slate-50 dark:bg-slate-900/90 border border-slate-200 dark:border-slate-800 font-mono text-xs text-slate-800 dark:text-slate-200 max-h-56 overflow-y-auto shadow-sm dark:shadow-none transition-colors">
                      <div className="text-[11px] text-sky-600 dark:text-sky-400 mb-2 font-semibold">State Mutation Snapshot:</div>
                      <pre className="text-xs leading-relaxed overflow-x-auto bg-white dark:bg-slate-950/60 p-3 rounded-md border border-slate-200 dark:border-slate-800/80">
                        {JSON.stringify(
                          currentStep?.state_snapshot ?? executionResult?.output ?? {},
                          null,
                          2
                        )}
                      </pre>
                    </div>
                  </div>
                )}
              </div>
            </div>

            {/* Telemetry & Asymptotic Specs Panel */}
            <div className="space-y-4">
              {/* Live Instrumentation Card */}
              <Card headerTag="Execution Telemetry">
                <div className="space-y-2.5 font-mono text-xs">
                  <div className="p-3 rounded-lg bg-slate-50 dark:bg-slate-900/80 border border-slate-200 dark:border-slate-800 flex items-center justify-between transition-colors">
                    <span className="text-slate-600 dark:text-slate-400">Comparisons</span>
                    <span className="text-amber-600 dark:text-amber-400 font-semibold tabular-nums text-sm">
                      {executionResult?.metrics?.comparisons || 0}
                    </span>
                  </div>

                  <div className="p-3 rounded-lg bg-slate-50 dark:bg-slate-900/80 border border-slate-200 dark:border-slate-800 flex items-center justify-between transition-colors">
                    <span className="text-slate-600 dark:text-slate-400">Swaps / Moves</span>
                    <span className="text-rose-600 dark:text-rose-400 font-semibold tabular-nums text-sm">
                      {executionResult?.metrics?.swaps || 0}
                    </span>
                  </div>

                  <div className="p-3 rounded-lg bg-slate-50 dark:bg-slate-900/80 border border-slate-200 dark:border-slate-800 flex items-center justify-between transition-colors">
                    <span className="text-slate-600 dark:text-slate-400">Total Steps Traced</span>
                    <span className="text-sky-600 dark:text-sky-400 font-semibold tabular-nums text-sm">
                      {executionResult?.steps.length || 0}
                    </span>
                  </div>

                  <div className="p-3 rounded-lg bg-slate-50 dark:bg-slate-900/80 border border-slate-200 dark:border-slate-800 flex items-center justify-between transition-colors">
                    <span className="text-slate-600 dark:text-slate-400">Recursive Calls</span>
                    <span className="text-purple-600 dark:text-purple-400 font-semibold tabular-nums text-sm">
                      {executionResult?.metrics?.recursive_calls || 0}
                    </span>
                  </div>

                  <div className="p-3 rounded-lg bg-slate-50 dark:bg-slate-900/80 border border-slate-200 dark:border-slate-800 flex items-center justify-between transition-colors">
                    <span className="text-slate-600 dark:text-slate-400">Peak Heap Memory</span>
                    <span className="text-emerald-600 dark:text-emerald-400 font-semibold tabular-nums text-sm">
                      {(executionResult?.metrics?.peak_memory_kb || 0).toFixed(2)} KB
                    </span>
                  </div>
                </div>
              </Card>

              {/* Theoretical Specifications */}
              {algoDetails && (
                <Card
                  headerTag="Theoretical Asymptotics"
                  headerRight={
                    <Badge variant="default" mono size="sm">
                      {algoDetails.paradigm}
                    </Badge>
                  }
                >
                  <div className="space-y-2 font-mono text-xs">
                    <div className="flex justify-between py-1.5 border-b border-slate-200 dark:border-slate-800/80">
                      <span className="text-slate-600 dark:text-slate-400">Best Case:</span>
                      <span className="text-emerald-600 dark:text-emerald-400 font-semibold">{algoDetails.best_case || algoDetails.time_complexity_best}</span>
                    </div>
                    <div className="flex justify-between py-1.5 border-b border-slate-200 dark:border-slate-800/80">
                      <span className="text-slate-600 dark:text-slate-400">Average Case:</span>
                      <span className="text-sky-600 dark:text-sky-400 font-semibold">{algoDetails.average_case || algoDetails.time_complexity_average}</span>
                    </div>
                    <div className="flex justify-between py-1.5 border-b border-slate-200 dark:border-slate-800/80">
                      <span className="text-slate-600 dark:text-slate-400">Worst Case:</span>
                      <span className="text-amber-600 dark:text-amber-400 font-semibold">{algoDetails.worst_case || algoDetails.time_complexity_worst}</span>
                    </div>
                    <div className="flex justify-between py-1.5 border-b border-slate-200 dark:border-slate-800/80">
                      <span className="text-slate-600 dark:text-slate-400">Aux Space:</span>
                      <span className="text-purple-600 dark:text-purple-400 font-semibold">{algoDetails.space_complexity}</span>
                    </div>
                    {algoDetails.recurrence_relation && (
                      <div className="flex flex-col gap-1 py-1.5">
                        <span className="text-slate-600 dark:text-slate-400">Recurrence:</span>
                        <span className="text-slate-900 dark:text-slate-200 font-semibold text-[11px]">{algoDetails.recurrence_relation}</span>
                      </div>
                    )}
                  </div>
                </Card>
              )}

              {/* Quick Links */}
              <div className="p-3 rounded-xl bg-slate-50 dark:bg-slate-900/60 border border-slate-200 dark:border-slate-800 flex items-center justify-between text-xs font-mono shadow-sm dark:shadow-none transition-colors">
                <Link
                  to={`/complexity?algorithm=${selectedAlgoSlug}`}
                  className="text-sky-600 dark:text-sky-400 hover:text-sky-500 dark:hover:text-sky-300 transition-colors flex items-center gap-1 font-medium"
                >
                  <span>Complexity Analysis &rarr;</span>
                </Link>
                <Link
                  to={`/benchmarks?algorithm=${selectedAlgoSlug}`}
                  className="text-purple-600 dark:text-purple-400 hover:text-purple-500 dark:hover:text-purple-300 transition-colors flex items-center gap-1 font-medium"
                >
                  <span>Benchmark Arena &rarr;</span>
                </Link>
              </div>
            </div>
          </div>
        )}
      </div>
    </Layout>
  );
}

