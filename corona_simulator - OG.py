import cv2
import numpy as np
from ball import ball_handler

w = 700
h = 700


# TODO #1 Create more than one ball
bh = ball_handler(w,h, num_balls = 1) # create a ball handler canvas

while True:
    img = np.zeros((h, w, 3), dtype=np.uint8)

    bh.draw(img)

    cv2.imshow("Corona Sim", img)
    cv2.waitKey(20) # this changes how fast your simulation cycles

    bh.move(img)
