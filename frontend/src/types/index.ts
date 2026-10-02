/**
 * Complete DAA Laboratory & Algorithm Benchmark System Type Definitions
 */

export type ParadigmType =
  | "Sorting"
  | "Searching"
  | "Divide & Conquer"
  | "Greedy"
  | "Dynamic Programming"
  | "Graph"
  | "Backtracking"
  | "General";

export interface Algorithm {
  id?: string;
  slug: string;
  name: string;
  category: string;
  paradigm: ParadigmType | string;
  description: string;
  best_case?: string;
  average_case?: string;
  worst_case?: string;
  time_complexity_best?: string;
  time_complexity_average?: string;
  time_complexity_worst?: string;
  space_complexity: string;
  recurrence_relation?: string | null;
  is_stable?: boolean;
  is_in_place?: boolean;
  is_adaptive?: boolean;
  is_deterministic?: boolean;
  advantages?: string[];
  disadvantages?: string[];
  suitable_cases?: string[];
  unsuitable_cases?: string[];
  code_snippet?: string;
  pseudocode?: string;
  c_source_code?: string;
  implementation_python?: string;
  daa_concept_notes?: string;
  tags?: string[];
}

export interface AlgorithmDetailData extends Algorithm {
  id: string;
  created_at?: string;
}

export interface ApplicableAlgorithm {
  id: string;
  slug: string;
  name: string;
  category: string;
  paradigm: string;
  time_complexity_average: string;
  space_complexity: string;
  suitability_score?: number;
  notes?: string;
}

export interface Problem {
  id?: string;
  slug: string;
  name?: string;
  title?: string;
  category: string;
  paradigm: string;
  description: string;
  input_format?: string;
  output_format?: string;
  constraints?: string;
  data_type?: string;
  daa_topics?: string[];
  supported_algorithms?: string[];
  example_input?: any;
  example_output?: any;
  applicable_algorithms?: ApplicableAlgorithm[];
}

export interface ProblemDetailData extends Problem {
  id: string;
  applicable_algorithms: ApplicableAlgorithm[];
}

export interface CurriculumGeneralMethod {
  title: string;
  recurrence_template?: string;
  principles?: string[];
  master_theorem_cases?: string[];
}

export interface CurriculumTopic {
  topic_id: string;
  name: string;
  type: "computational" | "theoretical_foundation" | "theoretical";
  slug: string;
  algorithm_slug?: string;
  algorithm_slugs?: string[];
  problem_slug?: string;
  method_name?: string;
  time_complexity?: string;
  space_complexity?: string;
  recurrence?: string;
  description: string;
  invariance?: string;
  real_world_applications?: string[];
  default_input?: any;
  asymptotic_characterization?: string;
  canonical_examples?: string[];
  key_takeaway?: string;
  formal_definition?: string;
  properties?: string[];
  canonical_reductions?: string[];
  theorem_statement?: string;
  proof_architecture?: string[];
  impact?: string;
}

export interface CurriculumModule {
  module_id: number;
  slug: string;
  name: string;
  short_name: string;
  description: string;
  general_method?: CurriculumGeneralMethod;
  topics: CurriculumTopic[];
}

export interface Dataset {
  id: string;
  name: string;
  problem_type: string;
  data_type: string;
  size: number;
  distribution: string;
  random_seed?: number;
  characteristics: Record<string, any>;
  preview_sample?: any;
  data_payload?: any;
  created_at?: string;
}

export interface ExecutionMetrics {
  comparisons: number;
  swaps: number;
  recursive_calls: number;
  operations: number;
  peak_memory_kb: number;
  allocated_memory_kb: number;
}

export interface ExecutionStep {
  step_id: number;
  action: string; // 'compare' | 'swap' | 'visit' | 'set_dp' | 'backtrack' | 'split' | 'merge' | 'select'
  indices: number[];
  values: any[];
  state_snapshot: any;
  description: string;
  highlight_line?: number;
  metadata?: Record<string, any>;
}

export interface AlgorithmExecutionResult {
  algorithm_slug: string;
  output: any;
  metrics: ExecutionMetrics;
  steps: ExecutionStep[];
  success: boolean;
  error_message?: string;
}

export interface TimeStats {
  mean_ns: number;
  mean_ms: number;
  median_ms: number;
  min_ms: number;
  max_ms: number;
  std_dev_ms: number;
  variance_ms: number;
  p95_ms: number;
  p99_ms: number;
  iqr_ms: number;
}

export interface MemoryStats {
  peak_kb: number;
  allocated_kb: number;
  growth_kb: number;
}

export interface OperationStats {
  comparisons: number;
  swaps: number;
  recursive_calls: number;
  operations: number;
}

