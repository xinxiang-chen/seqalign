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
    # print(seq_dict)
    
    # Build sequence
    ret = []
    for k, v in seq_dict.items():
        seq = k     # base
        for i in v:
            seq = seq[:i+1] + seq + seq[i+1:]
            # print(seq)
        ret.append(seq)
    return ret


if __name__ == "__main__":
    print(generate("Datapoints/in15.txt"))
    assert generate("Datapoints/test.txt")[0] == "ACACTGACTACTGACTGGTGACTACTGACTGG", ()
    assert generate("Datapoints/test.txt")[1] == "TATTATACGCTATTATACGCGACGCGGACGCG", ()