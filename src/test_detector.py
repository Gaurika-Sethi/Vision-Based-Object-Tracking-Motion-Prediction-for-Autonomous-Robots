import cv2
from detector import detect_person

video = cv2.VideoCapture("data/video.mp4")

print("Loaded:", video.isOpened())
frame_count = 0


while True:
    ret, frame = video.read()
    if not ret:
        break

    bbox, output, mask = detect_person(frame)

    if frame_count % 20 == 0:
        cv2.imwrite(f"./results/frame_{frame_count}.jpg", output)
        cv2.imwrite(f"./results/mask_{frame_count}.jpg", mask)


    frame_count += 1

video.release()