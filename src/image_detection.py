import cv2
import numpy as np
import pygame


def start():
    cap = cv2.VideoCapture(0)
    while True:
        _, frame = cap.read()
        #hue saturation value
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        lower_pink = np.array([10, 150, 100])
        upper_pink = np.array([30, 255, 255])

        mask = cv2.inRange(hsv, lower_pink, upper_pink)

        kernal = np.ones((15, 15), np.float32)/225
        opening = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernal)
        cnts = cv2.findContours(opening.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
        center = None
        if len(cnts) > 0:
            c = max(cnts, key=cv2.contourArea)
            ((x,y), radius) = cv2.minEnclosingCircle(c)
            M = cv2.moments(c)

            if radius > 10:
                cv2.circle(frame, (int(x), int(y)), int(radius), (0, 255, 255), 2)
                cv2.circle(frame, (int(x), int(y)), 1, (0, 255, 255), -1)

        cv2.imshow('frame', frame)
        cv2.imshow('mask', mask)
        k = cv2.waitKey(5) & 0xFF
        if k == 27:
            break

    cv2.destroyAllWindows()
    cap.release()
