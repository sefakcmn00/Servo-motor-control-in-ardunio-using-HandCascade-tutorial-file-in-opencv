import cv2
from cvzone.HandTrackingModule import HandDetector
import numpy as np
import pyfirmata

cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)

detector = HandDetector(detectionCon=0.8, maxHands=1)

minHand, maxHand = 20, 250
minBar, maxBar = 400, 150
minAngle, maxAngle = 0, 180

port = "COM5"
board = pyfirmata.Arduino(port)
servoPin = board.get_pin('d:5:s') # pin 5 Arduino


while True:
    success, img = cap.read()
    hands, img = detector.findHands(img)

    if hands:
        thumbTip = hands[0]["lmList"][4][0:2]
        indexTip = hands[0]["lmList"][8][0:2]

        length, _, _ = detector.findDistance(indexTip, thumbTip, img)
        print(int(length))

        servoVal = np.interp(length, [minHand, maxHand], [minAngle, maxAngle])
        print(int(servoVal))

        cv2.rectangle(img, (100,100), (360, 30), (255, 0, 0), cv2.FILLED)
        cv2.putText(img, f'Length: {int(length)}', (130, 70), cv2.FONT_HERSHEY_PLAIN, 2,
                    (0, 255, 255), 3)

        cv2.rectangle(img, (500, 100), (760, 30), (0, 255, 255), cv2.FILLED)
        cv2.putText(img, f'Servo: {int(servoVal)}', (530, 70), cv2.FONT_HERSHEY_PLAIN, 2,
                        (255, 0, 0), 3)

        bar = np.interp(length, [minHand, maxHand], [minBar, maxBar])
        cv2.rectangle(img, (1180, 150), (1215, 400), (255, 0, 0), 3)
        cv2.rectangle(img, (1180, int(bar)), (1215, 400), (0, 255, 0), cv2.FILLED)

        servoPin.write(servoVal)

    cv2.imshow("Image", img)
    cv2.waitKey(1)