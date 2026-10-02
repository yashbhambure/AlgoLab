import { useState, useEffect, useMemo } from "react";
import { useSearchParams, Link } from "react-router-dom";
import {
  Search,
  Play,
  BarChart3,
  Code2,
  CheckCircle2,
  XCircle,
  X,
  Copy,
  Check,
  Layers,
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
import type { Algorithm } from "../types";

const PARADIGM_OPTIONS = [
  "All",
  "Divide & Conquer",
  "Backtracking",
  "Dynamic Programming",
  "Greedy Method",
  "Branch & Bound",
];

function matchesParadigmFilter(algo: Algorithm, selected: string): boolean {
  if (!selected || selected === "All") return true;

  const normalize = (str: string) =>
    (str || "")
      .toLowerCase()
      .replace(/&/g, "and")
      .replace(/[^a-z0-9]/g, "");

  const target = normalize(selected);
  const paradigm = normalize(algo.paradigm);
  const category = normalize(algo.category);

  if (target === "divideandconquer") {
    return paradigm === "divideandconquer" || category === "divideandconquer";
  }

  if (target === "sorting") {
    return category === "sorting" || paradigm === "sorting";
  }

  if (target === "searching") {
    return category === "searching" || paradigm === "searching";
  }

  if (target === "greedy") {
    return paradigm === "greedy" || category === "greedy";
  }

  if (target === "dynamicprogramming" || target === "dp") {
    return paradigm === "dynamicprogramming" || category === "dynamicprogramming";
  }

  if (target === "branchandbound" || target === "bb") {
    return (
      paradigm === "branchandbound" ||
      category === "branchandbound" ||
      category === "branchandboundtechniques"
    );
  }

  if (target === "graph") {
    return (
      category === "graph" ||
      paradigm === "graph" ||
      paradigm.startsWith("graphtraversal")
    );
  }

  if (target === "backtracking") {
    return paradigm === "backtracking" || category === "backtracking";
  }

  return paradigm === target || category === target;
}

export default function CatalogPage() {
  const [searchParams, setSearchParams] = useSearchParams();
  const initialParadigm = searchParams.get("paradigm") || "All";

  const [algorithms, setAlgorithms] = useState<Algorithm[]>([]);
  const [curriculumSlugs, setCurriculumSlugs] = useState<Set<string>>(new Set());
  const [loading, setLoading] = useState(true);
  const [searchQuery, setSearchQuery] = useState("");
  const [selectedParadigm, setSelectedParadigm] = useState(initialParadigm);

  useEffect(() => {
    const p = searchParams.get("paradigm");
    if (p) {
      setSelectedParadigm(p);
    } else if (p === null && selectedParadigm !== "All") {
      setSelectedParadigm("All");
    }
  }, [searchParams]);

  // Modal for source code viewer
  const [activeCodeAlgo, setActiveCodeAlgo] = useState<Algorithm | null>(null);
  const [codeData, setCodeData] = useState<{ code: string; pseudocode: string } | null>(null);
  const [loadingCode, setLoadingCode] = useState(false);
  const [copiedCode, setCopiedCode] = useState(false);
  const [activeCodeTab, setActiveCodeTab] = useState<"c" | "pseudocode">("c");

  useEffect(() => {
    Promise.all([
      api.getAlgorithms(),
      api.getApprovedCurriculumSlugs().catch(() => [] as string[])
    ])
      .then(([algos, slugs]) => {
        setAlgorithms(algos);
        setCurriculumSlugs(new Set(slugs));
      })
      .catch((err) => console.error("Failed to fetch algorithm catalog:", err))
      .finally(() => setLoading(false));
  }, []);

  const handleOpenCode = async (algo: Algorithm) => {
    setActiveCodeAlgo(algo);
    setActiveCodeTab("c");
    setLoadingCode(true);
    try {
      const data = await api.getAlgorithmCode(algo.slug);
      const cSource = data.c_source_code || (data as any).code || `/* C implementation for ${algo.name} */`;
      const pseudoSource = data.pseudocode || `// Formal pseudocode for ${algo.name}`;
      setCodeData({
        code: cSource,
        pseudocode: pseudoSource,
      });
    } catch (err) {
      console.error("Failed to load code:", err);
      setCodeData({
        code: `/* Unable to fetch C source code for ${algo.name} */`,
        pseudocode: `// Formal pseudocode for ${algo.name}`,
      });
    } finally {
      setLoadingCode(false);
    }
  };

  const handleCopy = (text?: string) => {
    if (!text) return;
    navigator.clipboard.writeText(text);
    setCopiedCode(true);
    setTimeout(() => setCopiedCode(false), 2000);
  };

  const filteredAlgorithms = useMemo(() => {
    return algorithms.filter((algo) => {
      const matchesSearch =
        algo.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
        algo.slug.toLowerCase().includes(searchQuery.toLowerCase()) ||
        algo.category.toLowerCase().includes(searchQuery.toLowerCase()) ||
        algo.description.toLowerCase().includes(searchQuery.toLowerCase());

      const matchesParadigm = matchesParadigmFilter(algo, selectedParadigm);

      return matchesSearch && matchesParadigm;
    });
  }, [algorithms, searchQuery, selectedParadigm]);

  return (
    <Layout>
      <div className="space-y-6 animate-in fade-in duration-200">
        {/* Page Header */}
        <PageHeader
          breadcrumb="DAA Reference"
          title="Algorithm Catalog & Specifications"
          description={`Browse and examine ${algorithms.length || 46} algorithms across ${PARADIGM_OPTIONS.length - 1} design paradigms with formal asymptotic bounds, auxiliary space, and implementation code.`}
          actions={
            <div className="flex items-center gap-2.5">
              <Link to="/benchmark">
                <Button variant="primary" icon={<BarChart3 className="w-4 h-4" />}>
                  Benchmark Arena
                </Button>
              </Link>
              <Link to="/recommend">
                <Button variant="secondary" icon={<Sparkles className="w-4 h-4" />}>
                  MCDA Evaluation
                </Button>
              </Link>
            </div>
          }
        />

        {/* Filter and Search Bar */}
        <div className="p-4 rounded-xl bg-[#0e131f] border border-slate-800 space-y-3">
          <div className="flex flex-col md:flex-row gap-3 items-stretch md:items-center justify-between">
            {/* Search Box */}
            <div className="relative flex-1 max-w-md">
              <Search className="w-4 h-4 text-slate-400 absolute left-3.5 top-1/2 -translate-y-1/2 pointer-events-none" />
              <input
                type="text"
                placeholder="Search by name, category, or keyword..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                className="w-full pl-9 pr-8 py-2 bg-slate-900/90 border border-slate-800 rounded-lg text-xs font-mono text-slate-100 placeholder-slate-500 focus:outline-none focus:border-sky-500 focus:ring-1 focus:ring-sky-500 transition-colors"
              />
              {searchQuery && (
                <button
                  onClick={() => setSearchQuery("")}
                  className="absolute right-2.5 top-1/2 -translate-y-1/2 text-slate-400 hover:text-white text-xs p-1"
                  title="Clear search"
                >
                  <X className="w-3.5 h-3.5" />
                </button>
              )}
            </div>

            {/* Results Count */}
            <div className="flex items-center gap-2 text-xs font-mono text-slate-400 justify-between md:justify-end">
              <span>
                Showing <strong className="text-white">{filteredAlgorithms.length}</strong> of {algorithms.length || 35} algorithms
              </span>
            </div>
          </div>

          {/* Paradigm Chips */}
          <div className="flex items-center gap-1.5 overflow-x-auto pt-1 pb-1 scrollbar-thin border-t border-slate-800/80">
            <span className="text-[11px] font-mono text-slate-400 mr-1 hidden sm:inline">Paradigm:</span>
            {PARADIGM_OPTIONS.map((paradigm) => {
              const active = selectedParadigm === paradigm;
              return (
                <button
                  key={paradigm}
                  onClick={() => {
                    setSelectedParadigm(paradigm);
                    setSearchParams(paradigm === "All" ? {} : { paradigm });
                  }}
                  className={`px-3 py-1.5 rounded-lg text-xs font-medium whitespace-nowrap transition-colors flex items-center gap-1.5 ${
                    active
                      ? "bg-sky-500/15 text-sky-400 border border-sky-500/30 font-semibold"
                      : "bg-slate-900/60 border border-slate-800 text-slate-400 hover:text-slate-200 hover:border-slate-700"
                  }`}
                >
                  {paradigm === "All" && <Layers className="w-3 h-3 text-slate-400" />}
                  <span>{paradigm}</span>
                </button>
              );
            })}
          </div>
        </div>

        {/* Algorithms Grid */}
        {loading ? (
          <div className="py-20">
            <LoadingState message="Loading canonical algorithm specifications..." />
          </div>
        ) : filteredAlgorithms.length === 0 ? (
          <EmptyState
            title="No matching algorithms found"
            message={`No specifications found matching "${searchQuery}" in ${selectedParadigm}. Try resetting filters.`}
            action={
              <Button
                variant="secondary"
                size="sm"
                onClick={() => {
                  setSearchQuery("");
                  setSelectedParadigm("All");
                  setSearchParams({});
                }}
              >
                Reset All Filters
              </Button>
            }
          />
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {filteredAlgorithms.map((algo) => (
              <Card
                key={algo.slug}
                className="flex flex-col justify-between hover:border-slate-700 transition-colors"
              >
                <div className="space-y-3.5">
                  {/* Card Header */}
                  <div className="flex items-start justify-between gap-2 border-b border-slate-800/80 pb-3">
                    <div>
                      <span className="text-[11px] font-mono font-medium text-sky-400 block mb-0.5">
                        {algo.paradigm}
                      </span>
                      <Link to={`/algorithms/${algo.slug}`}>
                        <h3 className="font-semibold text-base text-white tracking-tight hover:text-sky-300 transition-colors">
                          {algo.name}
                        </h3>
                      </Link>
                    </div>
                    <div className="flex flex-col items-end gap-1.5">
                      {curriculumSlugs.has(algo.slug) ? (
                        <span className="px-2 py-0.5 rounded text-[10px] font-mono font-medium bg-emerald-500/15 text-emerald-400 border border-emerald-500/30">
                          Curriculum
                        </span>
                      ) : (
                        <span className="px-2 py-0.5 rounded text-[10px] font-mono font-medium bg-slate-800/80 text-slate-400 border border-slate-700/60">
                          Supplementary
                        </span>
                      )}
                      <Badge variant="default" mono size="sm">
                        {algo.category}
                      </Badge>
                    </div>
                  </div>

                  {/* Description */}
                  <p className="text-slate-400 text-xs leading-relaxed line-clamp-2">
                    {algo.description}
                  </p>

                  {/* Asymptotic Complexity Matrix */}
                  <div className="grid grid-cols-2 gap-2 p-3 rounded-lg bg-slate-900/80 border border-slate-800 text-[11px] font-mono">
                    <div className="space-y-0.5">
                      <span className="text-slate-400 text-[10px] block">Best Case</span>
                      <span className="text-emerald-400 font-semibold">{algo.best_case || algo.time_complexity_best || "O(?)"}</span>
                    </div>
                    <div className="space-y-0.5">
                      <span className="text-slate-400 text-[10px] block">Average Case</span>
                      <span className="text-sky-400 font-semibold">{algo.average_case || algo.time_complexity_average || "O(?)"}</span>
                    </div>
                    <div className="space-y-0.5">
                      <span className="text-slate-400 text-[10px] block">Worst Case</span>
                      <span className="text-amber-400 font-semibold">{algo.worst_case || algo.time_complexity_worst || "O(?)"}</span>
                    </div>
                    <div className="space-y-0.5">
                      <span className="text-slate-400 text-[10px] block">Aux Space</span>
                      <span className="text-purple-400 font-semibold">{algo.space_complexity}</span>
                    </div>
                  </div>

                  {/* Algorithmic Properties */}
                  <div className="flex items-center gap-4 text-xs font-mono text-slate-400 pt-1">
                    <span className="flex items-center gap-1.5">
                      {algo.is_stable ? (
                        <CheckCircle2 className="w-3.5 h-3.5 text-emerald-400" />
                      ) : (
                        <XCircle className="w-3.5 h-3.5 text-slate-600" />
                      )}
                      <span className={algo.is_stable ? "text-slate-300" : "text-slate-400"}>
                        Stable
                      </span>
                    </span>

                    <span className="flex items-center gap-1.5">
                      {algo.is_in_place ? (
                        <CheckCircle2 className="w-3.5 h-3.5 text-emerald-400" />
                      ) : (
                        <XCircle className="w-3.5 h-3.5 text-slate-600" />
                      )}
                      <span className={algo.is_in_place ? "text-slate-300" : "text-slate-400"}>
                        In-Place
                      </span>
                    </span>
                  </div>
                </div>

                {/* Card Actions */}
                <div className="flex items-center justify-between pt-3.5 mt-4 border-t border-slate-800">
                  <div className="flex items-center gap-2">
                    <button
                      onClick={() => handleOpenCode(algo)}
                      className="text-xs font-mono font-medium text-sky-400 hover:text-sky-300 flex items-center gap-1 transition-colors"
                      title="View C source & pseudocode"
                    >
                      <Code2 className="w-3.5 h-3.5" />
                      <span>Code</span>
                    </button>
                    <Link
                      to={`/algorithms/${algo.slug}`}
                      className="text-xs font-mono font-medium text-slate-400 hover:text-white flex items-center gap-1 transition-colors"
                    >
                      <span>Detail</span>
                    </Link>
                  </div>

                  <div className="flex items-center gap-1.5">
                    <Link to={`/visualizer?algo=${algo.slug}`}>
                      <Button variant="ghost" size="sm" icon={<Play className="w-3 h-3" />}>
                        Visualizer
                      </Button>
                    </Link>

                    <Link to={`/benchmark?algos=${algo.slug}`}>
                      <Button variant="secondary" size="sm" icon={<BarChart3 className="w-3 h-3" />}>
                        Benchmark
                      </Button>
                    </Link>
                  </div>
                </div>
              </Card>
            ))}
          </div>
        )}

        {/* Source Code Modal */}
        {activeCodeAlgo && (
          <div
            className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/80 backdrop-blur-sm animate-in fade-in duration-150"
            role="dialog"
            aria-modal="true"
            aria-labelledby="code-modal-title"
          >
            <div className="relative w-full max-w-4xl max-h-[85vh] overflow-hidden rounded-xl bg-[#0e131f] border border-slate-800 shadow-2xl flex flex-col">
              {/* Modal Header */}
              <div className="flex items-center justify-between px-6 py-4 border-b border-slate-800 bg-[#141b2d]">
                <div className="flex items-center gap-3">
                  <div className="p-2 rounded-lg bg-sky-500/10 border border-sky-500/20 text-sky-400">
                    <Code2 className="w-5 h-5" />
                  </div>
                  <div>
                    <h3 id="code-modal-title" className="font-semibold text-white text-base">
                      {activeCodeAlgo.name}
                    </h3>
                    <div className="flex items-center gap-2 text-xs font-mono text-slate-400 mt-0.5">
                      <span>{activeCodeAlgo.paradigm}</span>
                      <span>&bull;</span>
                      <span>{activeCodeAlgo.category}</span>
                    </div>
                  </div>
                </div>

                <div className="flex items-center gap-2">
                  <Button
                    variant="ghost"
                    size="sm"
                    onClick={() =>
                      handleCopy(
                        activeCodeTab === "c" ? codeData?.code : codeData?.pseudocode
                      )
                    }
                    icon={copiedCode ? <Check className="w-3.5 h-3.5 text-emerald-400" /> : <Copy className="w-3.5 h-3.5" />}
                  >
                    {copiedCode ? "Copied" : "Copy"}
                  </Button>
                  <button
                    onClick={() => setActiveCodeAlgo(null)}
                    className="p-1.5 rounded-lg text-slate-400 hover:text-white hover:bg-slate-800 transition-colors"
                    aria-label="Close modal"
                  >
                    <X className="w-5 h-5" />
                  </button>
                </div>
              </div>

              {/* View Tabs */}
              <div className="flex items-center gap-2 px-6 pt-3 pb-2 border-b border-slate-800/80 bg-[#0e131f]">
                <button
                  onClick={() => setActiveCodeTab("c")}
                  className={`px-3 py-1.5 rounded-lg text-xs font-mono font-medium transition-colors ${
                    activeCodeTab === "c"
                      ? "bg-sky-500/15 text-sky-400 border border-sky-500/30"
                      : "text-slate-400 hover:text-white"
                  }`}
                >
                  C Implementation
                </button>
                <button
                  onClick={() => setActiveCodeTab("pseudocode")}
                  className={`px-3 py-1.5 rounded-lg text-xs font-mono font-medium transition-colors ${
                    activeCodeTab === "pseudocode"
                      ? "bg-purple-500/15 text-purple-400 border border-purple-500/30"
                      : "text-slate-400 hover:text-white"
                  }`}
                >
                  Formal DAA Pseudocode
                </button>
              </div>

              {/* Modal Body */}
              <div className="p-6 overflow-y-auto font-mono text-xs">
                {loadingCode ? (
                  <div className="py-16">
                    <LoadingState message="Extracting source code and pseudocode..." />
                  </div>
                ) : (
                  <div className="space-y-4">
                    {activeCodeTab === "c" && (
                      <div>
                        <div className="flex items-center justify-between mb-2">
                          <span className="text-[11px] text-slate-400">C11 Standard Source Code</span>
                          <span className="text-[11px] text-emerald-400 font-mono">GCC C11 Compilable</span>
                        </div>
                        <pre className="p-4 rounded-lg bg-[#080b11] border border-slate-800 text-slate-200 overflow-x-auto text-xs leading-relaxed">
                          <code>{codeData?.code}</code>
                        </pre>
                      </div>
                    )}

                    {activeCodeTab === "pseudocode" && (
                      <div>
                        <div className="flex items-center justify-between mb-2">
                          <span className="text-[11px] text-slate-400">Formal Academic Pseudocode</span>
                          <span className="text-[11px] text-slate-400">CLRS Standard</span>
                        </div>
                        <pre className="p-4 rounded-lg bg-[#080b11] border border-slate-800 text-slate-300 overflow-x-auto text-xs leading-relaxed">
                          <code>{codeData?.pseudocode}</code>
                        </pre>
                      </div>
                    )}
                  </div>
                )}
              </div>
            </div>
          </div>
        )}
      </div>
    </Layout>
  );
}
