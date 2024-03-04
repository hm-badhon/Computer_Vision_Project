from cropLineDetector import *

import cv2
import numpy as np

# Insert a video path
INPUT_FILE_PATH = "/media/nsl47/hdd/AI_project/AI/Computer_vision/Crop_line_detection/crop_line_detector_cv-master/scripts/crops.mp4"

# The interpolated polynomial's degree
POLY_DEGREE = 1


def main():
    cap = cv2.VideoCapture(INPUT_FILE_PATH)
    if not cap.isOpened():
        print("Cannot open video")
        exit()
    print('im here..........')
    detector = None
    while detector is None:
        ret, image = cap.read()
        if not ret:
            continue
        else:
            detector = cropLineDetector(original_frame=image,
                                        poly_deg=POLY_DEGREE,
                                        viz_options= DRAW_LANE_AREA_MASK |
                                                    DRAW_SLIDING_WINDOW_RESULT |
                                                    DRAW_FINAL_RESULT |
                                                    DRAW_CENTER_ESTIMATIONS)

    while True:
        ret, image = cap.read()
        if not ret:
            break

        # The purpose of this whole class is to determine the heading angle error
        heading_angle_error = detector.get_heading_angle_error(image)

        # Correct using the determined angle!
        print(heading_angle_error)

        # This waits for a key press to advance for debugging purposes
        if cv2.waitKey(0) == ord('q'):
            break
    else:
        cap.release()
        cv2.destroyAllWindows()


print('im here..........')
if __name__ == '__main__':
    main()
