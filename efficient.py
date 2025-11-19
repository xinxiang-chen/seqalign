import sys
import time
import psutil
import os


def generate(file: str) -> list:
    """ Generate the sequence from input files

    Args:
        file (str): file path

    Returns:
        list: 2 generated substring, [seq1, seq2]
    """

    # Read file and store data as a map: subsequence -> [insert position]
    seq_dict = {}
    with open(file) as f:
        subseq = ""
        insert_position = []
        for line in f:
            line = line.strip()
            try:
                line = int(line)
                insert_position.append(line)
            except:
                if subseq != "":
                    seq_dict[subseq] = insert_position
                    insert_position = []
                subseq = line
        seq_dict[subseq] = insert_position
    
    # Build sequence
    ret = []
    for k, v in seq_dict.items():
        seq = k     # base
        for i in v:
            seq = seq[:i+1] + seq + seq[i+1:]
        ret.append(seq)
    return ret

delta= 30  # gap penalty

alpha = {
    ('A','A'): 0, ('A','C'): 110, ('A','G'): 48, ('A','T'): 94,
    ('C','A'): 110, ('C','C'): 0, ('C','G'): 118, ('C','T'): 48,
    ('G','A'): 48, ('G','C'): 118, ('G','G'): 0, ('G','T'): 110,
    ('T','A'): 94, ('T','C'): 48, ('T','G'): 110, ('T','T'): 0
}


# Compute last DP row using only O(n) space
def compute_dp_row(X, Y):
    """ Computes DP last row for aligning X and Y using O(len(Y)) space """
    prev = [j * delta for j in range(len(Y) + 1)]
    curr = [0] * (len(Y) + 1)

    for i in range(1, len(X) + 1):
        curr[0] = i * delta
        for j in range(1, len(Y) + 1):
            cost_match = prev[j-1] + alpha[(X[i-1], Y[j-1])]
            cost_del = prev[j] + delta
            cost_ins = curr[j-1] + delta
            curr[j] = min(cost_match, cost_del, cost_ins)
        prev, curr = curr, prev   # swap (curr reused)
    
    return prev

# Hirschberg Divide-and-Conquer Alignment


def hirschberg(X, Y):
    """ Returns (aligned_X, aligned_Y) using Hirschberg """
    m, n = len(X), len(Y)

    # Base cases
    if m == 0:
        return "_" * n, Y
    if n == 0:
        return X, "_" * m
    if m == 1 or n == 1:
        return basic_align(X, Y)

    # Divide
    mid = m // 2

    # Forward cost
    left_cost = compute_dp_row(X[:mid], Y)

    # Backward cost (compute on reversed)
    right_cost = compute_dp_row(X[mid:][::-1], Y[::-1])
    right_cost = right_cost[::-1]

    # Choose best split in Y
    split = min(range(len(Y)+1), key=lambda j: left_cost[j] + right_cost[j])

    # Recurse
    (X_left, Y_left) = hirschberg(X[:mid], Y[:split])
    (X_right, Y_right) = hirschberg(X[mid:], Y[split:])

    return X_left + X_right, Y_left + Y_right


# Basic DP for small cases (used inside Hirschberg)

def basic_align(X, Y):
    """ Full DP for tiny strings (used only when one dimension <=1) """
    m, n = len(X), len(Y)
    dp = [[0]*(n+1) for _ in range(m+1)]

    for i in range(m+1):
        dp[i][0] = i * delta
    for j in range(n+1):
        dp[0][j] = j * delta

    for i in range(1, m+1):
        for j in range(1, n+1):
            dp[i][j] = min(
                dp[i-1][j-1] + alpha[(X[i-1], Y[j-1])],
                dp[i-1][j] + delta,
                dp[i][j-1] + delta
            )
    
     # BACKTRACK
    aligned_X = []
    aligned_Y = []
    i, j = m, n

    while i > 0 or j > 0:
        if i > 0 and j > 0 and dp[i][j] == dp[i-1][j-1] + alpha[(X[i-1], Y[j-1])]:
            aligned_X.append(X[i-1])
            aligned_Y.append(Y[j-1])
            i -= 1
            j -= 1
        elif i > 0 and dp[i][j] == dp[i-1][j] + delta:
            aligned_X.append(X[i-1])
            aligned_Y.append("_")
            i -= 1
        else:
            aligned_X.append("_")
            aligned_Y.append(Y[j-1])
            j -= 1

    # Reverse the alignment
    aligned_X = "".join(reversed(aligned_X))
    aligned_Y = "".join(reversed(aligned_Y))

    return aligned_X, aligned_Y

#  Compute cost of final alignment

def compute_alignment_cost(A, B):
    cost = 0
    for x, y in zip(A, B):
        if x == "_" or y == "_":
            cost += delta
        else:
            cost += alpha[(x, y)]
    return cost

if __name__ == "__main__":
    pass
    if len(sys.argv) != 3:
        print("Usage: python3 efficient.py input_path output_path")
        sys.exit(1)

    input_path = sys.argv[1]
    output_path = sys.argv[2]

    # Generate sequences
    seq1, seq2 = generate(input_path)

    start_time = time.time()

    # Hirschberg alignment
    aligned1, aligned2 = hirschberg(seq1, seq2)

    end_time = time.time()
    total_time = (end_time - start_time) * 1000  # ms

    # Compute memory
    process = psutil.Process(os.getpid())
    memory_kb = process.memory_info().rss / 1024

    # Cost
    cost = compute_alignment_cost(aligned1, aligned2)
    
    print(seq1)
    print(seq2)

    # Output in EXACT required format
    with open(output_path, "w") as f:
        f.write(str(cost) + "\n")
        f.write(aligned1 + "\n")
        f.write(aligned2 + "\n")
        f.write(f"{total_time:.3f}\n")
        f.write(f"{memory_kb:.3f}")
    # if len(sys.argv) != 3:
    #     print("Usage: python3 efficient.py input_path output_path", file=sys.stderr)
    #     sys.exit(2)
    # _, input_path, output_path = sys.argv
    # generate(input_path)