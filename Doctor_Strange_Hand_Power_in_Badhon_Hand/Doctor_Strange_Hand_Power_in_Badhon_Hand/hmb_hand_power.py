##################### Doctor Strange Shield Effect ###########################
########--------------Created by HMB-----------------###########


## pip install opencv-python, cvzone, numpy ##

import math
import cv2
from cvzone.HandTrackingModule import HandDetector
print("Made by H.M.Badhon")


detector = HandDetector()


cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
shield = cv2.VideoCapture("shield.mp4")


def mapFromTo(x,a,b,c,d):
    return (x-a)/(b-a)*(d-c)+c

def Overlay (background, overlay, x, y, size):
    background_h, background_w, c = background.shape
    imgScale = mapFromTo(size, 200, 20, 1.5, 0.2)
    overlay = cv2.resize(overlay, (0, 0), fx=imgScale, fy=imgScale)
    h, w, c = overlay.shape
    try:
        if x + w/2 >= background_w or y + h/2 >= background_h or x - w/2 <= 0 or y - h/2 <= 0:
            return background
        else:
            overlayImage = overlay[..., :3]
            mask = overlay / 255.0
            background[int(y-h/2):int(y+h/2), int(x-w/2):int(x+w/2)] = (1-mask)*background[int(y-h/2):int(y+h/2), int(x-w/2):int(x+w/2)] + overlay
            return background
    except:
        return background

def findDistance(point1, point2):
    return math.sqrt((point1[0] - point2[0])**2 + (point1[1] - point2[1])**2)

showShield = True
changeTimer = 0

while True:
    success, img = cap.read()
    hands = detector.findHands(img, False)
    final = img
    if hands:
        success, shieldImage = shield.read()
        if not success:
            shield.set(cv2.CAP_PROP_POS_FRAMES, 0)
            success, shieldImage = shield.read()

    if len(hands) == 2:
        changeTimer += 1
        if findDistance(hands[0]["lmList"][9], hands[1]["lmList"][9]) < 30:
            if changeTimer > 100:
                if showShield == False:
                    showShield = True
                    changeTimer = 0
                else:
                    showShield = False
                    changeTimer = 0
        if showShield:
            for hand in hands:
                bbox = hand["bbox"]
                handSize = bbox[2]
                cx, cy = hand["center"]
                if 1 in detector.fingersUp(hand):
                    final = Overlay(img, shieldImage, cx, cy, handSize)

    elif len(hands) == 1:
        for hand in hands:
            bbox = hand["bbox"]
            handSize = bbox[2]
            cx, cy = hand["center"]
            if 1 in detector.fingersUp(hand):
                final = Overlay(img, shieldImage, cx, cy, handSize)
    cv2.imshow("Doctor Strange", cv2.flip(final, 1))
    cv2.waitKey(2)