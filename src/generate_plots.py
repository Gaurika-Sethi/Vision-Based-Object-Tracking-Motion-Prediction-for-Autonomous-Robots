import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

df = pd.read_csv("results/trajectory_log.csv", header=None)

# Assign proper column names
df.columns = ["frame", "mx", "my", "px", "py"]

# Trajectory plot
plt.figure(figsize=(6,6))
plt.plot(df["mx"], df["my"], 'r-', label="Measured (Optical Flow)")
plt.plot(df["px"], df["py"], 'b-', label="Predicted (Kalman)")
plt.gca().invert_yaxis()
plt.xlabel("X position (pixels)")
plt.ylabel("Y position (pixels)")
plt.title("Measured vs Predicted Trajectory")
plt.legend()
plt.tight_layout()
plt.savefig("results/measured_vs_predicted_scatter.png")
plt.show()

# Error computation
error = np.sqrt((df["mx"] - df["px"])**2 + (df["my"] - df["py"])**2)

# Error vs frame
plt.figure(figsize=(7,4))
plt.plot(df["frame"], error)
plt.xlabel("Frame Index")
plt.ylabel("Prediction Error (pixels)")
plt.title("Prediction Error vs Frame")
plt.tight_layout()
plt.savefig("results/error_vs_frame_plot.png")
plt.show()

# Error histogram
plt.figure(figsize=(6,4))
plt.hist(error, bins=30)
plt.xlabel("Prediction Error (pixels)")
plt.ylabel("Frequency")
plt.title("Error Distribution")
plt.tight_layout()
plt.savefig("results/error_histogram.png")
plt.show()