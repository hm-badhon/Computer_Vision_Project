import cv2
import numpy as np
from scipy.ndimage import gaussian_filter
from time import time

def compute_heart_rate(frame_intensities, frame_timings):
    """
    Computes the heart rate based on the intensities and timings of the frames.
    """
    # Compute the differences in intensities
    dx = np.diff(frame_intensities)

    # Find the longest sequence of small differences
    max_seq_len, max_seq = 0, None
    seq_start, seq_end = -1, -1
    hb_idx = []  # Initialize hb_idx
    for i in range(20, len(dx)):
        if np.max(dx[i - 20: i]) < 5:
            if seq_start == -1:
                seq_start = i
            seq_end = i
        else:
            if seq_end != -1:
                seq_len = seq_end - seq_start
                if seq_len > max_seq_len:
                    max_seq = (seq_start, seq_end)
                    max_seq_len = seq_len
                seq_start, seq_end = -1, -1
        if i >= len(dx) - 1:
            max_seq = (seq_start, seq_end)
            max_seq_len = seq_end - seq_start

    # Check if the data is valid
    if max_seq_len == 0:
        print("Bad data...")
        return 0

    # Filter and differentiate the sequence of interest
    heart_peaks = frame_intensities[max_seq[0]: max_seq[1]]
    smoothed_peaks = gaussian_filter(heart_peaks, sigma=5)
    sp_dx = np.diff(smoothed_peaks)

    # Find the indices of the heartbeats
    hb_idx = [i + max_seq[0] for i in range(len(sp_dx) - 1) if sp_dx[i] >= 0 and sp_dx[i+1] < 0]

    # Check if the data is valid
    if len(hb_idx) < 5:
        print("Bad data...")
        return 0

    # Compute the heart rate
    total_time = frame_timings[hb_idx[-1]] - frame_timings[hb_idx[0]]
    heart_rate = ((len(hb_idx)- 1) / total_time) * 60
    print(f"Heart rate: {heart_rate}")

    return heart_rate  # Return the computed heart rate

def main():
    """
    Captures video from the camera and computes the heart rate.
    """
    camera_index = 0
    cap = cv2.VideoCapture(camera_index)
    if not cap.isOpened():
        print("Error: Could not open camera.")
        return

    # Buffer for storing frames and frame timings
    frame_intensities, frame_timings, frame_count = [], [], 0

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error: Could not read frame.")
            break

        # Convert the frame to grayscale and compute its mean intensity
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        frame_intensities.append(np.mean(gray_frame))
        frame_timings.append(time())

        # Keep only the most recent 500 frames
        if len(frame_intensities) > 500:
            frame_intensities.pop(0)
            frame_timings.pop(0)

        # Compute heart rate every 100 frames
        if len(frame_intensities) >= 100 and frame_count % 100 == 0:
            frame_count = 0
            heart_rate = compute_heart_rate(frame_intensities, frame_timings)
            # Draw bounding box in green color and add text
            x, y, w, h = 100, 100, 200, 200  # Example coordinates, replace with your detection results
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.putText(frame, f"Heart Rate: {heart_rate:.2f}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)

            # Display the video stream
            cv2.imshow("Video", frame)

        # Break the loop if 'q' key is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        frame_count += 1

    # Release the camera and close the OpenCV windows
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
