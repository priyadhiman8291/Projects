import cv2
import numpy as np


# web camera
cap= cv2.VideoCapture('4K Road traffic video for object detection and tracking - free download now!.mp4')

#minimum width and height of rectangle 
min_width_react=80
min_height_react=80

count_line_position=250
# vehicle detection algo
# initialize substractor

algo = cv2.bgsegm.createBackgroundSubtractorMOG()      # ignore background


# Counter for count

def center_handle(x,y,w,h):
    x1=int(w/2)
    y1=int(h/2)
    cx=x+x1
    cy=y+y1
    return cx,cy

detect = []
offset=6        # allowable error between pixel
counter = 0


while True:
    ret, frame1=cap.read()      #read  the video
    grey=cv2.cvtColor(frame1,cv2.COLOR_BGR2GRAY)
    blur=cv2.GaussianBlur(grey,(3,3),5) 
    #apply on each frame
    img_sub=algo.apply(blur)
    dilat = cv2.dilate(img_sub,np.ones((5,5)))        # structue the element is specifies at  a point
    kernel= cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(5,5))       # it gives the shape and proceed further
    dilatada =cv2.morphologyEx(dilat,cv2.MORPH_CLOSE,kernel)
    dilatada =cv2.morphologyEx(dilatada,cv2.MORPH_CLOSE,kernel)   
    counterShape,h=cv2.findContours(dilatada,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)                #images get reduced and get in shape
  
    # to draw a line
    cv2.line(frame1,(0 ,count_line_position),(1200,count_line_position),(255,127,0),3)

    # draw rectangle on each vehicle

    for (i,c) in enumerate(counterShape):
        (x,y,w,h)  = cv2.boundingRect(c)
        validate_counter = (w>= min_width_react) and (h>= min_height_react)   
        if not validate_counter:
            continue

        cv2.rectangle(frame1,(x,y),(x+w,y+h),(0,255,0),2)                  
        cv2.putText(frame1,"Vehicle"+str(counter),(x,y-20),cv2.FONT_HERSHEY_SIMPLEX,1,(255,244,0),2)    


    #count the vehicles
    # we will make a circle on vehicle and we will append in a list counter

        center=center_handle(x,y,w,h)
        detect.append(center)
        cv2.circle(frame1,center,4,(0,0,255),-1)

    for (x,y) in detect:
        if y<(count_line_position+offset) and y>(count_line_position-offset):
            counter+=1
            cv2.line(frame1,(0,count_line_position),(1200,count_line_position),(0,127,255),3)
            detect.remove((x,y))
            print("Counter : "+str(counter))


    cv2.putText(frame1,"Counter : "+str(counter),(0,70),cv2.FONT_HERSHEY_SIMPLEX,2,(0,0,255),2)        


    #cv2.imshow('Detector',dilatada)
    cv2.imshow('video Original',frame1)

    if cv2.waitKey(1) == 13:
        break


cv2.destroyAllWindows()
cap.release()    