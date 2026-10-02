import { useState, useEffect } from "react";
import { useParams, Link } from "react-router-dom";
import {
  ArrowLeft,
  Play,
  BarChart3,
  Code2,
  GraduationCap,
  Sparkles,
  FileCode,
  Scale,
} from "lucide-react";
import { Layout } from "../components/layout/Layout";
import { PageHeader } from "../components/layout/PageHeader";
import { Card } from "../components/common/Card";
import { Button } from "../components/common/Button";
import { Badge } from "../components/common/Badge";
import { LoadingState } from "../components/common/LoadingState";
import { EmptyState } from "../components/common/EmptyState";
import { api } from "../services/api";
import type { ProblemDetailData, CurriculumModule } from "../types";

export default function ProblemDetailPage() {
  const { slug } = useParams<{ slug: string }>();

  const [problem, setProblem] = useState<ProblemDetailData | null>(null);
  const [curriculumModules, setCurriculumModules] = useState<CurriculumModule[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!slug) return;
    setLoading(true);
    setError(null);

    Promise.all([
      api.getProblemDetail(slug),
      api.getCurriculumModules().catch(() => [] as CurriculumModule[]),
    ])
      .then(([problemData, modules]) => {
        setProblem(problemData);

        // Find any curriculum modules that reference this problem slug
        const matchingModules = modules.filter((m) =>
          m.topics?.some((t) => t.problem_slug === slug)
        );
        setCurriculumModules(matchingModules);
      })
      .catch((err) => {
        console.error("Failed to load problem detail:", err);
        setError(err.message || `Problem '${slug}' not found.`);
      })
      .finally(() => setLoading(false));
  }, [slug]);

  if (loading) {
    return (
      <Layout>
        <div className="py-24">
          <LoadingState message={`Loading specification for problem '${slug}'...`} />
        </div>
      </Layout>
    );
  }

  if (error || !problem) {
    return (
      <Layout>
        <div className="space-y-6">
          <PageHeader
            breadcrumb="Canonical Problems"
            title="Problem Not Found"
            description="The requested canonical computational problem does not exist."
          />
          <EmptyState
            title="Problem not found"
            message={error || `No canonical problem matching '${slug}' was found.`}
            action={
              <Link to="/problems">
                <Button variant="secondary" icon={<ArrowLeft className="w-4 h-4" />}>
                  Back to Problems Hub
                </Button>
              </Link>
            }
          />
        </div>
      </Layout>
    );
  }

  const applicableAlgos = problem.applicable_algorithms || [];
  const algoSlugsQuery = applicableAlgos.map((a) => a.slug).join(",");

  return (
    <Layout>
      <div className="space-y-8 animate-in fade-in duration-200">
        {/* Navigation Breadcrumb */}
        <div className="flex items-center justify-between">
          <Link
            to="/problems"
            className="inline-flex items-center gap-1.5 text-xs font-mono text-slate-400 hover:text-white transition-colors"
          >
            <ArrowLeft className="w-3.5 h-3.5" />
            <span>Canonical Problems Hub</span>
          </Link>

          <div className="flex items-center gap-2">
            {curriculumModules.map((m) => (
              <Link key={m.module_id} to={`/curriculum/${m.module_id}`}>
                <span className="px-2.5 py-1 rounded text-xs font-mono text-sky-400 bg-sky-950/40 border border-sky-800/40 hover:bg-sky-900/50 transition-colors flex items-center gap-1.5">
                  <GraduationCap className="w-3.5 h-3.5" />
                  <span>Module {m.module_id}: {m.short_name}</span>
                </span>
              </Link>
            ))}
          </div>
        </div>

        {/* Page Header */}
        <PageHeader
          breadcrumb={problem.paradigm}
          title={problem.name || problem.title || slug || "Problem Specification"}
          description={problem.description}
          actions={
            <div className="flex items-center gap-2.5">
              {applicableAlgos.length > 1 && (
                <Link to={`/benchmark?algos=${algoSlugsQuery}`}>
                  <Button variant="primary" icon={<BarChart3 className="w-4 h-4" />}>
                    Compare All ({applicableAlgos.length}) in Arena
                  </Button>
                </Link>
              )}
              <Badge variant="default" mono size="md">
                {problem.category}
              </Badge>
            </div>
          }
        />

        {/* Formal Input, Output & Constraints */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <Card className="p-4 space-y-2 bg-slate-900/60 border-slate-800">
            <span className="text-[11px] font-mono text-slate-400 uppercase tracking-wider block">
              Formal Input Format
            </span>
            <div className="text-xs font-mono text-slate-200">
              {problem.input_format || "Not specified"}
            </div>
          </Card>

          <Card className="p-4 space-y-2 bg-slate-900/60 border-slate-800">
            <span className="text-[11px] font-mono text-slate-400 uppercase tracking-wider block">
              Formal Output Format
            </span>
            <div className="text-xs font-mono text-slate-200">
              {problem.output_format || "Not specified"}
            </div>
          </Card>

          <Card className="p-4 space-y-2 bg-slate-900/60 border-slate-800">
            <span className="text-[11px] font-mono text-slate-400 uppercase tracking-wider block">
              Instance Constraints
            </span>
            <div className="text-xs font-mono text-slate-200">
              {problem.constraints || "Standard bounds"}
            </div>
          </Card>
        </div>

        {/* Example Input / Output if available */}
        {(problem.example_input || problem.example_output) && (
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {problem.example_input && (
              <Card className="p-4 space-y-2 bg-[#0a0e17] border-slate-800">
                <span className="text-[11px] font-mono text-sky-400 uppercase tracking-wider block">
                  Example Input:
                </span>
                <pre className="text-xs font-mono text-slate-200 overflow-x-auto bg-slate-950 p-2.5 rounded border border-slate-800/80">
                  {typeof problem.example_input === "object"
                    ? JSON.stringify(problem.example_input, null, 2)
                    : String(problem.example_input)}
                </pre>
              </Card>
            )}

            {problem.example_output && (
              <Card className="p-4 space-y-2 bg-[#0a0e17] border-slate-800">
                <span className="text-[11px] font-mono text-emerald-400 uppercase tracking-wider block">
                  Example Output:
                </span>
                <pre className="text-xs font-mono text-slate-200 overflow-x-auto bg-slate-950 p-2.5 rounded border border-slate-800/80">
                  {typeof problem.example_output === "object"
                    ? JSON.stringify(problem.example_output, null, 2)
                    : String(problem.example_output)}
                </pre>
              </Card>
            )}
          </div>
        )}

        {/* DAA Topics Tags */}
        {problem.daa_topics && problem.daa_topics.length > 0 && (
          <div className="p-4 rounded-xl bg-[#0e131f] border border-slate-800 space-y-2">
            <span className="text-xs font-mono font-semibold text-slate-300 flex items-center gap-1.5">
              <Sparkles className="w-3.5 h-3.5 text-sky-400" />
              Related DAA Theoretical Concepts:
            </span>
            <div className="flex flex-wrap gap-2">
              {problem.daa_topics.map((topic, i) => (
                <span
                  key={i}
                  className="px-2.5 py-1 rounded text-xs font-mono bg-slate-900 text-slate-200 border border-slate-800"
                >
                  {topic}
                </span>
              ))}
            </div>
          </div>
        )}

        {/* Compatible Implementations Section */}
        <div className="space-y-4">
          <div className="flex items-center justify-between border-b border-slate-800 pb-2">
            <div className="flex items-center gap-2">
              <Code2 className="w-4 h-4 text-sky-400" />
              <h2 className="text-base font-bold text-white tracking-tight">
                Compatible Algorithm Implementations ({applicableAlgos.length})
              </h2>
            </div>

            <div className="flex items-center gap-2">
              <Link to={`/complexity?problem=${problem.slug}`}>
                <Button variant="ghost" size="sm" icon={<Scale className="w-3.5 h-3.5" />}>
                  Complexity Comparison
                </Button>
              </Link>
              {applicableAlgos.length > 1 && (
                <Link to={`/benchmark?algos=${algoSlugsQuery}`}>
                  <Button variant="secondary" size="sm" icon={<BarChart3 className="w-3.5 h-3.5" />}>
                    Head-to-Head Benchmark
                  </Button>
                </Link>
              )}
            </div>
          </div>

          {applicableAlgos.length === 0 ? (
            <Card className="p-8 text-center text-slate-400 font-mono text-xs">
              No compatible algorithms currently registered for this problem.
            </Card>
          ) : (
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              {applicableAlgos.map((algo) => (
                <Card
                  key={algo.slug}
                  className="p-5 flex flex-col justify-between space-y-4 hover:border-slate-700 transition-colors"
                >
                  <div className="space-y-3">
                    {/* Header */}
                    <div className="flex items-start justify-between gap-2 border-b border-slate-800/80 pb-2.5">
                      <div>
                        <span className="text-[10px] font-mono text-sky-400 block mb-0.5">
                          {algo.paradigm}
                        </span>
                        <Link to={`/algorithms/${algo.slug}`}>
                          <h3 className="font-semibold text-base text-white hover:text-sky-300 transition-colors">
                            {algo.name}
                          </h3>
                        </Link>
                      </div>
                      {algo.suitability_score !== undefined && (
                        <span className="px-2 py-0.5 rounded text-[11px] font-mono font-bold bg-emerald-950/40 text-emerald-400 border border-emerald-800/40">
                          {Math.round(algo.suitability_score * 100)}% Fit
                        </span>
                      )}
                    </div>

                    {/* Complexity Details */}
                    <div className="grid grid-cols-2 gap-2 p-2.5 rounded-lg bg-slate-900/80 border border-slate-800 text-[11px] font-mono">
                      <div>
                        <span className="text-slate-400 text-[10px] block">Average Time:</span>
                        <span className="text-sky-400 font-semibold">{algo.time_complexity_average}</span>
                      </div>
                      <div>
                        <span className="text-slate-400 text-[10px] block">Aux Space:</span>
                        <span className="text-purple-400 font-semibold">{algo.space_complexity}</span>
                      </div>
                    </div>

                    {/* Notes */}
                    {algo.notes && (
                      <p className="text-xs text-slate-300 leading-relaxed font-sans">
                        {algo.notes}
                      </p>
                    )}
                  </div>

                  {/* Actions */}
                  <div className="pt-3 border-t border-slate-800 flex items-center justify-between">
                    <Link to={`/algorithms/${algo.slug}`}>
                      <Button variant="secondary" size="sm" icon={<FileCode className="w-3 h-3" />}>
                        Algorithm Detail
                      </Button>
                    </Link>

                    <div className="flex items-center gap-1.5">
                      <Link to={`/visualizer?algo=${algo.slug}`}>
                        <Button variant="ghost" size="sm" icon={<Play className="w-3 h-3" />}>
                          Visualize
                        </Button>
                      </Link>

                      <Link to={`/benchmark?algos=${algo.slug}`}>
                        <Button variant="ghost" size="sm" icon={<BarChart3 className="w-3 h-3" />}>
                          Benchmark
                        </Button>
                      </Link>
                    </div>
                  </div>
                </Card>
              ))}
            </div>
          )}
        </div>
      </div>
    </Layout>
  );
}
