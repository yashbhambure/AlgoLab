import { useState, useEffect } from "react";
import { useParams, Link } from "react-router-dom";
import {
  ArrowLeft,
  Play,
  BarChart3,
  Sigma,
  Sparkles,
  Code2,
  Copy,
  Check,
  CheckCircle2,
  XCircle,
  Layers,
  GraduationCap,
  Cpu,
} from "lucide-react";
import { Layout } from "../components/layout/Layout";
import { PageHeader } from "../components/layout/PageHeader";
import { Card } from "../components/common/Card";
import { Button } from "../components/common/Button";
import { Badge } from "../components/common/Badge";
import { LoadingState } from "../components/common/LoadingState";
import { EmptyState } from "../components/common/EmptyState";
import { AlgorithmTradeoffs } from "../components/algorithm/AlgorithmTradeoffs";
import { api } from "../services/api";
import type { AlgorithmDetailData, ProblemDetailData, ApplicableAlgorithm, CurriculumModule } from "../types";

export default function AlgorithmDetailPage() {
  const { slug } = useParams<{ slug: string }>();

  const [algorithm, setAlgorithm] = useState<AlgorithmDetailData | null>(null);
  const [codeData, setCodeData] = useState<{ pseudocode?: string; c_source_code?: string; implementation_python?: string; daa_concept_notes?: string } | null>(null);
  const [canonicalProblem, setCanonicalProblem] = useState<ProblemDetailData | null>(null);
  const [siblingAlgorithms, setSiblingAlgorithms] = useState<ApplicableAlgorithm[]>([]);
  const [curriculumModule, setCurriculumModule] = useState<CurriculumModule | null>(null);
  const [curriculumSlugs, setCurriculumSlugs] = useState<Set<string>>(new Set());

  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [activeCodeTab, setActiveCodeTab] = useState<"c" | "pseudocode">("c");
  const [copiedCode, setCopiedCode] = useState(false);

  useEffect(() => {
    if (!slug) return;
    setLoading(true);
    setError(null);

    Promise.all([
      api.getAlgorithmDetail(slug),
      api.getAlgorithmCode(slug).catch(() => null),
      api.getApprovedCurriculumSlugs().catch(() => [] as string[]),
      api.getCurriculumModules().catch(() => [] as CurriculumModule[]),
      api.getProblems().catch(() => []),
    ])
      .then(async ([algoData, codeRes, approvedSlugs, modules, allProblems]) => {
        setAlgorithm(algoData);
        if (codeRes) setCodeData(codeRes);
        setCurriculumSlugs(new Set(approvedSlugs));

        // Find associated curriculum module if any
        let foundMod: CurriculumModule | null = null;
        for (const m of modules) {
          for (const t of m.topics || []) {
            if (
              t.algorithm_slug === slug ||
              (t.algorithm_slugs && t.algorithm_slugs.includes(slug))
            ) {
              foundMod = m;
              break;
            }
          }
          if (foundMod) break;
        }
        setCurriculumModule(foundMod);

        // Find canonical problem for this algorithm
        for (const p of allProblems) {
          try {
            const probDetail = await api.getProblemDetail(p.slug);
            const hasAlgo = probDetail.applicable_algorithms?.some((a) => a.slug === slug);
            if (hasAlgo) {
              setCanonicalProblem(probDetail);
              const siblings = probDetail.applicable_algorithms.filter((a) => a.slug !== slug);
              setSiblingAlgorithms(siblings);
              break;
            }
          } catch {
            // Ignore single problem lookup failure
          }
        }
      })
      .catch((err) => {
        console.error("Failed to load algorithm detail:", err);
        setError(err.message || `Algorithm '${slug}' not found.`);
      })
      .finally(() => setLoading(false));
  }, [slug]);

  const handleCopy = (text?: string) => {
    if (!text) return;
    navigator.clipboard.writeText(text);
    setCopiedCode(true);
    setTimeout(() => setCopiedCode(false), 2000);
  };

  if (loading) {
    return (
      <Layout>
        <div className="py-24">
          <LoadingState message={`Loading specification for '${slug}'...`} />
        </div>
      </Layout>
    );
  }

  if (error || !algorithm) {
    return (
      <Layout>
        <div className="space-y-6">
          <PageHeader
            breadcrumb="Algorithm Specifications"
            title="Algorithm Not Found"
            description="The requested algorithm does not exist in the DAA registry."
          />
          <EmptyState
            title="Algorithm not found"
            message={error || `No algorithm matching '${slug}' was found.`}
            action={
              <Link to="/catalog">
                <Button variant="secondary" icon={<ArrowLeft className="w-4 h-4" />}>
                  Back to Catalog
                </Button>
              </Link>
            }
          />
        </div>
      </Layout>
    );
  }

  const isCurriculum = curriculumSlugs.has(algorithm.slug);
  const bestCase = algorithm.best_case || algorithm.time_complexity_best || "Not documented";
  const avgCase = algorithm.average_case || algorithm.time_complexity_average || "Not documented";
  const worstCase = algorithm.worst_case || algorithm.time_complexity_worst || "Not documented";
  const spaceComp = algorithm.space_complexity || "Not documented";
  const cSource =
    codeData?.c_source_code ||
    algorithm.c_source_code ||
    `/* C implementation for ${algorithm.name}\n * Standard C11 source code\n */`;
  const pseudocodeSource =
    codeData?.pseudocode ||
    algorithm.pseudocode ||
    `// Formal pseudocode for ${algorithm.name}`;
  const conceptNotes =
    codeData?.daa_concept_notes ||
    algorithm.daa_concept_notes ||
    null;

  return (
    <Layout>
      <div className="space-y-8 animate-in fade-in duration-200">
        {/* Navigation Breadcrumb */}
        <div className="flex items-center justify-between">
          <Link
            to="/catalog"
            className="inline-flex items-center gap-1.5 text-xs font-mono text-slate-400 hover:text-white transition-colors"
          >
            <ArrowLeft className="w-3.5 h-3.5" />
            <span>Algorithm Catalog</span>
          </Link>

          <div className="flex items-center gap-2">
            {curriculumModule && (
              <Link to={`/curriculum/${curriculumModule.module_id}`}>
                <span className="px-2.5 py-1 rounded text-xs font-mono text-sky-400 bg-sky-950/40 border border-sky-800/40 hover:bg-sky-900/50 transition-colors flex items-center gap-1.5">
                  <GraduationCap className="w-3.5 h-3.5" />
                  <span>Module {curriculumModule.module_id}: {curriculumModule.short_name}</span>
                </span>
              </Link>
            )}

            {canonicalProblem && (
              <Link to={`/problems/${canonicalProblem.slug}`}>
                <span className="px-2.5 py-1 rounded text-xs font-mono text-emerald-400 bg-emerald-950/40 border border-emerald-800/40 hover:bg-emerald-900/50 transition-colors flex items-center gap-1.5">
                  <Layers className="w-3.5 h-3.5" />
                  <span>{canonicalProblem.name || canonicalProblem.title || canonicalProblem.slug}</span>
                </span>
              </Link>
            )}
          </div>
        </div>

        {/* Identity Page Header */}
        <PageHeader
          breadcrumb={algorithm.paradigm}
          title={algorithm.name}
          description={algorithm.description}
          actions={
            <div className="flex flex-wrap items-center gap-2">
              {isCurriculum ? (
                <span className="px-3 py-1 rounded-md text-xs font-mono font-medium bg-emerald-500/15 text-emerald-400 border border-emerald-500/30">
                  Curriculum Module
                </span>
              ) : (
                <span className="px-3 py-1 rounded-md text-xs font-mono font-medium bg-slate-800/80 text-slate-400 border border-slate-700/60">
                  Supplementary Algorithm
                </span>
              )}
              <Badge variant="default" mono size="md">
                {algorithm.category}
              </Badge>
            </div>
          }
        />

        {/* Action Bar (Deep Links) */}
        <div className="p-4 rounded-xl bg-[#0e131f] border border-slate-800 flex flex-wrap items-center justify-between gap-3">
          <div className="flex items-center gap-2 text-xs font-mono text-slate-400">
            <Cpu className="w-4 h-4 text-sky-400" />
            <span>Interactive Laboratory Actions:</span>
          </div>

          <div className="flex flex-wrap items-center gap-2.5">
            <Link to={`/visualizer?algo=${algorithm.slug}`}>
              <Button variant="primary" icon={<Play className="w-4 h-4" />}>
                Visualize Execution
              </Button>
            </Link>

            <Link to={`/benchmark?algos=${algorithm.slug}`}>
              <Button variant="secondary" icon={<BarChart3 className="w-4 h-4" />}>
                Benchmark Arena
              </Button>
            </Link>

            <Link to={`/complexity?algorithm=${algorithm.slug}`}>
              <Button variant="ghost" icon={<Sigma className="w-4 h-4" />}>
                Complexity Analysis
              </Button>
            </Link>

            <Link to="/recommend">
              <Button variant="ghost" icon={<Sparkles className="w-4 h-4" />}>
                MCDA Ranking
              </Button>
            </Link>
          </div>
        </div>

        {/* Asymptotic Complexity & Recurrence Matrix */}
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          <Card className="p-4 space-y-1 bg-slate-900/60 border-slate-800">
            <span className="text-[11px] font-mono text-slate-400 uppercase tracking-wider block">
              Best Case Time
            </span>
            <div className="text-lg font-bold font-mono text-emerald-400">
              {bestCase}
            </div>
            <span className="text-[10px] text-slate-400 block">Lower bound asymptotic time</span>
          </Card>

          <Card className="p-4 space-y-1 bg-slate-900/60 border-slate-800">
            <span className="text-[11px] font-mono text-slate-400 uppercase tracking-wider block">
              Average Case Time
            </span>
            <div className="text-lg font-bold font-mono text-sky-400">
              {avgCase}
            </div>
            <span className="text-[10px] text-slate-400 block">Expected execution complexity</span>
          </Card>

          <Card className="p-4 space-y-1 bg-slate-900/60 border-slate-800">
            <span className="text-[11px] font-mono text-slate-400 uppercase tracking-wider block">
              Worst Case Time
            </span>
            <div className="text-lg font-bold font-mono text-amber-400">
              {worstCase}
            </div>
            <span className="text-[10px] text-slate-400 block">Upper bound asymptotic growth</span>
          </Card>

          <Card className="p-4 space-y-1 bg-slate-900/60 border-slate-800">
            <span className="text-[11px] font-mono text-slate-400 uppercase tracking-wider block">
              Auxiliary Space
            </span>
            <div className="text-lg font-bold font-mono text-purple-400">
              {spaceComp}
            </div>
            <span className="text-[10px] text-slate-400 block">Additional memory allocation</span>
          </Card>
        </div>

        {/* Recurrence Relation (if present in authoritative metadata) */}
        {algorithm.recurrence_relation && (
          <div className="p-4 rounded-xl bg-slate-900/80 border border-slate-800 flex flex-col sm:flex-row sm:items-center justify-between gap-3">
            <div className="flex items-center gap-2.5">
              <Sigma className="w-4 h-4 text-emerald-400" />
              <span className="text-xs font-mono text-slate-300 font-semibold">
                Recurrence Relation:
              </span>
            </div>
            <code className="text-xs font-mono font-bold text-emerald-300 bg-emerald-950/40 px-3 py-1 rounded-lg border border-emerald-800/40">
              {algorithm.recurrence_relation}
            </code>
          </div>
        )}

        {/* Algorithmic Properties & Behavioral Characteristics */}
        <Card className="space-y-3">
          <div className="text-xs font-mono text-slate-400 uppercase tracking-wider border-b border-slate-800/80 pb-2">
            Algorithmic Invariants & Operational Properties
          </div>
          <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 text-xs font-mono">
            <div className="p-3 rounded-lg bg-slate-900/70 border border-slate-800 flex items-center justify-between">
              <span className="text-slate-400">Stability:</span>
              <span className={`font-semibold flex items-center gap-1 ${algorithm.is_stable ? "text-emerald-400" : "text-slate-400"}`}>
                {algorithm.is_stable ? <CheckCircle2 className="w-3.5 h-3.5" /> : <XCircle className="w-3.5 h-3.5" />}
                {algorithm.is_stable ? "Stable" : "Unstable"}
              </span>
            </div>

            <div className="p-3 rounded-lg bg-slate-900/70 border border-slate-800 flex items-center justify-between">
              <span className="text-slate-400">In-Place:</span>
              <span className={`font-semibold flex items-center gap-1 ${algorithm.is_in_place ? "text-emerald-400" : "text-slate-400"}`}>
                {algorithm.is_in_place ? <CheckCircle2 className="w-3.5 h-3.5" /> : <XCircle className="w-3.5 h-3.5" />}
                {algorithm.is_in_place ? "Yes (O(1))" : "No"}
              </span>
            </div>

            <div className="p-3 rounded-lg bg-slate-900/70 border border-slate-800 flex items-center justify-between">
              <span className="text-slate-400">Adaptive:</span>
              <span className={`font-semibold flex items-center gap-1 ${algorithm.is_adaptive ? "text-emerald-400" : "text-slate-400"}`}>
                {algorithm.is_adaptive ? <CheckCircle2 className="w-3.5 h-3.5" /> : <XCircle className="w-3.5 h-3.5" />}
                {algorithm.is_adaptive ? "Yes" : "No"}
              </span>
            </div>

            <div className="p-3 rounded-lg bg-slate-900/70 border border-slate-800 flex items-center justify-between">
              <span className="text-slate-400">Deterministic:</span>
              <span className={`font-semibold flex items-center gap-1 ${algorithm.is_deterministic !== false ? "text-emerald-400" : "text-amber-400"}`}>
                {algorithm.is_deterministic !== false ? <CheckCircle2 className="w-3.5 h-3.5" /> : <XCircle className="w-3.5 h-3.5" />}
                {algorithm.is_deterministic !== false ? "Deterministic" : "Randomized"}
              </span>
            </div>
          </div>
        </Card>

        {/* Theoretical Notes & Academic Insights */}
        {conceptNotes && (
          <div className="p-5 rounded-xl bg-[#0e131f] border border-slate-800 space-y-2">
            <div className="flex items-center gap-2 text-xs font-mono font-semibold text-sky-400">
              <Sparkles className="w-4 h-4" />
              <span>DAA Concept & Theoretical Mechanics:</span>
            </div>
            <p className="text-xs text-slate-300 leading-relaxed font-sans whitespace-pre-line">
              {conceptNotes}
            </p>
          </div>
        )}

        {/* Tradeoffs: Advantages, Disadvantages, Suitability */}
        <AlgorithmTradeoffs
          advantages={algorithm.advantages}
          suitableCases={algorithm.suitable_cases}
          disadvantages={algorithm.disadvantages}
          unsuitableCases={algorithm.unsuitable_cases}
        />

        {/* Sibling Implementations (Multi-Implementation Comparison) */}
        {siblingAlgorithms.length > 0 && canonicalProblem && (
          <div className="p-5 rounded-xl bg-[#0e131f] border border-sky-900/40 space-y-4">
            <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2 border-b border-slate-800/80 pb-3">
              <div className="space-y-0.5">
                <span className="text-[11px] font-mono font-semibold text-sky-400 uppercase tracking-wider">
                  Sibling Implementations for Canonical Problem:
                </span>
                <h3 className="text-base font-bold text-white tracking-tight">
                  {canonicalProblem.name || canonicalProblem.title}
                </h3>
              </div>

              <Link to={`/problems/${canonicalProblem.slug}`}>
                <Button variant="secondary" size="sm" icon={<Layers className="w-3.5 h-3.5" />}>
                  Compare All in Problem View
                </Button>
              </Link>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-3">
              {siblingAlgorithms.map((sibling) => (
                <Card
                  key={sibling.slug}
                  className="p-3.5 space-y-2.5 bg-slate-900/70 hover:border-slate-700 transition-colors flex flex-col justify-between"
                >
                  <div className="space-y-1.5">
                    <div className="flex items-center justify-between">
                      <span className="text-[10px] font-mono text-sky-400">{sibling.paradigm}</span>
                      <span className="text-[10px] font-mono text-slate-400">{sibling.category}</span>
                    </div>
                    <h4 className="font-semibold text-sm text-white">{sibling.name}</h4>
                    <div className="text-[11px] font-mono text-slate-300 space-y-0.5">
                      <div>
                        Time: <span className="text-sky-300 font-semibold">{sibling.time_complexity_average}</span>
                      </div>
                      <div>
                        Space: <span className="text-purple-300 font-semibold">{sibling.space_complexity}</span>
                      </div>
                    </div>
                    {sibling.notes && (
                      <p className="text-[11px] text-slate-400 line-clamp-2 pt-1">{sibling.notes}</p>
                    )}
                  </div>

                  <div className="pt-2 border-t border-slate-800 flex items-center justify-between">
                    <Link to={`/algorithms/${sibling.slug}`}>
                      <Button variant="secondary" size="sm">
                        View Sibling
                      </Button>
                    </Link>
                    <Link to={`/benchmark?algos=${algorithm.slug},${sibling.slug}`}>
                      <Button variant="ghost" size="sm" icon={<BarChart3 className="w-3 h-3" />}>
                        Compare
                      </Button>
                    </Link>
                  </div>
                </Card>
              ))}
            </div>
          </div>
        )}

        {/* Source Code & Pseudocode Viewer */}
        <Card className="p-0 overflow-hidden border-slate-800">
          <div className="flex flex-wrap items-center justify-between gap-3 px-4 py-3 bg-slate-900 border-b border-slate-800">
            <div className="flex flex-wrap items-center gap-3">
              <Code2 className="w-4 h-4 text-sky-400" />
              <div className="flex rounded-lg bg-slate-950 p-0.5 border border-slate-800">
                <button
                  onClick={() => setActiveCodeTab("c")}
                  className={`px-3 py-1 rounded text-xs font-mono transition-colors ${
                    activeCodeTab === "c"
                      ? "bg-sky-500/20 text-sky-300 font-semibold border border-sky-500/40"
                      : "text-slate-400 hover:text-slate-200"
                  }`}
                >
                  C Implementation
                </button>
                <button
                  onClick={() => setActiveCodeTab("pseudocode")}
                  className={`px-3 py-1 rounded text-xs font-mono transition-colors ${
                    activeCodeTab === "pseudocode"
                      ? "bg-sky-500/20 text-sky-300 font-semibold border border-sky-500/40"
                      : "text-slate-400 hover:text-slate-200"
                  }`}
                >
                  Formal Pseudocode
                </button>
              </div>

              {activeCodeTab === "c" && (
                <span className="hidden sm:inline-flex items-center gap-1.5 px-2 py-0.5 rounded text-[10px] font-mono text-emerald-400 bg-emerald-950/40 border border-emerald-800/40">
                  <span className="w-1.5 h-1.5 rounded-full bg-emerald-400"></span>
                  C11 Standard Source Code
                </span>
              )}
            </div>

            <Button
              variant="ghost"
              size="sm"
              icon={copiedCode ? <Check className="w-3.5 h-3.5 text-emerald-400" /> : <Copy className="w-3.5 h-3.5" />}
              onClick={() => handleCopy(activeCodeTab === "c" ? cSource : pseudocodeSource)}
            >
              {copiedCode ? "Copied" : "Copy Code"}
            </Button>
          </div>

          <div className="p-4 bg-[#080b11] overflow-x-auto max-h-[500px]">
            <pre className="font-mono text-xs text-slate-200 leading-relaxed">
              <code>{activeCodeTab === "c" ? cSource : pseudocodeSource}</code>
            </pre>
          </div>
        </Card>
      </div>
    </Layout>
  );
}
