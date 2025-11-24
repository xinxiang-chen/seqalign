import sys
import time
from typing import List, Tuple
from strgen import generate

# Scoring constants from the project spec
DELTA = 30
ALPHA = {
    "A": {"A": 0, "C": 110, "G": 48, "T": 94},
    "C": {"A": 110, "C": 0, "G": 118, "T": 48},
    "G": {"A": 48, "C": 118, "G": 0, "T": 110},
    "T": {"A": 94, "C": 48, "G": 110, "T": 0},
}


def _alignment_dp(x: str, y: str) -> Tuple[str, str]:
    """Classic O(mn) dynamic programming alignment with backtracking."""
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

    # Backtrack to build aligned strings
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


def alignment_cost(ax: str, ay: str) -> int:
    """Compute alignment cost given two aligned strings."""
    cost = 0
    for a, b in zip(ax, ay):
        if a == "_" or b == "_":
            cost += DELTA
        else:
            cost += ALPHA[a][b]
    return cost


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
            return float(usage.ru_maxrss)
        except ImportError:
            return 0.0


def main(argv: List[str]) -> int:
    if len(argv) != 3:
        print("Usage: python3 basic.py input_path output_path", file=sys.stderr)
        return 2
    _, input_path, output_path = argv

    strings = generate(input_path)
    if len(strings) != 2:
        raise ValueError("Expected exactly two generated strings")
    x, y = strings[0], strings[1]

    # Use time.perf_counter() for highest resolution on Windows
    t0 = time.perf_counter()
    ax, ay = _alignment_dp(x, y)
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
