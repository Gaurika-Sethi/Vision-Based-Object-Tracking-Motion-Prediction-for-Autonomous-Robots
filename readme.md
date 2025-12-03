# Vision-Based Human Motion Tracking and Prediction

This project implements a complete vision pipeline to **track a walking person and predict future positions** using **optical flow** and a **Kalman filter**. It is designed as a research-oriented proof of concept for robotics and defence labs (e.g., IIT / IIIT / DRDO environments).

---

## 🎯 Overview

**Goal:**  
Given a static-camera video of a person walking sideways, the system should:

1. Detect the person in each frame  
2. Track motion over time using optical flow  
3. Estimate velocity and **predict future positions** with a Kalman filter  
4. Analyse prediction accuracy with quantitative plots

**Core ideas:**

- Background subtraction (MOG2) for foreground segmentation  
- Lucas–Kanade optical flow for local motion tracking  
- Constant-velocity Kalman filter with state  
  \[
  x = [x, y, v_x, v_y]^T
  \]
- Future-position visualisation by projecting the state a few frames ahead

---

## 🧱 System Architecture

1. **Person Detection (`detector.py`)**
   - Uses OpenCV's MOG2 background subtractor
   - Performs morphological operations to clean the foreground mask
   - Finds the largest contour and draws a bounding box around the person

2. **Optical Flow Tracker (`optical_flow_tracker.py`)**
   - Detects good feature points (Shi–Tomasi) inside the bounding box
   - Tracks these points with pyramidal Lucas–Kanade optical flow
   - Computes the mean of valid tracked points as a **pseudo-centroid**
   - Stores centroids as the **measured trajectory**

3. **Kalman Predictor (`kalman_filter.py`)**
   - 4D state: position and velocity in image coordinates
   - Constant-velocity transition model, tuned process and measurement noise
   - Initialised from the first valid optical-flow measurement
   - Generates a **future position** by
     \[
     (x_{\text{pred}}, y_{\text{pred}}) = (x + \alpha v_x, ~y + \alpha v_y)
     \]
     with \(\alpha \approx 1\!-\!2\).

4. **Main Runner (`run_tracking.py`)**
   - Ties together detection, optical flow, and Kalman prediction
   - Draws:
     - **Red line**: measured trajectory (optical flow)
     - **Blue line**: forward-predicted trajectory (Kalman)
   - Logs data to `results/trajectory_log.csv` for offline analysis

5. **Analysis Script (`results/generate_plots.py`)**
   - Reads trajectory log
   - Computes prediction error per frame
   - Generates:
     - `error_vs_frame_plot.png`
     - `measured_vs_predicted_scatter.png`
     - `error_histogram.png`

---

## 📂 Repository Structure

```text
.
├── data/
│   └── video.mp4                 
├── src/
│   ├── detector.py               
│   ├── optical_flow_tracker.py  
│   ├── kalman_filter.py         
│   └── run_tracking.py          
├── results/
│   ├── kalman_tracking_*.jpg    
│   ├── trajectory_log.csv      
│   ├── generate_plots.py       
│   ├── measured_vs_predicted_scatter.png
│   └── error_histogram.png
└── report.tex                    