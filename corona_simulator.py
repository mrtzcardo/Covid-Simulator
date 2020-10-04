import cv2
import numpy as np
from ball import ball_handler
import matplotlib.pyplot as plt
import xlsxwriter

w = 1200
h = 600

bh = ball_handler(w,h, num_balls = 50) # create a ball handler canvas

health_history = bh.health_history
infected_history = bh.infected_history
dead_history = bh.death_history
recover_history = bh.recover_history

while bh.survivors() == True: # cont = contine() while TRUE continue function is true so it can end
    img = np.zeros((h, w, 3), dtype=np.uint8)

    bh.draw(img)

    cv2.imshow("Corona Sim", img)
    cv2.waitKey(1) # this changes how fast your simulation cycles
    bh.move(img)

    #now make it graph the history

x = range(0, len(health_history))
y1 = infected_history
y2 = health_history
y3 = recover_history
y4 = dead_history

# Basic stacked area chart.
plt.stackplot(x, y1, y2, y3, y4, labels=['Infected', 'Healthy', 'Recovered', 'Dead'])
plt.legend(loc='upper left')
plt.show()

# import xlsxwriter module


workbook = xlsxwriter.Workbook('Covid.xlsx')

# By default worksheet names in the spreadsheet will be
# Sheet1, Sheet2 etc., but we can also specify a name.
worksheet = workbook.add_worksheet("coviD")

# Some data we want to write to the worksheet.

# Start from the first cell. Rows and
# columns are zero indexed.
worksheet.write(0, 0, "Infected")
worksheet.write(0, 1, "Healthy")
worksheet.write(0, 2, "Recovered")
worksheet.write(0, 3, "Dead")

row = 1
col = 0

# Iterate over the data and write it out row by row.
for value in y1:
    worksheet.write(row, col, value)
    row += 1

row = 1
for value in y2:
    worksheet.write(row, col+1, value)
    row += 1

row = 1
for value in y3:
    worksheet.write(row, col+2, value)
    row += 1

row = 1
for value in y4:
    worksheet.write(row, col+3, value)
    row += 1

workbook.close()
