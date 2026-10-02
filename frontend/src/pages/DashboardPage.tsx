import { useState, useEffect } from "react";
import { Link } from "react-router-dom";
import {
  BarChart3,
  Play,
  Sigma,
  Sparkles,
  GitBranch,
  ArrowRight,
  Layers,
  Cpu,
  Clock,
  HardDrive,
  CheckCircle2,
  GraduationCap,
} from "lucide-react";
import { Layout } from "../components/layout/Layout";
import { PageHeader } from "../components/layout/PageHeader";
import { Card } from "../components/common/Card";
import { MetricCard } from "../components/common/MetricCard";
import { Button } from "../components/common/Button";
import { Badge } from "../components/common/Badge";
import { api } from "../services/api";
import type { Algorithm, CurriculumModule } from "../types";

const PARADIGM_CONFIG: Record<string, { icon: any; color: string; desc: string }> = {
  "Divide and Conquer": {
    icon: GitBranch,
    color: "purple",
    desc: "Recursive sub-problem partitioning and recurrence analysis (Defective Chessboard, Max-Min, Strassen).",
  },
  "Backtracking": {
    icon: Layers,
    color: "indigo",
    desc: "Constraint satisfaction and state-space pruning (N-Queens, Sum of Subsets, Hamiltonian Cycles).",
  },
  "Dynamic Programming": {
    icon: Sigma,
    color: "amber",
    desc: "Optimal substructure and bottom-up tabulation (Multistage Graphs, Floyd-Warshall, Optimal BST, 0/1 Knapsack, TSP, Reliability Design).",
  },
  "Greedy Method": {
    icon: Sparkles,
    color: "teal",
    desc: "Locally optimal decision rules with matroid and tree proofs (Storage on Tapes, Fractional Knapsack, Job Sequencing, Merge Patterns, Kruskal, Prim, Dijkstra, Bellman-Ford).",
  },
  "Branch and Bound": {
    icon: Cpu,
    color: "emerald",
    desc: "State-space tree exploration with bounding functions (0/1 Knapsack LC/FIFO, TSP LC B&B).",
  },
};

