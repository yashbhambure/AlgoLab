"""
Authoritative C11 Source Code Repository for all 23 Executable Curriculum Algorithms.
Each implementation is algorithmically authentic, complete, educational, and C11-compliant.
"""
from typing import Dict, Optional

# Module 1: Divide and Conquer
DEFECTIVE_CHESSBOARD_C = r"""/**
 * Problem: Defective Chessboard (Tromino Tiling)
 * Paradigm: Divide and Conquer
 * Standard: C11
 *
 * Description: Tiles a 2^k x 2^k chessboard containing exactly one defective
 * (missing) cell using L-shaped trominoes (3-cell tiles).
 * Recurrence: T(n) = 4T(n/2) + O(1) => O(4^k) = O(n^2)
 */
#include <stdio.h>
#include <stdlib.h>

#define MAX_N 64

static int tile_id = 1;
static int board[MAX_N][MAX_N];

/**
 * Recursively tile a quadrant of size n x n.
 * (tr, tc): top-left row and column of the current subgrid.
 * (dr, dc): coordinates of the defective/missing cell in this subgrid.
 */
void tile_board(int tr, int tc, int dr, int dc, int size) {
    if (size == 1) return;

    int t = tile_id++;
    int half = size / 2;

    // Top-Left Quadrant
    if (dr < tr + half && dc < tc + half) {
        tile_board(tr, tc, dr, dc, half);
    } else {
        board[tr + half - 1][tc + half - 1] = t;
        tile_board(tr, tc, tr + half - 1, tc + half - 1, half);
    }

    // Top-Right Quadrant
    if (dr < tr + half && dc >= tc + half) {
        tile_board(tr, tc + half, dr, dc, half);
    } else {
        board[tr + half - 1][tc + half] = t;
        tile_board(tr, tc + half, tr + half - 1, tc + half, half);
    }

    // Bottom-Left Quadrant
    if (dr >= tr + half && dc < tc + half) {
        tile_board(tr + half, tc, dr, dc, half);
    } else {
        board[tr + half][tc + half - 1] = t;
        tile_board(tr + half, tc, tr + half, tc + half - 1, half);
    }

    // Bottom-Right Quadrant
    if (dr >= tr + half && dc >= tc + half) {
        tile_board(tr + half, tc + half, dr, dc, half);
    } else {
        board[tr + half][tc + half] = t;
        tile_board(tr + half, tc + half, tr + half, tc + half, half);
    }
}

int main(void) {
    int k = 3;             // 2^3 = 8x8 board
    int n = 1 << k;        // n = 8
    int dr = 2, dc = 3;    // Defective cell at (row 2, col 3)

    // Mark defective cell as -1
    board[dr][dc] = -1;

    tile_board(0, 0, dr, dc, n);

    printf("Defective Chessboard Tiling (N = %d, Defect at [%d, %d]):\n", n, dr, dc);
    for (int i = 0; i < n; i++) {
        for (int j = 0; j < n; j++) {
            if (board[i][j] == -1) {
                printf("  XX");
            } else {
                printf("%4d", board[i][j]);
            }
        }
        printf("\n");
    }
    return 0;
}
"""

MAX_MIN_DC_C = r"""/**
 * Problem: Finding Maximum and Minimum
 * Paradigm: Divide and Conquer
 * Standard: C11
 *
 * Description: Simultaneously finds the maximum and minimum elements of an array
 * using tournament divide-and-conquer with at most 3n/2 - 2 comparisons.
 * Recurrence: T(n) = 2T(n/2) + 2 comparisons => O(n)
 */
#include <stdio.h>

typedef struct {
    int min;
    int max;
} MinMax;

/**
 * Tournament divide-and-conquer search for min and max.
 */
MinMax find_min_max(const int arr[], int low, int high) {
    MinMax result;

    // Base Case 1: Single element
    if (low == high) {
        result.min = arr[low];
        result.max = arr[low];
        return result;
    }

    // Base Case 2: Two elements (1 comparison)
    if (high == low + 1) {
        if (arr[low] < arr[high]) {
            result.min = arr[low];
            result.max = arr[high];
        } else {
            result.min = arr[high];
            result.max = arr[low];
        }
        return result;
    }

    // Divide: Split array into halves
    int mid = low + (high - low) / 2;
    MinMax left = find_min_max(arr, low, mid);
    MinMax right = find_min_max(arr, mid + 1, high);

    // Combine: 2 comparisons
    result.min = (left.min < right.min) ? left.min : right.min;
    result.max = (left.max > right.max) ? left.max : right.max;

    return result;
}

int main(void) {
    int data[] = {22, 13, -5, 88, 90, 3, 45, 12, 77, -10};
    int n = (int)(sizeof(data) / sizeof(data[0]));

    MinMax res = find_min_max(data, 0, n - 1);

    printf("Input Array: ");
    for (int i = 0; i < n; i++) printf("%d ", data[i]);
    printf("\n");
    printf("Minimum element: %d\n", res.min);
    printf("Maximum element: %d\n", res.max);

    return 0;
}
"""

STRASSEN_MATRIX_C = r"""/**
 * Problem: Strassen's Matrix Multiplication
 * Paradigm: Divide and Conquer
 * Standard: C11
 *
 * Description: Multiplies two n x n matrices in O(n^log2(7)) ~= O(n^2.8074)
 * time using 7 recursive block multiplications instead of 8 standard multiplications.
 * Recurrence: T(n) = 7T(n/2) + O(n^2)
 */
#include <stdio.h>
#include <stdlib.h>

#define MAX_DIM 16

void matrix_add(int n, int A[MAX_DIM][MAX_DIM], int B[MAX_DIM][MAX_DIM], int C[MAX_DIM][MAX_DIM]) {
    for (int i = 0; i < n; i++) {
        for (int j = 0; j < n; j++) {
            C[i][j] = A[i][j] + B[i][j];
        }
    }
}

void matrix_sub(int n, int A[MAX_DIM][MAX_DIM], int B[MAX_DIM][MAX_DIM], int C[MAX_DIM][MAX_DIM]) {
    for (int i = 0; i < n; i++) {
        for (int j = 0; j < n; j++) {
            C[i][j] = A[i][j] - B[i][j];
        }
    }
}

void strassen_multiply(int n, int A[MAX_DIM][MAX_DIM], int B[MAX_DIM][MAX_DIM], int C[MAX_DIM][MAX_DIM]) {
    if (n <= 2) {
        // Base case: Standard 2x2 multiplication
        for (int i = 0; i < n; i++) {
            for (int j = 0; j < n; j++) {
                C[i][j] = 0;
                for (int k = 0; k < n; k++) {
                    C[i][j] += A[i][k] * B[k][j];
                }
            }
        }
        return;
    }

    int half = n / 2;
    int A11[MAX_DIM][MAX_DIM], A12[MAX_DIM][MAX_DIM], A21[MAX_DIM][MAX_DIM], A22[MAX_DIM][MAX_DIM];
    int B11[MAX_DIM][MAX_DIM], B12[MAX_DIM][MAX_DIM], B21[MAX_DIM][MAX_DIM], B22[MAX_DIM][MAX_DIM];
    int C11[MAX_DIM][MAX_DIM], C12[MAX_DIM][MAX_DIM], C21[MAX_DIM][MAX_DIM], C22[MAX_DIM][MAX_DIM];

    // Partition A and B into 4 submatrices
    for (int i = 0; i < half; i++) {
        for (int j = 0; j < half; j++) {
            A11[i][j] = A[i][j];
            A12[i][j] = A[i][j + half];
            A21[i][j] = A[i + half][j];
            A22[i][j] = A[i + half][j + half];

            B11[i][j] = B[i][j];
            B12[i][j] = B[i][j + half];
            B21[i][j] = B[i + half][j];
            B22[i][j] = B[i + half][j + half];
        }
    }

    int M1[MAX_DIM][MAX_DIM], M2[MAX_DIM][MAX_DIM], M3[MAX_DIM][MAX_DIM], M4[MAX_DIM][MAX_DIM];
    int M5[MAX_DIM][MAX_DIM], M6[MAX_DIM][MAX_DIM], M7[MAX_DIM][MAX_DIM];
    int T1[MAX_DIM][MAX_DIM], T2[MAX_DIM][MAX_DIM];

    // M1 = (A11 + A22) * (B11 + B22)
    matrix_add(half, A11, A22, T1);
    matrix_add(half, B11, B22, T2);
    strassen_multiply(half, T1, T2, M1);

    // M2 = (A21 + A22) * B11
    matrix_add(half, A21, A22, T1);
    strassen_multiply(half, T1, B11, M2);

    // M3 = A11 * (B12 - B22)
    matrix_sub(half, B12, B22, T2);
    strassen_multiply(half, A11, T2, M3);

    // M4 = A22 * (B21 - B11)
    matrix_sub(half, B21, B11, T2);
    strassen_multiply(half, A22, T2, M4);

    // M5 = (A11 + A12) * B22
    matrix_add(half, A11, A12, T1);
    strassen_multiply(half, T1, B22, M5);

    // M6 = (A21 - A11) * (B11 + B12)
    matrix_sub(half, A21, A11, T1);
    matrix_add(half, B11, B12, T2);
    strassen_multiply(half, T1, T2, M6);

    // M7 = (A12 - A22) * (B21 + B22)
    matrix_sub(half, A12, A22, T1);
    matrix_add(half, B21, B22, T2);
    strassen_multiply(half, T1, T2, M7);

    // C11 = M1 + M4 - M5 + M7
    matrix_add(half, M1, M4, T1);
    matrix_sub(half, T1, M5, T2);
    matrix_add(half, T2, M7, C11);

    // C12 = M3 + M5
    matrix_add(half, M3, M5, C12);

    // C21 = M2 + M4
    matrix_add(half, M2, M4, C21);

    // C22 = M1 - M2 + M3 + M6
    matrix_sub(half, M1, M2, T1);
    matrix_add(half, T1, M3, T2);
    matrix_add(half, T2, M6, C22);

    // Combine 4 submatrices into result C
    for (int i = 0; i < half; i++) {
        for (int j = 0; j < half; j++) {
            C[i][j] = C11[i][j];
            C[i][j + half] = C12[i][j];
            C[i + half][j] = C21[i][j];
            C[i + half][j + half] = C22[i][j];
        }
    }
}

int main(void) {
    int n = 4;
    int A[MAX_DIM][MAX_DIM] = {
        {1, 2, 3, 4},
        {5, 6, 7, 8},
        {9, 1, 2, 3},
        {4, 5, 6, 7}
    };
    int B[MAX_DIM][MAX_DIM] = {
        {1, 0, 0, 0},
        {0, 1, 0, 0},
        {0, 0, 1, 0},
        {0, 0, 0, 1}
    };
    int C[MAX_DIM][MAX_DIM] = {0};

    strassen_multiply(n, A, B, C);

    printf("Strassen's Matrix Multiplication Result (%dx%d):\n", n, n);
    for (int i = 0; i < n; i++) {
        for (int j = 0; j < n; j++) {
            printf("%4d", C[i][j]);
        }
        printf("\n");
    }

    return 0;
}
"""

