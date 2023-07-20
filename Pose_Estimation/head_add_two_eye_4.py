import cv2
import mediapipe as mp

mp_drawing = mp.solutions.drawing_utils
mp_face_mesh = mp.solutions.face_mesh

face_mesh = mp_face_mesh.FaceMesh(static_image_mode=False, max_num_faces=1, min_detection_confidence=0.5, min_tracking_confidence=0.5)
drawing_spec = mp_drawing.DrawingSpec(thickness=1, circle_radius=1)

cap = cv2.VideoCapture(0)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = face_mesh.process(image_rgb)

    if results.multi_face_landmarks:
        for face_landmarks in results.multi_face_landmarks:
            # Draw landmarks
            mp_drawing.draw_landmarks(frame, face_landmarks, mp_face_mesh.FACEMESH_TESSELATION, drawing_spec, drawing_spec)

            # Extract left and right eye landmarks
            left_eye_landmarks = face_landmarks.landmark[249:269]
            right_eye_landmarks = face_landmarks.landmark[390:410]

            # Draw lines for the left eye
            for i in range(len(left_eye_landmarks) - 1):
                cv2.line(frame, (int(left_eye_landmarks[i].x * frame.shape[1]), int(left_eye_landmarks[i].y * frame.shape[0])),
                         (int(left_eye_landmarks[i+1].x * frame.shape[1]), int(left_eye_landmarks[i+1].y * frame.shape[0])),
                         (0, 0, 255), 1)

            # Draw lines for the right eye
            for i in range(len(right_eye_landmarks) - 1):
                cv2.line(frame, (int(right_eye_landmarks[i].x * frame.shape[1]), int(right_eye_landmarks[i].y * frame.shape[0])),
                         (int(right_eye_landmarks[i+1].x * frame.shape[1]), int(right_eye_landmarks[i+1].y * frame.shape[0])),
                         (0, 45, 255), 1)

    cv2.imshow('Eye Detection', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
