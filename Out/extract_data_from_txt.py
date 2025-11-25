#!/usr/bin/env python3
import os
import sys

def main(folder):
    # if len(sys.argv) != 2:
    #     print(f"Usage: python {sys.argv[0]} <folder_path>")
    #     sys.exit(1)

    # folder = sys.argv[1]

    if not os.path.isdir(folder):
        print(f"Folder does not exist: {folder}")
        sys.exit(1)

    # from out1.txt to out15.txt
    for i in range(1, 16):
        filename = f"out{i}.txt"
        filepath = os.path.join(folder, filename)

        # print(f"\n=== {filename} ===")

        if not os.path.isfile(filepath):
            print("File not found.")
            continue

        with open(filepath, "r", encoding="utf-8") as f:
            lines = f.readlines()

        if len(lines) < 5:
            print(f"File has only {len(lines)} lines, cannot get 4th and 5th.")
            continue

        line4 = lines[3].rstrip("\n")
        line5 = lines[4].rstrip("\n")

        print(f"{line4}")
        # print(f"{line5}")

if __name__ == "__main__":
    main('./Out/efficient')