import cv2
import cvzone
from cvzone.FaceMeshModule import FaceMeshDetector

cap = cv2.VideoCapture(0)
detector = FaceMeshDetector(maxFaces=10)
while True:
    success, img = cap.read()
    img, faces = detector.findFaceMesh(img)

    i=0
    for face in faces:
        i+=1
    print(i)
    x = 0
    if faces:
        while x < i:
            face = faces[x]
            pointLeft = face[145]
            pointRight = face[374]
            cv2.line(img, pointLeft, pointRight, (0, 200, 0), 3)
            cv2.circle(img, pointLeft, 5, (255, 0, 255), cv2.FILLED)
            cv2.circle(img, pointRight, 5, (255, 0, 255), cv2.FILLED)
            w, _ = detector.findDistance(pointLeft, pointRight)
            W = 6.3
            f=840
            d = (W*f)/w
            print(int(d))
            cvzone.putTextRect(img,f'distance: {int(d)}cm',(face[10][0]-75,face[10][1]-50),scale=2)
            x+=1

    cv2.imshow("Image", img)
    cv2.waitKey(1)