import cv2 #OpenCV-Python is a library of Python designed to solve computer vision problems.
import numpy as np #NumPy is a Python library used for working with arrays.
import HandTrackingModule as htm
import time #for delaying the script
import pyautogui #PyAutoGUI is a Python automation library used to click, drag, scroll, move, etc. It can be used to click at an exact position

######################
wCam, hCam = 640, 480 #setting width and height of the video
frameR = 100     #Frame Reduction
smoothening = 7  #random value
######################

pTime = 0
plocX, plocY = 0, 0
clocX, clocY = 0, 0
cap = cv2.VideoCapture(1) #Start video capture usingout builtin camera which is 0. we can set one or anyother values for other devices
cap.set(3, wCam)#setting the width and height, 3 is the prop id for width
cap.set(4, hCam)

detector = htm.handDetector(maxHands=1) #creating object and specifying that we need one maximum hand detecting
wScr, hScr = pyautogui.size()

# print(wScr, hScr)

while True:
    # Step1: Find the landmarks
    success, img = cap.read()
    img = detector.findHands(img)
    lmList, bbox = detector.findPosition(img) # detects and and also draws

    # Step2: Get the tip of  the index and middle finger
    if len(lmList) != 0:
        x1, y1 = lmList[8][1:]
        x2, y2 = lmList[12][1:]

        # Step3: Check which fingers are up
        fingers = detector.fingersUp()
        cv2.rectangle(img, (frameR, frameR), (wCam - frameR, hCam - frameR),
                      (255, 0, 255), 2)

        # Step4: Only Index Finger: Moving Mode
        if fingers[1] == 1 and fingers[2] == 0: # this is Wine index finger is up in the middle finger is down

            # Step5: Convert the coordinates because screen w and h is diff from the video w and h
            x3 = np.interp(x1, (frameR, wCam-frameR), (0, wScr))# converting from range to another range. The first range is from 02 with of the camera and the second range is 0 to the width of the screen
            y3 = np.interp(y1, (frameR, hCam-frameR), (0, hScr))

            # Step6: Smooth Values so the mouse isnt very jittery while operating
            clocX = plocX + (x3 - plocX) / smoothening
            clocY = plocY + (y3 - plocY) / smoothening

            # Step7: Move Mouse
            pyautogui.moveTo(wScr - clocX, clocY) #inverting the mouse movement on the x axis using wscr - clocx
            cv2.circle(img, (x1, y1), 15, (255, 0, 255), cv2.FILLED)
            plocX, plocY = clocX, clocY

        # Step8: Both Index and middle are up: Clicking Mode
        if fingers[1] == 1 and fingers[2] == 1 and fingers[3] == 0:

            # Step9: Find distance between fingers
            length, img, lineInfo = detector.findDistance(8, 12, img)

            # Step10: Click mouse if distance short
            if length < 25:
                cv2.circle(img, (lineInfo[4], lineInfo[5]), 15, (0, 255, 0), cv2.FILLED)
                pyautogui.click()
                
        if fingers[1] == 1 and fingers[2] == 1 and fingers[3] == 1:
            
            
            
            """
            if length < 40:
                lenght, img, lineInfo = detector.findDistance(8, 16, img)
                if lenght < 40:
                    cv2.circle(img, (lineInfo[4], lineInfo[5]), 15, (0, 255, 0), cv2.FILLED)
                    pyautogui.click(button = 'right')
            """
            lenght, img, lineInfo = detector.findDistance(8, 12, img)
            lenghtTaI = lenght
            lenght, img, lineInfo = detector.findDistance(8, 16, img)
            lenghtIaM = lenght
            
            if lenghtTaI < 40 and lenghtIaM < 40:
                cv2.circle(img, (lineInfo[4], lineInfo[5]), 15, (0, 255, 0), cv2.FILLED)
                pyautogui.click(button = 'right')

    # Step11: Frame rate
    cTime = time.time() #current time
    fps = 1/(cTime-pTime)
    pTime = cTime
    cv2.putText(img, str(int(fps)), (28, 58), cv2.FONT_HERSHEY_PLAIN, 3, (255, 8, 8), 3)#postion, fonts, thickness, color

    # Step12: Display
    cv2.imshow("Image", img)
    cv2.waitKey(1)
