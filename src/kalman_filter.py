import numpy as np
import cv2
class KalmanPredictor:
    def __init__(self, R_value=20.0):
        self.kf = cv2.KalmanFilter(4, 2)

        self.kf.transitionMatrix = np.array([
            [1, 0, 1, 0],
            [0, 1, 0, 1],
            [0, 0, 1, 0],
            [0, 0, 0, 1]
        ], np.float32)

        self.kf.measurementMatrix = np.array([
            [1, 0, 0, 0],
            [0, 1, 0, 0]
        ], np.float32)

        self.kf.processNoiseCov = np.eye(4, dtype=np.float32) * 1e-3
        self.kf.measurementNoiseCov = np.eye(2, dtype=np.float32) * R_value

        self.initialized = False
        self.pred_traj = []
        self.meas_traj = []

    def update(self, meas):
        """
        meas: (mx, my) from optical flow tracker.
        Returns predicted (px, py) for visualization.
        """
        if meas is None:
            if not self.initialized:
                self.pred_traj.append(None)
                self.meas_traj.append(None)
                return None

            prediction = self.kf.predict()
            px, py = int(prediction[0]), int(prediction[1])
            self.pred_traj.append((px, py))
            self.meas_traj.append(None)
            return (px, py)

        mx, my = meas

        if not self.initialized:
            self.kf.statePost = np.array([[mx], [my], [0], [0]], np.float32)
            self.initialized = True
            self.pred_traj.append((mx, my))
            self.meas_traj.append((mx, my))
            return (mx, my)

        self.kf.predict()
        meas_pt = np.array([[np.float32(mx)], [np.float32(my)]])
        corrected = self.kf.correct(meas_pt)

        cx = float(corrected[0])
        cy = float(corrected[1])
        vx = float(corrected[2])
        vy = float(corrected[3])

        fx = int(cx + vx * 2)
        fy = int(cy + vy * 2)

        self.pred_traj.append((fx, fy))
        self.meas_traj.append((mx, my))
        return (fx, fy)