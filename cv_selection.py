import os

import cv2
from cvzone.HandTrackingModule import HandDetector


cap = cv2.VideoCapture(1)
cap.set(3,640)
cap.set(4,480)

#import background image
imgBackground = cv2.imread("Resources/Background.png")
#import mode images into list
folderPathModes = "Resources/Modes"
listImgModesPath = os.listdir(folderPathModes)
listImgModes = []
for imgModePath in listImgModesPath:
    listImgModes.append(cv2.imread(os.path.join(folderPathModes, imgModePath)))
#print(listImgModes)

#import icons to list
folderPathIcons = "Resources/Icons"
listImgIconsPath = os.listdir(folderPathIcons)
listImgIcons = []
for imgIconPath in listImgIconsPath:
    listImgIcons.append(cv2.imread(os.path.join(folderPathIcons, imgIconPath)))
print(listImgIcons)
modeType = 0 #here you can change the selection of modes
selection = -1 #is a choice selected
counter = 0 #counter to not directly choose but just when some time goes by and the selection is sure
selectionSpeed = 7 #multiplier to ellipse faster
detector = HandDetector(detectionCon=0.8, maxHands=1)
modePositions = [(1136, 196),(999,389),(1140,586)]
counterPause = 0
selectionList = [-1,-1,-1]

while True:
    success, img = cap.read()

    # Find the hand and its landmarks
    hands, img = detector.findHands(img)  # with draw
    # hands = detector.findHands(img, draw=False)  # without draw
    #overlay webcam on background
    imgBackground[139:139+480, 49:49+640] = img
    imgBackground[0:720, 847:1280] = listImgModes[modeType]



    if hands and counterPause == 0 and modeType<3:
        # Hand 1
        hand1 = hands[0]
        fingers1 = detector.fingersUp(hand1)
        print(fingers1)

        if fingers1 == [0,1,0,0,0]:
            if selection !=1:
                counter = 1
            selection = 1

        elif fingers1 == [0,1,1,0,0]:
            if selection !=2:
                counter = 1
            selection = 2

        elif fingers1 == [0,1,0,0,1]:
            if selection !=3:
                counter = 1
            selection = 3
        else:
            selection =-1
            counter = 0

        if counter > 0:
            counter+=1
            print(counter)
            cv2.ellipse(imgBackground, modePositions[selection-1], (103,103),0,0,counter*selectionSpeed,(0,255,0), 20)

            if counter*selectionSpeed>360:
                selectionList[modeType]=selection
                modeType +=1
                counter = 0
                selection = -1
                counterPause = 1
    #to Pause afetr each selection
    if counterPause>0:
        counterPause+=1
        if counterPause>40:
            counterPause = 0

    #Add selection icon at the bottom
    if selectionList[0] != -1:
        imgBackground[636:636+65, 133:133+65] = listImgIcons[selectionList[0]-1]
    if selectionList[1] != -1:
        imgBackground[636:636+65, 340:340+65] = listImgIcons[2+selectionList[1]]
    if selectionList[2
    ] != -1:
        imgBackground[636:636+65, 542:542+65] = listImgIcons[5+selectionList[2]]
    #display the image
    cv2.imshow("Dat Bild Digger", imgBackground)
    #cv2.imshow("Orsted CI Academy", imgBackground)

    cv2.waitKey(1)

