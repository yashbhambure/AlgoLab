import { useState, useEffect } from "react";
import { Link } from "react-router-dom";
import {
  GraduationCap,
  Layers,
  Cpu,
  Sigma,
  Code2,
  CheckCircle2,
  ShieldCheck,
  ChevronRight,
  Sparkles,
} from "lucide-react";
import { Layout } from "../components/layout/Layout";
import { PageHeader } from "../components/layout/PageHeader";
import { Card } from "../components/common/Card";
import { Button } from "../components/common/Button";
import { Badge } from "../components/common/Badge";
import { LoadingState } from "../components/common/LoadingState";
import { EmptyState } from "../components/common/EmptyState";
import { api } from "../services/api";
import type { CurriculumModule } from "../types";

export default function CurriculumHubPage() {
  const [modules, setModules] = useState<CurriculumModule[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    api
      .getCurriculumModules()
      .then((data) => {
        setModules(data);
      })
      .catch((err) => {
        console.error("Failed to load curriculum modules:", err);
        setError(err.message || "Failed to load curriculum modules.");
      })
      .finally(() => setLoading(false));
  }, []);

  const totalTopics = modules.reduce(
    (acc, m) => acc + (m.topics ? m.topics.length : 0),
    0
  );
  const computationalModules = modules.filter((m) => m.module_id <= 7);
  const theoreticalModules = modules.filter((m) => m.module_id >= 8);

  return (
    <Layout>
      <div className="space-y-8 animate-in fade-in duration-200">
        {/* Page Header */}
        <PageHeader
          breadcrumb="Academic Spine"
          title="DAA Curriculum Hub"
          description="Authoritative 9-Module Design and Analysis of Algorithms syllabus. Explore formal General Methods, canonical computational problems, executable algorithm implementations, and computational complexity foundations."
          actions={
            <div className="flex items-center gap-2.5">
              <Link to="/problems">
                <Button variant="secondary" icon={<Layers className="w-4 h-4" />}>
                  Canonical Problems
                </Button>
              </Link>
              <Link to="/catalog">
                <Button variant="primary" icon={<Code2 className="w-4 h-4" />}>
                  Algorithm Catalog
                </Button>
              </Link>
            </div>
          }
        />

        {/* Syllabus Summary Strip */}
        <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 p-4 rounded-xl bg-[#0e131f] border border-slate-800">
          <div className="flex items-center gap-3">
            <div className="p-2.5 rounded-lg bg-sky-950/50 border border-sky-800/60 text-sky-400">
              <GraduationCap className="w-5 h-5" />
            </div>
            <div>
              <div className="text-xl font-bold font-mono text-white">9 Modules</div>
              <div className="text-[11px] text-slate-400">Full DAA Syllabus</div>
            </div>
          </div>

          <div className="flex items-center gap-3">
            <div className="p-2.5 rounded-lg bg-emerald-950/50 border border-emerald-800/60 text-emerald-400">
              <Cpu className="w-5 h-5" />
            </div>
            <div>
              <div className="text-xl font-bold font-mono text-white">7 Applied</div>
              <div className="text-[11px] text-slate-400">General Methods & Problems</div>
            </div>
          </div>

          <div className="flex items-center gap-3">
            <div className="p-2.5 rounded-lg bg-purple-950/50 border border-purple-800/60 text-purple-400">
              <Sigma className="w-5 h-5" />
            </div>
            <div>
              <div className="text-xl font-bold font-mono text-white">2 Theory</div>
              <div className="text-[11px] text-slate-400">P, NP & Reductions</div>
            </div>
          </div>

          <div className="flex items-center gap-3">
            <div className="p-2.5 rounded-lg bg-amber-950/50 border border-amber-800/60 text-amber-400">
              <CheckCircle2 className="w-5 h-5" />
            </div>
            <div>
              <div className="text-xl font-bold font-mono text-white">{totalTopics} Topics</div>
              <div className="text-[11px] text-slate-400">100% Authoritative Coverage</div>
            </div>
          </div>
        </div>

        {loading ? (
          <div className="py-24">
            <LoadingState message="Loading 9 DAA Curriculum modules..." />
          </div>
        ) : error ? (
          <EmptyState
            title="Failed to load curriculum"
            message={error}
            action={
              <Button variant="secondary" onClick={() => window.location.reload()}>
                Retry
              </Button>
            }
          />
        ) : (
          <div className="space-y-10">
            {/* Section 1: Applied Paradigms & General Methods (Modules 1-7) */}
            <div className="space-y-4">
              <div className="flex items-center justify-between border-b border-slate-800 pb-3">
                <div className="flex items-center gap-2.5">
                  <div className="w-2 h-2 rounded-full bg-sky-400" />
                  <h2 className="text-lg font-bold text-white tracking-tight">
                    Applied Algorithmic Paradigms (Modules 1–7)
                  </h2>
                </div>
                <span className="text-xs font-mono text-slate-400">
                  General Method → Canonical Problem → Executable Implementations
                </span>
              </div>

              <div className="grid grid-cols-1 lg:grid-cols-2 gap-5">
                {computationalModules.map((module) => {
                  const computationalTopics = module.topics.filter(
                    (t) => t.type === "computational"
                  );
                  const theoreticalTopics = module.topics.filter(
                    (t) => t.type === "theoretical_foundation"
                  );

                  return (
                    <Card
                      key={module.module_id}
                      className="flex flex-col justify-between hover:border-slate-700 transition-all group"
                    >
                      <div className="space-y-4">
                        {/* Header */}
                        <div className="flex items-start justify-between gap-3 border-b border-slate-800/80 pb-3">
                          <div className="space-y-1">
                            <div className="flex items-center gap-2">
                              <span className="px-2 py-0.5 rounded text-[10px] font-mono font-bold bg-sky-950/80 text-sky-400 border border-sky-800/60">
                                MODULE {module.module_id}
                              </span>
                              <Badge variant="default" mono size="sm">
                                {module.short_name}
                              </Badge>
                            </div>
                            <h3 className="text-base font-semibold text-white tracking-tight group-hover:text-sky-300 transition-colors">
                              {module.name}
                            </h3>
                          </div>
                          <span className="px-2 py-0.5 rounded text-[10px] font-mono text-emerald-400 bg-emerald-950/40 border border-emerald-800/40 whitespace-nowrap">
                            Executable Suite
                          </span>
                        </div>

                        {/* Description */}
                        <p className="text-xs text-slate-400 leading-relaxed line-clamp-2">
                          {module.description}
                        </p>

                        {/* General Method Box */}
                        {module.general_method && (
                          <div className="p-3 rounded-lg bg-slate-900/90 border border-slate-800 space-y-1.5 text-xs">
                            <div className="flex items-center justify-between">
                              <span className="text-[11px] font-mono font-semibold text-sky-400 flex items-center gap-1.5">
                                <Sparkles className="w-3 h-3" />
                                {module.general_method.title}
                              </span>
                              {module.general_method.recurrence_template && (
                                <code className="text-[10px] font-mono text-emerald-300 bg-emerald-950/40 px-1.5 py-0.5 rounded border border-emerald-800/40">
                                  {module.general_method.recurrence_template}
                                </code>
                              )}
                            </div>
                            {module.general_method.principles && (
                              <p className="text-[11px] text-slate-400 line-clamp-2">
                                {module.general_method.principles[0]}
                              </p>
                            )}
                          </div>
                        )}

                        {/* Topics Summary List */}
                        <div className="space-y-1.5 pt-1">
                          <div className="text-[11px] font-mono text-slate-400 uppercase tracking-wider">
                            Curriculum Topics ({module.topics.length}):
                          </div>
                          <div className="flex flex-wrap gap-1.5">
                            {theoreticalTopics.map((t) => (
                              <span
                                key={t.topic_id}
                                className="px-2 py-1 rounded text-[11px] font-mono bg-purple-950/30 text-purple-300 border border-purple-800/40"
                              >
                                {t.topic_id} {t.name}
                              </span>
                            ))}
                            {computationalTopics.map((t) => (
                              <span
                                key={t.topic_id}
                                className="px-2 py-1 rounded text-[11px] font-mono bg-slate-800/70 text-slate-200 border border-slate-700/60"
                              >
                                {t.topic_id} {t.name}
                              </span>
                            ))}
                          </div>
                        </div>
                      </div>

                      {/* Footer Actions */}
                      <div className="flex items-center justify-between pt-4 mt-4 border-t border-slate-800">
                        <div className="text-[11px] font-mono text-slate-400">
                          <span className="text-white font-medium">
                            {computationalTopics.length}
                          </span>{" "}
                          Computational /{" "}
                          <span className="text-white font-medium">
                            {theoreticalTopics.length}
                          </span>{" "}
                          Theory
                        </div>

                        <Link to={`/curriculum/${module.module_id}`}>
                          <Button
                            variant="secondary"
                            size="sm"
                            icon={<ChevronRight className="w-3.5 h-3.5" />}
                          >
                            Explore Module
                          </Button>
                        </Link>
                      </div>
                    </Card>
                  );
                })}
              </div>
            </div>

            {/* Section 2: Complexity Foundations (Modules 8-9) */}
            <div className="space-y-4">
              <div className="flex items-center justify-between border-b border-slate-800 pb-3">
                <div className="flex items-center gap-2.5">
                  <div className="w-2 h-2 rounded-full bg-purple-400" />
                  <h2 className="text-lg font-bold text-white tracking-tight">
                    Theoretical Complexity Foundations (Modules 8–9)
                  </h2>
                </div>
                <span className="text-xs font-mono text-slate-400">
                  P, NP, Reductions, NP-Hardness & Cook's Theorem
                </span>
              </div>

              <div className="grid grid-cols-1 lg:grid-cols-2 gap-5">
                {theoreticalModules.map((module) => (
                  <Card
                    key={module.module_id}
                    className="flex flex-col justify-between hover:border-purple-800/60 transition-all border-purple-900/30 group"
                  >
                    <div className="space-y-4">
                      {/* Header */}
                      <div className="flex items-start justify-between gap-3 border-b border-slate-800/80 pb-3">
                        <div className="space-y-1">
                          <div className="flex items-center gap-2">
                            <span className="px-2 py-0.5 rounded text-[10px] font-mono font-bold bg-purple-950/80 text-purple-400 border border-purple-800/60">
                              MODULE {module.module_id}
                            </span>
                            <Badge variant="warning" mono size="sm">
                              Pure Theory
                            </Badge>
                          </div>
                          <h3 className="text-base font-semibold text-white tracking-tight group-hover:text-purple-300 transition-colors">
                            {module.name}
                          </h3>
                        </div>
                        <span className="px-2 py-0.5 rounded text-[10px] font-mono text-purple-400 bg-purple-950/40 border border-purple-800/40 whitespace-nowrap">
                          Complexity Proofs
                        </span>
                      </div>

                      {/* Description */}
                      <p className="text-xs text-slate-400 leading-relaxed">
                        {module.description}
                      </p>

                      {/* General Method / Theoretical Architecture */}
                      {module.general_method && (
                        <div className="p-3 rounded-lg bg-slate-900/90 border border-slate-800 space-y-1.5 text-xs">
                          <span className="text-[11px] font-mono font-semibold text-purple-400 block">
                            {module.general_method.title}
                          </span>
                          {module.general_method.principles && (
                            <p className="text-[11px] text-slate-400 line-clamp-2">
                              {module.general_method.principles[0]}
                            </p>
                          )}
                        </div>
                      )}

                      {/* Topics List */}
                      <div className="space-y-1.5 pt-1">
                        <div className="text-[11px] font-mono text-slate-400 uppercase tracking-wider">
                          Theoretical Classes & Theorems:
                        </div>
                        <div className="grid grid-cols-1 sm:grid-cols-2 gap-2">
                          {module.topics.map((t) => (
                            <div
                              key={t.topic_id}
                              className="p-2 rounded bg-slate-900/60 border border-slate-800/80 text-xs space-y-0.5"
                            >
                              <div className="font-mono text-[11px] text-purple-300 font-semibold">
                                {t.topic_id} {t.name}
                              </div>
                              <div className="text-[10px] text-slate-400 line-clamp-1">
                                {t.description}
                              </div>
                            </div>
                          ))}
                        </div>
                      </div>
                    </div>

                    {/* Footer Actions */}
                    <div className="flex items-center justify-between pt-4 mt-4 border-t border-slate-800">
                      <span className="text-[11px] font-mono text-slate-400 flex items-center gap-1.5">
                        <ShieldCheck className="w-3.5 h-3.5 text-purple-400" />
                        Formal Definitions & Reductions
                      </span>

                      <Link to={`/curriculum/${module.module_id}`}>
                        <Button
                          variant="secondary"
                          size="sm"
                          icon={<ChevronRight className="w-3.5 h-3.5" />}
                        >
                          View Theory Treatise
                        </Button>
                      </Link>
                    </div>
                  </Card>
                ))}
              </div>
            </div>
          </div>
        )}
      </div>
    </Layout>
  );
}