# Module 2: Backtracking
N_QUEENS_C = r"""/**
 * Problem: N-Queens Problem
 * Paradigm: Backtracking
 * Standard: C11
 *
 * Description: Places N non-attacking queens on an N x N chessboard using
 * recursive state-space tree exploration with row-by-row pruning.
 * Time Complexity: O(N!)
 * Space Complexity: O(N)
 */
#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>

#define MAX_N 20

static int solution_count = 0;

/**
 * Check if placing queen at (row, col) conflicts with previous queens.
 */
bool is_safe(const int board[], int row, int col) {
    for (int prev_row = 0; prev_row < row; prev_row++) {
        int prev_col = board[prev_row];
        // Check column conflict
        if (prev_col == col) return false;
        // Check major and minor diagonal conflict: |r1 - r2| == |c1 - c2|
        if (abs(prev_row - row) == abs(prev_col - col)) return false;
    }
    return true;
}

/**
 * Backtracking procedure: explores row by row.
 */
void solve_n_queens(int board[], int row, int n) {
    if (row == n) {
        solution_count++;
        if (solution_count == 1) {
            printf("First Solution for N = %d:\n", n);
            for (int r = 0; r < n; r++) {
                for (int c = 0; c < n; c++) {
                    printf("%s ", (board[r] == c) ? "Q" : ".");
                }
                printf("\n");
            }
        }
        return;
    }

    for (int col = 0; col < n; col++) {
        if (is_safe(board, row, col)) {
            board[row] = col;       // Place queen
            solve_n_queens(board, row + 1, n); // Recurse
            board[row] = -1;        // Backtrack
        }
    }
}

int main(void) {
    int n = 8;
    int board[MAX_N];
    for (int i = 0; i < MAX_N; i++) board[i] = -1;

    solve_n_queens(board, 0, n);
    printf("Total valid placements found for N = %d: %d\n", n, solution_count);

    return 0;
}
"""

SUBSET_SUM_C = r"""/**
 * Problem: Sum of Subsets
 * Paradigm: Backtracking
 * Standard: C11
 *
 * Description: Finds all subsets of a given set of non-negative integers that
 * sum exactly to target weight W using state-space tree bounding.
 * Time Complexity: O(2^n) worst-case, pruned by bounds
 * Space Complexity: O(n) call stack
 */
#include <stdio.h>
#include <stdbool.h>

#define MAX_ITEMS 50

static int subset_count = 0;

/**
 * Backtracking subset sum search with pruning.
 * weights: sorted array of item weights
 * chosen: boolean vector indicating inclusion of element i
 */
void sum_of_subsets(const int weights[], bool chosen[], int current_sum, int remaining_sum, int index, int target, int n) {
    // Solution found
    if (current_sum == target) {
        subset_count++;
        printf("Subset #%d: { ", subset_count);
        for (int i = 0; i < index; i++) {
            if (chosen[i]) printf("%d ", weights[i]);
        }
        printf("}\n");
        return;
    }

    if (index >= n) return;

    // Pruning Condition 1: Can we include weights[index]?
    if (current_sum + weights[index] <= target) {
        chosen[index] = true;
        sum_of_subsets(weights, chosen, current_sum + weights[index], remaining_sum - weights[index], index + 1, target, n);
        chosen[index] = false; // Backtrack
    }

    // Pruning Condition 2: Can we skip weights[index] and still reach target?
    if (current_sum + (remaining_sum - weights[index]) >= target) {
        sum_of_subsets(weights, chosen, current_sum, remaining_sum - weights[index], index + 1, target, n);
    }
}

int main(void) {
    int weights[] = {5, 10, 12, 13, 15, 18};
    int target = 30;
    int n = (int)(sizeof(weights) / sizeof(weights[0]));

    int total_sum = 0;
    for (int i = 0; i < n; i++) total_sum += weights[i];

    bool chosen[MAX_ITEMS] = {false};

    printf("Sum of Subsets (Target = %d):\n", target);
    sum_of_subsets(weights, chosen, 0, total_sum, 0, target, n);
    printf("Total valid subsets found: %d\n", subset_count);

    return 0;
}
"""

HAMILTONIAN_CYCLE_C = r"""/**
 * Problem: Hamiltonian Cycles
 * Paradigm: Backtracking
 * Standard: C11
 *
 * Description: Finds all simple cycles in an undirected graph that visit
 * every vertex exactly once and return to the starting vertex.
 * Time Complexity: O(N!)
 * Space Complexity: O(N)
 */
#include <stdio.h>
#include <stdbool.h>

#define MAX_V 16

static int cycle_count = 0;

/**
 * Check if vertex v can be added to path at position pos.
 */
bool is_valid_vertex(int v, int graph[MAX_V][MAX_V], const int path[], int pos) {
    // Must be adjacent to previous vertex in path
    if (graph[path[pos - 1]][v] == 0) return false;

    // Must not have already been visited
    for (int i = 0; i < pos; i++) {
        if (path[i] == v) return false;
    }
    return true;
}

/**
 * Backtracking recursive cycle generator.
 */
void hamiltonian_cycle_util(int graph[MAX_V][MAX_V], int path[], int pos, int v_count) {
    // If all vertices are in path
    if (pos == v_count) {
        // Check if edge exists from last vertex back to starting vertex path[0]
        if (graph[path[pos - 1]][path[0]] == 1) {
            cycle_count++;
            printf("Hamiltonian Cycle #%d: ", cycle_count);
            for (int i = 0; i < v_count; i++) printf("%d -> ", path[i]);
            printf("%d\n", path[0]);
        }
        return;
    }

    for (int v = 1; v < v_count; v++) {
        if (is_valid_vertex(v, graph, path, pos)) {
            path[pos] = v;
            hamiltonian_cycle_util(graph, path, pos + 1, v_count);
            path[pos] = -1; // Backtrack
        }
    }
}

int main(void) {
    int v_count = 5;
    int graph[MAX_V][MAX_V] = {
        {0, 1, 0, 1, 0},
        {1, 0, 1, 1, 1},
        {0, 1, 0, 0, 1},
        {1, 1, 0, 0, 1},
        {0, 1, 1, 1, 0}
    };

    int path[MAX_V];
    for (int i = 0; i < MAX_V; i++) path[i] = -1;
    path[0] = 0; // Fix starting vertex to avoid circular rotational duplicates

    printf("Searching Hamiltonian Cycles for V = %d...\n", v_count);
    hamiltonian_cycle_util(graph, path, 1, v_count);
    printf("Total Hamiltonian cycles found: %d\n", cycle_count);

    return 0;
}
"""

