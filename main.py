import cv2
from cvzone.HandTrackingModule import HandDetector
import math
import numpy as np
import cvzone


#Webcam
cap = cv2.VideoCapture(0)
# cambiar la resolucion a preferencia
cap.set(3, 800)
cap.set(4, 600)
# detector de manos
detector = HandDetector(detectionCon=0.8, maxHands=1)

# funcion
# y es la distancia en cm
#x = [300, 245, 200, 170, 145, 130, 112, 103, 93, 87, 80, 75, 70, 67, 62, 59, 57]
#y = [20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90, 95, 100]

x = [185, 134, 99, 94, 87, 79, 63]
y = [20, 25, 30, 35, 40 , 45, 50]
coff = np.polyfit(x, y, 2) # y = Ax^2 + Bx + C

while True:
    success, img = cap.read()
    hands = detector.findHands(img, draw=False)

    if hands:
        lmList = hands[0]['lmList']
        x, y, w, h = hands[0]['bbox']
        x1, y1 = lmList[5]
        x2, y2 = lmList[17]

        distance = int(math.sqrt((y2 - y1) ** 2 + (x2 - x1) ** 2))

        A, B, C = coff

        distanceCM = A * distance**2  + B*distance + C

        print(distanceCM, distance)

        cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 3)

        cvzone.putTextRect(img, f'{int(distanceCM)} cm', (x+5, y-10))


    cv2.imshow("Image", img)
    ## presionar Q para detener el programa
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


# while True :
#     success, img = cap.read()
#     img, hands = detector.findHands(img, draw=False)
#
#     print(type(hands))
#
#     if hands is not None and hands.size > 0:
#         hand = hands[0]
#         lmList = hand['lmList']
#         x, y, w , h = hand['bbox']
#         x1, y1 = lmList[5]
#         x2, y2 = lmList[17]
#
#         distance = int(math.sqrt((x1 - x1) ** 2 + (y1 - y1) ** 2))
#         A, B, C = coff
#         distanceCM = A * distance**2 + B * distance + C
#
#         print(distanceCM, distance)
#
#         cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 255), 3)
#         cvzone.putTextRect(img, f"{int(distanceCM)} cm", (x+5, y-10))
#
#     cv2.imshow("Image", img)
#     cv2.waitKey(1)