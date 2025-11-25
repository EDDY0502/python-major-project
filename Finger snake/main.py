import cvzone # type: ignore
import cv2 # type: ignore
import numpy as np # type: ignore
from cvzone.HandTrackingModule import HandDetector # type: ignore
import math
import random


cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)
detector= HandDetector(detectionCon=0.8, maxHands=1)


class SnakeGameClass:
  def __init__(self):
    self.points = [] # all points
    self.lengths = [] # distance between points
    self.currentLength = 0 # total length
    self.allowedLength = 150 # length allowed
    self.previousHead = 0,0

    self.imageFood = cv2.imread("Finger snake/Donut.png", cv2.IMREAD_UNCHANGED)
    self.hfood, self.wfood, _ = self.imageFood.shape
    self.foodPoint = 0,0
    self.randomFoodLocation()

    self.score = 0
    self.gameOver = False

  def randomFoodLocation(self):  
      self.foodPoint = random.randint(100, 1000), random.randint(100, 600)


  def update(self, imgMain, currentHead):

    if self.gameOver:
            cvzone.putTextRect(imgMain, "Game Over", [300, 400],scale=7, thickness=5, offset=20)
            cvzone.putTextRect(imgMain, f'Your Score: {self.score}', [300, 550], scale=7, thickness=5, offset=20)


    else:
      pc,py=self.previousHead
      cx,cy=currentHead
      if pc == 0 and py == 0:
        self.previousHead = cx, cy
        return imgMain

      self.points.append([cx,cy])
      distance = math.hypot(cx - pc, cy - py)
      self.lengths.append(distance)
      self.currentLength += distance
      self.previousHead = cx,cy


    # Length Reduction
      if self.currentLength > self.allowedLength:
        for i,length in enumerate(self.lengths):
          self.currentLength -= length
          self.lengths.pop(i)
          self.points.pop(i)
          if self.currentLength < self.allowedLength:
            break

      # check if snake ate the food
      rx,ry=self.foodPoint
      if rx - self.wfood//2 <cx <rx +self.wfood//2 and ry - self.wfood//2 <cy <ry +self.hfood//2:
        self.randomFoodLocation()
        self.allowedLength +=50
        self.score +=1
        print(self.score)

      #draw snake
      if self.points:
        for i,points in enumerate(self.points):
          if i!=0:
            cv2.line(imgMain,self.points[i-1],self.points[i],(0,0,255),20)
        cv2.circle(imgMain, self.points[-1], 20, (200,0,200), cv2.FILLED) 


      #draw food
      rx,ry=self.foodPoint
      imgMain=cvzone.overlayPNG(imgMain, self.imageFood, (rx - self.wfood//2, ry - self.hfood//2))



    # check for the collision 
      if len(self.points) > 4:
        pts = np.array(self.points[:-2], np.int32)
        pts = pts.reshape((-1,1,2))
        cv2.polylines(imgMain,[pts],False,(0,200,0),3)
        dist = cv2.pointPolygonTest(pts,(cx,cy),True)

        if -1 <= dist <= 1:
          print("Game Over")
          self.gameOver = True
          self.points = []
          self.lengths = []
          self.currentLength = 0
          self.allowedLength = 150
          self.previousHead = 0,0
          self.randomFoodLocation()


    return imgMain

game = SnakeGameClass() 


while True:
  success, img = cap.read()
  img=cv2.flip(img,1)
  hand,img=detector.findHands(img, flipType=False)

  if hand:
    lmList =hand[0]['lmList']
    pointIndex = lmList[8][0:2]
    img = game.update(img, pointIndex)
        

  cv2.imshow("Image", img)
  key = cv2.waitKey(1)

  if key == ord('r'):
    game = SnakeGameClass()

  


