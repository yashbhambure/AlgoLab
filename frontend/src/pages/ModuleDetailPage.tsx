import { useState, useEffect } from "react";
import { useParams, Link } from "react-router-dom";
import {
  ArrowLeft,
  ArrowRight,
  Layers,
  Sigma,
  Code2,
  Play,
  BarChart3,
  ExternalLink,
  Sparkles,
  FileCode,
} from "lucide-react";
import { Layout } from "../components/layout/Layout";
import { PageHeader } from "../components/layout/PageHeader";
import { Card } from "../components/common/Card";
import { Button } from "../components/common/Button";
import { Badge } from "../components/common/Badge";
import { LoadingState } from "../components/common/LoadingState";
import { EmptyState } from "../components/common/EmptyState";
import { api } from "../services/api";
import type { CurriculumModule, CurriculumTopic } from "../types";

export default function ModuleDetailPage() {
  const { moduleId } = useParams<{ moduleId: string }>();

  const [moduleData, setModuleData] = useState<CurriculumModule | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!moduleId) return;
    setLoading(true);
    setError(null);

    api
      .getCurriculumModule(moduleId)
      .then((data) => {
        setModuleData(data);
      })
      .catch((err) => {
        console.error("Failed to load module:", err);
        setError(err.message || `Curriculum Module '${moduleId}' not found.`);
      })
      .finally(() => setLoading(false));
  }, [moduleId]);

  if (loading) {
    return (
      <Layout>
        <div className="py-24">
          <LoadingState message={`Loading Curriculum Module ${moduleId}...`} />
        </div>
      </Layout>
    );
  }

  if (error || !moduleData) {
    return (
      <Layout>
        <div className="space-y-6">
          <PageHeader
            breadcrumb="Curriculum"
            title="Module Not Found"
            description="The requested curriculum module could not be found."
          />
          <EmptyState
            title="Module not found"
            message={error || `Module '${moduleId}' does not exist in the 7-module syllabus.`}
            action={
              <Link to="/curriculum">
                <Button variant="secondary" icon={<ArrowLeft className="w-4 h-4" />}>
                  Back to Curriculum Hub
                </Button>
              </Link>
            }
          />
        </div>
      </Layout>
    );
  }

  const isTheoryModule = moduleData.module_id >= 6;
  const prevModuleId = moduleData.module_id > 1 ? moduleData.module_id - 1 : null;
  const nextModuleId = moduleData.module_id < 7 ? moduleData.module_id + 1 : null;

  return (
    <Layout>
      <div className="space-y-8 animate-in fade-in duration-200">
        {/* Navigation Breadcrumb Bar */}
        <div className="flex items-center justify-between">
          <Link
            to="/curriculum"
            className="inline-flex items-center gap-1.5 text-xs font-mono text-slate-400 hover:text-white transition-colors"
          >
            <ArrowLeft className="w-3.5 h-3.5" />
            <span>Curriculum Hub</span>
          </Link>

          <div className="flex items-center gap-2">
            {prevModuleId && (
              <Link to={`/curriculum/${prevModuleId}`}>
                <Button variant="ghost" size="sm" icon={<ArrowLeft className="w-3 h-3" />}>
                  Module {prevModuleId}
                </Button>
              </Link>
            )}
            {nextModuleId && (
              <Link to={`/curriculum/${nextModuleId}`}>
                <Button variant="ghost" size="sm">
                  <span>Module {nextModuleId}</span>
                  <ArrowRight className="w-3 h-3 ml-1" />
                </Button>
              </Link>
            )}
          </div>
        </div>

        {/* Page Header */}
        <PageHeader
          breadcrumb={`Module ${moduleData.module_id} / 9`}
          title={moduleData.name}
          description={moduleData.description}
          actions={
            <div className="flex items-center gap-2">
              <span className="px-2.5 py-1 rounded text-xs font-mono font-medium bg-sky-950/60 text-sky-400 border border-sky-800/60">
                {isTheoryModule ? "Theoretical Foundation" : "Computational Paradigm"}
              </span>
              <Badge variant="default" mono size="sm">
                {moduleData.topics.length} Topics
              </Badge>
            </div>
          }
        />

        {/* General Method Box */}
        {moduleData.general_method && (
          <div className="p-5 rounded-xl bg-[#0e131f] border border-slate-800 space-y-4">
            <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2 border-b border-slate-800/80 pb-3">
              <div className="flex items-center gap-2">
                <Sparkles className="w-4 h-4 text-sky-400" />
                <h2 className="font-semibold text-white text-sm tracking-tight">
                  {moduleData.general_method.title}
                </h2>
              </div>
              {moduleData.general_method.recurrence_template && (
                <div className="flex items-center gap-2 text-xs font-mono">
                  <span className="text-slate-400 text-[11px]">Template:</span>
                  <code className="text-emerald-400 bg-emerald-950/50 px-2 py-0.5 rounded border border-emerald-800/50">
                    {moduleData.general_method.recurrence_template}
                  </code>
                </div>
              )}
            </div>

            {/* Principles */}
            {moduleData.general_method.principles && (
              <div className="space-y-2">
                <div className="text-[11px] font-mono text-slate-400 uppercase tracking-wider">
                  Core Mathematical & Algorithmic Principles:
                </div>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-2.5">
                  {moduleData.general_method.principles.map((principle, idx) => (
                    <div
                      key={idx}
                      className="p-3 rounded-lg bg-slate-900/80 border border-slate-800 text-xs text-slate-300 leading-relaxed flex items-start gap-2"
                    >
                      <span className="text-sky-400 font-mono font-bold text-[11px] mt-0.5">
                        {idx + 1}.
                      </span>
                      <span>{principle}</span>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {/* Master Theorem Cases if available (Module 1) */}
            {moduleData.general_method.master_theorem_cases && (
              <div className="space-y-2 pt-2 border-t border-slate-800/80">
                <div className="flex items-center justify-between">
                  <span className="text-[11px] font-mono text-slate-400 uppercase tracking-wider">
                    Master Theorem Asymptotic Bounds:
                  </span>
                  <Link
                    to="/complexity"
                    className="text-[11px] font-mono text-sky-400 hover:text-sky-300 flex items-center gap-1"
                  >
                    Interactive Master Theorem Solver
                    <ExternalLink className="w-3 h-3" />
                  </Link>
                </div>
                <div className="grid grid-cols-1 md:grid-cols-3 gap-2">
                  {moduleData.general_method.master_theorem_cases.map((c, i) => (
                    <div
                      key={i}
                      className="p-2.5 rounded-lg bg-slate-900/60 border border-slate-800 text-[11px] font-mono text-slate-300 space-y-1"
                    >
                      <div className="text-sky-400 font-semibold">{c.split("=>")[0]}</div>
                      {c.includes("=>") && (
                        <div className="text-emerald-400 font-bold bg-emerald-950/30 px-1.5 py-0.5 rounded">
                          ⇒ {c.split("=>")[1]}
                        </div>
                      )}
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>
        )}

        {/* Topic Breakdown */}
        {!isTheoryModule ? (
          /* ================================================================= */
          /* MODULES 1 - 7: COMPUTATIONAL TOPICS & CANONICAL PROBLEMS           */
          /* ================================================================= */
          <div className="space-y-6">
            <div className="flex items-center justify-between border-b border-slate-800 pb-2">
              <h2 className="text-base font-bold text-white tracking-tight flex items-center gap-2">
                <Layers className="w-4 h-4 text-sky-400" />
                <span>Curriculum Topics & Algorithm Implementations</span>
              </h2>
              <span className="text-xs font-mono text-slate-400">
                Authoritative Syllabus Items
              </span>
            </div>

            <div className="space-y-4">
              {moduleData.topics.map((topic: CurriculumTopic) => {
                const isTheoryFoundation = topic.type === "theoretical_foundation";
                const algoSlugs = topic.algorithm_slugs || (topic.algorithm_slug ? [topic.algorithm_slug] : []);

                return (
                  <Card
                    key={topic.topic_id}
                    className={`space-y-4 transition-all ${
                      isTheoryFoundation ? "border-purple-900/40 bg-purple-950/10" : ""
                    }`}
                  >
                    {/* Topic Header */}
                    <div className="flex flex-col sm:flex-row sm:items-start justify-between gap-2 border-b border-slate-800/80 pb-3">
                      <div className="space-y-1">
                        <div className="flex items-center gap-2">
                          <span
                            className={`px-2 py-0.5 rounded text-[10px] font-mono font-bold ${
                              isTheoryFoundation
                                ? "bg-purple-950/80 text-purple-400 border border-purple-800/60"
                                : "bg-sky-950/80 text-sky-400 border border-sky-800/60"
                            }`}
                          >
                            TOPIC {topic.topic_id}
                          </span>
                          <span className="text-xs font-semibold text-white">{topic.name}</span>
                          {topic.method_name && (
                            <span className="text-xs text-slate-400 font-mono hidden md:inline">
                              • {topic.method_name}
                            </span>
                          )}
                        </div>
                        <p className="text-xs text-slate-400 leading-relaxed">
                          {topic.description}
                        </p>
                      </div>

                      <div className="flex items-center gap-2 self-start">
                        {topic.problem_slug && (
                          <Link to={`/problems/${topic.problem_slug}`}>
                            <span className="px-2 py-1 rounded text-[11px] font-mono text-sky-300 bg-sky-950/40 border border-sky-800/40 hover:bg-sky-900/60 transition-colors flex items-center gap-1">
                              <Layers className="w-3 h-3" />
                              Canonical Problem
                            </span>
                          </Link>
                        )}
                      </div>
                    </div>

                    {/* Complexity & Recurrence Strip */}
                    {(topic.time_complexity || topic.space_complexity || topic.recurrence) && (
                      <div className="grid grid-cols-1 sm:grid-cols-3 gap-2 p-2.5 rounded-lg bg-slate-900/80 border border-slate-800 text-[11px] font-mono">
                        {topic.time_complexity && (
                          <div>
                            <span className="text-slate-400 text-[10px] block">Time Complexity:</span>
                            <span className="text-sky-400 font-semibold">{topic.time_complexity}</span>
                          </div>
                        )}
                        {topic.space_complexity && (
                          <div>
                            <span className="text-slate-400 text-[10px] block">Auxiliary Space:</span>
                            <span className="text-purple-400 font-semibold">{topic.space_complexity}</span>
                          </div>
                        )}
                        {topic.recurrence && (
                          <div>
                            <span className="text-slate-400 text-[10px] block">Recurrence / Bound:</span>
                            <span className="text-emerald-400 font-semibold">{topic.recurrence}</span>
                          </div>
                        )}
                      </div>
                    )}

                    {/* Invariance if present */}
                    {topic.invariance && (
                      <div className="p-2.5 rounded bg-amber-950/20 border border-amber-800/30 text-xs text-amber-300/90 font-mono">
                        <strong>Loop / Algorithmic Invariant:</strong> {topic.invariance}
                      </div>
                    )}

                    {/* Real-World Applications */}
                    {topic.real_world_applications && topic.real_world_applications.length > 0 && (
                      <div className="space-y-1">
                        <div className="text-[10px] font-mono text-slate-400 uppercase tracking-wider">
                          Real-World Applications:
                        </div>
                        <div className="flex flex-wrap gap-1.5">
                          {topic.real_world_applications.map((app, i) => (
                            <span
                              key={i}
                              className="px-2 py-0.5 rounded text-[10px] font-mono bg-slate-900 text-slate-300 border border-slate-800"
                            >
                              {app}
                            </span>
                          ))}
                        </div>
                      </div>
                    )}

                    {/* Executable Algorithms Implementation Strip */}
                    {algoSlugs.length > 0 && (
                      <div className="pt-3 border-t border-slate-800 flex flex-col sm:flex-row sm:items-center justify-between gap-3">
                        <div className="flex items-center gap-2 text-xs font-mono text-slate-400">
                          <Code2 className="w-3.5 h-3.5 text-emerald-400" />
                          <span>
                            {algoSlugs.length === 1
                              ? "Executable Algorithm:"
                              : `Executable Implementations (${algoSlugs.length}):`}
                          </span>
                        </div>

                        <div className="flex flex-wrap items-center gap-2">
                          {algoSlugs.map((slug) => (
                            <div key={slug} className="flex items-center gap-1.5">
                              <Link to={`/algorithms/${slug}`}>
                                <Button
                                  variant="secondary"
                                  size="sm"
                                  icon={<FileCode className="w-3 h-3" />}
                                >
                                  {slug}
                                </Button>
                              </Link>
                              <Link to={`/visualizer?algo=${slug}`}>
                                <Button
                                  variant="ghost"
                                  size="sm"
                                  icon={<Play className="w-3 h-3" />}
                                  title="Open in Visualizer"
                                >
                                  Visualizer
                                </Button>
                              </Link>
                              <Link to={`/benchmark?algos=${slug}`}>
                                <Button
                                  variant="ghost"
                                  size="sm"
                                  icon={<BarChart3 className="w-3 h-3" />}
                                  title="Benchmark this algorithm"
                                >
                                  Benchmark
                                </Button>
                              </Link>
                            </div>
                          ))}
                        </div>
                      </div>
                    )}
                  </Card>
                );
              })}
            </div>
          </div>
        ) : (
          /* ================================================================= */
          /* MODULES 8 - 9: PURE THEORETICAL COMPLEXITY TREATISE              */
          /* ================================================================= */
          <div className="space-y-6">
            <div className="flex items-center justify-between border-b border-purple-900/40 pb-2">
              <h2 className="text-base font-bold text-white tracking-tight flex items-center gap-2">
                <Sigma className="w-4 h-4 text-purple-400" />
                <span>Theoretical Complexity Foundations & Formal Proofs</span>
              </h2>
              <span className="text-xs font-mono text-purple-400">
                Non-Executable Academic Classifications
              </span>
            </div>

            <div className="space-y-5">
              {moduleData.topics.map((topic: CurriculumTopic) => (
                <Card
                  key={topic.topic_id}
                  className="space-y-4 border-purple-900/30 hover:border-purple-800/60 transition-colors"
                >
                  {/* Topic Title & Description */}
                  <div className="flex items-start justify-between gap-3 border-b border-slate-800/80 pb-3">
                    <div>
                      <div className="flex items-center gap-2 mb-1">
                        <span className="px-2 py-0.5 rounded text-[10px] font-mono font-bold bg-purple-950/80 text-purple-400 border border-purple-800/60">
                          TOPIC {topic.topic_id}
                        </span>
                        <h3 className="text-sm font-bold text-white tracking-tight">
                          {topic.name}
                        </h3>
                      </div>
                      <p className="text-xs text-slate-300 leading-relaxed">
                        {topic.description}
                      </p>
                    </div>
                  </div>

                  {/* Formal Definition */}
                  {topic.formal_definition && (
                    <div className="p-3 rounded-lg bg-slate-900/90 border border-purple-900/40 space-y-1">
                      <span className="text-[10px] font-mono text-purple-400 uppercase tracking-wider block">
                        Formal Mathematical Definition:
                      </span>
                      <code className="text-xs font-mono text-purple-300 block bg-black/40 p-2 rounded border border-purple-950">
                        {topic.formal_definition}
                      </code>
                    </div>
                  )}

                  {/* Theorem Statement & Proof Architecture (Cook's Theorem 9.3) */}
                  {topic.theorem_statement && (
                    <div className="p-3 rounded-lg bg-purple-950/30 border border-purple-800/50 space-y-2">
                      <span className="text-[11px] font-mono font-bold text-purple-300 uppercase tracking-wider block">
                        Theorem Statement:
                      </span>
                      <div className="text-xs text-slate-200 font-mono bg-black/40 p-2 rounded">
                        {topic.theorem_statement}
                      </div>
                      {topic.proof_architecture && (
                        <div className="space-y-1.5 pt-1">
                          <span className="text-[10px] font-mono text-slate-400 uppercase tracking-wider block">
                            Cook-Levin Proof Architecture:
                          </span>
                          {topic.proof_architecture.map((step, idx) => (
                            <div
                              key={idx}
                              className="text-xs text-slate-300 p-2 rounded bg-slate-900/80 border border-slate-800"
                            >
                              {step}
                            </div>
                          ))}
                        </div>
                      )}
                      {topic.impact && (
                        <div className="text-[11px] text-purple-300/90 pt-1">
                          <strong>Academic Impact:</strong> {topic.impact}
                        </div>
                      )}
                    </div>
                  )}

                  {/* Asymptotic Characterization */}
                  {topic.asymptotic_characterization && (
                    <div className="p-2.5 rounded bg-slate-900/80 border border-slate-800 text-xs font-mono">
                      <span className="text-slate-400 text-[10px] block">
                        Asymptotic Growth Bound:
                      </span>
                      <span className="text-emerald-400 font-semibold">
                        {topic.asymptotic_characterization}
                      </span>
                    </div>
                  )}

                  {/* Canonical Examples */}
                  {topic.canonical_examples && topic.canonical_examples.length > 0 && (
                    <div className="space-y-1.5">
                      <span className="text-[10px] font-mono text-slate-400 uppercase tracking-wider block">
                        Canonical Problem Instances:
                      </span>
                      <div className="flex flex-wrap gap-1.5">
                        {topic.canonical_examples.map((ex, i) => (
                          <span
                            key={i}
                            className="px-2 py-1 rounded text-[11px] font-mono bg-slate-900 text-slate-200 border border-slate-800"
                          >
                            {ex}
                          </span>
                        ))}
                      </div>
                    </div>
                  )}

                  {/* Properties */}
                  {topic.properties && topic.properties.length > 0 && (
                    <div className="space-y-1.5">
                      <span className="text-[10px] font-mono text-slate-400 uppercase tracking-wider block">
                        Key Complexity Properties:
                      </span>
                      <div className="space-y-1">
                        {topic.properties.map((prop, i) => (
                          <div
                            key={i}
                            className="text-xs text-slate-300 p-2 rounded bg-slate-900/50 border border-slate-800/80 flex items-start gap-2"
                          >
                            <span className="text-purple-400 font-bold">•</span>
                            <span>{prop}</span>
                          </div>
                        ))}
                      </div>
                    </div>
                  )}

                  {/* Canonical Reductions (Topic 9.2) */}
                  {topic.canonical_reductions && (
                    <div className="space-y-2 pt-2 border-t border-slate-800">
                      <span className="text-[11px] font-mono font-semibold text-purple-300 block">
                        Karp's 21 Polynomial-Time Reduction Chains (L₁ ≤ₚ L₂):
                      </span>
                      <div className="space-y-1 font-mono text-xs">
                        {topic.canonical_reductions.map((red, i) => (
                          <div
                            key={i}
                            className="p-2 rounded bg-slate-900 border border-purple-950 text-purple-200"
                          >
                            {red}
                          </div>
                        ))}
                      </div>
                    </div>
                  )}

                  {/* Key Takeaway */}
                  {topic.key_takeaway && (
                    <div className="p-2.5 rounded bg-sky-950/20 border border-sky-800/30 text-xs text-sky-300 font-mono">
                      <strong>Takeaway:</strong> {topic.key_takeaway}
                    </div>
                  )}
                </Card>
              ))}
            </div>
          </div>
        )}
      </div>
    </Layout>
  );
}
