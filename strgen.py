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


if __name__ == "__main__":
    pass