import numpy as np

class CentroidTracker:
    def __init__(self, smoothing=5):
        self.trajectory = []
        self.smoothing = smoothing

    def update(self, bbox):
        if bbox is None:
            self.trajectory.append(None)
            return None
        
        x, y, w, h = bbox
        cx = int(x + w / 2)
        cy = int(y + h / 2)

        if len(self.trajectory) > 0 and self.trajectory[-1] is not None:
            prev = self.trajectory[-1]
            cx = int((cx + prev[0] * self.smoothing) / (self.smoothing + 1))
            cy = int((cy + prev[1] * self.smoothing) / (self.smoothing + 1))

        self.trajectory.append((cx, cy))
        return (cx, cy)
