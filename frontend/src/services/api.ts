/**
 * DAA Benchmark & Recommendation System API Client
 */
import type {
  Algorithm,
  AlgorithmDetailData,
  Problem,
  ProblemDetailData,
  CurriculumModule,
  Dataset,
  AlgorithmExecutionResult,
  BenchmarkResponse,
  MasterTheoremRequest,
  MasterTheoremResponse,
  CurveFitResponse,
  RecommendationResponse,
  DecisionTreeNode,
  Experiment,
  AlgorithmComplexityProfile,
  CompatibleComparisonGroup,
} from "../types";

const rawApiBase = import.meta.env.VITE_API_BASE_URL;
const API_BASE_URL = rawApiBase
  ? `${rawApiBase.replace(/\/+$/, "")}/api/v1`
  : "/api/v1";

async function request<T>(endpoint: string, options?: RequestInit): Promise<T> {
  const url = `${API_BASE_URL}${endpoint}`;
  const headers = {
    "Content-Type": "application/json",
    ...options?.headers,
  };

  const response = await fetch(url, { ...options, headers });

  if (!response.ok) {
    let errorDetail = "An unexpected error occurred.";
    try {
      const errorJson = await response.json();
      errorDetail = errorJson.detail || errorJson.message || errorDetail;
    } catch {
      errorDetail = `HTTP ${response.status}: ${response.statusText}`;
    }
    throw new Error(errorDetail);
  }

  return response.json();
}