# Module 3: Dynamic Programming
MULTISTAGE_GRAPH_C = r"""/**
 * Problem: Multistage Graphs
 * Paradigm: Dynamic Programming
 * Standard: C11
 *
 * Description: Finds the minimum cost path from source vertex to sink vertex
 * in a k-stage directed acyclic graph.
 * Recurrence: cost(i) = min { c(i, j) + cost(j) } for all valid forward edges (i, j)
 * Time Complexity: O(V^2) or O(V + E)
 * Space Complexity: O(V)
 */
#include <stdio.h>
#include <limits.h>

#define MAX_V 32
#define INF 999999

int main(void) {
    int n = 8; // Vertices: 0 to 7 (0: Source, 7: Sink)

    // Directed edge costs (INF if no edge)
    int cost_matrix[MAX_V][MAX_V];
    for (int i = 0; i < n; i++) {
        for (int j = 0; j < n; j++) {
            cost_matrix[i][j] = (i == j) ? 0 : INF;
        }
    }

    // Stage 1 -> Stage 2
    cost_matrix[0][1] = 1; cost_matrix[0][2] = 2; cost_matrix[0][3] = 5;
    // Stage 2 -> Stage 3
    cost_matrix[1][4] = 4; cost_matrix[1][5] = 11;
    cost_matrix[2][4] = 9; cost_matrix[2][5] = 5; cost_matrix[2][6] = 16;
    cost_matrix[3][6] = 2;
    // Stage 3 -> Stage 4 (Sink)
    cost_matrix[4][7] = 18; cost_matrix[5][7] = 13; cost_matrix[6][7] = 2;

    int cost[MAX_V];
    int next_node[MAX_V];

    // Base case: Sink has cost 0
    cost[n - 1] = 0;
    next_node[n - 1] = n - 1;

    // Backward induction from n-2 down to 0
    for (int i = n - 2; i >= 0; i--) {
        cost[i] = INF;
        for (int j = i + 1; j < n; j++) {
            if (cost_matrix[i][j] != INF) {
                int total = cost_matrix[i][j] + cost[j];
                if (total < cost[i]) {
                    cost[i] = total;
                    next_node[i] = j;
                }
            }
        }
    }

    printf("Multistage Graph Minimum Cost (Source 0 to Sink %d): %d\n", n - 1, cost[0]);
    printf("Optimal Path: 0");
    int curr = 0;
    while (curr != n - 1) {
        curr = next_node[curr];
        printf(" -> %d", curr);
    }
    printf("\n");

    return 0;
}
"""

FLOYD_WARSHALL_C = r"""/**
 * Problem: All-Pairs Shortest Path (Floyd-Warshall)
 * Paradigm: Dynamic Programming
 * Standard: C11
 *
 * Description: Computes shortest paths between all pairs of vertices in an edge-weighted
 * directed graph with possible negative edges (no negative cycles).
 * Recurrence: D^(k)[i][j] = min(D^(k-1)[i][j], D^(k-1)[i][k] + D^(k-1)[k][j])
 * Time Complexity: O(V^3)
 * Space Complexity: O(V^2)
 */
#include <stdio.h>

#define MAX_V 16
#define INF 999999

void floyd_warshall(int dist[MAX_V][MAX_V], int next_hop[MAX_V][MAX_V], int v) {
    for (int k = 0; k < v; k++) {
        for (int i = 0; i < v; i++) {
            for (int j = 0; j < v; j++) {
                if (dist[i][k] != INF && dist[k][j] != INF) {
                    if (dist[i][k] + dist[k][j] < dist[i][j]) {
                        dist[i][j] = dist[i][k] + dist[k][j];
                        next_hop[i][j] = next_hop[i][k];
                    }
                }
            }
        }
    }
}

int main(void) {
    int v = 4;
    int dist[MAX_V][MAX_V] = {
        {0,   3,   INF, 5},
        {2,   0,   INF, 4},
        {INF, 1,   0,   INF},
        {INF, INF, 2,   0}
    };

    int next_hop[MAX_V][MAX_V];
    for (int i = 0; i < v; i++) {
        for (int j = 0; j < v; j++) {
            next_hop[i][j] = (dist[i][j] != INF && i != j) ? j : -1;
        }
    }

    floyd_warshall(dist, next_hop, v);

    printf("Floyd-Warshall All-Pairs Distance Matrix (%dx%d):\n", v, v);
    for (int i = 0; i < v; i++) {
        for (int j = 0; j < v; j++) {
            if (dist[i][j] == INF) printf(" INF");
            else printf("%4d", dist[i][j]);
        }
        printf("\n");
    }

    return 0;
}
"""

OPTIMAL_BST_C = r"""/**
 * Problem: Optimal Binary Search Trees (OBST)
 * Paradigm: Dynamic Programming
 * Standard: C11
 *
 * Description: Constructs a binary search tree of minimum expected search cost
 * given key access probabilities and dummy unsuccessful search frequencies.
 * Recurrence: e[i][j] = min_{i<=r<=j} { e[i][r-1] + e[r+1][j] + w(i, j) }
 * Time Complexity: O(n^3)
 * Space Complexity: O(n^2)
 */
#include <stdio.h>
#include <float.h>

#define MAX_KEYS 20

void compute_obst(int n, const double p[], const double q[], double e[MAX_KEYS][MAX_KEYS], int root[MAX_KEYS][MAX_KEYS]) {
    double w[MAX_KEYS][MAX_KEYS];

    // Base case: empty subtrees
    for (int i = 1; i <= n + 1; i++) {
        e[i][i - 1] = q[i - 1];
        w[i][i - 1] = q[i - 1];
    }

    // l is length of subtree
    for (int l = 1; l <= n; l++) {
        for (int i = 1; i <= n - l + 1; i++) {
            int j = i + l - 1;
            e[i][j] = DBL_MAX;
            w[i][j] = w[i][j - 1] + p[j] + q[j];

            for (int r = i; r <= j; r++) {
                double t = e[i][r - 1] + e[r + 1][j] + w[i][j];
                if (t < e[i][j]) {
                    e[i][j] = t;
                    root[i][j] = r;
                }
            }
        }
    }
}

int main(void) {
    int n = 4;
    // Keys k1 < k2 < k3 < k4 (1-indexed for algorithm fidelity)
    double p[] = {0.0, 0.15, 0.10, 0.05, 0.10}; // Successful key probabilities
    double q[] = {0.05, 0.10, 0.05, 0.05, 0.10}; // Dummy failure probabilities

    double e[MAX_KEYS][MAX_KEYS] = {{0}};
    int root[MAX_KEYS][MAX_KEYS] = {{0}};

    compute_obst(n, p, q, e, root);

    printf("Optimal BST Minimum Expected Search Cost: %.4f\n", e[1][n]);
    printf("Optimal Root for keys 1..%d: Key %d\n", n, root[1][n]);

    return 0;
}
"""

KNAPSACK_01_DP_C = r"""/**
 * Problem: 0/1 Knapsack Problem
 * Paradigm: Dynamic Programming
 * Standard: C11
 *
 * Description: Given items with discrete weights and profits, maximizes total
 * profit packed into a knapsack of capacity W without item splitting.
 * Recurrence: V[i][w] = max(V[i-1][w], profit[i] + V[i-1][w - weight[i]])
 * Time Complexity: O(n * W)
 * Space Complexity: O(n * W)
 */
#include <stdio.h>

#define MAX_N 64
#define MAX_W 256

static inline int max(int a, int b) { return (a > b) ? a : b; }

int knapsack_01(int n, int capacity, const int weights[], const int profits[], int dp[MAX_N][MAX_W], int selected[]) {
    // Fill DP table
    for (int i = 0; i <= n; i++) {
        for (int w = 0; w <= capacity; w++) {
            if (i == 0 || w == 0) {
                dp[i][w] = 0;
            } else if (weights[i - 1] <= w) {
                dp[i][w] = max(dp[i - 1][w], profits[i - 1] + dp[i - 1][w - weights[i - 1]]);
            } else {
                dp[i][w] = dp[i - 1][w];
            }
        }
    }

    // Backtrack to identify selected items
    int w = capacity;
    int sel_count = 0;
    for (int i = n; i > 0 && w > 0; i--) {
        if (dp[i][w] != dp[i - 1][w]) {
            selected[sel_count++] = i - 1; // Item index
            w -= weights[i - 1];
        }
    }
    return sel_count;
}

int main(void) {
    int weights[] = {2, 3, 4, 5};
    int profits[] = {3, 4, 5, 6};
    int capacity = 5;
    int n = 4;

    int dp[MAX_N][MAX_W];
    int selected[MAX_N];

    int count = knapsack_01(n, capacity, weights, profits, dp, selected);

    printf("0/1 Knapsack (DP) Maximum Profit: %d\n", dp[n][capacity]);
    printf("Selected Items: ");
    for (int i = 0; i < count; i++) {
        printf("Item #%d (w=%d, p=%d) ", selected[i], weights[selected[i]], profits[selected[i]]);
    }
    printf("\n");

    return 0;
}
"""

