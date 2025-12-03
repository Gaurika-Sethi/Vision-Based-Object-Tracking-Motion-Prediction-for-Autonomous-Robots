import csv
import math
import matplotlib.pyplot as plt

# Path to the CSV you already generated from run_tracking.py
CSV_PATH = "trajectory_log.csv"  # inside results/

frames = []
mx_list, my_list = [], []
px_list, py_list = [], []
errors = []

with open(CSV_PATH, "r") as f:
    reader = csv.reader(f)
    for row in reader:
        # each row: frame, mx, my, px, py
        if len(row) < 5:
            continue
        frame = int(row[0])
        mx, my = float(row[1]), float(row[2])
        px, py = float(row[3]), float(row[4])

        frames.append(frame)
        mx_list.append(mx)
        my_list.append(my)
        px_list.append(px)
        py_list.append(py)

        err = math.sqrt((mx - px)**2 + (my - py)**2)
        errors.append(err)

# 1) Error vs Frame
plt.figure()
plt.plot(frames, errors)
plt.xlabel("Frame")
plt.ylabel("Prediction Error (pixels)")
plt.title("Kalman Prediction Error vs Frame")
plt.grid(True)
plt.tight_layout()
plt.savefig("error_vs_frame_plot.png", dpi=300)

# 2) Measured vs Predicted Scatter (X–Y)
plt.figure()
plt.plot(mx_list, my_list, label="Measured (Optical Flow)", linewidth=1)
plt.plot(px_list, py_list, label="Predicted (Kalman)", linewidth=1)
plt.xlabel("X position (pixels)")
plt.ylabel("Y position (pixels)")
plt.title("Measured vs Predicted Trajectory")
plt.legend()
plt.gca().invert_yaxis()  # image coords: top-left origin
plt.grid(True)
plt.tight_layout()
plt.savefig("measured_vs_predicted_scatter.png", dpi=300)

# 3) Error histogram (optional but nice)
plt.figure()
plt.hist(errors, bins=20)
plt.xlabel("Prediction Error (pixels)")
plt.ylabel("Frequency")
plt.title("Distribution of Prediction Error")
plt.tight_layout()
plt.savefig("error_histogram.png", dpi=300)

print("Plots saved as:")
print("  error_vs_frame_plot.png")
print("  measured_vs_predicted_scatter.png")
print("  error_histogram.png")