export interface BenchmarkAlgorithmResult {
  algorithm_slug: string;
  algorithm_name: string;
  paradigm?: string;
  category?: string;
  input_size?: number;
  iterations?: number;
  iterations_run?: number;
  raw_durations_ms?: number[];
  time_stats: TimeStats;
  execution_time_ms?: number;
  memory_stats: MemoryStats;
  operations?: OperationStats;
  metrics?: {
    comparisons?: number;
    swaps?: number;
    recursive_calls?: number;
    operations?: number;
  };
  repetition_times_ms?: number[];
  success?: boolean;
  error_message?: string;
  theoretical_complexity?: {
    best: string;
    average: string;
    worst: string;
    space: string;
  };
}

export interface BenchmarkResponse {
  dataset_name?: string;
  dataset_size?: number;
  data_type?: string;
  distribution?: string;
  repetitions?: number;
  warmup_runs?: number;
  total_candidates?: number;
  successful_runs?: number;
  results: BenchmarkAlgorithmResult[];
  ranking_by_speed?: string[];
  ranking_by_memory?: string[];
  speedup_ratios?: Record<string, number>;
  fastest_algorithm?: string | null;
  most_memory_efficient?: string | null;
  errors?: Record<string, string>;
  created_at?: string;
}

export interface MasterTheoremRequest {
  a: number;
  b: number;
  k: number;
  p?: number;
}

export interface MasterTheoremResponse {
  a: number;
  b: number;
  k: number;
  p: number;
  critical_exponent: number;
  case_number: number;
  complexity: string;
  latex: string;
  regularity_satisfied?: boolean;
  explanation: string;
  steps: string[];
  recurrence_form?: string;
  case_description?: string;
  condition_check?: string;
  asymptotic_solution?: string;
  step_by_step_proof?: string[];
}

export interface ModelFitResult {
  complexity: string;
  name: string;
  model_name: string;
  coefficient?: number;
  r_squared: number;
  rmse: number;
  aic?: number;
  predicted_curve?: Array<{ n: number; predicted_time_ms: number }>;
}

export interface CurveFitResponse {
  best_fit_complexity: string;
  best_fit_name: string;
  best_fit_model: string;
  best_r_squared: number;
  fits: ModelFitResult[];
  all_models?: ModelFitResult[];
  sample_count: number;
  data_points: Array<{ n: number; time_ms: number }>;
  interpretation: string;
}

export interface MCDARankingItem {
  algorithm_slug: string;
  algorithm_name: string;
  paradigm: string;
  category: string;
  score: number;
  breakdown: {
    theoretical_score: number;
    empirical_score: number;
    space_score: number;
    input_suitability_score: number;
    requirements_score: number;
  };
  complexities: {
    best: string;
    average: string;
    worst: string;
    space: string;
  };
  is_stable: boolean;
  is_in_place: boolean;
  input_reasons: string[];
  requirement_reasons: string[];
  empirical_time_ms?: number;
}

export interface RecommendationResponse {
  objective: string;
  weights_used: Record<string, number>;
  input_properties: Record<string, any>;
  has_empirical_data?: boolean;
  recommended_algorithm: string;
  recommended_name: string;
  winning_score: number;
  explanation: {
    summary: string;
    formal_theoretical_reasoning?: string;
    practical_heuristic_reasoning?: string;
    empirical_benchmark_evidence?: string;
    key_advantages: string[];
    runner_up_comparison?: string;
    disqualified_or_penalized?: Array<{
      algorithm: string;
      reasons: string[];
    }>;
  };
  rankings: MCDARankingItem[];
  trade_offs: Array<{
    algorithm: string;
    time_efficiency: number;
    memory_efficiency: number;
    dataset_fitness: number;
    constraint_compliance: number;
    overall_score: number;
  }>;
}

export interface DecisionTreeNode {
  id: string;
  question: string;
  options: Array<{
    text: string;
    next_node_id?: string;
    recommendation?: {
      algorithm_slug: string;
      name: string;
      reason: string;
    };
  }>;
}

export interface Experiment {
  id: string;
  title: string;
  description?: string;
  status: string;
  benchmark_payload?: any;
  recommendation_payload?: any;
  created_at: string;
}

export interface AlgorithmComplexityProfile {
  slug: string;
  name: string;
  category: string;
  paradigm: string;
  is_curriculum: boolean;
  module_id?: number | null;
  best_case: string;
  average_case: string;
  worst_case: string;
  space_complexity: string;
  recurrence_relation?: string | null;
  is_stable?: boolean;
  is_in_place?: boolean;
  description?: string;
  theoretical_vs_empirical_note?: string;
}

export interface CompatibleComparisonGroup {
  problem_slug: string;
  problem_name: string;
  category: string;
  is_curriculum: boolean;
  constraints?: string;
  algorithms: AlgorithmComplexityProfile[];
}