TSP_HELD_KARP_DP_C = r"""/**
 * Problem: Traveling Salesman Problem (TSP)
 * Paradigm: Dynamic Programming (Held-Karp)
 * Standard: C11
 *
 * Description: Solves the exact TSP tour using subproblem memoization over
 * vertex subsets represented as bitmasks.
 * Recurrence: C(S, j) = min_{k in S \ {j}} { C(S \ {j}, k) + dist[k][j] }
 * Time Complexity: O(n^2 * 2^n)
 * Space Complexity: O(n * 2^n)
 */
#include <stdio.h>
#include <limits.h>

#define MAX_CITIES 12
#define INF 999999

static inline int min(int a, int b) { return (a < b) ? a : b; }

int tsp_held_karp(int n, int dist[MAX_CITIES][MAX_CITIES]) {
    int num_subsets = 1 << n;
    static int dp[1 << MAX_CITIES][MAX_CITIES];

    // Initialize DP table with INF
    for (int mask = 0; mask < num_subsets; mask++) {
        for (int i = 0; i < n; i++) {
            dp[mask][i] = INF;
        }
    }

    // Base Case: start at city 0
    dp[1][0] = 0;

    // Iterate over all subsets of cities
    for (int mask = 1; mask < num_subsets; mask++) {
        for (int u = 0; u < n; u++) {
            if (!(mask & (1 << u)) || dp[mask][u] == INF) continue;

            for (int v = 0; v < n; v++) {
                if (!(mask & (1 << v))) {
                    int next_mask = mask | (1 << v);
                    dp[next_mask][v] = min(dp[next_mask][v], dp[mask][u] + dist[u][v]);
                }
            }
        }
    }

    // Complete the tour: return to city 0
    int min_tour_cost = INF;
    int all_visited = (1 << n) - 1;
    for (int i = 1; i < n; i++) {
        if (dp[all_visited][i] != INF) {
            min_tour_cost = min(min_tour_cost, dp[all_visited][i] + dist[i][0]);
        }
    }

    return min_tour_cost;
}

int main(void) {
    int n = 4;
    int dist[MAX_CITIES][MAX_CITIES] = {
        {0, 10, 15, 20},
        {10, 0, 35, 25},
        {15, 35, 0, 30},
        {20, 25, 30, 0}
    };

    int cost = tsp_held_karp(n, dist);
    printf("Held-Karp Exact TSP Minimum Tour Cost (N = %d): %d\n", n, cost);

    return 0;
}
"""

RELIABILITY_DESIGN_DP_C = r"""/**
 * Problem: Reliability Design
 * Paradigm: Dynamic Programming
 * Standard: C11
 *
 * Description: Maximizes total system reliability product Prod_{i=1}^n (1 - (1 - r_i)^{m_i})
 * under a total cost constraint sum_{i=1}^n c_i * m_i <= TotalCost.
 * Recurrence: f_i(x) = max_{1 <= m_i <= u_i} { phi_i(m_i) * f_{i-1}(x - c_i * m_i) }
 * Time Complexity: O(n * C * m_max)
 * Space Complexity: O(n * C)
 */
#include <stdio.h>
#include <math.h>

#define MAX_STAGES 16
#define MAX_BUDGET 200

typedef struct {
    double reliability;
    int cost;
} DeviceStage;

double reliability_design(int n, int budget, const DeviceStage stages[], int copies[]) {
    // DP table: dp[stage][cost_spent]
    double dp[MAX_STAGES][MAX_BUDGET] = {{0.0}};

    // Base cost: at least 1 device per stage must be bought
    int base_cost = 0;
    for (int i = 0; i < n; i++) base_cost += stages[i].cost;
    if (base_cost > budget) return 0.0;

    // Initialize stage 0
    for (int b = 0; b <= budget; b++) {
        for (int m = 1; m * stages[0].cost <= b; m++) {
            double rel = 1.0 - pow(1.0 - stages[0].reliability, (double)m);
            if (rel > dp[0][b]) dp[0][b] = rel;
        }
    }

    // Dynamic programming over remaining stages
    for (int i = 1; i < n; i++) {
        for (int b = 0; b <= budget; b++) {
            for (int m = 1; m * stages[i].cost <= b; m++) {
                int rem_budget = b - m * stages[i].cost;
                if (dp[i - 1][rem_budget] > 0.0) {
                    double rel = (1.0 - pow(1.0 - stages[i].reliability, (double)m)) * dp[i - 1][rem_budget];
                    if (rel > dp[i][b]) dp[i][b] = rel;
                }
            }
        }
    }

    // Identify optimal copies via greedy/backtracking evaluation
    int rem = budget;
    for (int i = n - 1; i >= 0; i--) {
        copies[i] = 1;
        double best_val = -1.0;
        int best_m = 1;
        for (int m = 1; m * stages[i].cost <= rem; m++) {
            double cur_rel = 1.0 - pow(1.0 - stages[i].reliability, (double)m);
            double prev_rel = (i > 0) ? dp[i - 1][rem - m * stages[i].cost] : 1.0;
            if (cur_rel * prev_rel > best_val) {
                best_val = cur_rel * prev_rel;
                best_m = m;
            }
        }
        copies[i] = best_m;
        rem -= best_m * stages[i].cost;
    }

    return dp[n - 1][budget];
}

int main(void) {
    int n = 3;
    int budget = 105;
    DeviceStage stages[] = {
        {0.90, 30},
        {0.80, 15},
        {0.50, 20}
    };
    int copies[MAX_STAGES];

    double max_rel = reliability_design(n, budget, stages, copies);

    printf("Optimal System Reliability (Budget = %d): %.6f\n", budget, max_rel);
    for (int i = 0; i < n; i++) {
        printf("Stage #%d: %d copies (Unit cost: %d, Single rel: %.2f)\n",
               i + 1, copies[i], stages[i].cost, stages[i].reliability);
    }

    return 0;
}
"""

# Module 4: Greedy Method
OPTIMAL_STORAGE_TAPES_C = r"""/**
 * Problem: Optimal Storage on Tapes
 * Paradigm: Greedy Method
 * Standard: C11
 *
 * Description: Orders n programs of lengths l_1, l_2, ..., l_n on a sequential tape
 * to minimize the Mean Retrieval Time (MRT = 1/n * sum_{i=1}^n sum_{j=1}^i l_j).
 * Greedy Choice: Sort program lengths in non-decreasing order (Shortest Processing Time).
 * Time Complexity: O(n log n)
 * Space Complexity: O(1) auxiliary
 */
#include <stdio.h>
#include <stdlib.h>

int compare_lengths(const void *a, const void *b) {
    return (*(const int *)a - *(const int *)b);
}

double compute_mrt(int lengths[], int n) {
    // Greedy strategy: Sort lengths ascending
    qsort(lengths, (size_t)n, sizeof(int), compare_lengths);

    double total_retrieval_time = 0;
    int cumulative_sum = 0;

    for (int i = 0; i < n; i++) {
        cumulative_sum += lengths[i];
        total_retrieval_time += cumulative_sum;
    }

    return total_retrieval_time / (double)n;
}

int main(void) {
    int lengths[] = {12, 5, 8, 32, 7, 3};
    int n = (int)(sizeof(lengths) / sizeof(lengths[0]));

    double mrt = compute_mrt(lengths, n);

    printf("Optimal Storage on Tapes Ordering (N = %d):\n", n);
    printf("Optimal Program Sequence: ");
    for (int i = 0; i < n; i++) printf("%d ", lengths[i]);
    printf("\nMinimum Mean Retrieval Time (MRT): %.2f\n", mrt);

    return 0;
}
"""

