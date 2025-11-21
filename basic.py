import sys
import time
import psutil


DELTA = 30

ALPHA = {
    ('A', 'A'): 0,   ('A', 'C'): 110, ('A', 'G'): 48,  ('A', 'T'): 94,
    ('C', 'A'): 110, ('C', 'C'): 0,   ('C', 'G'): 118, ('C', 'T'): 48,
    ('G', 'A'): 48,  ('G', 'C'): 118, ('G', 'G'): 0,   ('G', 'T'): 110,
    ('T', 'A'): 94,  ('T', 'C'): 48,  ('T', 'G'): 110, ('T', 'T'): 0,
}

def mismatch_cost(a, b):
    return ALPHA[(a, b)]


def generate_string(base, indices):
    s = base
    for idx in indices:
        s = s[:idx+1] + s + s[idx+1:]
    return s


def parse_input(path):
    with open(path, 'r') as f:
        lines = [line.strip() for line in f if line.strip()]

    p = 0
    s0 = lines[p]; p += 1

    s_indices = []
    while p < len(lines):
        try:
            s_indices.append(int(lines[p]))
            p += 1
        except:
            break

    t0 = lines[p]; p += 1

    t_indices = []
    while p < len(lines):
        t_indices.append(int(lines[p]))
        p += 1

    s = generate_string(s0, s_indices)
    t = generate_string(t0, t_indices)
    return s, t


def process_memory_kb():
    process = psutil.Process()
    return int(process.memory_info().rss / 1024)


def measure_algorithm(func, *args):
    before = process_memory_kb()
    start = time.time()

    cost, ax, ay = func(*args)

    end = time.time()
    after = process_memory_kb()

    return cost, ax, ay, (end - start) * 1000, after - before


def basic_alignment(X, Y):
    m, n = len(X), len(Y)

    dp = [[0] * (n+1) for _ in range(m+1)]
    parent = [[None] * (n+1) for _ in range(m+1)]

    for i in range(1, m+1):
        dp[i][0] = i * DELTA
        parent[i][0] = 'U'
    for j in range(1, n+1):
        dp[0][j] = j * DELTA
        parent[0][j] = 'L'

    for i in range(1, m+1):
        for j in range(1, n+1):
            diag = dp[i-1][j-1] + mismatch_cost(X[i-1], Y[j-1])
            up = dp[i-1][j] + DELTA
            left = dp[i][j-1] + DELTA

            best = diag
            move = 'D'
            if up < best:
                best = up
                move = 'U'
            if left < best:
                best = left
                move = 'L'

            dp[i][j] = best
            parent[i][j] = move

    aligned_X = []
    aligned_Y = []
    i, j = m, n

    while i > 0 or j > 0:
        move = parent[i][j]
        if move == 'D':
            aligned_X.append(X[i-1])
            aligned_Y.append(Y[j-1])
            i -= 1
            j -= 1
        elif move == 'U':
            aligned_X.append(X[i-1])
            aligned_Y.append('_')
            i -= 1
        elif move == 'L':
            aligned_X.append('_')
            aligned_Y.append(Y[j-1])
            j -= 1

    aligned_X.reverse()
    aligned_Y.reverse()

    return dp[m][n], ''.join(aligned_X), ''.join(aligned_Y)


def write_output(path, cost, ax, ay, t_ms, mem_kb):
    with open(path, 'w') as f:
        f.write(str(cost) + "\n")
        f.write(ax + "\n")
        f.write(ay + "\n")
        f.write(str(t_ms) + "\n")
        f.write(str(mem_kb) + "\n")


def main():
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    X, Y = parse_input(input_file)
    cost, ax, ay, t_ms, mem_kb = measure_algorithm(basic_alignment, X, Y)
    write_output(output_file, cost, ax, ay, t_ms, mem_kb)


if __name__ == "__main__":
    main()
