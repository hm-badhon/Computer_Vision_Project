import cv2
import numpy as np

known_distance = 76.2
known_width = 14.3
cap = cv2.VideoCapture(0)

face_detector = cv2.CascadeClassifier("model/haarcascade_frontalface_default.xml")
def focal_length(measured_distance,real_width,width_in_ref_img):
    focal_length =  (width_in_ref_img * measured_distance) / real_width
    return focal_length

def find_distance(focal_length,real_width,face_width_in_frame):
    distance = (real_width * focal_length) / face_width_in_frame
    return distance

def face_data(img):
    gray_img = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    faces = face_detector.detectMultiScale(gray_img,1.3,5)
    face_width = 0
    for (x,y,h,w) in faces:
        cv2.rectangle(img, (x,y),(x+w,y+h),(0,255,0),3)
        face_width = w
    return  face_width


ref_img = cv2.imread("images/Me.jpg")
#cv2.imshow("Ref Img",ref_img)
width_of_ref_img = face_data(ref_img)
focal_length_found = focal_length(known_distance,known_width,width_of_ref_img)
print(focal_length_found)



while (1):
    ret, frame = cap.read()
    face_width_in_frame = face_data(frame)
    if face_width_in_frame != 0:
        distance = find_distance(focal_length_found,known_width,face_width_in_frame)
        cv2.putText(frame,f"Distance: {round(distance,2)} C.M",(50,50),cv2.FONT_HERSHEY_SIMPLEX,1,(255,0,0),3)

    cv2.imshow("Frame",frame)
    if cv2.waitKey(1) & 0xff == ord("q"):
        break


cap.release()
cv2.destroyAllWindows()





