import sys
import time
from typing import List, Tuple

# Scoring constants (fixed by spec)
DELTA = 30
ALPHA = {
    "A": {"A": 0, "C": 110, "G": 48, "T": 94},
    "C": {"A": 110, "C": 0, "G": 118, "T": 48},
    "G": {"A": 48, "C": 118, "G": 0, "T": 110},
    "T": {"A": 94, "C": 48, "G": 110, "T": 0},
}


def generate(file: str) -> list:
    """ Generate the sequence from input files

    Args:
        file (str): file path

    Returns:
        list: 2 generated substring, [s1, s2]
    """

    # Read file and store data as a list of pairs: (base_string, [insert_positions])
    pairs = []
    current_base = ""
    positions = []

    with open(file) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                idx = int(line)
                positions.append(idx)
            except ValueError:
                if current_base:
                    pairs.append((current_base, positions))
                    positions = []
                current_base = line
        # capture last block
        if current_base:
            pairs.append((current_base, positions))
    
    # Build sequence
    ret = []
    for base, idxs in pairs:
        seq = base
        for i in idxs:
            seq = seq[:i+1] + seq + seq[i+1:]
        ret.append(seq)
    return ret


def alignment_cost(ax: str, ay: str) -> int:
    """Compute total alignment cost for two aligned strings."""
    cost = 0
    for a, b in zip(ax, ay):
        if a == "_" or b == "_":
            cost += DELTA
        else:
            cost += ALPHA[a][b]
    return cost


def _dp_full(x: str, y: str) -> Tuple[str, str]:
    """Full O(mn) DP with backtracking. Used for small subproblems."""
    m, n = len(x), len(y)
    dp = [[0] * (n + 1) for _ in range(m + 1)]

    for i in range(1, m + 1):
        dp[i][0] = i * DELTA
    for j in range(1, n + 1):
        dp[0][j] = j * DELTA

    for i in range(1, m + 1):
        xi = x[i - 1]
        row = dp[i]
        prev_row = dp[i - 1]
        for j in range(1, n + 1):
            yj = y[j - 1]
            match = prev_row[j - 1] + ALPHA[xi][yj]
            gap_x = prev_row[j] + DELTA
            gap_y = row[j - 1] + DELTA
            row[j] = min(match, gap_x, gap_y)

    # Backtrack
    ax: List[str] = []
    ay: List[str] = []
    i, j = m, n
    while i > 0 or j > 0:
        if i > 0 and j > 0 and dp[i][j] == dp[i - 1][j - 1] + ALPHA[x[i - 1]][y[j - 1]]:
            ax.append(x[i - 1])
            ay.append(y[j - 1])
            i -= 1
            j -= 1
        elif i > 0 and dp[i][j] == dp[i - 1][j] + DELTA:
            ax.append(x[i - 1])
            ay.append("_")
            i -= 1
        else:
            ax.append("_")
            ay.append(y[j - 1])
            j -= 1

    ax.reverse()
    ay.reverse()
    return "".join(ax), "".join(ay)


def dp_last_row(x: str, y: str) -> List[int]:
    """Return last row of DP table for x vs y using O(len(y)) {O(n)} space."""
    n = len(y)
    prev = [j * DELTA for j in range(n + 1)]

    for i, xi in enumerate(x, start=1):
        curr = [0] * (n + 1)
        curr[0] = i * DELTA
        for j, yj in enumerate(y, start=1):
            match = prev[j - 1] + ALPHA[xi][yj]
            gap_x = prev[j] + DELTA
            gap_y = curr[j - 1] + DELTA
            curr[j] = min(match, gap_x, gap_y)
        prev = curr
    return prev


def hirschberg(x: str, y: str) -> Tuple[str, str]:
    """Memory-efficient Hirschberg alignment returning aligned strings."""
    m, n = len(x), len(y)

    # Simple bases
    if m == 0:
        return "_" * n, y
    if n == 0:
        return x, "_" * m

    # Use full DP for small subproblems
    if m * n <= 50:  # threshold keeps recursion shallow on tiny cases
        return _dp_full(x, y)

    mid = m // 2
    x_front, x_back = x[:mid], x[mid:]

    L = dp_last_row(x_front, y)

    x_back_rev = x_back[::-1]
    y_rev = y[::-1]
    R_rev = dp_last_row(x_back_rev, y_rev)

    # Find split k minimizing L[k] + R_rev[n - k]
    best_k = 0
    best_cost = L[0] + R_rev[n]
    for k in range(1, n + 1):
        cost = L[k] + R_rev[n - k]
        if cost < best_cost:
            best_cost = cost
            best_k = k

    ax1, ay1 = hirschberg(x_front, y[:best_k])
    ax2, ay2 = hirschberg(x_back, y[best_k:])
    return ax1 + ax2, ay1 + ay2


def _measure_memory_kb() -> float:
    """Best-effort memory measurement; returns 0.0 if unsupported."""
    # Prioritize psutil as per sample code suggestion
    try:
        import psutil
        process = psutil.Process()
        memory_info = process.memory_info()
        # rss is in bytes, convert to KB
        return memory_info.rss / 1024.0
    except ImportError:
        # Fallback to resource (standard on Linux)
        try:
            import resource
            usage = resource.getrusage(resource.RUSAGE_SELF)
            # Note: ru_maxrss is in KB on Linux, Bytes on macOS. 
            # Assuming Linux environment for grading if psutil is missing.
            return float(usage.ru_maxrss)
        except ImportError:
            return 0.0


def main(argv: List[str]) -> int:
    if len(argv) != 3:
        print("Usage: python3 efficient.py input_path output_path", file=sys.stderr)
        return 2
    _, input_path, output_path = argv

    strings = generate(input_path)
    if len(strings) != 2:
        raise ValueError("Expected exactly two generated strings")
    x, y = strings[0], strings[1]

    # Use time.perf_counter() for highest resolution on Windows
    t0 = time.perf_counter()
    ax, ay = hirschberg(x, y)
    t1 = time.perf_counter()

    time_ms = (t1 - t0) * 1000.0
    mem_kb = _measure_memory_kb()
    cost = alignment_cost(ax, ay)

    lines = [
        str(cost),
        ax,
        ay,
        f"{time_ms:.3f}",
        f"{mem_kb:.3f}",
    ]

    with open(output_path, "w") as f:
        f.write("\n".join(lines))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
