#title           :corona_simulator.py
#description     :This program simulates the spread of covid with balls bouncing around a boundary
#author          :Ricardo Martinez
#date            :October 5th 2020
#python_version  :3.8.7  
#email           :mrtzcardo.gmail.com
#github          :github.com/mrtzcardo
#instagram       :@cardo.love
#==============================================================================

import cv2
import numpy as np
from ball import ball_handler
import matplotlib.pyplot as plt
from stats import xlsx_stats

w = 1400            # desired width of screen 1200
h = 800             # desired height of screen 600
inf_pop = .2        # desired inital percentange  of infected population 
at_risk_pop = .6    # desired risk factor muliplier (decreases time on death clock by a given percentage)
num_balls = 80      # desired number of balls/samples 

bh = ball_handler(w,h, num_balls, at_risk_pop, inf_pop) # create a ball handler canvas

health_history = bh.health_history
infected_history = bh.infected_history
dead_history = bh.death_history
recover_history = bh.recover_history

while bh.survivors() == True: # while is not completely dead or recovered
    img = np.zeros((h, w, 3), dtype=np.uint8)

    bh.draw(img)

    cv2.imshow("Corona Sim", img)
    cv2.waitKey(1) # this changes how fast the simulation cycles
    bh.move(img)


# graph of health data over time
x = range(0, len(health_history))
y1 = infected_history
y2 = health_history
y3 = recover_history
y4 = dead_history

# Basic stacked area chart
plt.stackplot(x, y1, y2, y3, y4, labels=['Infected', 'Healthy', 'Recovered', 'Dead'])
plt.legend(loc='upper left')
plt.show()

# exports data to .xlsx file
#xlsx_stats(y1, y2, y3, y4)