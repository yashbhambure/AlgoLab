import { useState, useEffect } from "react";
import {
  Play,
  Download,
  FileText,
} from "lucide-react";
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from "recharts";
import { Layout } from "../components/layout/Layout";
import { PageHeader } from "../components/layout/PageHeader";
import { Card } from "../components/common/Card";
import { Button } from "../components/common/Button";
import { Badge } from "../components/common/Badge";
import { LoadingState } from "../components/common/LoadingState";
import { EmptyState } from "../components/common/EmptyState";
import { api } from "../services/api";
import type { Experiment, Algorithm } from "../types";

const SIZES = [50, 100, 250, 500, 1000, 2500, 5000];
const CHART_COLORS = [
  "#38bdf8", // Sky 400
  "#818cf8", // Indigo 400
  "#34d399", // Emerald 400
  "#fbbf24", // Amber 400
  "#f43f5e", // Rose 500
  "#c084fc", // Purple 400
  "#2dd4bf", // Teal 400
  "#fb923c", // Orange 400
];

export default function ExperimentsPage() {
  const [experiments, setExperiments] = useState<Experiment[]>([]);
  const [loading, setLoading] = useState(true);
  const [selectedExperiment, setSelectedExperiment] = useState<Experiment | null>(null);

  // New Experiment Run State
  const [expTitle, setExpTitle] = useState("0/1 Knapsack Paradigm Comparison Run");
  const expDesc = "Comparing Dynamic Programming vs Branch & Bound scaling curves across item sizes.";
  const [selectedAlgos, setSelectedAlgos] = useState<string[]>([
    "0-1-knapsack-dp",
    "0-1-knapsack-lc-bb",
    "0-1-knapsack-fifo-bb",
  ]);
  const [availableAlgos, setAvailableAlgos] = useState<Algorithm[]>([]);
  const [selectedSizes, setSelectedSizes] = useState<number[]>([4, 6, 8, 10, 12]);
  const [distribution, setDistribution] = useState("random");
  const [running, setRunning] = useState(false);
  const [runProgress, setRunProgress] = useState(0);

  useEffect(() => {
    loadExperiments();
    api.getAlgorithms()
      .then(setAvailableAlgos)
      .catch(console.error);
  }, []);

  const loadExperiments = async () => {
    setLoading(true);
    try {
      const res = await api.getExperiments();
      setExperiments(res);
      if (res.length > 0 && !selectedExperiment) {
        setSelectedExperiment(res[0]);
      }
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleToggleSize = (size: number) => {
    if (selectedSizes.includes(size)) {
      if (selectedSizes.length > 2) {
        setSelectedSizes(selectedSizes.filter((s) => s !== size));
      }
    } else {
      setSelectedSizes([...selectedSizes, size].sort((a, b) => a - b));
    }
  };

  const handleToggleAlgo = (slug: string) => {
    if (selectedAlgos.includes(slug)) {
      if (selectedAlgos.length > 1) {
        setSelectedAlgos(selectedAlgos.filter((s) => s !== slug));
      }
    } else {
      setSelectedAlgos([...selectedAlgos, slug]);
    }
  };

  const handleRunExperiment = async () => {
    setRunning(true);
    setRunProgress(0);

    const resultsSummary: Record<string, Array<{ n: number; mean_ms: number; mem_kb: number }>> = {};
    selectedAlgos.forEach((slug) => {
      resultsSummary[slug] = [];
    });

    try {
      const totalSteps = selectedSizes.length;
      for (let i = 0; i < totalSteps; i++) {
        const size = selectedSizes[i];

        // 1. Generate dataset
        const dataset = await api.generateDataset({
          problem_type: "sorting",
          data_type: "array",
          size: size,
          distribution: distribution,
        });

        // 2. Run benchmark for all candidates on this size
        const bench = await api.runComparisonBenchmark({
          algorithm_slugs: selectedAlgos,
          dataset_name: `N=${size}`,
          input_data: dataset.data_payload,
          repetitions: 3,
          warmup_runs: 1,
        });

        bench.results.forEach((r) => {
          if (!resultsSummary[r.algorithm_slug]) {
            resultsSummary[r.algorithm_slug] = [];
          }
          resultsSummary[r.algorithm_slug].push({
            n: size,
            mean_ms: Number(r.time_stats.mean_ms.toFixed(4)),
            mem_kb: Number(r.memory_stats.peak_kb.toFixed(2)),
          });
        });

        setRunProgress(Math.round(((i + 1) / totalSteps) * 100));
      }

      // 3. Save experiment to database
      const saved = await api.createExperiment({
        title: expTitle,
        description: expDesc,
        benchmark_payload: {
          results: resultsSummary,
          input_sizes: selectedSizes,
          distribution: distribution,
          algorithm_ids: selectedAlgos,
        },
      });

      await loadExperiments();
      setSelectedExperiment(saved);
    } catch (err) {
      console.error("Experiment failed:", err);
    } finally {
      setRunning(false);
    }
  };

  const handleExport = async (id: string, format: "json" | "markdown") => {
    try {
      const url = `/api/v1/experiments/${id}/export?format=${format}`;
      const response = await fetch(url);
      const text = await response.text();

      const blob = new Blob([text], {
        type: format === "markdown" ? "text/markdown" : "application/json",
      });
      const downloadUrl = URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = downloadUrl;
      a.download = `experiment_${id}.${format === "markdown" ? "md" : "json"}`;
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
    } catch (err) {
      console.error(err);
    }
  };

  // Prepare chart data for selected experiment
  const activeResults =
    selectedExperiment?.benchmark_payload?.results ||
    (selectedExperiment as any)?.results_summary ||
    {};

  const chartDataMap: Record<number, any> = {};
  Object.keys(activeResults).forEach((slug) => {
    const points = activeResults[slug];
    if (Array.isArray(points)) {
      points.forEach((pt: any) => {
        if (!chartDataMap[pt.n]) chartDataMap[pt.n] = { n: pt.n };
        chartDataMap[pt.n][slug] = pt.mean_ms;
      });
    }
  });

  const chartData = Object.values(chartDataMap).sort((a: any, b: any) => a.n - b.n);

  return (
    <Layout>
      <div className="space-y-6 animate-in fade-in duration-200">
        {/* Page Header */}
        <PageHeader
          breadcrumb="Empirical Laboratory"
          title="Scaling Experiments & Reproducibility"
          description="Conduct multi-size dataset scaling sweeps, track asymptotic growth curves, manage persistent experiment archives, and export peer-reviewed reports."
        />

        {/* Create New Experiment Panel */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-5">
          <div className="lg:col-span-2">
            <Card
              headerTag="Configure Scaling Sweep"
              headerRight={
                <Badge variant="primary" mono size="sm">
                  {selectedAlgos.length} Algorithms &bull; {selectedSizes.length} Sizes
                </Badge>
              }
            >
              <div className="space-y-4 font-mono text-xs">
                {/* Title & Distribution */}
                <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
                  <div>
                    <label className="text-[11px] text-slate-400 block mb-1">
                      Experiment Title
                    </label>
                    <input
                      type="text"
                      value={expTitle}
                      onChange={(e) => setExpTitle(e.target.value)}
                      className="w-full px-3 py-1.5 rounded-lg bg-slate-900 border border-slate-800 text-xs text-white focus:outline-none focus:border-sky-500"
                    />
                  </div>
                  <div>
                    <label className="text-[11px] text-slate-400 block mb-1">
                      Dataset Distribution
                    </label>
                    <select
                      value={distribution}
                      onChange={(e) => setDistribution(e.target.value)}
                      className="w-full px-3 py-1.5 rounded-lg bg-slate-900 border border-slate-800 text-xs text-white focus:outline-none focus:border-sky-500 font-sans"
                    >
                      <option value="random">Random Uniform</option>
                      <option value="nearly_sorted">Nearly Sorted</option>
                      <option value="reverse">Strictly Reverse Sorted</option>
                    </select>
                  </div>
                </div>

                {/* Candidate Selection */}
                <div>
                  <label className="text-[11px] text-slate-400 block mb-1.5">
                    Candidate Algorithms
                  </label>
                  <div className="flex flex-wrap gap-1.5">
                    {availableAlgos.map((algo) => {
                      const sel = selectedAlgos.includes(algo.slug);
                      return (
                        <button
                          key={algo.slug}
                          onClick={() => handleToggleAlgo(algo.slug)}
                          className={`px-3 py-1.5 rounded-lg text-xs font-medium transition-colors ${
                            sel
                              ? "bg-sky-500/15 text-sky-400 border border-sky-500/30 font-semibold"
                              : "bg-slate-900/60 border border-slate-800 text-slate-400 hover:text-slate-200 hover:border-slate-700"
                          }`}
                        >
                          {algo.name}
                        </button>
                      );
                    })}
                  </div>
                </div>

                {/* Input Sizes */}
                <div>
                  <label className="text-[11px] text-slate-400 block mb-1.5">
                    Input Sizes Sweep (N)
                  </label>
                  <div className="flex flex-wrap gap-1.5">
                    {SIZES.map((size) => {
                      const sel = selectedSizes.includes(size);
                      return (
                        <button
                          key={size}
                          onClick={() => handleToggleSize(size)}
                          className={`px-3 py-1.5 rounded-lg text-xs font-medium transition-colors ${
                            sel
                              ? "bg-purple-500/15 text-purple-400 border border-purple-500/30 font-semibold"
                              : "bg-slate-900/60 border border-slate-800 text-slate-400 hover:text-slate-200 hover:border-slate-700"
                          }`}
                        >
                          N={size}
                        </button>
                      );
                    })}
                  </div>
                </div>

                {/* Progress Bar when running */}
                {running && (
                  <div className="space-y-1.5 pt-2">
                    <div className="flex justify-between text-[11px] text-slate-400">
                      <span>Executing scaling iterations...</span>
                      <span className="text-sky-400 font-semibold">{runProgress}%</span>
                    </div>
                    <div className="w-full h-2 bg-slate-900 rounded-full overflow-hidden border border-slate-800">
                      <div
                        style={{ width: `${runProgress}%` }}
                        className="h-full bg-sky-500 transition-all duration-200"
                      />
                    </div>
                  </div>
                )}

                {/* Launch Button */}
                <div className="pt-2">
                  <Button
                    variant="primary"
                    onClick={handleRunExperiment}
                    disabled={running || selectedAlgos.length === 0}
                    loading={running}
                    icon={<Play className="w-3.5 h-3.5" />}
                    className="w-full justify-center"
                  >
                    {running ? `Running Scaling Sweep (${runProgress}%)...` : "Execute Scaling Experiment"}
                  </Button>
                </div>
              </div>
            </Card>
          </div>

          {/* Past Experiments List */}
          <Card
            headerTag="Experiment Archive"
            headerRight={
              <Badge variant="default" mono size="sm">
                {experiments.length} Saved
              </Badge>
            }
          >
            <div className="space-y-2 max-h-[340px] overflow-y-auto font-mono text-xs pr-1 scrollbar-thin">
              {loading ? (
                <div className="py-12">
                  <LoadingState message="Loading archived experiments..." />
                </div>
              ) : experiments.length === 0 ? (
                <div className="py-12">
                  <EmptyState
                    title="No experiments saved"
                    message="Configure and run your first scaling sweep on the left to persist empirical benchmarks."
                  />
                </div>
              ) : (
                experiments.map((exp) => {
                  const isSelected = selectedExperiment?.id === exp.id;
                  return (
                    <div
                      key={exp.id}
                      onClick={() => setSelectedExperiment(exp)}
                      className={`p-3 rounded-lg border cursor-pointer transition-colors ${
                        isSelected
                          ? "bg-sky-500/10 border-sky-500/30 text-white"
                          : "bg-slate-900/60 border-slate-800 text-slate-400 hover:text-slate-200 hover:border-slate-700"
                      }`}
                    >
                      <div className="font-semibold text-slate-200 truncate">
                        {exp.title || (exp as any).name}
                      </div>
                      <div className="text-[10px] text-slate-500 mt-1 flex items-center justify-between">
                        <span>{new Date(exp.created_at).toLocaleDateString()}</span>
                        <span className="text-sky-400">{(exp as any).dataset_distribution || "random"}</span>
                      </div>
                    </div>
                  );
                })
              )}
            </div>
          </Card>
        </div>

        {/* Selected Experiment View */}
        {selectedExperiment && (
          <div className="space-y-5 animate-in fade-in duration-200">
            {/* Experiment Detail & Export Controls Card */}
            <Card
              headerTag="Experiment Session Analysis"
              headerRight={
                <div className="flex items-center gap-2">
                  <Button
                    variant="ghost"
                    size="sm"
                    onClick={() => handleExport(selectedExperiment.id, "markdown")}
                    icon={<FileText className="w-3.5 h-3.5" />}
                  >
                    Export Markdown
                  </Button>
                  <Button
                    variant="secondary"
                    size="sm"
                    onClick={() => handleExport(selectedExperiment.id, "json")}
                    icon={<Download className="w-3.5 h-3.5" />}
                  >
                    Export JSON
                  </Button>
                </div>
              }
            >
              <div className="space-y-4">
                <div>
                  <h3 className="text-xl font-semibold text-white tracking-tight">
                    {selectedExperiment.title || (selectedExperiment as any).name}
                  </h3>
                  <p className="text-xs text-slate-400 font-sans mt-1">
                    {(selectedExperiment as any).conclusion_notes ||
                      selectedExperiment.description ||
                      "Empirical scaling curve verification across input sizes."}
                  </p>
                </div>

                {/* Scaling Growth Chart */}
                {chartData.length > 0 ? (
                  <div className="pt-3 border-t border-slate-800">
                    <div className="flex items-center justify-between mb-3 text-xs font-mono text-slate-400">
                      <span>Empirical Scaling Curves (N vs Mean Runtime ms)</span>
                      <span>Logarithmic Grid</span>
                    </div>

                    <div className="h-80 w-full">
                      <ResponsiveContainer width="100%" height="100%">
                        <LineChart data={chartData} margin={{ top: 10, right: 10, left: 0, bottom: 20 }}>
                          <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" />
                          <XAxis
                            dataKey="n"
                            stroke="#64748b"
                            fontSize={11}
                            fontFamily="JetBrains Mono, monospace"
                            label={{
                              value: "Input Size (N)",
                              position: "insideBottom",
                              offset: -12,
                              fill: "#64748b",
                              fontSize: 11,
                              fontFamily: "JetBrains Mono, monospace",
                            }}
                          />
                          <YAxis
                            stroke="#64748b"
                            fontSize={11}
                            fontFamily="JetBrains Mono, monospace"
                            label={{
                              value: "Mean Time (ms)",
                              angle: -90,
                              position: "insideLeft",
                              fill: "#64748b",
                              fontSize: 11,
                              fontFamily: "JetBrains Mono, monospace",
                            }}
                          />
                          <Tooltip
                            contentStyle={{
                              backgroundColor: "#0e131f",
                              borderColor: "#1e293b",
                              borderRadius: "8px",
                              fontFamily: "JetBrains Mono, monospace",
                              fontSize: "11px",
                              color: "#f8fafc",
                            }}
                          />
                          <Legend
                            wrapperStyle={{
                              fontSize: "11px",
                              fontFamily: "JetBrains Mono, monospace",
                              paddingTop: "8px",
                            }}
                          />
                          {Object.keys(activeResults).map((slug, i) => (
                            <Line
                              key={slug}
                              type="monotone"
                              dataKey={slug}
                              stroke={CHART_COLORS[i % CHART_COLORS.length]}
                              strokeWidth={2}
                              dot={{ r: 3.5, fill: CHART_COLORS[i % CHART_COLORS.length] }}
                              name={slug.replace(/-/g, " ")}
                            />
                          ))}
                        </LineChart>
                      </ResponsiveContainer>
                    </div>
                  </div>
                ) : (
                  <div className="py-8">
                    <EmptyState
                      title="No telemetry datapoints"
                      message="No empirical timing series was recorded for this experiment payload."
                    />
                  </div>
                )}
              </div>
            </Card>
          </div>
        )}
      </div>
    </Layout>
  );
}
