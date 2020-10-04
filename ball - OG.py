import cv2
import math
import random
import copy

class ball():
    def __init__(self, x, y, radius):
        self.pos = (x,y)
        self.radius = radius
        self.__infected = False
        self.__infection_counter = 0
        self.__has_immunity = False

        # TODO #2 generate a random direction for the velocity, but all balls have constant speed
        #   Hint, use random module!
        x = random.randint(-1, 1)
        y = random.randint(-1, 1)
        x_velocity = x
        y_velocity = y
        self.velocity = [x_velocity, y_velocity]

    def draw(self, img):
        p = tuple([int(x) for x in self.pos]) # convert to int for drawing purposes
        c = (0xFF, 0xFF, 0xFF)
        # TODO #5 the ball should have a different color when infected
        # TODO #6 the ball should have a different color when cured

        cv2.circle(img, p, self.radius, color=c, thickness=-1)

    def move(self, img):
        '''Add the velocity vector to the current position of the ball to move it'''
        self.pos = tuple([sum(x) for x in zip(self.pos, self.velocity)])

    def recover(self):
        '''if infected, slowly recover, and finally be cured and get immunity'''
        # TODO #6 What should happen as a ball recovers after infection?

    def infect(self):
        '''mark this ball as infected if it doesn't have immunity'''
        # TODO #5 What should happen internally when a ball is infected?
        pass

    def isInfected(self):
        '''return whether this ball is infected or not'''
        return self.__infected

class ball_handler():
    def __init__(self, w, h, num_balls):
        self.balls = [ball(random.randint(0, w), random.randint(0, h), 6) for _ in range(num_balls)]

        # TODO #5 Some balls shoudl be infected at startup

    def move(self, img):
        for b in self.balls:
            # TODO #6 This might be a good place to recover
            b.move(img)

        self.collision_handler(img)

    def collision_handler(self, img):
        # TODO #3 Have balls bounce off of walls
        # Hint, use the height and width of your image canvas below to know when to
        #   mark
        h, w, _ = img.shape

        for b in self.balls:
            pass # TODO #3, check for wall hits here

        # -------------------------------------
        # TODO #4 Simulator balls bouncing off each other
        #   Hint: If you have the center point and radius of two balls, what's easiest
        #      equation to determine if they are touching?
        for i, b1 in enumerate(self.balls):
            for b2 in self.balls[i:]:
                # TODO #4 this loop will cycle through each pair of balls
                #   Note: this loop purposefully avoids pairing a ball up with itself,
                #   and a pair of balls that were previously paired
                pass


    def draw(self, img):
        for b in self.balls:
            b.draw(img)

        # TODO #8 Draw three lines of text on the screen for current healthy, infected, and cured counts.



        x = self.__step
        y = math.cos(x)*5
        r = random.randint(-10000,100000)
        mod = math.fmod(r, 100)

            #if mod >= r/2:
        if r < 0:
        #if x > 50:
            if self.velocity[0] > 0:
                self.velocity = [self.velocity[0], y]
            if self.velocity[0] < 0:
                self.velocity = [self.velocity[0], -y]

        #elif mod <= r/2:
        if r > 0:
        #if x < 50:
            if self.velocity[1] > 0:
                self.velocity = [y, self.velocity[1]]
            if self.velocity[1] < 0:
                self.velocity = [-y, self.velocity[1]]