FRACTIONAL_KNAPSACK_C = r"""/**
 * Problem: Fractional Knapsack Problem
 * Paradigm: Greedy Method
 * Standard: C11
 *
 * Description: Maximizes total value packed into a knapsack of capacity W where
 * arbitrary fractions of items can be taken.
 * Greedy Choice: Greedily select items by highest value-to-weight ratio (v_i / w_i).
 * Time Complexity: O(n log n) for sorting
 * Space Complexity: O(1) auxiliary
 */
#include <stdio.h>
#include <stdlib.h>

typedef struct {
    int id;
    double weight;
    double value;
    double ratio; // value / weight
} Item;

int compare_items(const void *a, const void *b) {
    const Item *ia = (const Item *)a;
    const Item *ib = (const Item *)b;
    if (ib->ratio > ia->ratio) return 1;
    if (ib->ratio < ia->ratio) return -1;
    return 0;
}

double fractional_knapsack(int n, double capacity, Item items[], double taken[]) {
    // Compute value-to-weight ratios
    for (int i = 0; i < n; i++) {
        items[i].ratio = items[i].value / items[i].weight;
        taken[i] = 0.0;
    }

    // Sort descending by ratio
    qsort(items, (size_t)n, sizeof(Item), compare_items);

    double current_weight = 0.0;
    double total_value = 0.0;

    for (int i = 0; i < n; i++) {
        if (current_weight + items[i].weight <= capacity) {
            // Take whole item
            current_weight += items[i].weight;
            total_value += items[i].value;
            taken[i] = 1.0;
        } else {
            // Take remaining fractional portion
            double remain = capacity - current_weight;
            taken[i] = remain / items[i].weight;
            total_value += items[i].value * taken[i];
            break;
        }
    }

    return total_value;
}

int main(void) {
    int n = 3;
    double capacity = 50.0;
    Item items[] = {
        {1, 10.0, 60.0, 0},
        {2, 20.0, 100.0, 0},
        {3, 30.0, 120.0, 0}
    };
    double taken[3];

    double max_val = fractional_knapsack(n, capacity, items, taken);

    printf("Fractional Knapsack (Greedy) Maximum Value: %.2f\n", max_val);
    for (int i = 0; i < n; i++) {
        printf("Item %d: fraction taken = %.2f (Value = %.1f, Weight = %.1f)\n",
               items[i].id, taken[i], items[i].value, items[i].weight);
    }

    return 0;
}
"""

JOB_SEQUENCING_C = r"""/**
 * Problem: Job Sequencing with Deadlines
 * Paradigm: Greedy Method
 * Standard: C11
 *
 * Description: Given n jobs with profits and deadlines, schedules jobs into unit
 * time slots before their deadlines to maximize total profit.
 * Greedy Choice: Sort jobs by profit descending; place in latest available free slot.
 * Time Complexity: O(n * min(n, max_deadline))
 * Space Complexity: O(max_deadline)
 */
#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>

typedef struct {
    char id;
    int deadline;
    int profit;
} Job;

int compare_jobs(const void *a, const void *b) {
    return (((const Job *)b)->profit - ((const Job *)a)->profit);
}

int job_sequencing(Job jobs[], int n, char schedule[]) {
    // 1. Sort jobs descending by profit
    qsort(jobs, (size_t)n, sizeof(Job), compare_jobs);

    // Find maximum deadline
    int max_deadline = 0;
    for (int i = 0; i < n; i++) {
        if (jobs[i].deadline > max_deadline) max_deadline = jobs[i].deadline;
    }

    bool slot[128] = {false};
    int total_profit = 0;

    for (int i = 0; i < n; i++) {
        // Greedily find latest free slot <= deadline
        for (int j = jobs[i].deadline; j > 0; j--) {
            if (!slot[j]) {
                slot[j] = true;
                schedule[j] = jobs[i].id;
                total_profit += jobs[i].profit;
                break;
            }
        }
    }

    return total_profit;
}

int main(void) {
    Job jobs[] = {
        {'a', 2, 100},
        {'b', 1, 19},
        {'c', 2, 27},
        {'d', 1, 25},
        {'e', 3, 15}
    };
    int n = (int)(sizeof(jobs) / sizeof(jobs[0]));
    char schedule[128] = {0};

    int max_profit = job_sequencing(jobs, n, schedule);

    printf("Job Sequencing with Deadlines (Greedy):\n");
    printf("Total Profit Achieved: %d\n", max_profit);
    printf("Scheduled Slots: ");
    for (int i = 1; i <= 3; i++) {
        if (schedule[i]) printf("[Slot %d: Job %c] ", i, schedule[i]);
    }
    printf("\n");

    return 0;
}
"""

OPTIMAL_MERGE_PATTERNS_C = r"""/**
 * Problem: Optimal Merge Patterns
 * Paradigm: Greedy Method
 * Standard: C11
 *
 * Description: Merges n sorted files of varying lengths into a single sorted file
 * with minimal total record comparisons using a greedy 2-way merge min-heap.
 * Greedy Choice: Always merge the two smallest available files first.
 * Time Complexity: O(n log n)
 * Space Complexity: O(n)
 */
#include <stdio.h>
#include <stdlib.h>

typedef struct {
    int *data;
    int size;
    int capacity;
} MinHeap;

MinHeap* create_heap(int capacity) {
    MinHeap *h = (MinHeap *)malloc(sizeof(MinHeap));
    h->data = (int *)malloc((size_t)capacity * sizeof(int));
    h->size = 0;
    h->capacity = capacity;
    return h;
}

void insert_heap(MinHeap *h, int val) {
    int i = h->size++;
    while (i > 0) {
        int parent = (i - 1) / 2;
        if (h->data[parent] <= val) break;
        h->data[i] = h->data[parent];
        i = parent;
    }
    h->data[i] = val;
}

int extract_min(MinHeap *h) {
    int min_val = h->data[0];
    int last = h->data[--h->size];
    int i = 0;
    while (2 * i + 1 < h->size) {
        int left = 2 * i + 1, right = 2 * i + 2;
        int smallest = (right < h->size && h->data[right] < h->data[left]) ? right : left;
        if (last <= h->data[smallest]) break;
        h->data[i] = h->data[smallest];
        i = smallest;
    }
    h->data[i] = last;
    return min_val;
}

int optimal_merge(const int file_sizes[], int n) {
    MinHeap *h = create_heap(n);
    for (int i = 0; i < n; i++) insert_heap(h, file_sizes[i]);

    int total_cost = 0;
    while (h->size > 1) {
        int first = extract_min(h);
        int second = extract_min(h);
        int merged = first + second;
        total_cost += merged;
        insert_heap(h, merged);
    }

    free(h->data);
    free(h);
    return total_cost;
}

int main(void) {
    int files[] = {20, 30, 10, 5, 30};
    int n = (int)(sizeof(files) / sizeof(files[0]));

    int min_comparisons = optimal_merge(files, n);

    printf("Optimal Merge Patterns (Greedy Min-Heap):\n");
    printf("Input File Sizes: ");
    for (int i = 0; i < n; i++) printf("%d ", files[i]);
    printf("\nTotal Record Comparisons Required: %d\n", min_comparisons);

    return 0;
}
"""

KRUSKAL_MST_C = r"""/**
 * Problem: Minimum Spanning Tree (Kruskal's Algorithm)
 * Paradigm: Greedy Method
 * Standard: C11
 *
 * Description: Finds an MST in a connected edge-weighted undirected graph by
 * greedily adding the lowest-weight available edge that does not form a cycle.
 * Data Structure: Disjoint Set Union (Union-Find) with path compression and union-by-rank.
 * Time Complexity: O(E log E) or O(E log V)
 * Space Complexity: O(V + E)
 */
#include <stdio.h>
#include <stdlib.h>

#define MAX_EDGES 128
#define MAX_VERTICES 64

typedef struct {
    int u, v, weight;
} Edge;

typedef struct {
    int parent[MAX_VERTICES];
    int rank[MAX_VERTICES];
} DSU;

void dsu_init(DSU *dsu, int n) {
    for (int i = 0; i < n; i++) {
        dsu->parent[i] = i;
        dsu->rank[i] = 0;
    }
}

int dsu_find(DSU *dsu, int i) {
    if (dsu->parent[i] != i) {
        dsu->parent[i] = dsu_find(dsu, dsu->parent[i]); // Path compression
    }
    return dsu->parent[i];
}

void dsu_union(DSU *dsu, int root_u, int root_v) {
    if (dsu->rank[root_u] < dsu->rank[root_v]) {
        dsu->parent[root_u] = root_v;
    } else if (dsu->rank[root_u] > dsu->rank[root_v]) {
        dsu->parent[root_v] = root_u;
    } else {
        dsu->parent[root_v] = root_u;
        dsu->rank[root_u]++;
    }
}

int compare_edges(const void *a, const void *b) {
    return (((const Edge *)a)->weight - ((const Edge *)b)->weight);
}

int kruskal_mst(int v_count, int e_count, Edge edges[], Edge mst[]) {
    // 1. Sort all edges non-decreasingly by weight
    qsort(edges, (size_t)e_count, sizeof(Edge), compare_edges);

    DSU dsu;
    dsu_init(&dsu, v_count);

    int mst_edges = 0;
    int total_weight = 0;

    for (int i = 0; i < e_count && mst_edges < v_count - 1; i++) {
        int root_u = dsu_find(&dsu, edges[i].u);
        int root_v = dsu_find(&dsu, edges[i].v);

        // If including edge does not cause cycle
        if (root_u != root_v) {
            mst[mst_edges++] = edges[i];
            total_weight += edges[i].weight;
            dsu_union(&dsu, root_u, root_v);
        }
    }

    return total_weight;
}

int main(void) {
    int v = 4;
    Edge edges[] = {
        {0, 1, 10},
        {0, 2, 6},
        {0, 3, 5},
        {1, 3, 15},
        {2, 3, 4}
    };
    int e = (int)(sizeof(edges) / sizeof(edges[0]));
    Edge mst[MAX_VERTICES];

    int mst_weight = kruskal_mst(v, e, edges, mst);

    printf("Kruskal's Minimum Spanning Tree (Total Cost = %d):\n", mst_weight);
    for (int i = 0; i < v - 1; i++) {
        printf("Edge %d -- %d (Weight: %d)\n", mst[i].u, mst[i].v, mst[i].weight);
    }

    return 0;
}
"""

