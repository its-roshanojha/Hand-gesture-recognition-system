# -*- coding: utf-8 -*-
"""
Created on Fri Nov 20 21:02:54 2020

@author: rajar
"""

import cv2
import numpy as np
import math
import time
import win32api, win32con

def click(x,y):
    win32api.SetCursorPos((x,y))
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,x,y,0,0)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,x,y,0,0)

cap = cv2.VideoCapture(0)


prev = time.time()
TIMER=int(5)

counter=0  
term1=-1
term2=-1
finalTerm=-1
ping=0

#finalTime=time.time()

while True:
    try:  #an error comes if it does not find anything in window as it cannot find contour of max area
          #therefore this try error statement
          
          #for infinite running of camera.
          ret, frame = cap.read()
          
          #initiate mirror image
          frame=cv2.flip(frame,1)
          frame=cv2.blur(frame,(20,20))
          kernel = np.ones((3,3),np.uint8)
          #define region of interest
          roi=frame[100:300, 100:300]
        
        
          cv2.rectangle(frame,(100,100),(300,300),(255,0,0),0)    
          hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
          
          # define range of skin color in HSV
          lower_skin = np.array([0,20,70], dtype=np.uint8)    
          upper_skin = np.array([150,255,255], dtype=np.uint8)
        
          #extract skin colur image  
          mask = cv2.inRange(hsv, lower_skin, upper_skin)
        
   
        
          #extrapolate the hand to fill dark spots within
          #Morphological Approximation
          erode=cv2.erode(mask,kernel,iterations=4);
          mask = cv2.dilate(mask,kernel,iterations = 4)
        
          #blur the image
          mask = cv2.GaussianBlur(mask,(5,5),100) 
        
          #find contours
          #cv2.findContours(img,contour retrival,approximation algo)
          contours,hierarchy= cv2.findContours(mask,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    
          #find contour of max area(hand)
          cnt = max(contours, key = lambda x: cv2.contourArea(x))
        
          #approx the contour a little
          #true -> closed Curve
          #Douglas-Peucker Algo
          epsilon = 0.0005*cv2.arcLength(cnt,True)
          approx= cv2.approxPolyDP(cnt,epsilon,True)
       
        
          #make convex hull around hand
          #To form the convex hull
          hull = cv2.convexHull(cnt)
        
          #define area of hull and area of hand
          areahull = cv2.contourArea(hull)
          areacnt = cv2.contourArea(cnt)
      
          #find the percentage of area not covered by hand in convex hull
          arearatio=((areahull-areacnt)/areacnt)*100
          ##############print("Area Ratio = "+str(arearatio))
    
          #find the defects in convex hull with respect to hand
          #since returnPoints are false so it will output those points where Convex Hull=Contour
          hull = cv2.convexHull(approx, returnPoints=False)
          defects = cv2.convexityDefects(approx, hull)
        
          # l = no. of defects
          l=0
        
          #code for finding no. of defects due to fingers
          for i in range(defects.shape[0]):
              s,e,f,d = defects[i,0]
              start = tuple(approx[s][0])
              end = tuple(approx[e][0])
              far = tuple(approx[f][0])
            
              # find length of all sides of triangle
              a = math.sqrt((end[0] - start[0])**2 + (end[1] - start[1])**2)
              b = math.sqrt((far[0] - start[0])**2 + (far[1] - start[1])**2)
              c = math.sqrt((end[0] - far[0])**2 + (end[1] - far[1])**2)
              s = (a+b+c)/2
              ar = math.sqrt(s*(s-a)*(s-b)*(s-c))
             
              #distance between point and convex hull
              d=(2*ar)/a
              
            
              # apply cosine rule here
              angle = math.acos((b**2 + c**2 - a**2)/(2*b*c)) * 57
            
        
              # ignore angles > 90 and ignore points very close to convex hull(they generally come due to noise)
              if angle <= 90 and d>30:
                  l += 1
                  cv2.circle(roi, far, 3, [255,0,0], -1)
            
              #draw lines around hand
              cv2.line(roi,start, end, [0,255,0], 2)
            
            
          l+=1
        
          #print corresponding gestures which are in their ranges
          font = cv2.FONT_HERSHEY_SIMPLEX
          
          #print(arearatio)
          
          cv2.putText(frame,'Timer : '+ str(TIMER),(400, 50), font,1.5, (0, 255, 255),2, cv2.LINE_AA)
          
          if l==1:
              if areacnt<2000:
                  cv2.putText(frame,'Put hand in the box',(0,50), font, 2, (0,0,255), 3, cv2.LINE_AA)
              else:
                  if arearatio<3: #7
                      
                      cv2.putText(frame,'0',(0,50), font, 2, (0,0,255), 3, cv2.LINE_AA)
                      l=0
                      
                  elif arearatio<10:
                      
                      cv2.putText(frame,'Clear',(0,50), font, 2, (0,0,255), 3, cv2.LINE_AA)
                      l=200
                      
                  elif arearatio<19: #15
                      
                      cv2.putText(frame,'Done',(0,50), font, 2, (0,0,255), 3, cv2.LINE_AA)
                      l=100
                   
                  else:
                      
                      cv2.putText(frame,'1',(0,50), font, 2, (0,0,255), 3, cv2.LINE_AA)
                    
          elif l==2:
              if arearatio>700:
                  cv2.putText(frame,'reposition',(0,50), font, 2, (0,0,255), 3, cv2.LINE_AA)
              else:
                  cv2.putText(frame,'2',(0,50), font, 2, (0,0,255), 3, cv2.LINE_AA)
            
          elif l==3:
         
              cv2.putText(frame,'3',(0,50), font, 2, (0,0,255), 3, cv2.LINE_AA)
                    
          elif l==4:
              
              cv2.putText(frame,'4',(0,50), font, 2, (0,0,255), 3, cv2.LINE_AA)
            
          elif l==5:
              
              cv2.putText(frame,'5',(0,50), font, 2, (0,0,255), 3, cv2.LINE_AA)
              
          elif l==6:
              
              cv2.putText(frame,'reposition',(0,50), font, 2, (0,0,255), 3, cv2.LINE_AA)
            
          else :
              
              cv2.putText(frame,'Something is wrong!',(10,50), font, 2, (0,0,255), 3, cv2.LINE_AA)
          
          
          cur=time.time()
          
          if cur-prev >= 1:
              prev=cur
              TIMER=TIMER-1
          
          if TIMER==-1:
              TIMER=5
              if counter==0:
                  if l==100:
                      click(969,671)
                      print("Done")
                      counter=0
                      continue
                  if l==200:
                      for k in range(4):
                          click(742,663)
                      print("Clear")
                      counter=0
                      continue
                  term1=l
                  print('First Term is :'+str(term1))
                  counter=1
                  
              elif counter==1:
                  if l==100:
                      click(969,671)
                      print("Done")
                      counter=0
                      continue
                  if l==200:
                      for k in range(4):
                          click(742,663)
                      print("Clear")
                      counter=0
                      continue
                  term2=l
                  print('Second Term is :'+str(term2))
                  counter=0
                  
                  
              if term1 >-1 and term2 >-1:
              #print('running')
                  finalTerm=term1+term2
                  term1=-1
                  term2=-1
                  print('Final Term is :'+str(finalTerm)+'\n')
              
              
                  if finalTerm==1:
                      click(768,359)
                  elif finalTerm==2:
                      click(861,337)
                  elif finalTerm==3:
                      click(971,343)
                  elif finalTerm==4:
                      click(750,451)
                  elif finalTerm==5:
                      click(860,449)
                  elif finalTerm==6:
                      click(971,451)
                  elif finalTerm==7:
                      click(749,555)
                  elif finalTerm==8:
                      click(861,556)
                  elif finalTerm==9:
                      click(970,557)
                  elif finalTerm==0:
                      click(862,670)
              
         
          
              
              
          
          if finalTerm !=-1:
             cv2.putText(frame,'Final Term is : '+str(finalTerm),(5,465), font,1.8, (0, 255, 0),2, cv2.LINE_AA)
             
          #if term1!=-1:
             #cv2.putText(frame,'First Term is : '+str(term1),(5,390), font,1, (255, 0, 0),2, cv2.LINE_AA)
             
          #if term2!=-1:
             #cv2.putText(frame,'Second Term is : '+str(term2),(5,420), font,1, (255, 0, 0),2, cv2.LINE_AA)
              
              
         
          #show the windows
          cv2.imshow('mask',mask)
          cv2.imshow('frame',frame)
          #cv2.imshow('erode',erode)
          
          
          

    except:
        pass

    #This breaks on 'q' key
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    

cap.release()
cv2.destroyAllWindows()