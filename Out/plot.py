#!/usr/bin/env python3
import pandas as pd
import matplotlib.pyplot as plt

def main(drawMem=False):
    # Read csv
    df = pd.read_csv("Out/datapoints_table.csv")

    # Check columns (optional sanity print)
    # print(df.head())

    x = df["size"]
    y_basic = df["time_basic"]
    y_effi = df["time_effi"]
    label = 'CPU Time (ms)'

    if drawMem:
        y_basic = df["mem_basic"]
        y_effi = df["mem_effi"]
        label = 'Memory (KB)'

    plt.figure(figsize=(10,6))

    # size vs time_basic
    plt.plot(x, y_basic, marker="o", linestyle="-", label="basic")

    # size vs time_effi
    plt.plot(x, y_effi, marker="o", linestyle="-", label="efficient")

    plt.xlabel("Problem Size")
    plt.ylabel(label)
    plt.title(f"Problem size vs {label}")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    # plt.show()
    plt.savefig('Out/time.png')

if __name__ == "__main__":
    main(drawMem=False)