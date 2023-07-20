import cv2
import mediapipe as mp

# Set up the MediaPipe and OpenCV components:
mp_drawing = mp.solutions.drawing_utils
mp_face_mesh = mp.solutions.face_mesh


# Initialize the MediaPipe Face Mesh and configure the drawing options:
face_mesh = mp_face_mesh.FaceMesh(static_image_mode = False, max_num_faces = 1, min_detection_confidence =0.5, min_tracking_confidence =0.5)
drawing_spec = mp_drawing.DrawingSpec(thickness =1, circle_radius =1)


# Capture the video stream using OpenCV:

cap = cv2.VideoCapture(0)
while cap.isOpened():
    ret, frame = cap.read()
    if not ret :
        break

    # Convert the image to RGB for MediaPipe
    image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)


    # Process the frame with  MediaPipe Face Mesh

    results = face_mesh.process(image_rgb)

    # Check if any face is detected
    if results.multi_face_landmarks:
        # Initialize variables to track the minimum and maximum coordinates

        min_x = frame.shape[1]
        min_y = frame.shape[0]
        max_x = 0
        max_y = 0
        for face_landmarks in results.multi_face_landmarks:
            # Iterate over the facial landmarks and draw them on the frame
            for idx, landmark in enumerate(face_landmarks.landmark):
                cx, cy = int(landmark.x * frame.shape[1]), int(landmark.y * frame.shape[0])

                # Update the minimum and maximum coordinates
                min_x = min(min_x, cx)
                min_y = min(min_y, cy)
                max_x = max(max_x, cx)
                max_y = max(max_y, cy)

                # Draw a small circle at each landmark position
                cv2.circle(frame, (cx, cy), 1, (0, 255, 0), 1)

            # Calculate the center point
            center_x = (min_x + max_x) // 2
            center_y = (min_y + max_y) // 2
            print("Center point : ", center_x, center_y)

            # Draw a larger circle at the center point
            cv2.circle(frame, (center_x, center_y), 5, (0, 0, 255), -1)

    cv2.imshow('Head Pose Estimation', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()
