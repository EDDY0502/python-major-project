  for i,points in enumerate(self.points):
        if i!=0:
          cv2.line(imgMain,self.points[i-1],self.points[i],(0,0,255),20)
      cv2.circle(imgMain, self.points[-1], 20, (200,0,200), cv2.FILLED) 