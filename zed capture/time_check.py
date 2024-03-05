import sys
import numpy as np
from pathlib import Path
import matplotlib.pyplot as plt

def main():
    if not sys.argv or len(sys.argv) != 2:
        sys.stdout.write("Input time txt file required!")
        exit()
    time_fname = Path(sys.argv[1])
    time_diffs = []
    time_prev = 0
    time_curr = 0
    with open(time_fname, "r") as f:
        for line in f:
            time_stamp = int(line.split(', ')[1])
            if time_prev == 0:
                time_prev = time_stamp
            else:
                time_curr = time_stamp
                time_diffs.append((time_curr - time_prev) / 1000)
                time_prev = time_curr
    print(time_diffs)

    plt.plot(np.array(time_diffs))
    plt.show()
    return

if __name__ == "__main__":
    main()
