#importing required dependencies and libraries
import cv2
from cv2 import FONT_HERSHEY_COMPLEX
import cvzone
import numpy as np
from random import choice

#printing version of OpenCV
print(cv2.__version__)

#setting the width and height of frame
width = 1280
height = 720

#importing all the required images
backGround = cv2.imread("C:/Users/kutka/Documents/python/Resources/BackGround.jpg")
drone_R = cv2.imread("C:/Users/kutka/Documents/python/Resources/droneR.png",cv2.IMREAD_UNCHANGED)
drone_L = cv2.imread("C:/Users/kutka/Documents/python/Resources/droneL.png",cv2.IMREAD_UNCHANGED)
drone_R_Fall = cv2.imread("C:/Users/kutka/Documents/python/Resources/drone_R_Fall.png",cv2.IMREAD_UNCHANGED)
drone_L_Fall = cv2.imread("C:/Users/kutka/Documents/python/Resources/drone_L_Fall.png",cv2.IMREAD_UNCHANGED)

#resizing the images
backGround = cv2.resize(backGround,(width,height))
drone_R = cv2.resize(drone_R,(0,0),None,0.5,0.5)
drone_R_cpy = drone_R.copy()
drone_L = cv2.resize(drone_L,(0,0),None,0.5,0.5)
drone_L_cpy = drone_L.copy()
drone_R_Fall = cv2.resize(drone_R_Fall,(0,0),None,0.5,0.5)
drone_L_Fall = cv2.resize(drone_L_Fall,(0,0),None,0.5,0.5)

drone_RS = cv2.resize(drone_R,(0,0),None,1.75,1.75)
drone_LS = cv2.resize(drone_L,(0,0),None,1.75,1.75)

h_drone, w_drone, c_drone = drone_R.shape # gives height,width,transperancy of drone img from murtaza video
h_back, w_back, c_back = backGround.shape

#setting up the webcam
cam=cv2.VideoCapture(0, cv2.CAP_DSHOW)
cam.set(cv2.CAP_PROP_FRAME_WIDTH, width)
cam.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
cam.set(cv2.CAP_PROP_FPS, 30)
cam.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*'MJPG'))

#start position of drone
DR_xPos = int(width/2) #Drone Right
DR_yPos = height-200
DL_xPos = int(width/2) #Drone Left
DL_yPos = height-200
delXR = 4
delYR = 4
delXL = 4
delYL = 4

#setting up HSV values for Color Tracking
hueLow=102
hueHigh=130
satLow=100
satHigh=206
valLow=72
valHigh=255

evt=0
target_pnt=(0,0)
kR=0
kL=0
angleR = 0
angleL = 0
cR=0
cL=0
cmd = 0
xLastR=0
yLastR=0
xLastL=0
yLastL=0
flagR=0
flagL=0
R=0
L=0
pL=0
pR=0

shot=3
hit=1
rnd=1

textFont1=cv2.FONT_HERSHEY_COMPLEX
textFont2=cv2.FONT_ITALIC
textColor=(255,255,255)
textSize=4
textThick=5
text1 = "DRONE HUNT"
text2 = "PRESS R TO START"
gameA = "ONE DRONE"
gameB = "TWO DRONES"
char = 'c'
textPosA = (int(width/2)-360,int(height/2)-50)
textPosB = (int(width/2)-360,int(height/2)+30)
score = 0
scorePos = (int(width/2)-200,int(height/2)+165)

def mouseClick(event, xPos, yPos, flag, params):
    global evt
    if event==cv2.EVENT_MBUTTONDOWN:
        evt=event

cv2.namedWindow('DRONE HUNT')
cv2.setMouseCallback('DRONE HUNT',mouseClick)

