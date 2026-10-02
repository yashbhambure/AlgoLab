import { useState, useEffect } from "react";
import { Link } from "react-router-dom";
import {
  RotateCcw,
  CheckCircle2,
  HelpCircle,
  Play,
  BarChart3,
  ArrowRight,
} from "lucide-react";
import { Layout } from "../components/layout/Layout";
import { PageHeader } from "../components/layout/PageHeader";
import { Card } from "../components/common/Card";
import { Button } from "../components/common/Button";
import { Badge } from "../components/common/Badge";
import { LoadingState } from "../components/common/LoadingState";
import { api } from "../services/api";

export default function DecisionTreePage() {
  const [answers, setAnswers] = useState<Record<string, string>>({});
  const [currentQuestion, setCurrentQuestion] = useState<{
    status: string;
    current_node_id?: string;
    question?: string;
    options?: string[];
    path_traversed?: Array<{ node_id: string; question: string; selected: string }>;
    recommendation?: {
      algorithm_slug: string;
      name: string;
      complexity: string;
      space: string;
      reasoning: string;
    };
  } | null>(null);

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const fetchStep = async (currentAnswers: Record<string, string>) => {
    setLoading(true);
    setError(null);
    try {
      const data = await api.traverseDecisionTree(currentAnswers);
      setCurrentQuestion(data);
    } catch (err: any) {
      console.error(err);
      setError(err.message || "Failed to traverse tree.");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchStep({});
  }, []);

  const handleSelectOption = (nodeId: string, optionLabel: string) => {
    const updated = { ...answers, [nodeId]: optionLabel };
    setAnswers(updated);
    fetchStep(updated);
  };

  const handleReset = () => {
    setAnswers({});
    fetchStep({});
  };

  return (
    <Layout>
      <div className="space-y-6 animate-in fade-in duration-200 max-w-5xl mx-auto">
        {/* Page Header */}
        <PageHeader
          breadcrumb="Decision Support"
          title="Interactive Algorithm Decision Tree"
          description="Deterministic guided selection navigating problem parameters, input distributions, memory limits, and invariance constraints."
          actions={
            <Button
              variant="ghost"
              size="sm"
              onClick={handleReset}
              icon={<RotateCcw className="w-3.5 h-3.5" />}
            >
              Reset Wizard
            </Button>
          }
        />

        {/* Path Traversal History */}
        {currentQuestion?.path_traversed && currentQuestion.path_traversed.length > 0 && (
          <div className="p-4 rounded-xl bg-[#0e131f] border border-slate-800 space-y-2">
            <div className="flex items-center justify-between text-[11px] font-mono text-slate-400">
              <span>Decision Path Traversed</span>
              <span>{currentQuestion.path_traversed.length} Step{currentQuestion.path_traversed.length > 1 ? "s" : ""}</span>
            </div>
            <div className="flex flex-wrap items-center gap-2 pt-1">
              {currentQuestion.path_traversed.map((step, idx) => (
                <div key={idx} className="flex items-center gap-2">
                  <div className="px-3 py-1.5 rounded-lg bg-slate-900 border border-slate-800 text-xs font-mono flex items-center gap-2">
                    <span className="text-slate-500 text-[10px]">#{idx + 1}</span>
                    <span className="text-sky-400 font-semibold">{step.selected}</span>
                  </div>
                  {idx < (currentQuestion.path_traversed?.length || 0) - 1 && (
                    <ArrowRight className="w-3 h-3 text-slate-600" />
                  )}
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Global Error */}
        {error && (
          <div className="p-4 rounded-xl bg-rose-500/10 border border-rose-500/30 text-rose-300 font-mono text-xs">
            {error}
          </div>
        )}

        {/* Loading State */}
        {loading && (
          <div className="p-12 rounded-xl bg-[#0e131f] border border-slate-800 text-center">
            <LoadingState message="Traversing decision tree branch..." />
          </div>
        )}

        {/* Current Active Question Node */}
        {currentQuestion?.status === "in_progress" && !loading && (
          <Card
            headerTag={`Decision Step ${(currentQuestion.path_traversed?.length || 0) + 1}`}
            headerRight={
              <Badge variant="primary" mono size="sm">
                Node ID: {currentQuestion.current_node_id || "root"}
              </Badge>
            }
          >
            <div className="space-y-6">
              <div className="flex items-start gap-3">
                <HelpCircle className="w-5 h-5 text-sky-400 flex-shrink-0 mt-0.5" />
                <h3 className="text-lg sm:text-xl font-semibold text-white tracking-tight leading-snug">
                  {currentQuestion.question}
                </h3>
              </div>

              <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 pt-1">
                {currentQuestion.options?.map((opt) => (
                  <button
                    key={opt}
                    disabled={loading}
                    onClick={() => handleSelectOption(currentQuestion.current_node_id || "root", opt)}
                    className="p-4 rounded-xl bg-slate-900 border border-slate-800 hover:border-sky-500/50 hover:bg-sky-500/5 text-left font-mono text-xs text-slate-200 hover:text-white transition-all flex items-center justify-between group cursor-pointer"
                  >
                    <span>{opt}</span>
                    <ArrowRight className="w-4 h-4 text-slate-500 group-hover:text-sky-400 group-hover:translate-x-0.5 transition-transform" />
                  </button>
                ))}
              </div>
            </div>
          </Card>
        )}

        {/* Final Recommendation Leaf */}
        {currentQuestion?.status === "completed" && currentQuestion.recommendation && !loading && (
          <Card
            headerTag="Deterministic Selection Result"
            headerRight={
              <Badge variant="success" mono size="md">
                Terminal Leaf Node
              </Badge>
            }
          >
            <div className="space-y-5">
              <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 border-b border-slate-800 pb-4">
                <div>
                  <div className="flex items-center gap-2 text-xs font-mono text-emerald-400 mb-1">
                    <CheckCircle2 className="w-4 h-4" />
                    <span>Exact Fit Decision Path</span>
                  </div>
                  <h2 className="text-2xl sm:text-3xl font-semibold text-white tracking-tight">
                    {currentQuestion.recommendation.name}
                  </h2>
                </div>

                <div className="flex items-center gap-2 flex-wrap">
                  <div className="px-3 py-1.5 rounded-lg bg-slate-900 border border-slate-800 text-xs font-mono">
                    <span className="text-slate-400">Time: </span>
                    <span className="text-emerald-400 font-semibold">{currentQuestion.recommendation.complexity}</span>
                  </div>
                  <div className="px-3 py-1.5 rounded-lg bg-slate-900 border border-slate-800 text-xs font-mono">
                    <span className="text-slate-400">Space: </span>
                    <span className="text-purple-400 font-semibold">{currentQuestion.recommendation.space}</span>
                  </div>
                </div>
              </div>

              <p className="text-sm text-slate-300 leading-relaxed font-sans">
                {currentQuestion.recommendation.reasoning}
              </p>

              {/* Action Buttons */}
              <div className="flex flex-wrap items-center gap-3 pt-3 border-t border-slate-800">
                <Link to={`/visualizer?algo=${currentQuestion.recommendation.algorithm_slug}`}>
                  <Button variant="primary" icon={<Play className="w-3.5 h-3.5" />}>
                    Step Visualizer
                  </Button>
                </Link>

                <Link to={`/complexity?algo=${currentQuestion.recommendation.algorithm_slug}`}>
                  <Button variant="secondary" icon={<HelpCircle className="w-3.5 h-3.5" />}>
                    Analyze Complexity
                  </Button>
                </Link>

                <Link to={`/benchmark?algos=${currentQuestion.recommendation.algorithm_slug}`}>
                  <Button variant="secondary" icon={<BarChart3 className="w-3.5 h-3.5" />}>
                    Benchmark Arena
                  </Button>
                </Link>

                <Link to={`/recommend?algos=${currentQuestion.recommendation.algorithm_slug}`}>
                  <Button variant="ghost" icon={<ArrowRight className="w-3.5 h-3.5" />}>
                    MCDA Evaluation
                  </Button>
                </Link>

                <Button variant="ghost" onClick={handleReset} icon={<RotateCcw className="w-3.5 h-3.5" />}>
                  Start New Query
                </Button>
              </div>
            </div>
          </Card>
        )}
      </div>
    </Layout>
  );
}
