import cv2


video_path = 'video/a.mp4'

cap = cv2.VideoCapture(video_path)

frame_rate = 20  # Extract one frame per second
frame_count = 0

while True:
    ret, frame = cap.read()

    if not ret:
        break
    if frame_count % frame_rate == 0:
        frame_filename = f'frame_{frame_count}.jpg'
        cv2.imwrite(frame_filename, frame)

    frame_count += 1

cap.release()
# cv2.destroyAllWindows()
