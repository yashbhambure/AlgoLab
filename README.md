# AlgoLab: Intelligent Algorithm Benchmark & MCDA Recommendation System

[![CI Quality Gate](https://github.com/daa-lab/algolab/actions/workflows/ci.yml/badge.svg)](https://github.com/daa-lab/algolab)
[![FastAPI](https://img.shields.io/badge/Backend-FastAPI_0.115+-009688?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![React 19](https://img.shields.io/badge/Frontend-React_19_+_Vite-61DAFB?logo=react&logoColor=black)](https://react.dev)
[![Tailwind CSS v4](https://img.shields.io/badge/Styling-Tailwind_CSS_v4-38B2AC?logo=tailwind-css&logoColor=white)](https://tailwindcss.com)
[![License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

An enterprise-grade academic research laboratory, hardware-isolated empirical microbenchmark harness, and Multi-Criteria Decision Analysis (MCDA) recommendation platform for the **Design and Analysis of Algorithms (DAA)**.

---

## 📑 Table of Contents
1. [Core Features & Capabilities](#-core-features--capabilities)
2. [Algorithmic Paradigms & 35 Canonical Implementations](#-algorithmic-paradigms--35-canonical-implementations)
3. [Microbenchmarking & Hardware Isolation Engine](#-microbenchmarking--hardware-isolation-engine)
4. [Multi-Criteria Decision Analysis (MCDA) Mathematics](#-multi-criteria-decision-analysis-mcda-mathematics)
5. [Theoretical Complexity & Master Theorem Engine](#-theoretical-complexity--master-theorem-engine)
6. [Interactive Algorithm Visualizer](#-interactive-algorithm-visualizer)
7. [System Architecture](#-system-architecture)
8. [API Endpoints Overview](#-api-endpoints-overview)
9. [Quick Start & Installation](#-quick-start--installation)
10. [Database Migrations (Alembic)](#-database-migrations-alembic)
11. [Docker Deployment](#-docker-deployment)
12. [Testing & Quality Assurance](#-testing--quality-assurance)

---

## 🌟 Core Features & Capabilities

- **35 Canonical Algorithms**: Complete, verified implementations across 7 algorithmic paradigms with both pure execution and step-by-step instrumented execution.
- **Hardware-Isolated Microbenchmarking**: High-resolution nanosecond execution timing via `time.perf_counter_ns()`, Python Garbage Collector disabling (`gc.disable()`), warmup iterations, and memory tracking via `tracemalloc`.
- **MCDA Recommendation Engine**: Recommends optimal algorithmic candidates based on theoretical bounds, empirical execution profiles, memory limits, input distribution characteristics, and strict user constraints (stability, in-place).
- **Master Theorem Recurrence Solver**: Analytical complexity solver for divide-and-conquer recurrences $T(n) = aT(n/b) + \Theta(n^k \log^p n)$, including standard Cases 1, 2, 3 and the extended logarithmic Case 2 ($p = -1$ and $p < -1$).
- **Non-Linear Big-O Empirical Curve Fitting**: Regression analysis against $O(1)$, $O(\log n)$, $O(n)$, $O(n \log n)$, $O(n^2)$, $O(n^3)$, and $O(2^n)$ with $R^2$, RMSE, and confidence estimation.
- **Interactive Step-by-Step Visualizer**: HUD-style execution visualizer with forward/backward stepping, auto-play animation, customizable playback speeds, and element comparison highlights.
- **Dynamic Decision Tree**: Guided algorithmic selection wizard traversing constraints (sortedness, density, negative edge weights, memory budget) to reach recommended algorithm leaves.

---

## 🧮 Algorithmic Paradigms & 35 Canonical Implementations

AlgoLab includes 35 algorithmic implementations across 7 paradigms:

| Paradigm | Algorithms | Time (Best / Avg / Worst) | Space |
|---|---|---|---|
| **Sorting** | Bubble Sort | $\Omega(n) / \Theta(n^2) / O(n^2)$ | $O(1)$ |
| | Selection Sort | $\Omega(n^2) / \Theta(n^2) / O(n^2)$ | $O(1)$ |
| | Insertion Sort | $\Omega(n) / \Theta(n^2) / O(n^2)$ | $O(1)$ |
| | Merge Sort | $\Omega(n \log n) / \Theta(n \log n) / O(n \log n)$ | $O(n)$ |
| | Quick Sort | $\Omega(n \log n) / \Theta(n \log n) / O(n^2)$ | $O(\log n)$ |
| | Heap Sort | $\Omega(n \log n) / \Theta(n \log n) / O(n \log n)$ | $O(1)$ |
| | Counting Sort | $\Omega(n+k) / \Theta(n+k) / O(n+k)$ | $O(k)$ |
| | Radix Sort | $\Omega(d(n+k)) / \Theta(d(n+k)) / O(d(n+k))$ | $O(n+k)$ |
| **Searching** | Linear Search | $\Omega(1) / \Theta(n) / O(n)$ | $O(1)$ |
| | Binary Search | $\Omega(1) / \Theta(\log n) / O(\log n)$ | $O(1)$ |
| | Jump Search | $\Omega(1) / \Theta(\sqrt{n}) / O(\sqrt{n})$ | $O(1)$ |
| | Interpolation Search | $\Omega(1) / \Theta(\log \log n) / O(n)$ | $O(1)$ |
| **Divide & Conquer** | Strassen's Matrix Mult | $\Theta(n^{\log_2 7}) \approx O(n^{2.807})$ | $O(n^2)$ |
| | Merge Sort (D&C) | $\Theta(n \log n)$ | $O(n)$ |
| | Quick Sort (D&C) | $\Theta(n \log n)$ | $O(\log n)$ |
| **Greedy** | Fractional Knapsack | $\Theta(n \log n)$ | $O(n)$ |
| | Activity Selection | $\Theta(n \log n)$ | $O(n)$ |
| | Huffman Coding | $\Theta(n \log n)$ | $O(n)$ |
| | Job Sequencing with Deadlines | $\Theta(n^2)$ | $O(n)$ |
| | Kruskal's MST (Disjoint Set) | $\Theta(E \log E)$ | $O(V)$ |
| | Prim's MST (Priority Queue) | $\Theta(E \log V)$ | $O(V)$ |
| | Dijkstra's SSSP | $\Theta((V+E) \log V)$ | $O(V)$ |
| **Dynamic Programming** | 0/1 Knapsack | $\Theta(n \cdot W)$ | $O(n \cdot W)$ |
| | Longest Common Subsequence (LCS) | $\Theta(m \cdot n)$ | $O(m \cdot n)$ |
| | Matrix Chain Multiplication | $\Theta(n^3)$ | $O(n^2)$ |
| | Coin Change Problem | $\Theta(n \cdot \text{amount})$ | $O(\text{amount})$ |
| | Rod Cutting Problem | $\Theta(n^2)$ | $O(n)$ |
| | Fibonacci (Tabulation & Space-Opt) | $\Theta(n)$ | $O(1)$ |
| | Floyd-Warshall APSP | $\Theta(V^3)$ | $O(V^2)$ |
| | Bellman-Ford SSSP | $\Theta(V \cdot E)$ | $O(V)$ |
| **Graph Traversal** | Breadth-First Search (BFS) | $\Theta(V + E)$ | $O(V)$ |
| | Depth-First Search (DFS) | $\Theta(V + E)$ | $O(V)$ |
| | Topological Sort (Kahn's / DFS) | $\Theta(V + E)$ | $O(V)$ |
| **Backtracking** | N-Queens Problem | $O(N!)$ | $O(N)$ |
| | Subset Sum Problem | $O(2^n)$ | $O(n)$ |
| | m-Graph Coloring | $O(m^V)$ | $O(V)$ |
| | Hamiltonian Cycle | $O(N!)$ | $O(N)$ |

---

## ⏱️ Microbenchmarking & Hardware Isolation Engine

To produce accurate empirical measurements unskewed by language runtime artifacts, the `BenchmarkRunner` implements:
1. **Garbage Collection Suspension**: Disables automatic GC cycles during measurement passes (`gc.disable()`) and runs manual collections between iterations (`gc.collect()`).
2. **Warmup Passes**: Executes unrecorded warmup passes to ensure JIT/CPU caches and branch predictors are primed.
3. **Immutability Protection**: Generates deep copies (`copy.deepcopy(input_data)`) before every iteration to ensure algorithms modifying arrays in-place (e.g., Quick Sort, Heap Sort) do not receive pre-sorted data on subsequent runs.
4. **Memory Profiling**: Tracks peak auxiliary bytes allocated using Python's `tracemalloc`.
5. **Statistical Dispersion**: Computes mean, median, standard deviation, minimum, maximum, variance, and 95% confidence intervals across user-configured repetitions ($k \le 50$).

---

## 📐 Multi-Criteria Decision Analysis (MCDA) Mathematics

The recommendation engine calculates a normalized composite utility score $U(A) \in [0, 100]$ for each candidate algorithm $A$:

$$U(A) = 100 \times \left( w_{\text{theo}} S_{\text{theo}}(A) + w_{\text{emp}} S_{\text{emp}}(A) + w_{\text{mem}} S_{\text{mem}}(A) + w_{\text{input}} S_{\text{input}}(A) + w_{\text{req}} S_{\text{req}}(A) \right) - \sum P_{\text{violation}}$$

Where:
- $\sum w_i = 1.0$ (Weights dynamically configured or selected via optimization profiles: *Balanced*, *Maximum Speed*, *Minimum Memory*, *Stability & Correctness*).
- $S_{\text{theo}}(A) = \frac{\log(\text{WorstBound}_{\max}) - \log(\text{WorstBound}_A)}{\log(\text{WorstBound}_{\max}) - \log(\text{WorstBound}_{\min}) + \epsilon}$
- $S_{\text{emp}}(A) = 1 - \frac{T_A - T_{\min}}{T_{\max} - T_{\min} + \epsilon}$
- $S_{\text{mem}}(A) = 1 - \frac{M_A - M_{\min}}{M_{\max} - M_{\min} + \epsilon}$
- $S_{\text{input}}(A)$: Fitness bonus based on input distribution (e.g., $O(n)$ Insertion Sort for nearly-sorted arrays, Counting Sort for small integer ranges $k \le 2n$).
- $P_{\text{violation}}$: Strict constraint disqualifications (e.g., stability requirement on unstable sorts, in-place requirements on $O(n)$ space sorts, or negative weight edges on Dijkstra).

---

## ⚡ Theoretical Complexity & Master Theorem Engine

Solves divide-and-conquer recurrences of the form:

$$T(n) = a T\left(\frac{n}{b}\right) + f(n), \quad \text{where } f(n) = \Theta(n^k \log^p n)$$

- **Critical Exponent**: $c_{\text{crit}} = \log_b a$
- **Case 1 ($k < c_{\text{crit}}$)**: Leaf-dominated $\implies T(n) = \Theta(n^{\log_b a})$
- **Case 2 ($k = c_{\text{crit}}$)**:
  - $p > -1 \implies T(n) = \Theta(n^{\log_b a} \log^{p+1} n)$
  - $p = -1 \implies T(n) = \Theta(n^{\log_b a} \log(\log n))$ *(Extended Case 2)*
  - $p < -1 \implies T(n) = \Theta(n^{\log_b a})$ *(Extended Case 2)*
- **Case 3 ($k > c_{\text{crit}}$)**: Root-dominated with regularity condition $a f(n/b) \le c f(n) \implies T(n) = \Theta(n^k \log^p n)$

---

## 🖥️ System Architecture

```
algolab/
├── backend/
│   ├── alembic/                # Database migrations
│   ├── app/
│   │   ├── algorithms/         # 35 Canonical DAA algorithms (Pure & Instrumented)
│   │   ├── api/v1/             # RESTful API endpoints (Auth, Algos, Benchmarks, MCDA, Tree)
│   │   ├── benchmark/          # Isolated timing harness & tracemalloc memory tracker
│   │   ├── complexity/         # Master Theorem & Big-O regression solvers
│   │   ├── core/               # Database, Security (JWT/bcrypt), Exceptions
│   │   ├── models/             # SQLAlchemy 2.0 ORM models
│   │   ├── recommendation/     # MCDA scoring engine, Input analyzer, Decision tree
│   │   ├── schemas/            # Pydantic v2 validation models
│   │   ├── seed/               # DAA seed catalogs (algorithms, problems, datasets)
│   │   ├── config.py           # Pydantic Settings configuration
│   │   └── main.py             # FastAPI application entrypoint & lifespan
│   ├── tests/                  # Pytest test suite (113 comprehensive tests)
│   ├── Dockerfile              # Production backend container definition
│   └── requirements.txt        # Python dependency manifest
│
└── frontend/
    ├── src/
    │   ├── components/         # HUD Cards, Interactive Charts, Visualizers
    │   ├── pages/              # Benchmark, MCDA Recommender, Visualizer, Decision Tree, Master Theorem
    │   ├── services/           # Typed REST API Client
    │   └── types/              # TypeScript 6.0 interface models
    ├── Dockerfile              # Multi-stage production Nginx container definition
    ├── nginx.conf              # Production reverse proxy config
    └── package.json            # Vite, React 19, Tailwind CSS v4 dependencies
```

---

## 📡 API Endpoints Overview

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/health` | System health and environment metadata |
| `GET` | `/api/v1/algorithms/` | Catalog of all 35 algorithms with theoretical complexities |
| `GET` | `/api/v1/algorithms/{slug}` | Detailed algorithm metadata, pseudocode, and properties |
| `POST` | `/api/v1/benchmarks/run` | Execute hardware-isolated microbenchmark |
| `POST` | `/api/v1/benchmarks/step-execute` | Instrumented step-by-step execution for visualizer |
| `POST` | `/api/v1/recommendations/evaluate` | Multi-Criteria Decision Analysis (MCDA) candidate ranking |
| `GET` | `/api/v1/recommendations/decision-tree` | Algorithmic Decision Tree graph structure and traversal |
| `POST` | `/api/v1/complexity/master-theorem` | Solve recurrence $T(n) = aT(n/b) + \Theta(n^k \log^p n)$ |
| `POST` | `/api/v1/complexity/curve-fit` | Fit empirical data points to asymptotic Big-O functions |
| `POST` | `/api/v1/auth/login` | JWT access token issuance |
| `POST` | `/api/v1/auth/register` | User account registration |

Interactive OpenAPI documentation is available at `/docs` (Swagger UI) and `/redoc` (ReDoc).

---

## 🚀 Quick Start & Installation

### Prerequisites
- Python 3.12+ (or 3.13)
- Node.js 18+ & npm
- Git

### 1. Clone & Configure
```bash
git clone https://github.com/daa-lab/algolab.git
cd algolab
cp .env.example .env
```

### 2. Backend Setup
```bash
# Navigate to backend and install requirements
cd backend
pip install -r requirements.txt

# Run database migrations
python -m alembic upgrade head

# Start FastAPI development server (auto-seeds database on startup)
uvicorn app.main:app --reload --port 8000
```
Backend API will be live at `http://localhost:8000`.

### 3. Frontend Setup
```bash
# In a new terminal, navigate to frontend
cd frontend
npm install

# Start Vite development server
npm run dev
```
Frontend UI will be live at `http://localhost:5173`.

---

## 🗄️ Database Migrations (Alembic)

```bash
# Generate a new migration revision
PYTHONPATH=backend python -m alembic -c backend/alembic.ini revision --autogenerate -m "Add new feature tables"

# Apply migrations to database
PYTHONPATH=backend python -m alembic -c backend/alembic.ini upgrade head

# Rollback one migration step
PYTHONPATH=backend python -m alembic -c backend/alembic.ini downgrade -1
```

---

## 🐳 Docker Deployment

Run the complete full-stack environment via Docker Compose:

```bash
# Build and run containers in background
docker compose up -d --build

# Verify container status
docker compose ps

# View live application logs
docker compose logs -f
```

Services exposed:
- **Frontend Web UI**: `http://localhost:3000` (or `http://localhost:80`)
- **Backend API & Swagger**: `http://localhost:8000/docs`
- **PostgreSQL Database** (when enabled): `localhost:5432`

---

## 🧪 Testing & Quality Assurance

Run the test suite across backend algorithms, benchmark runners, MCDA engines, and complexity analyzers:

```bash
# Run 113 comprehensive backend unit & integration tests
PYTHONPATH=backend pytest backend/tests -v

# Run frontend typecheck and production build
npm --prefix frontend run build

# Run frontend linter
npm --prefix frontend run lint
```

---

## 📜 License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.
