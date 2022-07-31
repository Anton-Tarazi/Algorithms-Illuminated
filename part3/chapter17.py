def sequence_alignment(x: str, y: str, gap_penalty: int, mismatch_penalty: int) \
        -> list[list[int]]:
    """Construct sequence alignment with the lowest NW of the sequences. O(mn) runtime."""
    subproblem_array = []

    # base cases
    for i in range(len(x) + 1):
        subproblem_array.append([gap_penalty * i])

    for j in range(1, len(y) + 1):
        subproblem_array[0].append(gap_penalty * j)

    # construct solution as min of three possible subproblems
    for i in range(1, len(x) + 1):
        for j in range(1, len(y) + 1):
            # case 1: symbols are matched in last column of alignment
            # case 2: last symbol of x matched with gap
            # case 3: last symbol of y matched with gap
            if x[i - 1] == y[j - 1]:
                match = 0
            else:
                match = mismatch_penalty
            case1 = subproblem_array[i - 1][j - 1] + match
            case2 = subproblem_array[i - 1][j] + gap_penalty
            case3 = subproblem_array[i][j - 1] + gap_penalty

            subproblem_array[i].append(min(case1, case2, case3))

    return subproblem_array


def nw_score(sequences: tuple[str, str], gap_penalty: int, mismatch_penalty: int) -> int:
    x = sequences[0]
    y = sequences[1]
    return sequence_alignment(x, y, gap_penalty, mismatch_penalty)[-1][-1]


def reconstruction(sequences: tuple[str, str], gap_penalty: int, mismatch_penalty: int) \
        -> tuple[str, str]:
    """Reconstructs the alignment of the sequences. O(m + n) runtime once subproblems
    have been calculated."""
    x = sequences[0]
    y = sequences[1]
    subproblems = sequence_alignment(x, y, gap_penalty, mismatch_penalty)

    m = len(x)
    n = len(y)

    x_reconstruction = []
    y_reconstruction = []

    while m > 0 and n > 0:
        current_nw_score = subproblems[m][n]
        if current_nw_score == subproblems[m - 1][n] + gap_penalty:
            x_reconstruction.append(x[m - 1])
            y_reconstruction.append("-")
            m -= 1

        elif current_nw_score == subproblems[m][n - 1] + gap_penalty:
            x_reconstruction.append("-")
            y_reconstruction.append(y[n - 1])
            n -= 1

        else:
            x_reconstruction.append(x[m - 1])
            y_reconstruction.append(y[n - 1])
            m -= 1
            n -= 1

    while m > 0:
        x_reconstruction.append("-")
        m -= 1

    while n > 0:
        y_reconstruction.append("-")
        n -= 1

    x_sequence = "".join(x_reconstruction[::-1])
    y_sequence = "".join(y_reconstruction[::-1])

    return x_sequence, y_sequence


def verify_reconstruction(aligned: tuple[str, str], gap_penalty: int,
                          mismatch_penalty: int) -> int:
    """Verify that the penalty of the sequences produced by the reconstruction algorithm
    matches the NW score determined by the dynamic programming algorithm."""

    x_reconstruct = aligned[0]
    y_reconstruct = aligned[1]

    # reconstructed sequences should be the same length
    if len(x_reconstruct) != len(y_reconstruct):
        return -1

    n = len(x_reconstruct)
    penalty = 0
    for i in range(n):
        if x_reconstruct[i] == "-" or y_reconstruct[i] == "-":
            penalty += gap_penalty
        elif x_reconstruct[i] != y_reconstruct[i]:
            penalty += mismatch_penalty

    return penalty


def optimal_binary_search_tree(keys: list[int]) -> int:
    """Given a list of keys and frequencies, construct the optimal binary search tree-
    ie such that average depth is minimized. O(n^3) runtime"""

    n = len(keys)
    subproblems = [[0 for _ in range(n + 1)] for _ in range(n + 1)]

    for s in range(n):
        for i in range(n - s):

            # find root that minimized subproblem depth by exhaustive search
            min_sub = float('inf')
            for r in range(i, i + s + 1):
                min_sub = min(min_sub, subproblems[i][r] + subproblems[r + 1][i + s + 1])

            subproblems[i][i + s + 1] = sum(keys[i: i + s + 1]) + min_sub

    return subproblems[0][n]


def efficient_optimal_bst(keys: list[int]):
    """Optimized version of optimal bst algorithm. Precompute partial sums and cache best roots
    in to reduce computations within each loop. O(n^2) runtime"""

    n = len(keys)
    partial_sums = [[0 for _ in range(n)] for _ in range(n)]

    # calculate partial sums for keys from i: j
    for i in range(n):
        for j in range(i, n):
            if i == j:
                partial_sums[i][j] = keys[i]
            else:
                partial_sums[i][j] = partial_sums[i][j - 1] + keys[j]

    subproblems = [[(0, -1) for _ in range(n + 1)] for _ in range(n + 1)]

    # initialize main diagonal
    for i in range(n):
        subproblems[i][i + 1] = (keys[i], i)

    for s in range(1, n):
        for i in range(n - s):

            # to calculate the optimate root of keys[i:j], r(i, j) we must have:
            # r(i, j - 1) <= r(i , j) <= r(i + 1, j)
            # which allows us to check fewer roots for each iteration of the outer two for
            # loops
            min_sub = float('inf')
            best_root = -1
            root_min = subproblems[i][i + s][1]
            root_max = subproblems[i + 1][i + s + 1][1]

            for r in range(root_min, root_max + 1):
                if subproblems[i][r][0] + subproblems[r + 1][i + s + 1][0] < min_sub:
                    min_sub = subproblems[i][r][0] + subproblems[r + 1][i + s + 1][0]
                    best_root = r

            subproblems[i][i + s + 1] = (partial_sums[i][i + s] + min_sub, best_root)

    return subproblems[0][n][0]





