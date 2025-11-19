import sys

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


class Basic:
    delta = 30      # gap cost
    alpha = {       # mismatch cost table
        'A': {'A': 0, 'C': 110, 'G': 48, 'T': 94},
        'C': {'A': 110, 'C': 0, 'G': 118, 'T': 48},
        'G': {'A': 48, 'C': 118, 'G': 0, 'T': 110},
        'T': {'A': 94, 'C': 48, 'G': 110, 'T': 0},
    }

    def __init__(self, file_path):
        self.seq1, self.seq2 = generate(file_path)

    def set_seqs(self, seq1, seq2):
        self.seq1 = seq1
        self.seq2 = seq2


    def bottom_up(self):
        self.dp = [[0] * (len(self.seq2) + 1) for _ in range(len(self.seq1) + 1)]
        self.dp[0] = [self.delta * i for i in range(len(self.dp[0]))]
        for i in range(len(self.dp)):
            self.dp[i][0] = i * self.delta
        print(self.dp)

        for m in range(1, len(self.dp)):
            for n in range(1, len(self.dp[0])):
                self.dp[m][n] = min(self.dp[m-1][n-1] + self.alpha[self.seq1[m - 1]][self.seq2[n - 1]],                                                # x_m, y_n are aligned
                                    self.dp[m-1][n] + self.delta,   # x_m is not matched
                                    self.dp[m][n-1] + self.delta    # y_n is not matched
                                    )
        print(self.dp)
        return self.dp[-1][-1]

    def top_down(self):
        # cases:
        # 0 -> from (m, n-1)        seq2 is not matched
        # 1 -> from (m-1, n-1)      matched
        # 2 -> from (m-1, n)        seq1 is not matched
        m = len(self.dp) - 1
        n = len(self.dp[0]) - 1
        seq1_aligned = ''
        seq2_aligned = ''

        while m > 0 or n > 0:
            cell0 = self.dp[m][n-1] + self.delta
            cell1 = self.dp[m-1][n-1] + self.alpha[self.seq1[m - 1]][self.seq2[n - 1]]
            cell2 = self.dp[m-1][n] + self.delta

            values = [
                (0, cell0),
                (1, cell1),
                (2, cell2)
            ]
            best_cell, _ = min(values, key=lambda x: x[1])
            print(best_cell)

            if best_cell == 0:      # seq2 is not matched(seq1 has a gap)
                seq1_aligned = '_' + seq1_aligned
                seq2_aligned = self.seq2[n - 1] + seq2_aligned
                n -= 1
            elif best_cell == 1:    # matched
                seq1_aligned = self.seq1[m - 1] + seq1_aligned
                seq2_aligned = self.seq2[n - 1] + seq2_aligned
                m -= 1
                n -= 1
            elif best_cell == 2:    # seq1 is not matched(seq2 has a gap)
                seq2_aligned = '_' + seq2_aligned
                seq1_aligned = self.seq1[m - 1] + seq1_aligned
                m -= 1
        

        print(seq1_aligned)
        print(seq2_aligned)


        pass

        

if __name__ == "__main__":
    pass

    align = Basic('Datapoints/in1.txt')
    align.set_seqs('ACCGGTCG', 'CCAGGTGGC')
    print(align.seq1)
    print(align.seq2)
    align.bottom_up()
    align.top_down()