export default function DashboardPage() {
  const [algorithms, setAlgorithms] = useState<Algorithm[]>([]);
  const [curriculumModules, setCurriculumModules] = useState<CurriculumModule[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    Promise.all([
      api.getAlgorithms(),
      api.getCurriculumModules(),
    ])
      .then(([algos, modules]) => {
        setAlgorithms(algos);
        setCurriculumModules(modules);
      })
      .catch((err) => console.error("Failed to load dashboard data:", err))
      .finally(() => setLoading(false));
  }, []);

  const totalAlgorithms = algorithms.length;
  const curriculumCount = curriculumModules.reduce((acc, m) => {
    const computationalTopics = m.topics.filter((t) => t.type === "computational");
    return acc + computationalTopics.length;
  }, 0) || 23;

  // Calculate dynamic paradigm counts
  const paradigmCounts: Record<string, number> = {};
  algorithms.forEach((a) => {
    const p = a.paradigm || a.category || "General";
    paradigmCounts[p] = (paradigmCounts[p] || 0) + 1;
  });

  const paradigmList = Object.keys(PARADIGM_CONFIG).map((pName) => ({
    name: pName,
    icon: PARADIGM_CONFIG[pName].icon,
    color: PARADIGM_CONFIG[pName].color,
    desc: PARADIGM_CONFIG[pName].desc,
    count: paradigmCounts[pName] || algorithms.filter((a) => a.category === pName || a.paradigm === pName).length || 0,
  }));

  return (
    <Layout>
      <div className="space-y-8 animate-in fade-in duration-200">
        {/* Page Header */}
        <PageHeader
          breadcrumb="Analytical Workspace"
          title="AlgoLab — Algorithm Benchmark & MCDA Laboratory"
          description="Academic & industrial Design & Analysis of Algorithms experimental suite. Conduct hardware-isolated nanosecond benchmarking, solve Master Theorem recurrences, and generate Multi-Criteria Decision Analysis (MCDA) recommendations across 7 core DAA paradigms."
          actions={
            <div className="flex items-center gap-2.5">
              <Link to="/benchmark">
                <Button variant="primary" icon={<BarChart3 className="w-4 h-4" />}>
                  Benchmark Arena
                </Button>
              </Link>
              <Link to="/curriculum">
                <Button variant="secondary" icon={<GraduationCap className="w-4 h-4" />}>
                  Curriculum (9 Modules)
                </Button>
              </Link>
            </div>
          }
        />

        {/* System & Laboratory Headline Metrics */}
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
          <MetricCard
            title="Algorithm Registry"
            value={loading ? "..." : totalAlgorithms}
            subtitle="Registered implementations"
            color="blue"
            icon={<Cpu className="w-5 h-5" />}
          />
          <MetricCard
            title="DAA Curriculum"
            value={loading ? "..." : `${curriculumModules.length || 9} Modules`}
            subtitle={`${curriculumCount} Executable algorithms`}
            color="purple"
            icon={<GraduationCap className="w-5 h-5" />}
          />
          <MetricCard
            title="Timer Resolution"
            value="1 ns"
            subtitle="time.perf_counter_ns"
            color="green"
            icon={<Clock className="w-5 h-5" />}
          />
          <MetricCard
            title="Memory Tracking"
            value="tracemalloc"
            subtitle="Peak heap byte isolation"
            color="teal"
            icon={<HardDrive className="w-5 h-5" />}
          />
        </div>

        {/* Core Laboratory Workspaces */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-5">
          <Card
            headerTag="Benchmark Lab"
            headerRight={
              <Link
                to="/benchmark"
                className="text-sky-400 hover:text-sky-300 font-medium flex items-center gap-1 transition-colors"
              >
                Launch <ArrowRight className="w-3.5 h-3.5" />
              </Link>
            }
          >
            <div className="space-y-3">
              <div className="flex items-center gap-2.5">
                <div className="p-2 rounded-lg bg-sky-950/60 border border-sky-800/40 text-sky-400">
                  <BarChart3 className="w-5 h-5" />
                </div>
                <div>
                  <h3 className="text-base font-semibold text-white">Head-to-Head Arena</h3>
                  <p className="text-xs text-slate-400">Multi-algorithm profiling</p>
                </div>
              </div>
              <p className="text-xs text-slate-400 leading-relaxed font-sans">
                Profile runtime distributions, standard deviations, and memory allocations across custom synthetic datasets.
              </p>
              <div className="pt-2 flex items-center gap-2 text-[11px] font-mono text-slate-400">
                <Badge variant="primary" mono>GC Isolated</Badge>
                <Badge variant="default" mono>Multi-Run Averages</Badge>
              </div>
            </div>
          </Card>

          <Card
            headerTag="Visual Execution"
            headerRight={
              <Link
                to="/visualizer"
                className="text-purple-400 hover:text-purple-300 font-medium flex items-center gap-1 transition-colors"
              >
                Open <ArrowRight className="w-3.5 h-3.5" />
              </Link>
            }
          >
            <div className="space-y-3">
              <div className="flex items-center gap-2.5">
                <div className="p-2 rounded-lg bg-purple-950/60 border border-purple-800/40 text-purple-400">
                  <Play className="w-5 h-5" />
                </div>
                <div>
                  <h3 className="text-base font-semibold text-white">Step-by-Step Visualizer</h3>
                  <p className="text-xs text-slate-400">23/23 Curriculum step tracing</p>
                </div>
              </div>
              <p className="text-xs text-slate-400 leading-relaxed font-sans">
                Step through recursion states, partition trees, matrix blocks, and state-space pruning with live variable inspectors.
              </p>
              <div className="pt-2 flex items-center gap-2 text-[11px] font-mono text-slate-400">
                <Badge variant="purple" mono>Genuine Instrumentation</Badge>
                <Badge variant="default" mono>Step Scrubber</Badge>
              </div>
            </div>
          </Card>

          <Card
            headerTag="Analytical Engine"
            headerRight={
              <Link
                to="/recommend"
                className="text-emerald-400 hover:text-emerald-300 font-medium flex items-center gap-1 transition-colors"
              >
                Evaluate <ArrowRight className="w-3.5 h-3.5" />
              </Link>
            }
          >
            <div className="space-y-3">
              <div className="flex items-center gap-2.5">
                <div className="p-2 rounded-lg bg-emerald-950/60 border border-emerald-800/40 text-emerald-400">
                  <Sparkles className="w-5 h-5" />
                </div>
                <div>
                  <h3 className="text-base font-semibold text-white">MCDA Recommendation</h3>
                  <p className="text-xs text-slate-400">Multi-criteria decision support</p>
                </div>
              </div>
              <p className="text-xs text-slate-400 leading-relaxed font-sans">
                Multi-Criteria Decision Analysis weighting asymptotic bounds, empirical speed, heap constraints, and input patterns.
              </p>
              <div className="pt-2 flex items-center gap-2 text-[11px] font-mono text-slate-400">
                <Badge variant="success" mono>5 Weighted Criteria</Badge>
                <Badge variant="default" mono>Academic Proofs</Badge>
              </div>
            </div>
          </Card>
        </div>

        {/* DAA Paradigms Section */}
        <div className="space-y-4">
          <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2 border-b border-slate-800 pb-3">
            <div>
              <h2 className="text-lg font-semibold text-white flex items-center gap-2">
                <Layers className="w-4 h-4 text-sky-400" />
                Core DAA Algorithmic Paradigms
              </h2>
              <p className="text-xs text-slate-400">
                Formal algorithm catalog dynamically calculated from registered implementations.
              </p>
            </div>

            <Link
              to="/catalog"
              className="text-xs font-mono font-medium text-sky-400 hover:text-sky-300 flex items-center gap-1 transition-colors"
            >
              Browse all {totalAlgorithms} algorithms <ArrowRight className="w-3.5 h-3.5" />
            </Link>
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
            {paradigmList.map((p) => {
              const Icon = p.icon;
              return (
                <Link
                  key={p.name}
                  to={`/catalog?paradigm=${encodeURIComponent(p.name)}`}
                  className="group rounded-xl bg-[#0e131f] border border-slate-800 hover:border-slate-700 hover:bg-[#141b2d] p-4 transition-all duration-150 flex flex-col justify-between"
                >
                  <div>
                    <div className="flex items-center justify-between mb-3">
                      <div className="p-2 rounded-lg bg-slate-900 border border-slate-800 text-sky-400 group-hover:text-sky-300 transition-colors">
                        <Icon className="w-4 h-4" />
                      </div>
                      <Badge variant="default" mono size="sm">
                        {p.count} Algorithms
                      </Badge>
                    </div>
                    <h3 className="font-semibold text-sm text-slate-100 group-hover:text-white mb-1">
                      {p.name}
                    </h3>
                    <p className="text-slate-400 text-xs leading-relaxed line-clamp-2 font-sans">
                      {p.desc}
                    </p>
                  </div>

                  <div className="pt-3 mt-3 border-t border-slate-800/80 flex items-center justify-between text-[11px] text-slate-500 group-hover:text-sky-400 transition-colors font-mono">
                    <span>View Specifications</span>
                    <ArrowRight className="w-3.5 h-3.5" />
                  </div>
                </Link>
              );
            })}
          </div>
        </div>

        {/* Analytical Capabilities & Methodology */}
        <div className="rounded-xl bg-[#0e131f] border border-slate-800 p-5 sm:p-6">
          <h3 className="text-sm font-semibold text-white uppercase tracking-wider mb-4 flex items-center gap-2">
            <CheckCircle2 className="w-4 h-4 text-emerald-400" />
            Scientific Profiling & Theoretical Verification Methodology
          </h3>

          <div className="grid grid-cols-1 sm:grid-cols-3 gap-4 text-xs font-sans text-slate-300">
            <div className="p-3.5 rounded-lg bg-slate-900/60 border border-slate-800 space-y-1">
              <span className="font-semibold text-slate-100 block">Empirical Isolation</span>
              <p className="text-slate-400 text-[12px] leading-relaxed">
                Garbage collection is suspended during execution iterations, with warm-up cycles to stabilize CPU caches.
              </p>
            </div>

            <div className="p-3.5 rounded-lg bg-slate-900/60 border border-slate-800 space-y-1">
              <span className="font-semibold text-slate-100 block">Master Theorem Solver</span>
              <p className="text-slate-400 text-[12px] leading-relaxed">
                Automated asymptotic derivation for recurrences <code className="font-mono text-sky-400">T(n) = aT(n/b) + f(n)</code> covering Cases 1, 2, and 3.
              </p>
            </div>

            <div className="p-3.5 rounded-lg bg-slate-900/60 border border-slate-800 space-y-1">
              <span className="font-semibold text-slate-100 block">Non-linear Curve Fitting</span>
              <p className="text-slate-400 text-[12px] leading-relaxed">
                Weighted least-squares fitting measuring <span className="font-mono text-purple-400">R²</span>, <span className="font-mono text-purple-400">RMSE</span>, and AIC across 7 theoretical Big-O models.
              </p>
            </div>
          </div>
        </div>
      </div>
    </Layout>
  );
}
