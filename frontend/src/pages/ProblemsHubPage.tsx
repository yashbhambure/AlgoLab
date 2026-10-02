import { useState, useEffect, useMemo } from "react";
import { Link, useSearchParams } from "react-router-dom";
import {
  Search,
  Code2,
  GraduationCap,
  BarChart3,
  X,
  ChevronRight,
} from "lucide-react";
import { Layout } from "../components/layout/Layout";
import { PageHeader } from "../components/layout/PageHeader";
import { Card } from "../components/common/Card";
import { Button } from "../components/common/Button";
import { Badge } from "../components/common/Badge";
import { LoadingState } from "../components/common/LoadingState";
import { EmptyState } from "../components/common/EmptyState";
import { api } from "../services/api";
import type { Problem, ProblemDetailData } from "../types";

export default function ProblemsHubPage() {
  const [searchParams, setSearchParams] = useSearchParams();
  const initialCategory = searchParams.get("category") || "All";

  const [problems, setProblems] = useState<Problem[]>([]);
  const [problemDetails, setProblemDetails] = useState<Record<string, ProblemDetailData>>({});
  const [loading, setLoading] = useState(true);
  const [searchQuery, setSearchQuery] = useState("");
  const [selectedCategory, setSelectedCategory] = useState(initialCategory);

  useEffect(() => {
    const c = searchParams.get("category");
    if (c) setSelectedCategory(c);
  }, [searchParams]);

  useEffect(() => {
    api
      .getProblems()
      .then(async (data) => {
        setProblems(data);
        // Fetch details in background for applicable algorithm counts
        const detailsMap: Record<string, ProblemDetailData> = {};
        await Promise.all(
          data.map(async (p) => {
            try {
              const detail = await api.getProblemDetail(p.slug);
              detailsMap[p.slug] = detail;
            } catch {
              // ignore
            }
          })
        );
        setProblemDetails(detailsMap);
      })
      .catch((err) => console.error("Failed to fetch problems:", err))
      .finally(() => setLoading(false));
  }, []);

  const categories = useMemo(() => {
    const set = new Set<string>();
    problems.forEach((p) => {
      if (p.category) set.add(p.category);
    });
    return ["All", ...Array.from(set)];
  }, [problems]);

  const filteredProblems = useMemo(() => {
    return problems.filter((p) => {
      const name = (p.name || p.title || "").toLowerCase();
      const slug = (p.slug || "").toLowerCase();
      const desc = (p.description || "").toLowerCase();
      const cat = (p.category || "").toLowerCase();
      const query = searchQuery.toLowerCase();

      const matchesSearch =
        name.includes(query) ||
        slug.includes(query) ||
        desc.includes(query) ||
        cat.includes(query);

      const matchesCat =
        selectedCategory === "All" ||
        p.category.toLowerCase() === selectedCategory.toLowerCase();

      return matchesSearch && matchesCat;
    });
  }, [problems, searchQuery, selectedCategory]);

  return (
    <Layout>
      <div className="space-y-8 animate-in fade-in duration-200">
        {/* Page Header */}
        <PageHeader
          breadcrumb="Computational Taxonomy"
          title="Canonical Problems Hub"
          description="Explore formal canonical problem specifications in the DAA curriculum. Each canonical problem defines a formal computational challenge and unifies multiple solving paradigms and algorithmic implementations."
          actions={
            <div className="flex items-center gap-2.5">
              <Link to="/curriculum">
                <Button variant="secondary" icon={<GraduationCap className="w-4 h-4" />}>
                  Curriculum Hub
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

        {/* Filter and Search Bar */}
        <div className="p-4 rounded-xl bg-[#0e131f] border border-slate-800 space-y-3">
          <div className="flex flex-col md:flex-row gap-3 items-stretch md:items-center justify-between">
            {/* Search Box */}
            <div className="relative flex-1 max-w-md">
              <Search className="w-4 h-4 text-slate-400 absolute left-3.5 top-1/2 -translate-y-1/2 pointer-events-none" />
              <input
                type="text"
                placeholder="Search canonical problems by name, category, or keyword..."
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
                Showing <strong className="text-white">{filteredProblems.length}</strong> of {problems.length} canonical problems
              </span>
            </div>
          </div>

          {/* Category Chips */}
          <div className="flex items-center gap-1.5 overflow-x-auto pt-1 pb-1 scrollbar-thin border-t border-slate-800/80">
            <span className="text-[11px] font-mono text-slate-400 mr-1 hidden sm:inline">Category:</span>
            {categories.map((cat) => {
              const active = selectedCategory === cat;
              return (
                <button
                  key={cat}
                  onClick={() => {
                    setSelectedCategory(cat);
                    setSearchParams(cat === "All" ? {} : { category: cat });
                  }}
                  className={`px-3 py-1.5 rounded-lg text-xs font-medium whitespace-nowrap transition-colors flex items-center gap-1.5 ${
                    active
                      ? "bg-sky-500/15 text-sky-400 border border-sky-500/30 font-semibold"
                      : "bg-slate-900/60 border border-slate-800 text-slate-400 hover:text-slate-200 hover:border-slate-700"
                  }`}
                >
                  <span>{cat}</span>
                </button>
              );
            })}
          </div>
        </div>

        {/* Problems Grid */}
        {loading ? (
          <div className="py-24">
            <LoadingState message="Loading canonical computational problems..." />
          </div>
        ) : filteredProblems.length === 0 ? (
          <EmptyState
            title="No matching problems found"
            message={`No canonical problems found matching "${searchQuery}". Try resetting filters.`}
            action={
              <Button
                variant="secondary"
                size="sm"
                onClick={() => {
                  setSearchQuery("");
                  setSelectedCategory("All");
                  setSearchParams({});
                }}
              >
                Reset All Filters
              </Button>
            }
          />
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5">
            {filteredProblems.map((problem) => {
              const detail = problemDetails[problem.slug];
              const applicableAlgos = detail?.applicable_algorithms || [];
              const algoCount = applicableAlgos.length;

              return (
                <Card
                  key={problem.slug}
                  className="flex flex-col justify-between hover:border-slate-700 transition-all group"
                >
                  <div className="space-y-3.5">
                    {/* Header */}
                    <div className="flex items-start justify-between gap-2 border-b border-slate-800/80 pb-3">
                      <div>
                        <span className="text-[11px] font-mono font-medium text-sky-400 block mb-0.5">
                          {problem.paradigm}
                        </span>
                        <Link to={`/problems/${problem.slug}`}>
                          <h3 className="font-semibold text-base text-white tracking-tight group-hover:text-sky-300 transition-colors">
                            {problem.name || problem.title}
                          </h3>
                        </Link>
                      </div>
                      <Badge variant="default" mono size="sm">
                        {problem.category}
                      </Badge>
                    </div>

                    {/* Description */}
                    <p className="text-slate-400 text-xs leading-relaxed line-clamp-3">
                      {problem.description}
                    </p>

                    {/* Input/Output Format Preview */}
                    {(problem.input_format || problem.output_format) && (
                      <div className="p-2.5 rounded-lg bg-slate-900/80 border border-slate-800 text-[11px] font-mono space-y-1">
                        {problem.input_format && (
                          <div className="text-slate-300 truncate">
                            <span className="text-slate-400">Input: </span>
                            {problem.input_format}
                          </div>
                        )}
                        {problem.output_format && (
                          <div className="text-slate-300 truncate">
                            <span className="text-slate-400">Output: </span>
                            {problem.output_format}
                          </div>
                        )}
                      </div>
                    )}

                    {/* Compatible Implementations Strip */}
                    <div className="space-y-1.5 pt-1">
                      <div className="flex items-center justify-between text-[11px] font-mono text-slate-400">
                        <span>Compatible Algorithms:</span>
                        <span className="text-sky-400 font-semibold">{algoCount} Implementations</span>
                      </div>
                      <div className="flex flex-wrap gap-1.5">
                        {applicableAlgos.map((algo) => (
                          <Link key={algo.slug} to={`/algorithms/${algo.slug}`}>
                            <span className="px-2 py-0.5 rounded text-[10px] font-mono bg-slate-900 text-slate-300 border border-slate-800 hover:border-sky-700 hover:text-sky-300 transition-colors">
                              {algo.name}
                            </span>
                          </Link>
                        ))}
                      </div>
                    </div>
                  </div>

                  {/* Footer Actions */}
                  <div className="flex items-center justify-between pt-3.5 mt-4 border-t border-slate-800">
                    {algoCount > 1 ? (
                      <Link
                        to={`/benchmark?algos=${applicableAlgos.map((a) => a.slug).join(",")}`}
                        className="text-xs font-mono text-sky-400 hover:text-sky-300 flex items-center gap-1.5 transition-colors"
                      >
                        <BarChart3 className="w-3.5 h-3.5" />
                        <span>Compare All ({algoCount})</span>
                      </Link>
                    ) : (
                      <span className="text-xs font-mono text-slate-400">Canonical Problem</span>
                    )}

                    <Link to={`/problems/${problem.slug}`}>
                      <Button variant="secondary" size="sm" icon={<ChevronRight className="w-3.5 h-3.5" />}>
                        View Problem
                      </Button>
                    </Link>
                  </div>
                </Card>
              );
            })}
          </div>
        )}
      </div>
    </Layout>
  );
}