export const api = {
  // System Health
  getHealth: () => request<{ status: string; version: string; environment: string }>("/health"),

  // Curriculum
  getCurriculumModules: () => request<CurriculumModule[]>("/curriculum/modules"),
  getCurriculumModule: (moduleId: string | number) => request<CurriculumModule>(`/curriculum/modules/${moduleId}`),
  getApprovedCurriculumSlugs: () => request<string[]>("/curriculum/approved-algorithms"),
  getTheoreticalModules: () => request<CurriculumModule[]>("/curriculum/theoretical"),

  // Algorithms
  getAlgorithms: (params?: { category?: string; paradigm?: string; search?: string; problem_slug?: string }) => {
    const query = new URLSearchParams();
    if (params?.category) query.append("category", params.category);
    if (params?.paradigm) query.append("paradigm", params.paradigm);
    if (params?.search) query.append("search", params.search);
    if (params?.problem_slug) query.append("problem_slug", params.problem_slug);
    const queryString = query.toString() ? `?${query.toString()}` : "";
    return request<Algorithm[]>(`/algorithms${queryString}`);
  },

  getAlgorithm: (slug: string) => request<AlgorithmDetailData>(`/algorithms/${slug}`),
  getAlgorithmDetail: (slug: string) => request<AlgorithmDetailData>(`/algorithms/${slug}`),

  getAlgorithmCode: (slug: string) =>
    request<{
      slug: string;
      name: string;
      pseudocode?: string;
      c_source_code?: string;
      implementation_python?: string;
      code?: string;
      daa_concept_notes?: string;
    }>(`/algorithms/${slug}/code`),

  // Problems
  getProblems: (category?: string) => {
    const query = category ? `?category=${encodeURIComponent(category)}` : "";
    return request<Problem[]>(`/problems${query}`);
  },

  getProblem: (slug: string) => request<ProblemDetailData>(`/problems/${slug}`),
  getProblemDetail: (slug: string) => request<ProblemDetailData>(`/problems/${slug}`),

  // Datasets
  getDatasets: (problemType?: string) => {
    const query = problemType ? `?problem_type=${encodeURIComponent(problemType)}` : "";
    return request<Dataset[]>(`/datasets${query}`);
  },

  generateDataset: (payload: {
    problem_type?: string;
    data_type?: string;
    size?: number;
    distribution?: string;
    min_val?: number;
    max_val?: number;
    random_seed?: number;
    target_value?: any;
    num_vertices?: number;
    num_edges?: number;
    is_directed?: boolean;
    is_weighted?: boolean;
    graph_density?: string;
    allow_negative_weights?: boolean;
    knapsack_capacity?: number;
  }) => request<Dataset>("/datasets/generate", {
    method: "POST",
    body: JSON.stringify(payload),
  }),

  createCustomDataset: (payload: {
    name: string;
    problem_type: string;
    data_type: string;
    raw_data: any;
  }) => request<Dataset>("/datasets/custom", {
    method: "POST",
    body: JSON.stringify(payload),
  }),

  // Benchmarks
  runSingleBenchmark: (payload: {
    algorithm_slug: string;
    input_data: any;
    repetitions?: number;
    warmup_runs?: number;
  }) => request<any>("/benchmarks/run", {
    method: "POST",
    body: JSON.stringify(payload),
  }),

  runComparisonBenchmark: (payload: {
    algorithm_slugs: string[];
    dataset_name?: string;
    input_data?: any;
    repetitions?: number;
    warmup_runs?: number;
    data_type?: string;
    distribution?: string;
    size?: number;
  }) => request<BenchmarkResponse>("/benchmarks/compare", {
    method: "POST",
    body: JSON.stringify(payload),
  }),

  runStepExecution: (payload: {
    algorithm_slug: string;
    input_data: any;
    max_steps?: number;
  }) => request<AlgorithmExecutionResult>("/benchmarks/step", {
    method: "POST",
    body: JSON.stringify(payload),
  }),

  // Complexity Analysis
  solveMasterTheorem: (payload: MasterTheoremRequest) =>
    request<MasterTheoremResponse>("/complexity/master-theorem", {
      method: "POST",
      body: JSON.stringify(payload),
    }),

  fitBigOCurve: (payload: {
    input_sizes?: number[];
    measured_times_ms?: number[];
    data_points?: Array<{ n: number; time_ms: number }>;
  }) => request<CurveFitResponse>("/complexity/fit-big-o", {
    method: "POST",
    body: JSON.stringify(payload),
  }),

  getComplexityHierarchy: () => request<any>("/complexity/hierarchy"),

  getCompatibleGroups: (curriculumOnly: boolean = false) =>
    request<CompatibleComparisonGroup[]>(`/complexity/compatible-groups?curriculum_only=${curriculumOnly}`),

  getAlgorithmComplexityProfile: (slug: string) =>
    request<AlgorithmComplexityProfile>(`/complexity/algorithms/${slug}`),

  compareComplexities: (payload: { complexity_a: string; complexity_b: string }) =>
    request<{
      complexity_a: string;
      complexity_b: string;
      asymptotic_symbol: string;
      relation: string;
      description_a: string;
      description_b: string;
    }>("/complexity/compare", {
      method: "POST",
      body: JSON.stringify(payload),
    }),

  // Recommendation & MCDA
  evaluateRecommendations: (payload: {
    candidate_slugs: string[];
    input_data?: any;
    empirical_results?: any[];
    objective?: string;
    require_stable?: boolean;
    require_in_place?: boolean;
    custom_weights?: Record<string, number>;
  }) => request<RecommendationResponse>("/recommendations/evaluate", {
    method: "POST",
    body: JSON.stringify(payload),
  }),

  getDecisionTreeRoot: () => request<DecisionTreeNode>("/recommendations/decision-tree"),

  traverseDecisionTree: (answers: Record<string, string>) =>
    request<{
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
    }>("/recommendations/decision-tree/traverse", {
      method: "POST",
      body: JSON.stringify({ answers }),
    }),

  // Experiments
  getExperiments: () => request<Experiment[]>("/experiments"),

  getExperiment: (id: string) => request<Experiment>(`/experiments/${id}`),

  createExperiment: (payload: {
    title: string;
    description?: string;
    benchmark_payload?: any;
    recommendation_payload?: any;
  }) => request<Experiment>("/experiments", {
    method: "POST",
    body: JSON.stringify(payload),
  }),

  exportExperiment: (id: string, format: "json" | "markdown" = "json") =>
    request<{ format: string; content: any }>(`/experiments/${id}/export?format=${format}`),
};
