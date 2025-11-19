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

    def __init__(self, file_path=None):
        if file_path is None:
            self.seq1, self.seq2 = '', ''
        else:
            self.seq1, self.seq2 = generate(file_path)

    def set_seqs(self, seq1, seq2):
        self.seq1 = seq1
        self.seq2 = seq2

    def bottom_up(self):        # get the cost of alignment
        self.dp = [[0] * (len(self.seq2) + 1) for _ in range(len(self.seq1) + 1)]
        self.dp[0] = [self.delta * i for i in range(len(self.dp[0]))]
        for i in range(len(self.dp)):
            self.dp[i][0] = i * self.delta

        for m in range(1, len(self.dp)):
            for n in range(1, len(self.dp[0])):
                self.dp[m][n] = min(self.dp[m-1][n-1] + self.alpha[self.seq1[m - 1]][self.seq2[n - 1]],                                                # x_m, y_n are aligned
                                    self.dp[m-1][n] + self.delta,   # x_m is not matched
                                    self.dp[m][n-1] + self.delta    # y_n is not matched
                                    )
        print(self.dp)
        return self.dp[-1][-1]

    def top_down(self):         # trace back
        m = len(self.dp) - 1
        n = len(self.dp[0]) - 1
        seq1_aligned = ''
        seq2_aligned = ''

        while m > 0 or n > 0:
            if n > 0 and self.dp[m][n] == self.dp[m][n-1] + self.delta:      # seq2 is not matched(seq1 has a gap)
                seq1_aligned = '_' + seq1_aligned
                seq2_aligned = self.seq2[n - 1] + seq2_aligned
                n -= 1
            elif m > 0 and n > 0 and self.dp[m][n] == self.dp[m-1][n-1] + self.alpha[self.seq1[m - 1]][self.seq2[n - 1]]:    # matched
                seq1_aligned = self.seq1[m - 1] + seq1_aligned
                seq2_aligned = self.seq2[n - 1] + seq2_aligned
                m -= 1
                n -= 1
            elif m > 0 and self.dp[m][n] == self.dp[m-1][n] + self.delta:    # seq1 is not matched(seq2 has a gap)
                seq2_aligned = '_' + seq2_aligned
                seq1_aligned = self.seq1[m - 1] + seq1_aligned
                m -= 1
        
        return seq1_aligned, seq2_aligned


class Efficient:
    delta = 30      # gap cost
    alpha = {       # mismatch cost table
        'A': {'A': 0, 'C': 110, 'G': 48, 'T': 94},
        'C': {'A': 110, 'C': 0, 'G': 118, 'T': 48},
        'G': {'A': 48, 'C': 118, 'G': 0, 'T': 110},
        'T': {'A': 94, 'C': 48, 'G': 110, 'T': 0}
    }

    def __init__(self, file_path=None):
        if file_path is None:
            self.seq1, self.seq2 = '', ''
        else:
            self.seq1, self.seq2 = generate(file_path)

    def set_seqs(self, seq1, seq2):
        self.seq1 = seq1
        self.seq2 = seq2

    def xL_align_with_y_cost(self, xL, y):      # create the mem-efficient table with mem space O(len(y))
        xL_row = [self.delta * i for i in range(len(y) + 1)]        # previous row
        for i in range(1, len(xL) + 1):
            new_xL_row = [i * self.delta] + [0] * len(y)            # current row
            for j in range(1, len(new_xL_row)):
                new_xL_row[j] = min(    # here, replace[i-1] with xL_row, which is the previous row
                                        xL_row[j-1] + self.alpha[xL[i - 1]][y[j - 1]],   # x_m, y_n are aligned
                                        xL_row[j] + self.delta,                                         # x_m is not matched
                                        new_xL_row[j-1] + self.delta                                    # y_n is not matched
                                    )
            xL_row = new_xL_row
        return xL_row
    
    def xR_align_with_y_cost(self, xR, y):      # reverse: convert the xR and y to prefix style
        xR_reversed = xR[::-1]
        y_reversed = y[::-1]

        # reverse this before sum up xL and xR rows, that we can add two row up directly without iteration
        return self.xL_align_with_y_cost(xR_reversed, y_reversed)[::-1]     

    def rec_efficient(self, x, y):
        '''
        1. split x at middle 
        2. calculate cost for left and right (signle row)
        3. iterate every points in y, find best point k
        4. conquer split at best k
        '''
        m = len(x)
        n = len(y)

        # base case
        if m == 0:
            return '_' * n, y, self.delta * n
        if n == 0:
            return x, '_' * m, self.delta * m
        if m == 1 or n == 1:
            basicAlign = Basic()
            basicAlign.set_seqs(x, y)
            cost = basicAlign.bottom_up()
            x_align, y_align = basicAlign.top_down()
            return x_align, y_align, cost
        
        # devide step: devide X in 1/2
        xL = x[:m // 2]
        xR = x[m // 2:]

        # create memory-efficient dp table
        xL_row = self.xL_align_with_y_cost(xL, y)
        xR_row = self.xR_align_with_y_cost(xR, y)

        # add up xL and xR rows, find min value, which is the best split point
        x_row_sum = [a + b for a, b in zip(xL_row, xR_row)]
        best_value = min(x_row_sum)
        best_split_point = x_row_sum.index(best_value)
        
        xL_align, yL_align, costL = self.rec_efficient(xL, y[:best_split_point])
        xR_align, yR_align, costR = self.rec_efficient(xR, y[best_split_point:])

        return xL_align + xR_align, yL_align + yR_align, costL + costR
        
    def efficient(self):
        x, y, z = self.rec_efficient(self.seq1, self.seq2)
        print(x, y, z)


if __name__ == "__main__":
    align = Basic('Datapoints/in2.txt')
    align.bottom_up()
    print(align.top_down())

    align_e = Efficient('Datapoints/in2.txt')
    align_e.efficient()