PRIM_MST_C = r"""/**
 * Problem: Minimum Spanning Tree (Prim's Algorithm)
 * Paradigm: Greedy Method
 * Standard: C11
 *
 * Description: Finds an MST by growing a single tree from an arbitrary root,
 * greedily adding the minimum-weight edge connecting the tree to a non-tree vertex.
 * Time Complexity: O(V^2) with adjacency matrix
 * Space Complexity: O(V)
 */
#include <stdio.h>
#include <stdbool.h>
#include <limits.h>

#define MAX_V 32
#define INF 999999

int min_key_vertex(const int key[], const bool in_mst[], int v) {
    int min_val = INF, min_idx = -1;
    for (int i = 0; i < v; i++) {
        if (!in_mst[i] && key[i] < min_val) {
            min_val = key[i];
            min_idx = i;
        }
    }
    return min_idx;
}

int prim_mst(int v, int graph[MAX_V][MAX_V], int parent[]) {
    int key[MAX_V];
    bool in_mst[MAX_V];

    for (int i = 0; i < v; i++) {
        key[i] = INF;
        in_mst[i] = false;
        parent[i] = -1;
    }

    // Start with vertex 0
    key[0] = 0;

    int total_weight = 0;

    for (int count = 0; count < v - 1; count++) {
        int u = min_key_vertex(key, in_mst, v);
        in_mst[u] = true;

        for (int w = 0; w < v; w++) {
            if (graph[u][w] && !in_mst[w] && graph[u][w] < key[w]) {
                parent[w] = u;
                key[w] = graph[u][w];
            }
        }
    }

    for (int i = 1; i < v; i++) {
        total_weight += graph[i][parent[i]];
    }

    return total_weight;
}

int main(void) {
    int v = 5;
    int graph[MAX_V][MAX_V] = {
        {0, 2, 0, 6, 0},
        {2, 0, 3, 8, 5},
        {0, 3, 0, 0, 7},
        {6, 8, 0, 0, 9},
        {0, 5, 7, 9, 0}
    };

    int parent[MAX_V];
    int total_cost = prim_mst(v, graph, parent);

    printf("Prim's Minimum Spanning Tree (Total Weight = %d):\n", total_cost);
    for (int i = 1; i < v; i++) {
        printf("Edge %d -- %d (Weight: %d)\n", parent[i], i, graph[i][parent[i]]);
    }

    return 0;
}
"""

DIJKSTRA_SSSP_C = r"""/**
 * Problem: Single-Source Shortest Path (Dijkstra's Algorithm)
 * Paradigm: Greedy Method
 * Standard: C11
 *
 * Description: Computes shortest paths from a single source vertex to all other
 * vertices in a weighted graph with non-negative edge weights.
 * Greedy Choice: Always select the unvisited vertex with smallest provisional distance.
 * Time Complexity: O(V^2) with array / O(E log V) with min-heap
 * Space Complexity: O(V)
 */
#include <stdio.h>
#include <stdbool.h>

#define MAX_V 32
#define INF 999999

int min_distance_vertex(const int dist[], const bool visited[], int v) {
    int min_val = INF, min_idx = -1;
    for (int i = 0; i < v; i++) {
        if (!visited[i] && dist[i] < min_val) {
            min_val = dist[i];
            min_idx = i;
        }
    }
    return min_idx;
}

void dijkstra(int v, int graph[MAX_V][MAX_V], int source, int dist[]) {
    bool visited[MAX_V] = {false};

    for (int i = 0; i < v; i++) dist[i] = INF;
    dist[source] = 0;

    for (int count = 0; count < v - 1; count++) {
        int u = min_distance_vertex(dist, visited, v);
        if (u == -1) break; // Remaining vertices unreachable
        visited[u] = true;

        // Relaxation of outgoing non-negative edges
        for (int w = 0; w < v; w++) {
            if (!visited[w] && graph[u][w] && dist[u] != INF) {
                if (dist[u] + graph[u][w] < dist[w]) {
                    dist[w] = dist[u] + graph[u][w];
                }
            }
        }
    }
}

int main(void) {
    int v = 5;
    int graph[MAX_V][MAX_V] = {
        {0, 10, 0, 5, 0},
        {0, 0, 1, 2, 0},
        {0, 0, 0, 0, 4},
        {0, 3, 9, 0, 2},
        {7, 0, 6, 0, 0}
    };
    int source = 0;
    int dist[MAX_V];

    dijkstra(v, graph, source, dist);

    printf("Dijkstra Shortest Paths from Source %d:\n", source);
    for (int i = 0; i < v; i++) {
        printf("Vertex %d: distance = %d\n", i, dist[i]);
    }

    return 0;
}
"""

BELLMAN_FORD_SSSP_C = r"""/**
 * Problem: Single-Source Shortest Path (Bellman-Ford Algorithm)
 * Paradigm: Dynamic Programming / Graph Relaxation
 * Standard: C11
 *
 * Description: Computes shortest paths from a single source to all vertices in a
 * directed graph with arbitrary (including negative) edge weights, detecting negative cycles.
 * Recurrence: dist[v] = min(dist[v], dist[u] + weight(u, v)) repeated |V| - 1 times.
 * Time Complexity: O(V * E)
 * Space Complexity: O(V)
 */
#include <stdio.h>
#include <stdbool.h>

#define MAX_V 32
#define MAX_E 128
#define INF 999999

typedef struct {
    int u, v, weight;
} Edge;

bool bellman_ford(int v, int e, const Edge edges[], int source, int dist[]) {
    // Step 1: Initialize distances
    for (int i = 0; i < v; i++) dist[i] = INF;
    dist[source] = 0;

    // Step 2: Relax all edges |V| - 1 times
    for (int i = 1; i <= v - 1; i++) {
        for (int j = 0; j < e; j++) {
            int u = edges[j].u;
            int w = edges[j].v;
            int weight = edges[j].weight;
            if (dist[u] != INF && dist[u] + weight < dist[w]) {
                dist[w] = dist[u] + weight;
            }
        }
    }

    // Step 3: Check for negative-weight cycles
    for (int j = 0; j < e; j++) {
        int u = edges[j].u;
        int w = edges[j].v;
        int weight = edges[j].weight;
        if (dist[u] != INF && dist[u] + weight < dist[w]) {
            return false; // Negative cycle detected
        }
    }

    return true;
}

int main(void) {
    int v = 5;
    Edge edges[] = {
        {0, 1, -1},
        {0, 2, 4},
        {1, 2, 3},
        {1, 3, 2},
        {1, 4, 2},
        {3, 2, 5},
        {3, 1, 1},
        {4, 3, -3}
    };
    int e = (int)(sizeof(edges) / sizeof(edges[0]));
    int source = 0;
    int dist[MAX_V];

    bool no_neg_cycle = bellman_ford(v, e, edges, source, dist);

    if (no_neg_cycle) {
        printf("Bellman-Ford Shortest Paths from Source %d:\n", source);
        for (int i = 0; i < v; i++) {
            printf("Vertex %d: distance = %d\n", i, dist[i]);
        }
    } else {
        printf("Graph contains a negative weight cycle!\n");
    }

    return 0;
}
"""

