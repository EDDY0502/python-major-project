import cvzone # type: ignore  # Import the cvzone library (built on top of OpenCV) – it gives us helper functions like overlayPNG, fancy text, etc. The "# type: ignore" tells some editors to ignore type-checking errors.

import cv2 # type: ignore  # Import the main OpenCV (cv2) library, used for camera access, drawing, image processing, etc.

import numpy as np # type: ignore  # Import NumPy, a library for fast array and math operations. Here we use it for handling lists of points as arrays.

from cvzone.HandTrackingModule import HandDetector # type: ignore  # From cvzone, we import HandDetector, a ready-made class that detects hands and finger positions.

import math  # Import the math module to use functions like hypot() which calculates distance between two points.

import random  # Import random module to generate random positions for the food.


# ---------------- CAMERA SETUP ---------------- #

cap = cv2.VideoCapture(0)  # Create a VideoCapture object "cap" that tries to connect to the default webcam (0 = first camera device).

cap.set(3, 1280)  # Set property ID 3 (frame width) of the camera to 1280 pixels. This decides how wide the video frame will be.

cap.set(4, 720)   # Set property ID 4 (frame height) of the camera to 720 pixels. This decides how tall the video frame will be.

detector= HandDetector(detectionCon=0.8, maxHands=1)  
# Create a HandDetector object called "detector".
# detectionCon=0.8 means it needs at least 80% confidence to consider something as a hand.
# maxHands=1 means it will only track one hand, which is enough for this game.


# ---------------- SNAKE GAME CLASS ---------------- #

