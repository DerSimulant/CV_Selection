import os
import cv2
from cvzone.HandTrackingModule import HandDetector

# Initialisiere die Webcam
cap = cv2.VideoCapture(1)
cap.set(3, 640)  # Setze die Breite des Kamerabilds
cap.set(4, 480)  # Setze die Höhe des Kamerabilds

# Lade das Hintergrundbild
imgBackground = cv2.imread("Resources/Background.png")

# Lade die Bilder für die verschiedenen Modi in eine Liste
folderPathModes = "Resources/Modes"
listImgModesPath = os.listdir(folderPathModes)
listImgModes = [cv2.imread(os.path.join(folderPathModes, imgModePath)) for imgModePath in listImgModesPath]

# Lade die Icons in eine Liste
folderPathIcons = "Resources/Icons"
listImgIconsPath = os.listdir(folderPathIcons)
listImgIcons = [cv2.imread(os.path.join(folderPathIcons, imgIconPath)) for imgIconPath in listImgIconsPath]
print(listImgIcons)

# Initialisiere Variablen
modeType = 0  # Aktuelle Auswahl des Modus
selection = -1  # Aktuell getroffene Auswahl
counter = 0  # Zähler für die Auswahllogik
selectionSpeed = 7  # Geschwindigkeit der Auswahl
detector = HandDetector(detectionCon=0.8, maxHands=1)  # Initialisiere den Handdetektor
modePositions = [(1136, 196), (999, 389), (1140, 586)]  # Positionen der Auswahlmöglichkeiten
counterPause = 0  # Pausenzähler nach jeder Auswahl
selectionList = [-1, -1, -1]  # Liste der getroffenen Auswahlen
blink_counter = 0  # Zähler für das Blinken des Kreises
blink_state = True  # Zustand des Blinkens (an/aus)
blink_speed = 5  # Geschwindigkeit des Blinkens
num_blinks = 3  # Anzahl der Blinkzyklen

# Hauptprogrammschleife
while True:
    # Lese Kamerabild
    success, img = cap.read()

    # Finde die Hände und ihre Landmarken im Bild
    hands, img = detector.findHands(img)  # Zeichne die Hand mit Landmarken

    # Überlagere das Kamerabild auf den Hintergrund
    imgBackground[139:619, 49:689] = img
    imgBackground[0:720, 847:1280] = listImgModes[modeType]

    # Handerkennung und Auswahllogik
    if hands and counterPause == 0 and modeType < 3:
        hand1 = hands[0]  # Erste erkannte Hand
        fingers1 = detector.fingersUp(hand1)  # Zustand der Finger der ersten Hand
        print(fingers1)

        # Auswahllogik basierend auf den hochgestreckten Fingern
        if fingers1 == [0, 1, 0, 0, 0]:
            if selection != 1:
                counter = 1
            selection = 1
        elif fingers1 == [0, 1, 1, 0, 0]:
            if selection != 2:
                counter = 1
            selection = 2
        elif fingers1 == [0, 1, 0, 0, 1]:
            if selection != 3:
                counter = 1
            selection = 3
        else:
            selection = -1
            counter = 0

        # Zeichne den Auswahlkreis und überprüfe, ob die Auswahl getroffen wurde
        if counter > 0:
            counter += 1
            print(counter)
            if blink_counter == 0:  # Zeichne den Kreis nur, wenn nicht geblinkt wird
                cv2.ellipse(imgBackground, modePositions[selection-1], (103, 103), 0, 0, counter*selectionSpeed, (0, 255, 0), 20)
            if counter*selectionSpeed > 360:
                counter = 0  # Setze den Zähler zurück
                blink_counter = 1  # Starte das Blinken

    # Blink-Logik
    if blink_counter > 0:
        if blink_counter <= num_blinks * blink_speed * 2:
            if blink_counter % (blink_speed * 2) < blink_speed:
                cv2.ellipse(imgBackground, modePositions[selection-1], (103, 103), 0, 0, 360, (0, 255, 0), 20)
            blink_counter += 1
        else:
            selectionList[modeType] = selection
            modeType += 1
            selection = -1
            blink_counter = 0  # Setze den Blinkzähler zurück
            counterPause = 1  # Starte die Pause

    # Pausiere nach jeder Auswahl
    if counterPause > 0:
        counterPause += 1
        if counterPause > 40:
            counterPause = 0

    # Füge das Auswahl-Icon unten hinzu
    if selectionList[0] != -1:
        imgBackground[636:636 + 65, 133:133 + 65] = listImgIcons[selectionList[0] - 1]
    if selectionList[1] != -1:
        imgBackground[636:636 + 65, 340:340 + 65] = listImgIcons[2 + selectionList[1]]
    if selectionList[2
    ] != -1:
        imgBackground[636:636 + 65, 542:542 + 65] = listImgIcons[5 + selectionList[2]]

    # Zeige das Bild an
    cv2.imshow("Dat Bild Digger", imgBackground)

    # Warte auf Tastendruck (für interaktive Steuerung oder Programmbeendigung)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