# Module 5: Branch and Bound
KNAPSACK_LC_BB_C = r"""/**
 * Problem: 0/1 Knapsack Problem
 * Paradigm: Least-Cost (LC) Branch and Bound
 * Standard: C11
 *
 * Description: Solves 0/1 Knapsack by exploring states prioritized by their
 * fractional relaxation upper bound (Least-Cost / Best-First Search).
 * Bounding Function: Fractional knapsack greedy upper bound calculation.
 * Time Complexity: O(2^n) worst case, with significant pruning in practice.
 * Space Complexity: O(2^n) priority queue storage.
 */
#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>

#define MAX_ITEMS 32
#define MAX_QUEUE 1024

typedef struct {
    int level;          // Current item index considered
    int profit;         // Accumulated profit so far
    int weight;         // Accumulated weight so far
    double upper_bound; // Fractional knapsack bound
} LCNode;

typedef struct {
    LCNode nodes[MAX_QUEUE];
    int size;
} MaxPriorityQueue;

void pq_push(MaxPriorityQueue *pq, LCNode node) {
    int i = pq->size++;
    while (i > 0) {
        int parent = (i - 1) / 2;
        if (pq->nodes[parent].upper_bound >= node.upper_bound) break;
        pq->nodes[i] = pq->nodes[parent];
        i = parent;
    }
    pq->nodes[i] = node;
}

LCNode pq_pop(MaxPriorityQueue *pq) {
    LCNode top = pq->nodes[0];
    LCNode last = pq->nodes[--pq->size];
    int i = 0;
    while (2 * i + 1 < pq->size) {
        int left = 2 * i + 1, right = 2 * i + 2;
        int largest = (right < pq->size && pq->nodes[right].upper_bound > pq->nodes[left].upper_bound) ? right : left;
        if (last.upper_bound >= pq->nodes[largest].upper_bound) break;
        pq->nodes[i] = pq->nodes[largest];
        i = largest;
    }
    pq->nodes[i] = last;
    return top;
}

// Compute greedy upper bound via fractional relaxation
double calculate_bound(LCNode u, int n, int W, const int weights[], const int profits[]) {
    if (u.weight >= W) return 0.0;

    double profit_bound = (double)u.profit;
    int j = u.level + 1;
    int total_weight = u.weight;

    while (j < n && total_weight + weights[j] <= W) {
        total_weight += weights[j];
        profit_bound += profits[j];
        j++;
    }

    if (j < n) {
        profit_bound += (W - total_weight) * ((double)profits[j] / weights[j]);
    }

    return profit_bound;
}

int knapsack_lc_bb(int n, int W, const int weights[], const int profits[]) {
    MaxPriorityQueue pq = {.size = 0};

    LCNode u, v;
    u.level = -1;
    u.profit = 0;
    u.weight = 0;
    u.upper_bound = calculate_bound(u, n, W, weights, profits);

    pq_push(&pq, u);
    int max_profit = 0;

    while (pq.size > 0) {
        v = pq_pop(&pq);

        if (v.upper_bound > max_profit && v.level < n - 1) {
            // Branch 1: Include item (v.level + 1)
            u.level = v.level + 1;
            u.weight = v.weight + weights[u.level];
            u.profit = v.profit + profits[u.level];

            if (u.weight <= W && u.profit > max_profit) {
                max_profit = u.profit;
            }

            u.upper_bound = calculate_bound(u, n, W, weights, profits);
            if (u.upper_bound > max_profit) {
                pq_push(&pq, u);
            }

            // Branch 2: Exclude item (v.level + 1)
            u.weight = v.weight;
            u.profit = v.profit;
            u.upper_bound = calculate_bound(u, n, W, weights, profits);
            if (u.upper_bound > max_profit) {
                pq_push(&pq, u);
            }
        }
    }

    return max_profit;
}

int main(void) {
    int weights[] = {2, 4, 6, 9};
    int profits[] = {10, 10, 12, 18};
    int capacity = 15;
    int n = 4;

    int max_val = knapsack_lc_bb(n, capacity, weights, profits);

    printf("0/1 Knapsack (LC Branch & Bound) Maximum Profit: %d\n", max_val);
    return 0;
}
"""

KNAPSACK_FIFO_BB_C = r"""/**
 * Problem: 0/1 Knapsack Problem
 * Paradigm: FIFO Branch and Bound
 * Standard: C11
 *
 * Description: Solves 0/1 Knapsack using Breadth-First Search (FIFO Queue) state-space
 * exploration, maintaining an incumbent best profit to prune non-promising subtrees.
 * Bounding Function: Fractional upper bound compared against incumbent best.
 * Time Complexity: O(2^n) worst case.
 * Space Complexity: O(2^n) queue storage.
 */
#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>

#define MAX_ITEMS 32
#define MAX_QUEUE 2048

typedef struct {
    int level;
    int profit;
    int weight;
    double upper_bound;
} FIFONode;

typedef struct {
    FIFONode data[MAX_QUEUE];
    int front;
    int rear;
} FIFOQueue;

void q_init(FIFOQueue *q) { q->front = 0; q->rear = 0; }
bool q_empty(const FIFOQueue *q) { return q->front == q->rear; }
void q_push(FIFOQueue *q, FIFONode node) { q->data[q->rear++] = node; }
FIFONode q_pop(FIFOQueue *q) { return q->data[q->front++]; }

double compute_fifo_bound(FIFONode u, int n, int W, const int weights[], const int profits[]) {
    if (u.weight >= W) return 0.0;

    double bound = (double)u.profit;
    int j = u.level + 1;
    int current_weight = u.weight;

    while (j < n && current_weight + weights[j] <= W) {
        current_weight += weights[j];
        bound += profits[j];
        j++;
    }

    if (j < n) {
        bound += (W - current_weight) * ((double)profits[j] / weights[j]);
    }

    return bound;
}

int knapsack_fifo_bb(int n, int W, const int weights[], const int profits[]) {
    FIFOQueue q;
    q_init(&q);

    FIFONode u, v;
    u.level = -1;
    u.profit = 0;
    u.weight = 0;
    u.upper_bound = compute_fifo_bound(u, n, W, weights, profits);

    q_push(&q, u);
    int max_profit = 0;

    while (!q_empty(&q)) {
        v = q_pop(&q);

        // Pruning: Skip if bound is not better than current incumbent
        if (v.upper_bound <= max_profit || v.level >= n - 1) continue;

        // Child 1: Include item (v.level + 1)
        u.level = v.level + 1;
        u.weight = v.weight + weights[u.level];
        u.profit = v.profit + profits[u.level];

        if (u.weight <= W && u.profit > max_profit) {
            max_profit = u.profit;
        }

        u.upper_bound = compute_fifo_bound(u, n, W, weights, profits);
        if (u.upper_bound > max_profit) {
            q_push(&q, u);
        }

        // Child 2: Exclude item (v.level + 1)
        u.weight = v.weight;
        u.profit = v.profit;
        u.upper_bound = compute_fifo_bound(u, n, W, weights, profits);
        if (u.upper_bound > max_profit) {
            q_push(&q, u);
        }
    }

    return max_profit;
}

int main(void) {
    int weights[] = {2, 4, 6, 9};
    int profits[] = {10, 10, 12, 18};
    int capacity = 15;
    int n = 4;

    int max_val = knapsack_fifo_bb(n, capacity, weights, profits);

    printf("0/1 Knapsack (FIFO Branch & Bound) Maximum Profit: %d\n", max_val);
    return 0;
}
"""

