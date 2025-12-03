import cv2
import numpy as np

class OpticalFlowTracker:
    def __init__(self):
        self.prev_gray = None
        self.prev_points = None
        self.trajectory = []

    def update(self, frame, bbox):
        x, y, w, h = bbox
        roi = frame[y:y+h, x:x+w] 

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        if self.prev_gray is None:
            self.prev_gray = gray
            mask = np.zeros_like(frame)
            roi_gray = gray[y:y+h, x:x+w]

            pts = cv2.goodFeaturesToTrack(roi_gray, maxCorners=20, qualityLevel=0.3, minDistance=7, blockSize=7)
            if pts is not None:
                pts[:, 0, 0] += x
                pts[:, 0, 1] += y
            self.prev_points = pts
            return None

        next_points, status, _ = cv2.calcOpticalFlowPyrLK(
            self.prev_gray, gray, self.prev_points, None
        )

        good_new = next_points[status == 1]
        good_old = self.prev_points[status == 1]

        cx = int(np.mean(good_new[:, 0]))
        cy = int(np.mean(good_new[:, 1]))

        self.trajectory.append((cx, cy))

        self.prev_gray = gray
        self.prev_points = next_points

        return (cx, cy)