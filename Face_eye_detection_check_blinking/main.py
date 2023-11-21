'''
Face eye blinking using Dlib  and detect left or right eye blinking.
check sleep, drowsy, active 
'''

import cv2
import dlib
import numpy as np
from imutils import face_utils

def eye_aspect_ratio(eye):
    # compute the euclidean distances between the two sets of
    # vertical eye landmarks (x, y)-coordinates
    A = np.linalg.norm(eye[1] - eye[5])
    B = np.linalg.norm(eye[2] - eye[4])
    # compute the euclidean distance between the horizontal
    # eye landmark (x, y)-coordinates
    C = np.linalg.norm(eye[0] - eye[3])
    # compute the eye aspect ratio
    ear = (A + B) / (2.0 * C)
    # return the eye aspect ratio
    return ear
def draw_facial_landmarks(frame, landmarks):
    for (x, y) in landmarks:
        cv2.circle(frame, (x, y), 2, (0, 255, 0), -1)
def eye_blinking_detection(shape_detector, face_detector,blink_threshold=0.3):

    cap = cv2.VideoCapture(0)
    while True:
        ret, frame = cap.read()
        if ret == True:
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = face_detector(gray)
            for face in faces:
                landmarks = shape_detector(gray, face)
                landmarks = face_utils.shape_to_np(landmarks)
                left_eye = landmarks[36:42]
                right_eye = landmarks[42:48]
                left_eye_hull = cv2.convexHull(left_eye)
                right_eye_hull = cv2.convexHull(right_eye)
                cv2.drawContours(frame, [left_eye_hull], -1, (0, 0, 255), 1)
                cv2.drawContours(frame, [right_eye_hull], -1, (0, 0, 255), 1)
                left_eye_ratio = eye_aspect_ratio(left_eye)
                right_eye_ratio = eye_aspect_ratio(right_eye)

                print('left_eye_ratio: ',left_eye_ratio,'\t right_eye_ratio: ',right_eye_ratio)
 
                draw_facial_landmarks(frame, landmarks)
                
                # check left and right eye blinking
 
                if left_eye_ratio < blink_threshold and right_eye_ratio < blink_threshold:
                    cv2.putText(frame, "Both Eye Blinking and sleeping", (10, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
                elif left_eye_ratio < blink_threshold:
                    cv2.putText(frame, "Left Eye Blinking", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
                elif right_eye_ratio < blink_threshold:
                    cv2.putText(frame, "Right Eye Blinking", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
                else:
                    cv2.putText(frame, "Active", (10, 120), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
            cv2.imshow('frame', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        else:
            break
    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    face_landmark_path='shape_predictor_68_face_landmarks.dat'
    shape_detector = dlib.shape_predictor(face_landmark_path)
    face_detector = dlib.get_frontal_face_detector()
    blink_threshold=0.2
    eye_blinking_detection(shape_detector, face_detector,blink_threshold)