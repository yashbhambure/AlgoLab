import { useState, useEffect } from "react";
import { useSearchParams, Link } from "react-router-dom";
import {
  Sparkles,
  Sliders,
  Award,
  CheckCircle2,
  XCircle,
  Info,
  ShieldAlert,
  Play,
  BarChart3,
  BookOpen,
  Activity,
} from "lucide-react";
import { Layout } from "../components/layout/Layout";
import { PageHeader } from "../components/layout/PageHeader";
import { Card } from "../components/common/Card";
import { Button } from "../components/common/Button";
import { Badge } from "../components/common/Badge";
import { LoadingState } from "../components/common/LoadingState";
import { api } from "../services/api";
import type { Algorithm, RecommendationResponse } from "../types";

const OBJECTIVES = [
  { id: "balanced", label: "Balanced Evaluation", desc: "25% Asymptotic, 25% Empirical, 20% Memory, 20% Input, 10% Constraints" },
  { id: "speed", label: "Maximum Throughput", desc: "35% Asymptotic Time, 35% Empirical Time, 10% Memory, 15% Input, 5% Constraints" },
  { id: "memory", label: "Minimal Heap Allocation", desc: "50% Space Complexity, 15% Asymptotic Time, 10% Empirical, 10% Input, 15% Constraints" },
  { id: "stability", label: "Stability & Invariance", desc: "40% Constraint Match, 20% Asymptotic Time, 15% Space, 15% Empirical" },
];

const PARADIGMS = [
  "All Curriculum",
  "Divide and Conquer",
  "Backtracking",
  "Dynamic Programming",
  "Greedy Method",
  "Branch and Bound",
];

