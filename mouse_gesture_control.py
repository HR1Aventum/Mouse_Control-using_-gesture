import cv2
import numpy as np
from pynput.mouse import Button, Controller
import wx

mouse=Controller()
app=wx.App(False)
(sx,sy)=wx.GetDisplaySize()
(camx,camy)=(320,240)

lowerBound=np.array([33,80,40])
upperBound=np.array([102,255,255])

cam= cv2.VideoCapture(2)
kernelOpen=np.ones((5,5))
kernelClose=np.ones((20,20))
 



while True:
    ret, img=cam.read()
    img=cv2.resize(img,(340,220))

    
    imgHSV= cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
    mask=cv2.inRange(imgHSV,lowerBound,upperBound)
    maskOpen=cv2.morphologyEx(mask,cv2.MORPH_OPEN,kernelOpen)
    maskClose=cv2.morphologyEx(maskOpen,cv2.MORPH_CLOSE,kernelClose)

    maskFinal=maskClose
    conts,h=cv2.findContours(maskFinal.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
    if(len(conts)==1):
        x1,y1,w1,h1=cv2.boundingRect(conts[0])
        #x2,y2,w2,h2=cv2.boundingRect(conts[1])
        cv2.rectangle(img,(x1,y1),(x1+w1,y1+h1),(255,0,0),2)
        #cv2.rectangle(img,(x2,y2),(x2+w2,y2+h2),(255,0,0),2)
        cx1=x1+w1/2
        cy1=y1+h1/2
        #cx2=x2+w2/2
        #cy2=y2+h2/2
        #cx=(cx1+cx2)/2
        #cy=(cy1+cy2)/2
        mouse.position= (sx-(cx1*sx/camx),cy1*sy/camy)
        mouse.release(Button.left)
        
        
    elif(len(conts)==2):
                    (x,y,w,h)=cv2.boundingRect(conts[0])
                    (x2,y2,w2,h2)=cv2.boundingRect(conts[1])
                    mouse.press(Button.left)
                    cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
                    cv2.rectangle(img,(x2,y2),(x2+w2,y2+h2),(255,0,0),2)
                    mouse.press(Button.left)
            
        
    cv2.imshow("cam",img)
    cv2.waitKey(10)
