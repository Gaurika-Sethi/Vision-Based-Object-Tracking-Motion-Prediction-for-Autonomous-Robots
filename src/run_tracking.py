import cv2
import glob
import os

from detector import detect_person
from optical_flow_tracker import OpticalFlowTracker
from kalman_filter import KalmanPredictor

for f in glob.glob("./results/*.jpg"):
    os.remove(f)

video = cv2.VideoCapture("data/self_recorded_video.mp4")
print("Loaded:", video.isOpened())

flow_tracker = OpticalFlowTracker()
kalman = KalmanPredictor()
frame_count = 0

while True:
    ret, frame = video.read()
    if not ret:
        break

    bbox, output, mask = detect_person(frame)

    measured = None
    if bbox is not None:
        measured = flow_tracker.update(frame, bbox)   

    if measured is None:
        frame_count += 1
        continue

    pred = kalman.update(measured)

    with open("./results/trajectory_log.csv", "a") as f:
        mx, my = measured
        px, py = pred
        f.write(f"{frame_count},{mx},{my},{px},{py}\n")

    if len(flow_tracker.trajectory) > 1:
        for i in range(1, len(flow_tracker.trajectory)):
            p1 = flow_tracker.trajectory[i - 1]
            p2 = flow_tracker.trajectory[i]
            if p1 is None or p2 is None:
                continue
            cv2.line(output, p1, p2, (0, 0, 255), 2)

    if len(kalman.pred_traj) > 1:
        for i in range(1, len(kalman.pred_traj)):
            p1 = kalman.pred_traj[i - 1]
            p2 = kalman.pred_traj[i]
            if p1 is None or p2 is None:
                continue
            
    if frame_count % 20 == 0:
        cv2.imwrite(f"./results/kalman_tracking_{frame_count}.jpg", output)

    frame_count += 1

video.release()
print("Done.")