class SnakeGameClass:  # Define a class called SnakeGameClass. A class is like a blueprint for creating snake game objects.

  def __init__(self):  # This is the constructor method. It runs automatically when we create a new SnakeGameClass() object.
    self.points = [] # all points  # This list will store all (x, y) positions of the snake's body along its path.

    self.lengths = [] # distance between points  # This list will store the distance between each pair of consecutive points in the snake.

    self.currentLength = 0 # total length  # This variable keeps track of the total length of the snake by summing values in self.lengths.

    self.allowedLength = 150 # length allowed  # This is the maximum allowed length of the snake. If the snake goes beyond this length, we start removing tail segments.

    self.previousHead = 0,0  # This stores the previous position of the snake's head (initially (0,0) which means "not yet set").


    self.imageFood = cv2.imread("Finger snake/Donut.png", cv2.IMREAD_UNCHANGED)
    # Load the food image from the specified file path.
    # "Finger snake/Donut.png" is the relative path to the image.
    # cv2.IMREAD_UNCHANGED means we load the image with its alpha channel (transparency) preserved.

    self.hfood, self.wfood, _ = self.imageFood.shape
    # Get the height (hfood), width (wfood), and number of channels (_) of the loaded food image.
    # We ignore the last value with "_" because we don't need it directly.

    self.foodPoint = 0,0
    # This will store the (x, y) position where the food (donut) should appear on the screen.

    self.randomFoodLocation()
    # Call the function to immediately place the food at a random position when the game starts.

    self.score = 0
    # Initialize the player's score to 0. It will increase when the snake eats food.

    self.gameOver = False
    # This flag indicates whether the game is over or still running. Initially it's False (game is active).


  def randomFoodLocation(self):  
      # This method sets a random location for the food within some bounds of the camera frame.
      self.foodPoint = random.randint(100, 1000), random.randint(100, 600)
      # random.randint(a, b) returns a random integer between a and b inclusive.
      # Here, x is between 100 and 1000, y between 100 and 600, so the food appears somewhere in the visible area.


  def update(self, imgMain, currentHead):
    # This method is called every frame to update the game state.
    # imgMain is the current camera frame (image) on which we draw.
    # currentHead is the new position (x, y) of the snake's head (based on the index finger tip).


    if self.gameOver:
            cvzone.putTextRect(imgMain, "Game Over", [300, 400],scale=7, thickness=5, offset=20)
            # If gameOver is True, we draw a big "Game Over" message on the screen using cvzone.putTextRect.
            # [300, 400] is the position where the text rectangle starts, scale and thickness control size.

            cvzone.putTextRect(imgMain, f'Your Score: {self.score}', [300, 550], scale=7, thickness=5, offset=20)
            # Show the final score below the Game Over text.
            # We use an f-string to insert self.score into the text.

    else:
      # If the game is not over, we update the snake’s position and handle game logic.

      pc,py=self.previousHead
      # pc, py are the previous head coordinates (x,y).
      # We unpack self.previousHead (which is a tuple) into pc and py.

      cx,cy=currentHead
      # cx, cy are the current head coordinates (x,y) taken from the finger tracking.

      if pc == 0 and py == 0:
        # This checks if the previous head position is still (0,0),
        # which is our signal that this is the very first frame / first movement.
        self.previousHead = cx, cy
        # We set the previous head to the current head so that next time we can calculate distance properly.
        return imgMain
        # We return the image directly without drawing a line from (0,0) to the current head, which would look wrong.


      self.points.append([cx,cy])
      # Add the current head position as a new point in the snake's body path.
      # This builds a list of all positions the snake has moved through.

      distance = math.hypot(cx - pc, cy - py)
      # Calculate the distance between the new head position and the previous head position.
      # math.hypot(dx, dy) = sqrt(dx^2 + dy^2). This gives the straight-line distance.

      self.lengths.append(distance)
      # Store this distance in the lengths list to know how much the snake grew between these points.

      self.currentLength += distance
      # Increase the total snake length by this new segment distance.

      self.previousHead = cx,cy
      # Update the previous head to the current head, ready for the next frame’s calculation.


    # Length Reduction
    # This block ensures that the snake does not grow beyond self.allowedLength.
      if self.currentLength > self.allowedLength:
        # If the total length of the snake is greater than what is allowed, we need to remove segments from the tail.
        for i,length in enumerate(self.lengths):
          # Loop through all the segment lengths with their index i.
          self.currentLength -= length
          # Subtract this segment’s length from the current length total.

          self.lengths.pop(i)
          # Remove this segment length from the lengths list.

          self.points.pop(i)
          # Also remove the corresponding point from the points list (tail point).

          if self.currentLength < self.allowedLength:
            # Once the total length is back under the allowed limit, we stop removing.
            break


      # check if snake ate the food
      rx,ry=self.foodPoint
      # rx and ry are the x and y coordinates of the food.

      if rx - self.wfood//2 <cx <rx +self.wfood//2 and ry - self.wfood//2 <cy <ry +self.hfood//2:
        # This condition checks whether the snake's head (cx, cy) is within the rectangular area of the food.
        # rx - wfood//2 and rx + wfood//2 define the left and right bounds of the food.
        # ry - hfood//2 and ry + hfood//2 define the top and bottom bounds.
        # If the head is within these bounds, it means the snake has "eaten" the food.

        self.randomFoodLocation()
        # After eating, we move the food to a new random location.

        self.allowedLength +=50
        # Increase the maximum allowed snake length by 50 units so the snake grows longer over time.

        self.score +=1
        # Increment the score by 1 because the player successfully ate the food.

        print(self.score)
        # Print the score in the terminal as well (for debugging / visibility).


      #draw snake
      if self.points:
        # If there are any points in the snake body list (which there should be after movement):

        for i,points in enumerate(self.points):
          # Loop through each point, with i as the index and points as the actual [x, y] value (but we don't use 'points' variable directly here).

          if i!=0:
            # Skip the first point (i==0) because we can't draw a line from a non-existent previous point.
            cv2.line(imgMain,self.points[i-1],self.points[i],(0,0,255),20)
            # Draw a thick line segment from the previous point to the current point.
            # (0,0,255) is the color red in BGR format.
            # 20 is the line thickness.

        cv2.circle(imgMain, self.points[-1], 20, (200,0,200), cv2.FILLED)
        # Draw a filled circle at the last point in self.points (head of the snake).
        # Color (200,0,200) is a purple-like color. Radius is 20 pixels.


      #draw food
      rx,ry=self.foodPoint
      # Again, get the current food position (x,y).

      imgMain=cvzone.overlayPNG(imgMain, self.imageFood, (rx - self.wfood//2, ry - self.hfood//2))
      # Use cvzone's overlayPNG to draw the food image with transparency onto the main image.
      # We subtract half the width and height so that the food image is centered around (rx, ry), not drawn from its top-left corner.


    # check for the collision 
      if len(self.points) > 4:
        # Only check for collision if the snake has more than 4 points in its body.
        # Very short snakes are less likely to collide with themselves and may cause errors if checked too early.

        pts = np.array(self.points[:-2], np.int32)
        # Convert all body points except the last two into a NumPy array of type int32.
        # We exclude the last two points (head region) to only consider body segments.

        pts = pts.reshape((-1,1,2))
        # Reshape the array into the format required by OpenCV drawing and geometry functions:
        # a list of points where each point is wrapped in an extra dimension.

        cv2.polylines(imgMain,[pts],False,(0,200,0),3)
        # Draw a polyline (a connected series of lines) over the snake body path in green color.
        # This is mainly visual and also ensures the points shape is suitable for the next function.

        dist = cv2.pointPolygonTest(pts,(cx,cy),True)
        # cv2.pointPolygonTest checks the distance from a point (cx, cy) to a contour (pts).
        # It returns a positive value if inside, negative if outside, and near zero when on/near the edge.
        # Here we want to know how close the snake head is to its own body.

        if -0.3 <= dist <= 0.3:
          # If the distance is between -0.3 and +0.3, we consider that a collision.
          # Very small window means the game is somewhat forgiving but still detects hits.

          print("Game Over")
          # Print "Game Over" in the console.

          self.gameOver = True
          # Set the gameOver flag to True so that next frame we show the Game Over UI instead of updating the snake.

          self.points = []
          # Clear all snake body points so the snake disappears.

          self.lengths = []
          # Clear lengths list as well.

          self.currentLength = 0
          # Reset snake's current length.

          self.allowedLength = 150
          # Reset the maximum allowed length to the original starting value.

          self.previousHead = 0,0
          # Reset the previous head position to (0,0) so the starting logic works again next time.

          self.randomFoodLocation()
          # Move the food to a new random spot for the new game.


    return imgMain
    # Return the image after all drawing and updates, so the main loop can display it.


# ---------------- CREATE GAME INSTANCE ---------------- #

game = SnakeGameClass() 
# Create a new object from the SnakeGameClass.
# This initializes all variables and starts the game state.


# ---------------- MAIN LOOP (RUNS EVERY FRAME) ---------------- #

while True:
  # This is the main game loop. It runs over and over until we manually break (exit) it.

  success, img = cap.read()
  # cap.read() grabs a frame from the webcam.rr
  # 'success' is True if a frame was read correctly, 'img' is the image captured.

  img=cv2.flip(img,1)
  # Flip the image horizontally (mirror effect) so your movements feel natural (like a mirror).

  hand,img=detector.findHands(img, flipType=False)
  # Use the hand detector to find any hands in the image.
  # 'hand' will be a list of detected hands and their data.
  # 'img' is also returned with hand landmarks drawn on it (if flipType=False, we do not flip inside detector again).


  if hand:
    # If at least one hand is detected:

    lmList =hand[0]['lmList']
    # 'hand[0]' is the first (and only) detected hand.
    # 'lmList' is a list of 21 hand landmarks (points like finger tips, joints, etc.).
    # Each element is [x, y, z], but we mostly care about x and y.

    pointIndex = lmList[8][0:2]
    # Index 8 in the list is the tip of the index finger.
    # [0:2] takes only x and y coordinates (ignoring z).
    # So pointIndex is [x, y] of the index finger tip.

    img = game.update(img, pointIndex)
    # Call the game's update method with the current frame and the index finger position.
    # The game logic uses this position as the snake's head and returns the updated frame with snake, food, etc. drawn.


  cv2.imshow("Image", img)
  # Show the current frame in a window titled "Image".


  key = cv2.waitKey(1)
  # Wait for 1 millisecond for a key press.
  # If no key is pressed, it returns -1. If a key is pressed, it returns its ASCII code.

  if key == ord('r'):
    # If the user presses the 'r' key (ASCII code for 'r'):

    game = SnakeGameClass()
    # Reset the game by re-creating a new SnakeGameClass object.
    # This restarts everything: the snake, score, gameOver flag, and food position.
