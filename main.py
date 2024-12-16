import cv2
from cvzone.HandTrackingModule import HandDetector
import math
import numpy as np
import cvzone


#Webcam
cap = cv2.VideoCapture(0)

# dimensiones de la ventana en pixeles se calcula en base a la webcam usada

ancho = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
alto = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

cap.set(3, ancho)
cap.set(4, alto)
# detector de manos
detector = HandDetector(detectionCon=0.8, maxHands=1)

x = [185, 134, 99, 94, 87, 79, 63]
y = [20, 25, 30, 35, 40 , 45, 50]
coff = np.polyfit(x, y, 2) # y = Ax^2 + Bx + C

# Coordenadas del centro de la pantalla
frame_center_x = ancho // 2
frame_center_y = alto // 2


# ajustar este valor si los valores de X y Y no son coherentes
FOCAL_LENGTH_PIXELS = 500

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

        hand_x, hand_y = lmList[9]


        dist_x_pixels = hand_x - frame_center_x
        dist_y_pixels = hand_y - frame_center_y

        dist_x_cm = dist_x_pixels * (distanceCM / FOCAL_LENGTH_PIXELS)
        dist_y_cm = dist_y_pixels * (distanceCM / FOCAL_LENGTH_PIXELS)

        print(distanceCM, distance, dist_x_cm, dist_y_cm)

        cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)

        cvzone.putTextRect(img, f'Z: {int(distanceCM)} cm', (x+5, y-10), 1,1)
        cvzone.putTextRect(img, f"X: {int(dist_x_cm)} cm", (x+5, y-40), 1, 1)
        cvzone.putTextRect(img, f"Y: {int(dist_y_cm)} cm", (x + 5, y-70),1, 1)

        # También puedes visualizar una línea del centro a la mano
        cv2.line(img, (frame_center_x, frame_center_y), (hand_x, hand_y), (0, 255, 0), 1)
        cv2.circle(img, (frame_center_x, frame_center_y), 5, (0, 0, 255), cv2.FILLED)  # Marca el centro


    cv2.imshow("Image", img)
    ## presionar Q para detener el programa
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

