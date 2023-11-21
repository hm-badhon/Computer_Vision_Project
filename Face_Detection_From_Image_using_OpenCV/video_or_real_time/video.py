import cv2

# Load the cascade classifier
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')


# Detection from video

# if you want to detect from file
# capture = cv2.VideoCapture("a.mpv4")

#for real time

capture = cv2.VideoCapture(0)

while True:
    _, img = capture.read()



    # Convert the image to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Detect faces in the image
    faces = face_cascade.detectMultiScale(gray, 1.1, 4)

    # Draw a rectangle around the faces
    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)

    # Show the output
    cv2.imshow('img',img)

    k = cv2.waitKey(30) & 0xff
    if k ==27:
        break
capture.release()