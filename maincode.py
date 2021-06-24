import cv2
import numpy as np
import time
import os
import HandTrackingModule as htm

#######################
brushThickness = 20
eraserThickness = 40
shape=0
filled=0
drawColor = (0, 0, 0)
colorVol=(255,0,0)

########################





cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)
pTime = 0
sa=0
ca=0

detector = htm.handDetector(detectionCon=0.65,maxHands=1)
xp, yp = 0, 0
imgCanvas = np.zeros((720, 1280, 3), np.uint8)

while True:

    # 1. Import image
    success, img = cap.read()
    img = cv2.flip(img, 1)
    # setting values for base colors
    draw=np.copy(img)
    art=draw
    crop=img[50:100,70:120]


    b = crop[:, :, :1]
    g = crop[:, :, 1:2]
    r = crop[:, :, 2:]

    # computing the mean
    b_mean = np.mean(b)
    g_mean = np.mean(g)
    r_mean = np.mean(r)
    #cv2.rectangle(img, (2, 2), (50, 50), (b_mean, g_mean, r_mean), cv2.FILLED)

    # 2. Find Hand Landmarks
    img = detector.findHands(img)

    lmList = detector.findPosition(img, draw=False)


    g = 0
    x1=0
    y1=0
    if len(lmList) >= 2 and len(lmList[0])>12:

        # print(lmList)

        # tip of index and middle fingers
        x1, y1 = lmList[0][8][1:]
        x2, y2 = lmList[0][12][1:]
        drawsize=0

        # 3. Check which fingers are up
        fingers = detector.fingersUp()
        #print(fingers)

        # 4. If Selection Mode - Two finger are up

        if  fingers[2]:
            g=1

            print("Tools")
            #colors
            if y1 < 125:
                if 200 < x1 < 350:


                    drawColor = (0, 0, 255)
                    #cv2.rectangle(img, (250, 2), (450, 125), (0, 255, 0), 5)

                elif 400 < x1 < 550:


                    drawColor = (255, 59, 0)

                elif 600 < x1 < 750:

                    drawColor = (0, 255, 0)

                elif 800 < x1 < 950:
                    drawColor=(b_mean,g_mean,r_mean)

                elif 1000 < x1 < 1150:

                    drawColor = (0, 0, 0)
                elif x1>1200 and y1<80 :
                    exit("THANKS")
            #size
            if y1 > 200 and x1 > 900:

                # print(area)
                # Find Distance between index and Thumb
                length, img, lineInfo = detector.findDistance(4, 8, img)
                # print(length)

                # Convert Volume
                volBar = np.interp(length, [50, 200], [600, 350])
                volPer = np.interp(length, [50, 200], [0, 100])

                # Reduce Resolution to make it smoother
                smoothness = 2
                volPer = smoothness * round(volPer / smoothness)

                # Check fingers up
                fingers = detector.fingersUp()
                # print(fingers)

                # If pinky is down set volume
                if not fingers[4]:
                    if volPer > 0:
                        brushThickness = volPer
                        eraserThickness = volPer + 20
                        cv2.circle(img, (lineInfo[4], lineInfo[5]), 15, (0, 255, 0), cv2.FILLED)
                        colorVol = (0, 255, 0)
                else:
                    colorVol = (255, 0, 0)
                cv2.rectangle(img, (1200, 350), (1235, 600), (255, 0, 0), 3)
                cv2.rectangle(img, (1200, int(volBar)), (1235, 600), (255, 0, 0), cv2.FILLED)
                cv2.putText(img, f'{int(volPer)} %', (1180, 650), cv2.FONT_HERSHEY_COMPLEX,
                            1, (255, 0, 0), 3)
                cVol = brushThickness
                cv2.putText(img, f'Size : {int(cVol)}', (930, 300), cv2.FONT_HERSHEY_COMPLEX,
                            1, colorVol, 3)
            # shape
            if x1<300 and y1>200:
                if y1>200 and y1<300:
                    shape=1
                if y1>350 and y1<450:
                    shape=0
                if y1>500 and y1<600:
                    shape=2
            #filled
            if 750<x1<850 :
                if y1>400 and y1<500:
                    filled=1
                if y1>550 and y1<650:
                    filled=0


            #print(shape)
            # Drawings
            cv2.rectangle(img, (750, 400), (850, 500), (0, 0, 0), cv2.FILLED)
            cv2.rectangle(img, (750, 550), (850, 655), (0, 0, 0), 10)
            cv2.rectangle(img, (50, 70), (100, 120), (0, 0, 0), 2)
            cv2.putText(img, 'PICK', (43, 145), cv2.FONT_HERSHEY_COMPLEX,
                        0.8, (0, 0, 0), 2)
            cv2.rectangle(img, (x1, y1 - 25), (x2, y2 + 25), drawColor, cv2.FILLED)
            cv2.rectangle(img, (900, 200), (1250, 700), (0, 255, 0), 5)
            cv2.rectangle(img, (200, 2), (350, 125), (0, 0, 255), cv2.FILLED)
            cv2.rectangle(img, (400, 2), (550, 125), (255, 0, 0), cv2.FILLED)
            cv2.rectangle(img, (600, 2), (750, 125), (0, 255, 0), cv2.FILLED)
            cv2.rectangle(img, (800, 2), (950, 125), (b_mean,g_mean,r_mean), cv2.FILLED)
            cv2.rectangle(img, (1000, 2), (1150, 125), (0, 0, 0), cv2.FILLED)
            cv2.rectangle(img, (1200, 2), (1270, 80), (0, 0, 255), cv2.FILLED)
            cv2.rectangle(img, (2, 200), (300, 300), (20, 20, 20), cv2.FILLED)
            cv2.rectangle(img, (2, 350), (300, 450), (20, 20, 20), cv2.FILLED)
            cv2.rectangle(img, (2,500 ), (300, 600), (20, 20, 20), cv2.FILLED)
            cv2.putText(img, 'LINE', (50, 400), cv2.FONT_HERSHEY_COMPLEX,
                        1, (255, 255, 255), 2)
            cv2.putText(img, 'SQUARE', (50, 250), cv2.FONT_HERSHEY_COMPLEX,
                        1, (255, 255, 255), 2)
            cv2.putText(img, 'CIRCLE', (50, 550), cv2.FONT_HERSHEY_COMPLEX,
                        1, (255, 255, 255), 2)
            cv2.putText(img, 'Raj Aryan Srivastava', (20, 680), cv2.FONT_HERSHEY_COMPLEX_SMALL,
                        1, (0, 255, 255), 2)
            cv2.putText(img, 'ERASER', (1020, 70), cv2.FONT_HERSHEY_PLAIN,
                        1.5, (255, 255, 255), 2)
            cv2.putText(img, 'CUST0M', (820, 70), cv2.FONT_HERSHEY_PLAIN,
                        1.5, (80, 127, 255 ), 2)
            cv2.putText(img, 'EXIT', (1200, 40), cv2.FONT_HERSHEY_COMPLEX,
                        1, (0, 0, 0), 2)

            if shape == 1:
                cv2.rectangle(img, (2, 200), (300, 300), (0, 255, 0), 7)
            elif shape == 0:
                cv2.rectangle(img, (2, 350), (300, 450), (0, 255, 0), 7)
            elif shape==2:
                cv2.rectangle(img, (2, 500), (300, 600), (0, 255, 0), 7)
            if filled == 1:
                cv2.rectangle(img, (750, 400), (850, 500), (0, 255, 0), 7)
            elif filled == 0:
                cv2.rectangle(img, (750, 550), (850, 655), (0, 255, 0), 7)

            if not (x1>900 and y1>200) :
                cv2.putText(img, 'Change Size', (920, 300), cv2.FONT_HERSHEY_COMPLEX,
                            1, (0, 255, 0), 3)

        # 5. If Drawing Mode - Index finger is up
        if fingers[1] and not fingers[2] :

            g=0
            #cv2.circle(imgCanvas, (x1, y1), brushThickness, drawColor, cv2.FILLED)
            print("Drawing Pad")
            if shape==1:
                if fingers[0] != 0:
                    if filled==0:
                        cv2.rectangle(draw, (x1-brushThickness*10, y1-brushThickness*10), (x1+brushThickness*10, y1+brushThickness*10), drawColor, brushThickness)
                        cv2.rectangle(imgCanvas,(x1-brushThickness*10, y1-brushThickness*10), (x1+brushThickness*10, y1+brushThickness*10),drawColor, brushThickness)
                    else:
                        cv2.rectangle(draw, (x1 - brushThickness * 10, y1 - brushThickness * 10),
                                      (x1 + brushThickness * 10, y1 + brushThickness * 10), drawColor, cv2.FILLED)
                        cv2.rectangle(imgCanvas, (x1 - brushThickness * 10, y1 - brushThickness * 10),
                                      (x1 + brushThickness * 10, y1 + brushThickness * 10), drawColor, cv2.FILLED)

            if shape==2:
                if fingers[0] != 0:
                    if filled==0:
                        cv2.circle(draw, (x1, y1), brushThickness*5, drawColor, brushThickness)
                        cv2.circle(imgCanvas,(x1, y1), brushThickness*5,drawColor, brushThickness)
                    else:
                        cv2.circle(draw, (x1, y1),brushThickness*5
                                      , drawColor, cv2.FILLED)
                        cv2.circle(imgCanvas, (x1, y1),
                                      brushThickness*5, drawColor, cv2.FILLED)

            if shape==0:
                if xp == 0 and yp == 0:
                    xp, yp = x1, y1

                    # cv2.line(imgCanvas, (xp, yp), (x1, y1), drawColor, brushThickness)
                if fingers[0] != 0:
                    if drawColor == (0, 0, 0):
                        cv2.line(img, (xp, yp), (x1, y1), drawColor, eraserThickness)
                        cv2.line(imgCanvas, (xp, yp), (x1, y1), drawColor, eraserThickness)


                    else:
                        cv2.line(img, (xp, yp), (x1, y1), drawColor, brushThickness)
                        cv2.line(imgCanvas, (xp, yp), (x1, y1), drawColor, brushThickness)

                xp, yp = x1, y1
            if x1>1100 and y1<80:
                imgCanvas = np.zeros((720, 1280, 3), np.uint8)
            if x1 > 1100 and 100 <y1< 180:

                sa=1
                cv2.rectangle(draw, (1100, 100), (1260, 180), (0, 0, 0), cv2.FILLED)
                cv2.putText(draw, 'SAVED', (1115, 140), cv2.FONT_HERSHEY_COMPLEX,
                            1, (0, 255, 0), 4)
            if x1>1100 and 200<y1<280:
                ca=1
            else:
                ca=0
            #drawings
            cv2.rectangle(draw, (1100, 2), (1260, 80), (0, 0, 0), cv2.FILLED)
            cv2.putText(draw, 'NEW', (1125, 40), cv2.FONT_HERSHEY_COMPLEX,
                        1, (255, 255, 255), 2)
            cv2.rectangle(draw, (1100, 200), (1260, 280), (0, 0, 0), cv2.FILLED)
            cv2.putText(draw, 'CANVAS', (1115, 240), cv2.FONT_HERSHEY_COMPLEX,
                        1, (255, 255, 255), 2)

            if not(x1 > 1100 and 100 <y1< 180):
                cv2.rectangle(draw, (1100, 100), (1260, 180), (0, 0, 0), cv2.FILLED)
                cv2.putText(draw, 'SAVE', (1115, 140), cv2.FONT_HERSHEY_COMPLEX,
                            1, (255, 255, 255), 2)
            if shape==1:
                if filled==0:
                    cv2.rectangle(draw, (30, 30), (70, 70), (0, 0, 0), 2)
                else:
                    cv2.rectangle(draw, (30, 30), (70, 70), (0, 0, 0), cv2.FILLED)
            if shape==2:
                if filled==0:
                    cv2.circle(draw, (50, 50), 20, (0, 0, 0), 2)
                else:
                    cv2.circle(draw, (50,50), 20, (0, 0, 0), cv2.FILLED)
            if shape==0:
                cv2.line(draw,(25,25),(75,75),(0,0,0),2)

            cv2.rectangle(draw,(20,20),(80,80),(0,0,0),2)
            cv2.rectangle(draw, (20, 100), (80, 160), drawColor, cv2.FILLED)

            cv2.rectangle(draw, (20, 100), (80, 160), (0, 0, 0), 2)
            cv2.rectangle(draw, (20, 180), (80, 240), (0, 0, 0), 2)
            cv2.putText(draw, f'{int(brushThickness)}', (30, 220), cv2.FONT_HERSHEY_COMPLEX,
                        1, (0,0,0), 2)





        # # Clear Canvas when all fingers are up
        #if all(x >= 1 for x in fingers):



    imgGray = cv2.cvtColor(imgCanvas, cv2.COLOR_BGR2GRAY)
    _, imgInv = cv2.threshold(imgGray, 50, 255, cv2.THRESH_BINARY_INV)
    imgInv = cv2.cvtColor(imgInv, cv2.COLOR_GRAY2BGR)
    draw = cv2.bitwise_and(draw, imgInv)
    draw = cv2.bitwise_or(draw, imgCanvas)


    # img = cv2.addWeighted(img,0.5,imgCanvas,0.5,0)
    # Frame rate
    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    cv2.putText(img, f'FPS: {int(fps)}', (40, 50), cv2.FONT_HERSHEY_COMPLEX,
                1, (255, 0, 0), 3)
    cv2.circle(draw,(x1,y1),5,(0,0,0),5)

    if sa==1:
        cv2.imwrite('AI-Painter.jpeg', draw)
        cv2.imwrite('AI-Painter(1).jpeg', imgCanvas)
    sa=0
    #cv2.imshow("Canvas", imgCanvas)
    #cv2.imshow("Inv", imgInv)
    if ca==1:
        cv2.imshow("Canvas", imgCanvas)
    else:
        cv2.destroyWindow("Canvas")

    if g==0:

        cv2.imshow("Image", draw)
        cv2.destroyWindow("Drawing pad")

    else:

        cv2.imshow("Drawing pad",img)
        cv2.destroyWindow("Image")

    cv2.waitKey(1)