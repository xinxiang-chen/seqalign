# Sequence Align (CSCI570 - Final Project)

Alignment implementations for the CSCI570 final project. Two solvers are provided:
- `basic.py`: classic O(mn) dynamic programming with full table backtracking.
- `efficient.py`: Hirschberg-style divide-and-conquer with O(mn) time and O(m + n) memory.

## Repository layout
- `basic.py` / `efficient.py`: main entry points for the two solvers.
- `basic.sh` / `efficient.sh`: convenience wrappers for POSIX shells.
- `strgen.py`: expands the compact input format into full sequences.
- `Datapoints/`: sample input files from the assignment.

## Input format (per spec)
Each block starts with a base string, followed by integer lines indicating where to duplicate the current string:
```
BASESTRING
3
7
NEXTBASE
2
```
For each index `i`, the generator inserts the current string after position `i` (0-based) in the current string, doubling it. Two blocks produce two generated strings for alignment.

## Running locally
Prereqs: Python 3.8+ (tested with 3.11). `psutil` is optional and only affects memory reporting.

Basic DP solver:
- macOS/Linux: `python3 basic.py Datapoints/in1.txt out_basic.txt`
- Windows (PowerShell): `python basic.py Datapoints\\in1.txt out_basic.txt`

Efficient (Hirschberg) solver:
- macOS/Linux: `python3 efficient.py Datapoints/in1.txt out_efficient.txt`
- Windows (PowerShell): `python efficient.py Datapoints\\in1.txt out_efficient.txt`

Shell wrappers (macOS/Linux/WSL):
- `sh basic.sh Datapoints/in1.txt out_basic.txt`
- `sh efficient.sh Datapoints/in1.txt out_efficient.txt`

Note on spec requirement: The assignment asks for `basic.sh` and `efficient.sh` to compile/run the basic and efficient versions (example shows Java). This repo provides the same entrypoints for the Python implementations; the execution shape matches the spec: `./basic.sh input.txt output.txt` and `./efficient.sh input.txt output.txt`.

## Output file structure
Five lines are written:
1. Total alignment cost
2. Aligned first string
3. Aligned second string
4. Runtime in milliseconds
5. Memory in KB (0.0 if measurement unavailable)

## Notes
- `psutil` is preferred for memory measurement; if missing, the code falls back to `resource` on Linux or returns 0.0.
- The scoring matrix and gap penalty match the provided project specification.

## License
MIT (see LICENSE).***