export default function RecommendationPage() {
  const [searchParams] = useSearchParams();
  const [availableAlgorithms, setAvailableAlgorithms] = useState<Algorithm[]>([]);
  const [selectedParadigm, setSelectedParadigm] = useState("All Curriculum");
  const [selectedSlugs, setSelectedSlugs] = useState<string[]>([
    "0-1-knapsack-dp",
    "0-1-knapsack-lc-bb",
    "0-1-knapsack-fifo-bb",
  ]);

  // Objective & constraints
  const [objective, setObjective] = useState("balanced");
  const [requireStable, setRequireStable] = useState(false);
  const [requireInPlace, setRequireInPlace] = useState(false);

  // Input properties simulation
  const [inputSize, setInputSize] = useState(1000);
  const [sortedness, setSortedness] = useState<"random" | "nearly_sorted" | "reverse">("random");
  const [valRange, setValRange] = useState(1000);

  // Custom Weights
  const [useCustomWeights, setUseCustomWeights] = useState(false);
  const [wTheo, setWTheo] = useState(25);
  const [wEmp, setWEmp] = useState(25);
  const [wSpace, setWSpace] = useState(20);
  const [wInput, setWInput] = useState(20);
  const [wReq, setWReq] = useState(10);

  const [recommendationResult, setRecommendationResult] = useState<RecommendationResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  // Ingest candidates from search params if provided (e.g. from benchmark arena)
  useEffect(() => {
    const algosParam = searchParams.get("algos");
    if (algosParam) {
      const slugs = algosParam.split(",").map((s) => s.trim()).filter(Boolean);
      if (slugs.length > 0) {
        setSelectedSlugs(slugs);
      }
    }
  }, [searchParams]);

  useEffect(() => {
    const filter = selectedParadigm === "All Curriculum" ? undefined : { paradigm: selectedParadigm };
    api.getAlgorithms(filter)
      .then((algos) => {
        setAvailableAlgorithms(algos);
      })
      .catch((err) => console.error(err));
  }, [selectedParadigm]);

  const handleToggleSlug = (slug: string) => {
    if (selectedSlugs.includes(slug)) {
      if (selectedSlugs.length > 1) {
        setSelectedSlugs(selectedSlugs.filter((s) => s !== slug));
      }
    } else {
      setSelectedSlugs([...selectedSlugs, slug]);
    }
  };

  const handleSelectAllCandidates = () => {
    setSelectedSlugs(availableAlgorithms.map((a) => a.slug));
  };

  const handleEvaluate = async () => {
    setLoading(true);
    setError(null);

    try {
      let syntheticData: any = [];
      if (sortedness === "nearly_sorted") {
        syntheticData = Array.from({ length: inputSize }, (_, i) => i + (Math.random() < 0.1 ? Math.floor(Math.random() * 20) : 0));
      } else if (sortedness === "reverse") {
        syntheticData = Array.from({ length: inputSize }, (_, i) => inputSize - i);
      } else {
        syntheticData = Array.from({ length: inputSize }, () => Math.floor(Math.random() * valRange));
      }

      const customWeightsPayload = useCustomWeights
        ? {
            theo: wTheo / 100,
            emp: wEmp / 100,
            space: wSpace / 100,
            input: wInput / 100,
            req: wReq / 100,
          }
        : undefined;

      const res = await api.evaluateRecommendations({
        candidate_slugs: selectedSlugs,
        input_data: syntheticData,
        objective: objective,
        require_stable: requireStable,
        require_in_place: requireInPlace,
        custom_weights: customWeightsPayload,
      });

      setRecommendationResult(res);
    } catch (err: any) {
      setError(err.message || "Recommendation evaluation failed.");
    } finally {
      setLoading(false);
    }
  };

  const totalCustomWeight = wTheo + wEmp + wSpace + wInput + wReq;

  return (
    <Layout>
      <div className="space-y-6 animate-in fade-in duration-200">
        {/* Page Header */}
        <PageHeader
          breadcrumb="Decision Support"
          title="MCDA Algorithm Recommendation Engine"
          description="Multi-Criteria Decision Analysis ranking candidate algorithms across Asymptotic Bounds, Empirical Benchmarks, Auxiliary Memory, Input Distribution Fitness, and Strict Invariance Constraints."
          actions={
            <div className="flex items-center gap-2.5">
              <Button
                variant="primary"
                onClick={handleEvaluate}
                disabled={loading || selectedSlugs.length === 0}
                loading={loading}
                icon={<Sparkles className="w-4 h-4" />}
              >
                {loading ? "Evaluating MCDA Matrix..." : "Evaluate Candidates"}
              </Button>
            </div>
          }
        />

        {/* Configuration Matrix */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-5">
          {/* Candidates & Paradigm */}
          <div className="lg:col-span-2 space-y-4">
            <Card
              headerTag="Candidate Selection"
              headerRight={
                <div className="flex items-center gap-2">
                  <button
                    onClick={handleSelectAllCandidates}
                    className="text-[11px] font-mono text-sky-400 hover:text-sky-300 transition-colors"
                  >
                    Select All in View
                  </button>
                  <span className="text-slate-600">&bull;</span>
                  <Badge variant="primary" mono size="sm">
                    {selectedSlugs.length} Selected
                  </Badge>
                </div>
              }
            >
              <div className="space-y-4">
                {/* Paradigm Switcher */}
                <div className="flex items-center gap-1.5 overflow-x-auto pb-1 scrollbar-thin">
                  {PARADIGMS.map((p) => {
                    const active = selectedParadigm === p;
                    return (
                      <button
                        key={p}
                        onClick={() => setSelectedParadigm(p)}
                        className={`px-3 py-1.5 rounded-lg text-xs font-medium whitespace-nowrap transition-colors ${
                          active
                            ? "bg-sky-500/15 text-sky-400 border border-sky-500/30 font-semibold"
                            : "bg-slate-900/60 border border-slate-800 text-slate-400 hover:text-slate-200 hover:border-slate-700"
                        }`}
                      >
                        {p}
                      </button>
                    );
                  })}
                </div>

                {/* Candidate Checklist */}
                <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-2 max-h-72 overflow-y-auto pr-1">
                  {availableAlgorithms.map((algo) => {
                    const isSelected = selectedSlugs.includes(algo.slug);
                    return (
                      <button
                        key={algo.slug}
                        onClick={() => handleToggleSlug(algo.slug)}
                        className={`p-2.5 rounded-lg text-left border text-xs transition-colors flex items-center justify-between ${
                          isSelected
                            ? "bg-sky-500/10 border-sky-500/30 text-white font-medium"
                            : "bg-slate-900/60 border-slate-800 text-slate-400 hover:text-slate-200 hover:border-slate-700"
                        }`}
                      >
                        <div className="truncate pr-1.5">
                          <div className="font-semibold text-slate-200 truncate">{algo.name}</div>
                          <div className="text-[10px] text-slate-400 font-mono truncate">{algo.category || algo.paradigm}</div>
                        </div>
                        {isSelected ? (
                          <CheckCircle2 className="w-4 h-4 text-sky-400 flex-shrink-0" />
                        ) : (
                          <XCircle className="w-4 h-4 text-slate-600 flex-shrink-0" />
                        )}
                      </button>
                    );
                  })}
                </div>
              </div>
            </Card>

            {/* Input Profile Simulation & Strict Constraints */}
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
              <Card headerTag="Input Profile Simulation">
                <div className="space-y-3 font-sans text-xs">
                  <div>
                    <label className="text-[11px] font-mono text-slate-400 block mb-1">
                      Input Size (N)
                    </label>
                    <input
                      type="number"
                      min="10"
                      max="100000"
                      step="100"
                      value={inputSize}
                      onChange={(e) => setInputSize(Number(e.target.value))}
                      className="w-full px-3 py-1.5 rounded-lg bg-slate-900 border border-slate-800 text-xs font-mono text-white focus:outline-none focus:border-sky-500"
                    />
                  </div>

                  <div>
                    <label className="text-[11px] font-mono text-slate-400 block mb-1">
                      Sortedness / Pattern
                    </label>
                    <select
                      value={sortedness}
                      onChange={(e: any) => setSortedness(e.target.value)}
                      className="w-full px-3 py-1.5 rounded-lg bg-slate-900 border border-slate-800 text-xs text-white focus:outline-none focus:border-sky-500"
                    >
                      <option value="random">Random Uniform</option>
                      <option value="nearly_sorted">Nearly Sorted (90%+ sorted)</option>
                      <option value="reverse">Strictly Reverse Sorted</option>
                    </select>
                  </div>

                  <div>
                    <label className="text-[11px] font-mono text-slate-400 block mb-1">
                      Key Boundary Range (K)
                    </label>
                    <input
                      type="number"
                      value={valRange}
                      onChange={(e) => setValRange(Number(e.target.value))}
                      className="w-full px-3 py-1.5 rounded-lg bg-slate-900 border border-slate-800 text-xs font-mono text-white focus:outline-none focus:border-sky-500"
                    />
                  </div>
                </div>
              </Card>

              <Card headerTag="Strict Invariance Constraints">
                <div className="space-y-2.5 font-sans text-xs">
                  <div
                    onClick={() => setRequireStable(!requireStable)}
                    className={`p-3 rounded-lg border cursor-pointer transition-colors flex items-center justify-between ${
                      requireStable
                        ? "bg-purple-500/10 border-purple-500/30 text-white font-medium"
                        : "bg-slate-900/60 border-slate-800 text-slate-400 hover:text-slate-200"
                    }`}
                  >
                    <div>
                      <div className="font-semibold text-slate-200">Require Stability</div>
                      <div className="text-[11px] text-slate-400">Preserve relative key order</div>
                    </div>
                    {requireStable ? (
                      <CheckCircle2 className="w-4 h-4 text-purple-400" />
                    ) : (
                      <XCircle className="w-4 h-4 text-slate-600" />
                    )}
                  </div>

                  <div
                    onClick={() => setRequireInPlace(!requireInPlace)}
                    className={`p-3 rounded-lg border cursor-pointer transition-colors flex items-center justify-between ${
                      requireInPlace
                        ? "bg-sky-500/10 border-sky-500/30 text-white font-medium"
                        : "bg-slate-900/60 border-slate-800 text-slate-400 hover:text-slate-200"
                    }`}
                  >
                    <div>
                      <div className="font-semibold text-slate-200">Require In-Place</div>
                      <div className="text-[11px] text-slate-400">O(1) auxiliary space strictly required</div>
                    </div>
                    {requireInPlace ? (
                      <CheckCircle2 className="w-4 h-4 text-sky-400" />
                    ) : (
                      <XCircle className="w-4 h-4 text-slate-600" />
                    )}
                  </div>
                </div>
              </Card>
            </div>
          </div>

          {/* Objective & Weights */}
          <div>
            <Card
              headerTag="Optimization Objective"
              headerRight={
                useCustomWeights && (
                  <Badge variant={totalCustomWeight === 100 ? "success" : "warning"} mono size="sm">
                    {totalCustomWeight}% Weight
                  </Badge>
                )
              }
            >
              <div className="space-y-2.5 font-sans text-xs">
                {OBJECTIVES.map((obj) => {
                  const active = objective === obj.id && !useCustomWeights;
                  return (
                    <div
                      key={obj.id}
                      onClick={() => {
                        setObjective(obj.id);
                        setUseCustomWeights(false);
                      }}
                      className={`p-3 rounded-lg border cursor-pointer transition-colors ${
                        active
                          ? "bg-amber-500/10 border-amber-500/30 text-white font-medium"
                          : "bg-slate-900/60 border-slate-800 text-slate-400 hover:text-slate-200 hover:border-slate-700"
                      }`}
                    >
                      <div className="font-semibold text-amber-300">{obj.label}</div>
                      <div className="text-[11px] text-slate-400 mt-0.5">{obj.desc}</div>
                    </div>
                  );
                })}

                {/* Custom Weights Drawer */}
                <div className="pt-2 border-t border-slate-800">
                  <button
                    onClick={() => setUseCustomWeights(!useCustomWeights)}
                    className={`w-full p-2.5 rounded-lg border text-xs font-mono transition-colors flex items-center justify-between ${
                      useCustomWeights
                        ? "bg-sky-500/15 border-sky-500/30 text-sky-400 font-semibold"
                        : "bg-slate-900/60 border-slate-800 text-slate-400 hover:text-slate-200"
                    }`}
                  >
                    <span>Custom Weight Allocation</span>
                    <Sliders className="w-3.5 h-3.5" />
                  </button>

                  {useCustomWeights && (
                    <div className="space-y-2.5 pt-3 text-[11px] font-mono">
                      <div>
                        <div className="flex justify-between text-slate-400 mb-1">
                          <span>Theoretical Bounds</span>
                          <span className="text-sky-400">{wTheo}%</span>
                        </div>
                        <input type="range" min="0" max="100" value={wTheo} onChange={(e) => setWTheo(Number(e.target.value))} className="w-full accent-sky-400" />
                      </div>
                      <div>
                        <div className="flex justify-between text-slate-400 mb-1">
                          <span>Empirical Speed</span>
                          <span className="text-blue-400">{wEmp}%</span>
                        </div>
                        <input type="range" min="0" max="100" value={wEmp} onChange={(e) => setWEmp(Number(e.target.value))} className="w-full accent-blue-400" />
                      </div>
                      <div>
                        <div className="flex justify-between text-slate-400 mb-1">
                          <span>Memory Efficiency</span>
                          <span className="text-purple-400">{wSpace}%</span>
                        </div>
                        <input type="range" min="0" max="100" value={wSpace} onChange={(e) => setWSpace(Number(e.target.value))} className="w-full accent-purple-400" />
                      </div>
                      <div>
                        <div className="flex justify-between text-slate-400 mb-1">
                          <span>Input Distribution Fit</span>
                          <span className="text-emerald-400">{wInput}%</span>
                        </div>
                        <input type="range" min="0" max="100" value={wInput} onChange={(e) => setWInput(Number(e.target.value))} className="w-full accent-emerald-400" />
                      </div>
                      <div>
                        <div className="flex justify-between text-slate-400 mb-1">
                          <span>Strict Constraints</span>
                          <span className="text-amber-400">{wReq}%</span>
                        </div>
                        <input type="range" min="0" max="100" value={wReq} onChange={(e) => setWReq(Number(e.target.value))} className="w-full accent-amber-400" />
                      </div>
                    </div>
                  )}
                </div>
              </div>
            </Card>
          </div>
        </div>

        {/* Global Error */}
        {error && (
          <div className="p-4 rounded-xl bg-rose-500/10 border border-rose-500/30 text-rose-300 font-mono text-xs">
            {error}
          </div>
        )}

        {/* Loading State */}
        {loading && (
          <div className="p-12 rounded-xl bg-[#0e131f] border border-slate-800 text-center">
            <LoadingState message="Executing MCDA composite weight evaluation across all candidates..." />
          </div>
        )}

        {/* Recommendation Results */}
        {recommendationResult && !loading && (
          <div className="space-y-5">
            {/* Top Recommended Outcome Card */}
            <Card
              headerTag="MCDA Recommended Algorithm"
              headerRight={
                <Badge variant="success" mono size="md">
                  Rank #1 Champion
                </Badge>
              }
            >
              <div className="space-y-4">
                <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 border-b border-slate-800 pb-4">
                  <div>
                    <div className="flex items-center gap-2 text-xs font-mono text-emerald-400 mb-1">
                      <Award className="w-4 h-4" />
                      <span>Optimal Multi-Criteria Selection</span>
                    </div>
                    <h2 className="text-2xl sm:text-3xl font-semibold text-white tracking-tight">
                      {recommendationResult.recommended_name}
                    </h2>
                  </div>

                  <div className="flex sm:flex-col items-baseline sm:items-end gap-2 sm:gap-0 flex-shrink-0">
                    <div className="text-3xl sm:text-4xl font-semibold text-emerald-400 font-mono">
                      {recommendationResult.winning_score}
                      <span className="text-xs text-slate-500 font-normal"> / 100</span>
                    </div>
                    <span className="text-[11px] font-mono text-slate-400">MCDA Composite Score</span>
                  </div>
                </div>

                <p className="text-sm text-slate-300 leading-relaxed font-sans">
                  {recommendationResult.explanation.summary}
                </p>

                {/* Academic Reasoning Pillars */}
                <div className="grid grid-cols-1 md:grid-cols-3 gap-3 pt-2">
                  <div className="p-3 rounded-lg bg-slate-900/70 border border-slate-800 space-y-1.5">
                    <div className="flex items-center gap-1.5 text-xs font-mono text-sky-400">
                      <BookOpen className="w-3.5 h-3.5" />
                      <span>Formal Theoretical Reasoning</span>
                    </div>
                    <p className="text-xs text-slate-300 leading-relaxed">
                      {recommendationResult.explanation.formal_theoretical_reasoning || "Asymptotic scaling verified against upper/lower complexity bounds."}
                    </p>
                  </div>

                  <div className="p-3 rounded-lg bg-slate-900/70 border border-slate-800 space-y-1.5">
                    <div className="flex items-center gap-1.5 text-xs font-mono text-emerald-400">
                      <Activity className="w-3.5 h-3.5" />
                      <span>Practical Heuristic Reasoning</span>
                    </div>
                    <p className="text-xs text-slate-300 leading-relaxed">
                      {recommendationResult.explanation.practical_heuristic_reasoning || "Dataset operational characteristics evaluated under heuristic thresholds."}
                    </p>
                  </div>

                  <div className="p-3 rounded-lg bg-slate-900/70 border border-slate-800 space-y-1.5">
                    <div className="flex items-center gap-1.5 text-xs font-mono text-purple-400">
                      <BarChart3 className="w-3.5 h-3.5" />
                      <span>Empirical Benchmark Evidence</span>
                    </div>
                    <p className="text-xs text-slate-300 leading-relaxed">
                      {recommendationResult.explanation.empirical_benchmark_evidence || "Empirical benchmark timings referenced or theoretical proxy applied."}
                    </p>
                  </div>
                </div>

                {/* Key Advantages Matrix */}
                <div className="pt-3 border-t border-slate-800 grid grid-cols-1 sm:grid-cols-2 gap-3">
                  {recommendationResult.explanation.key_advantages.map((adv, i) => (
                    <div key={i} className="flex items-start gap-2.5 text-xs text-slate-300">
                      <CheckCircle2 className="w-4 h-4 text-emerald-400 flex-shrink-0 mt-0.5" />
                      <span className="flex-1 min-w-0 leading-relaxed font-sans text-slate-300 break-words">{adv}</span>
                    </div>
                  ))}
                </div>

                {/* Direct Action Deep Links */}
                <div className="flex flex-wrap items-center gap-3 pt-3 border-t border-slate-800">
                  <Link to={`/visualizer?algo=${recommendationResult.recommended_algorithm}`}>
                    <Button variant="primary" size="sm" icon={<Play className="w-3.5 h-3.5" />}>
                      Visualize Algorithm
                    </Button>
                  </Link>

                  <Link to={`/complexity?algo=${recommendationResult.recommended_algorithm}`}>
                    <Button variant="secondary" size="sm" icon={<BookOpen className="w-3.5 h-3.5" />}>
                      Analyze Complexity
                    </Button>
                  </Link>

                  <Link to={`/benchmark?algos=${recommendationResult.recommended_algorithm}`}>
                    <Button variant="ghost" size="sm" icon={<BarChart3 className="w-3.5 h-3.5" />}>
                      Benchmark Arena
                    </Button>
                  </Link>
                </div>
              </div>
            </Card>

            {/* Candidate Rankings & Multi-Criteria Score Breakdown */}
            <Card headerTag="Candidate Rankings & Multi-Criteria Breakdown">
              <div className="overflow-x-auto -mx-5 -mb-5">
                <table className="w-full text-left font-mono text-xs">
                  <thead className="border-b border-slate-800 bg-[#141b2d] text-[10px] text-slate-400 uppercase tracking-wider">
                    <tr>
                      <th className="py-3 px-4">Rank</th>
                      <th className="py-3 px-4">Algorithm</th>
                      <th className="py-3 px-4 text-emerald-400 font-semibold">Total Score</th>
                      <th className="py-3 px-4 text-sky-400">Theoretical</th>
                      <th className="py-3 px-4 text-purple-400">Space</th>
                      <th className="py-3 px-4 text-amber-400">Input Fit</th>
                      <th className="py-3 px-4">Constraints</th>
                      <th className="py-3 px-4">Properties</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-slate-800/60 text-slate-300">
                    {recommendationResult.rankings.map((item, idx) => (
                      <tr
                        key={item.algorithm_slug}
                        className={`hover:bg-slate-900/40 transition-colors ${
                          idx === 0 ? "bg-emerald-500/5 font-semibold text-white" : ""
                        }`}
                      >
                        <td className="py-3 px-4">
                          {idx === 0 ? (
                            <Badge variant="success" mono size="sm">#1 Pick</Badge>
                          ) : (
                            `#${idx + 1}`
                          )}
                        </td>
                        <td className="py-3 px-4 font-semibold text-white">
                          {item.algorithm_name}
                          <span className="block text-[10px] text-slate-400 font-normal">
                            {item.complexities.average} &bull; {item.complexities.space}
                          </span>
                        </td>
                        <td className="py-3 px-4 text-emerald-400 font-semibold text-sm tabular-nums">
                          {item.score}
                        </td>
                        <td className="py-3 px-4 text-sky-300 tabular-nums">{item.breakdown.theoretical_score}</td>
                        <td className="py-3 px-4 text-purple-300 tabular-nums">{item.breakdown.space_score}</td>
                        <td className="py-3 px-4 text-amber-300 tabular-nums">{item.breakdown.input_suitability_score}</td>
                        <td className="py-3 px-4 tabular-nums">{item.breakdown.requirements_score}</td>
                        <td className="py-3 px-4">
                          <div className="flex items-center gap-2 text-[10px]">
                            <span className={item.is_stable ? "text-emerald-400" : "text-slate-500"}>
                              {item.is_stable ? "Stable" : "Unstable"}
                            </span>
                            <span>&bull;</span>
                            <span className={item.is_in_place ? "text-emerald-400" : "text-slate-500"}>
                              {item.is_in_place ? "In-Place" : "Out-of-Place"}
                            </span>
                          </div>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </Card>

            {/* Disqualified or Penalized Candidates */}
            {recommendationResult.explanation.disqualified_or_penalized &&
              recommendationResult.explanation.disqualified_or_penalized.length > 0 && (
                <Card headerTag="Constraint Penalties & Disqualifications">
                  <div className="space-y-2">
                    {recommendationResult.explanation.disqualified_or_penalized.map((disq, idx) => (
                      <div key={idx} className="p-3 rounded-lg bg-slate-900 border border-slate-800/80 flex items-start gap-2.5 text-xs font-mono">
                        <ShieldAlert className="w-4 h-4 text-amber-400 flex-shrink-0 mt-0.5" />
                        <div>
                          <span className="font-semibold text-white">{disq.algorithm}: </span>
                          <span className="text-slate-300">{disq.reasons.join("; ")}</span>
                        </div>
                      </div>
                    ))}
                  </div>
                </Card>
              )}

            {/* Runner-Up & Trade-off Notes */}
            {recommendationResult.explanation.runner_up_comparison && (
              <Card headerTag="Runner-Up Trade-Off Analysis">
                <div className="flex items-start gap-2.5 text-xs text-slate-300 font-sans">
                  <Info className="w-4 h-4 text-sky-400 flex-shrink-0 mt-0.5" />
                  <p className="leading-relaxed">
                    {recommendationResult.explanation.runner_up_comparison}
                  </p>
                </div>
              </Card>
            )}
          </div>
        )}
      </div>
    </Layout>
  );
}