TSP_BRANCH_AND_BOUND_C = r"""/**
 * Problem: Traveling Salesman Problem (TSP)
 * Paradigm: Branch and Bound (Reduced Cost Matrix)
 * Standard: C11
 *
 * Description: Solves the exact TSP tour using reduced cost matrix lower-bounding
 * with best-first state-space search.
 * Bounding Function: Sum of row and column reductions on distance matrix.
 * Time Complexity: O(2^n * n^2)
 * Space Complexity: O(2^n)
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>

#define MAX_CITIES 12
#define INF 999999

typedef struct {
    int matrix[MAX_CITIES][MAX_CITIES];
    int path[MAX_CITIES];
    int level;
    int vertex;
    int cost;
} TSPNode;

// Reduce matrix rows and columns, accumulating reduction cost
int reduce_matrix(int n, int matrix[MAX_CITIES][MAX_CITIES]) {
    int reduction_cost = 0;

    // Row reduction
    for (int i = 0; i < n; i++) {
        int min_val = INF;
        for (int j = 0; j < n; j++) {
            if (matrix[i][j] < min_val) min_val = matrix[i][j];
        }
        if (min_val != INF && min_val > 0) {
            reduction_cost += min_val;
            for (int j = 0; j < n; j++) {
                if (matrix[i][j] != INF) matrix[i][j] -= min_val;
            }
        }
    }

    // Column reduction
    for (int j = 0; j < n; j++) {
        int min_val = INF;
        for (int i = 0; i < n; i++) {
            if (matrix[i][j] < min_val) min_val = matrix[i][j];
        }
        if (min_val != INF && min_val > 0) {
            reduction_cost += min_val;
            for (int i = 0; i < n; i++) {
                if (matrix[i][j] != INF) matrix[i][j] -= min_val;
            }
        }
    }

    return reduction_cost;
}

int tsp_branch_and_bound(int n, int initial_cost[MAX_CITIES][MAX_CITIES]) {
    TSPNode root;
    memcpy(root.matrix, initial_cost, sizeof(root.matrix));
    root.cost = reduce_matrix(n, root.matrix);
    root.level = 0;
    root.vertex = 0;
    root.path[0] = 0;

    // Best-first priority queue using a simple array for demonstration
    TSPNode queue[256];
    int q_size = 0;
    queue[q_size++] = root;

    int min_tour_cost = INF;

    while (q_size > 0) {
        // Find node with minimum lower bound cost
        int best_idx = 0;
        for (int i = 1; i < q_size; i++) {
            if (queue[i].cost < queue[best_idx].cost) best_idx = i;
        }

        TSPNode current = queue[best_idx];
        queue[best_idx] = queue[--q_size]; // Remove from queue

        if (current.cost >= min_tour_cost) continue;

        if (current.level == n - 1) {
            int last_edge = initial_cost[current.vertex][0];
            if (last_edge != INF && current.cost + last_edge < min_tour_cost) {
                min_tour_cost = current.cost + last_edge;
            }
            continue;
        }

        // Branch to next possible cities
        for (int next_city = 0; next_city < n; next_city++) {
            if (current.matrix[current.vertex][next_city] != INF) {
                TSPNode child;
                memcpy(child.matrix, current.matrix, sizeof(child.matrix));
                memcpy(child.path, current.path, sizeof(child.path));

                child.level = current.level + 1;
                child.vertex = next_city;
                child.path[child.level] = next_city;

                int edge_cost = current.matrix[current.vertex][next_city];

                // Invalidate row of current and col of next_city
                for (int j = 0; j < n; j++) child.matrix[current.vertex][j] = INF;
                for (int i = 0; i < n; i++) child.matrix[i][next_city] = INF;
                child.matrix[next_city][0] = INF; // Prevent premature return to start

                child.cost = current.cost + edge_cost + reduce_matrix(n, child.matrix);

                if (child.cost < min_tour_cost && q_size < 255) {
                    queue[q_size++] = child;
                }
            }
        }
    }

    return min_tour_cost;
}

int main(void) {
    int n = 4;
    int cost_matrix[MAX_CITIES][MAX_CITIES] = {
        {INF, 10, 15, 20},
        {10, INF, 35, 25},
        {15, 35, INF, 30},
        {20, 25, 30, INF}
    };

    int min_cost = tsp_branch_and_bound(n, cost_matrix);
    printf("TSP (Branch & Bound Reduced Cost Matrix) Minimum Tour Cost: %d\n", min_cost);

    return 0;
}
"""

# Map canonical slugs to C source code
C_SOURCES: Dict[str, str] = {
    # Module 1: Divide and Conquer
    "defective-chessboard": DEFECTIVE_CHESSBOARD_C,
    "max-min-divide-conquer": MAX_MIN_DC_C,
    "strassen-matrix-multiplication": STRASSEN_MATRIX_C,

    # Module 2: Backtracking
    "n-queens-backtracking": N_QUEENS_C,
    "subset-sum-backtracking": SUBSET_SUM_C,
    "hamiltonian-cycle-backtracking": HAMILTONIAN_CYCLE_C,

    # Module 3: Dynamic Programming
    "multistage-graph-dp": MULTISTAGE_GRAPH_C,
    "floyd-warshall-apsp": FLOYD_WARSHALL_C,
    "optimal-bst-dp": OPTIMAL_BST_C,
    "0-1-knapsack-dp": KNAPSACK_01_DP_C,
    "traveling-salesman-dp": TSP_HELD_KARP_DP_C,
    "reliability-design-dp": RELIABILITY_DESIGN_DP_C,

    # Module 4: Greedy Method
    "optimal-storage-tapes-greedy": OPTIMAL_STORAGE_TAPES_C,
    "fractional-knapsack": FRACTIONAL_KNAPSACK_C,
    "job-sequencing-deadlines": JOB_SEQUENCING_C,
    "optimal-merge-patterns-greedy": OPTIMAL_MERGE_PATTERNS_C,
    "kruskal-mst": KRUSKAL_MST_C,
    "prim-mst": PRIM_MST_C,
    "dijkstra-sssp": DIJKSTRA_SSSP_C,
    "bellman-ford-sssp": BELLMAN_FORD_SSSP_C,

    # Module 5: Branch and Bound
    "0-1-knapsack-lc-bb": KNAPSACK_LC_BB_C,
    "0-1-knapsack-fifo-bb": KNAPSACK_FIFO_BB_C,
    "traveling-salesman-bb": TSP_BRANCH_AND_BOUND_C,
}

# Alias resolution mapping matching registry.py
C_SOURCE_ALIASES: Dict[str, str] = {
    # Module 1
    "defective-chessboard-dc": "defective-chessboard",
    "tromino-tiling": "defective-chessboard",
    "max-min": "max-min-divide-conquer",
    "max-min-dc": "max-min-divide-conquer",
    "finding-max-min": "max-min-divide-conquer",
    "strassen-matrix": "strassen-matrix-multiplication",
    "strassen": "strassen-matrix-multiplication",

    # Module 2
    "n-queens": "n-queens-backtracking",
    "subset-sum": "subset-sum-backtracking",
    "sum-of-subsets": "subset-sum-backtracking",
    "hamiltonian-cycle": "hamiltonian-cycle-backtracking",
    "hamiltonian-cycles": "hamiltonian-cycle-backtracking",

    # Module 3
    "multistage-graph": "multistage-graph-dp",
    "multistage-graphs": "multistage-graph-dp",
    "floyd-warshall": "floyd-warshall-apsp",
    "all-pairs-shortest-path": "floyd-warshall-apsp",
    "all-pairs-shortest-path-dp": "floyd-warshall-apsp",
    "optimal-bst": "optimal-bst-dp",
    "optimal-binary-search-tree": "optimal-bst-dp",
    "optimal-binary-search-trees": "optimal-bst-dp",
    "0-1-knapsack": "0-1-knapsack-dp",
    "0-1-knapsack-problem": "0-1-knapsack-dp",
    "knapsack-0-1": "0-1-knapsack-dp",
    "knapsack-01": "0-1-knapsack-dp",
    "traveling-salesman": "traveling-salesman-dp",
    "traveling-salesperson": "traveling-salesman-dp",
    "tsp": "traveling-salesman-dp",
    "tsp-dp": "traveling-salesman-dp",
    "reliability-design": "reliability-design-dp",

    # Module 4
    "optimal-storage-on-tapes": "optimal-storage-tapes-greedy",
    "optimal-storage-tapes": "optimal-storage-tapes-greedy",
    "storage-on-tapes": "optimal-storage-tapes-greedy",
    "fractional-knapsack-greedy": "fractional-knapsack",
    "job-sequencing": "job-sequencing-deadlines",
    "job-sequencing-with-deadlines": "job-sequencing-deadlines",
    "optimal-merge-patterns": "optimal-merge-patterns-greedy",
    "optimal-merge": "optimal-merge-patterns-greedy",
    "kruskal": "kruskal-mst",
    "prim": "prim-mst",
    "dijkstra": "dijkstra-sssp",
    "dijkstra-greedy": "dijkstra-sssp",
    "bellman-ford": "bellman-ford-sssp",
    "single-source-shortest-path": "dijkstra-sssp",

    # Module 5
    "knapsack-lc-bb": "0-1-knapsack-lc-bb",
    "knapsack-lc-branch-and-bound": "0-1-knapsack-lc-bb",
    "0-1-knapsack-lc-branch-and-bound": "0-1-knapsack-lc-bb",
    "knapsack-fifo-bb": "0-1-knapsack-fifo-bb",
    "knapsack-fifo-branch-and-bound": "0-1-knapsack-fifo-bb",
    "0-1-knapsack-fifo-branch-and-bound": "0-1-knapsack-fifo-bb",
    "tsp-bb": "traveling-salesman-bb",
    "tsp-branch-and-bound": "traveling-salesman-bb",
    "traveling-salesman-branch-and-bound": "traveling-salesman-bb",
}

def get_c_source(slug: str) -> Optional[str]:
    """Retrieve C11 source code for a given curriculum algorithm slug or alias."""
    target_slug = C_SOURCE_ALIASES.get(slug, slug)
    return C_SOURCES.get(target_slug)

def get_all_c_sources() -> Dict[str, str]:
    """Retrieve mapping of all 23 curriculum algorithm slugs to their C11 source code."""
    return dict(C_SOURCES)
