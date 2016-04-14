import cv2
import numpy as np
import pygame
cap = cv2.VideoCapture(0)
screen = pygame.display.set_mode((620, 480))
while True:
    screen.fill((0,0,0))
    _, frame = cap.read()
    #hue saturation value
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    #M = cv2.getRotationMatrix2D((400, 400), 180, 1.0)
    #hsv = cv2.warpAffine(hsv, M, (w, h))
    #cv2.flip(hsv, 1, hsv)
    lower_pink = np.array([10,150,0])
    upper_pink = np.array([30,255,255])

    mask = cv2.inRange(hsv, lower_pink, upper_pink)

    kernal = np.ones((15, 15), np.float32)/225
    opening = cv2.morphologyEx(mask,cv2.MORPH_OPEN, kernal)
    cnts = cv2.findContours(opening.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
    center = None
    if len(cnts) > 0:
        c = max(cnts, key=cv2.contourArea)
        ((x,y), radius) = cv2.minEnclosingCircle(c)
        M = cv2.moments(c)

        if radius > 10:
            pygame.draw.circle(screen, (255, 0, 0), (int(x), int(y)), 10)
            print(x,y)

    cv2.imshow('frame', frame)
    pygame.display.update()
    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break


cv2.destroyAllWindows()
cv2.release()