while True:
    ignore,frame=cam.read()

    while (cmd==0):
        x=np.zeros([height,width,3],dtype=np.uint8)
        x[:,:]=(0,0,0)
        screen = cvzone.overlayPNG(x, drone_LS, ((w_back-w_drone-200),(h_back-h_drone-200)))
        screen1 = cvzone.overlayPNG(screen, drone_RS, ((70),(h_back-h_drone-200)))
        cv2.putText(screen1, text1, (200,150), textFont1, textSize, textColor, textThick)
        cv2.putText(screen1, text2, (350,height-80), textFont2, 2, (0,255,0), 3)
        cv2.putText(screen1, "GAME A : "+gameA, textPosA, textFont2, 2, (0,0,255), 2)
        cv2.putText(screen1, "GAME B : "+gameB, textPosB, textFont2, 2, (0,0,255), 2)
        cv2.putText(screen1, "SCORE : "+str(score), scorePos, textFont2, 2, (255,0,0), 2)
        cv2.imshow('DRONE HUNT', screen1)
        if cv2.waitKey(1) & 0xff==ord('a'):
            char='a'
            cmd=1
            break
        
        if cv2.waitKey(1) & 0xff==ord('r'):
            cmd=1
            break

    frame = cv2.flip(frame,1)
    frameHSV=cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)

    lowerBound=np.array([hueLow,satLow,valLow])
    upperBound=np.array([hueHigh,satHigh,valHigh])
    myMask=cv2.inRange(frameHSV,lowerBound,upperBound)

    x=np.zeros([height,width,3],dtype=np.uint8)
    x[:,:]=(0,0,0)

    if((DR_xPos>0 and DR_xPos<(w_back-w_drone)) and (DR_yPos>0 and DR_yPos<(h_back-h_drone)) and (kR==0 and R==0)):
        img = cvzone.overlayPNG(backGround,drone_R,(DR_xPos,DR_yPos))

    if((DL_xPos>0 and DL_xPos<(w_back-w_drone)) and (DL_yPos>0 and DL_yPos<(h_back-h_drone)) and (kL==0 and L==0)):
        if(pR==1 or pR==2):
            img = cvzone.overlayPNG(backGround,drone_L,(DL_xPos,DL_yPos))
        if(pL==0 and pR==0):
            img = cvzone.overlayPNG(img,drone_L,(DL_xPos,DL_yPos))

    if ((DR_xPos<20 or DR_xPos>(w_back-w_drone-10)) and kR==0 and R==0):
        delXR = delXR*(-1)

    if ((DL_xPos<20 or DL_xPos>(w_back-w_drone-10)) and kL==0 and L==0):
        delXL = delXL*(-1)

    if ((DR_yPos<20 or DR_yPos>(h_back-h_drone-10)) and kR==0 and R==0):
        delYR = delYR*(-1)

    if ((DL_yPos<20 or DL_yPos>(h_back-h_drone-10)) and kL==0 and L==0):
        delYL = delYL*(-1)

    contours,junk=cv2.findContours(myMask,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    for contour in contours:
        area=cv2.contourArea(contour) 
        if area>=400:
            x,y,W,H=cv2.boundingRect(contour) 
            cv2.line(img, (x+int(W/2),y+10), (x+int(W/2),y+H-10), (255,255,255), 2) # Vertical Line
            cv2.line(img, (x-10,y+int(H/2)), (x+W+10,y+int(H/2)), (255,255,255), 2) # Horizontal Line
            cv2.circle(img, (x+int(W/2),y+int(H/2)), 10, (0,0,255), 2) # Intersecting Circle
            target_pnt=(x+int(W/2),y+int(H/2))

    if((target_pnt[0]>(DR_xPos) and target_pnt[0]<(DR_xPos+100)) and (target_pnt[1]>(DR_yPos) and target_pnt[1]<(DR_yPos+100))):
        cv2.circle(img,target_pnt,30,(0,255,0),5)
        if (evt==3):
            value=choice([i for i in range(-8,9) if i not in [-3,-2,-1,0,1,2,3]])
            delXR = value
            delYR = value
            xLastR = DR_xPos
            yLastR = DR_yPos
            DR_xPos = int((width/2)+(abs(value*40)))
            DR_yPos = 400
            kR=1
            R=1
            score=score+50
            hit=hit+1
            pR=1
            shot=shot-1
            #print(p)
            evt=4

    if((target_pnt[0]>(DL_xPos) and target_pnt[0]<(DL_xPos+100)) and (target_pnt[1]>(DL_yPos) and target_pnt[1]<(DL_yPos+100))):
        cv2.circle(img,target_pnt,30,(0,0,255),5)
        if (evt==3):
            value=choice([i for i in range(-8,9) if i not in [-3,-2,-1,0,1,2,3]])
            delXL = value
            delYL = value
            xLastL = DL_xPos
            yLastL = DL_yPos
            DL_xPos = int((width/2)-(abs(value*40)))
            DL_yPos = height-200
            kL=1
            L=1
            score=score+100
            hit=hit+1
            shot=shot-1
            pL=3
            #print(p)
            evt=4
    
    if(kR==0 and R==0):
        cv2.imshow("DRONE HUNT",img)
        if (cR%100==0):
            value=choice([i for i in range(-8,9) if i not in [-3,-2,-1,0,1,2,3]])
            delXR = value
            value=choice([i for i in range(-8,9) if i not in [-3,-2,-1,0,1,2,3]])
            delYR = value
            cR=cR+1

        if(cR%100!=0):
            DR_xPos = DR_xPos + delXR
            DR_yPos = DR_yPos + delYR
            cR=cR+1

    if(kL==0 and L==0):
        cv2.imshow("DRONE HUNT",img)
        if (cL%100==0):
            value=choice([i for i in range(-8,9) if i not in [-3,-2,-1,0,1,2,3]])
            delXL = value
            value=choice([i for i in range(-8,9) if i not in [-3,-2,-1,0,1,2,3]])
            delYL = value
            cL=cL+1

        if(cL%100!=0):
            DL_xPos = DL_xPos + delXL
            DL_yPos = DL_yPos + delYL
            cL=cL+1

    if (kR==1 and flagR<6 and R==1):
        cv2.rectangle(img,(xLastR,yLastR),(xLastR+w_drone,yLastR+h_drone),(255,255,255),-1)
        cv2.putText(img, "50",(xLastR,yLastR), textFont1, 3, (0,0,255), 3)
        cv2.imshow("DRONE HUNT", img)
        flagR=flagR+1
        cv2.waitKey(1)
        #print(flagR)

    if (kL==1 and flagL<6 and L==1):
        cv2.rectangle(img,(xLastL,yLastL),(xLastL+w_drone,yLastL+h_drone),(255,255,255),-1)
        cv2.putText(img, "100",(xLastL,yLastL), textFont1, 3, (0,0,255), 3)
        cv2.imshow("DRONE HUNT", img)
        flagL=flagL+1
        cv2.waitKey(1)
        #print(flagL)

    if(kR==1 and angleR<15 and flagR>5 and R==1):
        angleR = angleR+1
        drone_R = cvzone.rotateImage(drone_R, angleR)
        img = cvzone.overlayPNG(backGround, drone_R, (xLastR,yLastR))
        cv2.imshow("DRONE HUNT", img)
        cv2.waitKey(1)

    if(kL==1 and angleL<15 and flagL>5 and L==1):
        angleL = angleL+1
        drone_L = cvzone.rotateImage(drone_L, -angleL)
        img = cvzone.overlayPNG(img, drone_L, (xLastL,yLastL))
        cv2.imshow("DRONE HUNT", img)
        cv2.waitKey(1)

    if(angleR>14 and R==1):
        if(yLastR<(h_back-h_drone-20)):
            img = cvzone.overlayPNG(backGround, drone_R_Fall, (xLastR,yLastR))
            yLastR=yLastR+10
            cv2.imshow("DRONE HUNT", img)
        else:
            pR=2
            #print(p)

    if(angleL>14 and L==1):
        if(yLastL<(h_back-h_drone-20)):
            img = cvzone.overlayPNG(img, drone_L_Fall, (xLastL,yLastL))
            yLastL=yLastL+10
            cv2.imshow("DRONE HUNT", img)
        else:
            pL=4
            #print(p)

    if(pR==2 and pL==4):
        kL=0
        L=0
        kR=0
        R=0
        pR=0
        pL=0
        angleR=0
        flagR=0
        drone_R = drone_R_cpy
        angleL=0
        flagL=0
        drone_L = drone_L_cpy
        shot=3

    if (hit == 10):
        rnd=2
    if (hit == 20):
        rnd=3

    if shot<0:
        score=score-100
        shot=3

    cv2.putText(img, "SHOT : "+str(shot), (50,height-50), cv2.FONT_HERSHEY_COMPLEX, 2, (0,255,0), 3)
    cv2.putText(img, "HITS : "+str(hit-1), (450,height-50), cv2.FONT_HERSHEY_COMPLEX, 2, (255,0,255), 3)
    cv2.putText(img, "SCORE : "+str(score), (820,height-50), cv2.FONT_HERSHEY_COMPLEX, 2, (255,0,0), 3)
    cv2.putText(img, "ROUND : "+str(rnd), (370,80), cv2.FONT_HERSHEY_COMPLEX, 3, (0,255,255), 3)
    cv2.imshow("DRONE HUNT", img)

    evt=4
    if cv2.waitKey(1) & 0xff==ord('r'): # To Restart game
        cmd=0
    if cv2.waitKey(1) & 0xff==ord('q'):
        break
cam.release()    
cv2.destroyAllWindows()