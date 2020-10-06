#==============================================================================
#title           :ball.py
#description     :This program creates and handles balls for COVID simulation
#author          :Ricardo Martinez
#date            :October 5th 2020
#python_version  :3.8.7  
#email           :mrtzcardo@gmail.com
#github          :github.com/mrtzcardo
#instagram       :@cardo.love
#==============================================================================

import cv2
import math
import random

class ball():

    '''Initalizing variables that will be used though out code'''
    def __init__(self, x, y, radius):
        self.pos = (x,y)
        self.radius = radius
        self.__infection = 0
        self.__death_clock = 0
        self.__death = 0
        self.__total_infected = 0
        self.__total_cured = 0
        self.__total_dead = 0
        self.__step = 0
        self.__has_immunity = False
        self.__is_dead = False
        self.__at_risk = False

        '''Giving a random direction for velocity'''
        x_velocity = random.randint(-100, 100) / 100
        y_velocity = random.randint(-100, 100) / 100
        self.velocity = [x_velocity, y_velocity]

    
    def draw(self, img):
        '''Gives colors to balls based on their health status: healthy, infected, cured, dead'''
        p = tuple([int(x) for x in self.pos]) # convert to int for drawing purposes
        c = (0xFF, 0xFF, 0xFF)
        i = (0x00,0x00,0xFF)
        r = (0xFF,0x00,0x00)
        d = (0x40,0x40,0x40)

        if not self.isInfected() and not self.isRecovered() and not self.isDead():
            cv2.circle(img, p, self.radius, color=c, thickness=-1)
        elif self.isDead():
            cv2.circle(img, p, self.radius, color=d, thickness=-1)
        elif self.isInfected() and not self.isRecovered():
            cv2.circle(img, p, self.radius, color=i, thickness=-1)
        elif self.isRecovered():
            cv2.circle(img, p, self.radius, color=r, thickness=-1)

    def move(self, img):
        '''Adds the velocity vector to the current position of the ball to move it'''
        self.pos = tuple([sum(x) for x in zip(self.pos, self.velocity)])

        # stops balls from moving if dead
        if self.__is_dead:
            self.velocity = [0, 0]
        self.pos = tuple([sum(x) for x in zip(self.pos, self.velocity)])
        self.__step += .1

    def risk(self):
        '''This flags ball as being in the portion of the population more likely to die if infected'''
        self.__at_risk = True

    def infect(self):
        '''Marks ball as infected giving them an infection value for rate of recovery and death clock'''
        
        # risk factor which decreases death clock count down by a given factor
        risk_factor = .5

        if self.isInfected() or self.__has_immunity:
            pass
        else:
            # initializes infection values
            self.__infection = random.randint(1000,1500)

            # initializes death clock value
            self.__death_clock = random.randint(1400, 1900)

            # adds multiplier to death clock if at risk
            if self.__at_risk:
                self.__death_clock = self.__death_clock * risk_factor

    def recover(self):
        '''Once infected they slowly recover then once recovered get immunity'''

        # if infection value reaches 0 then recovered/immune, else if death clock reaches 0 first they die
        if self.isInfected() and not self.__is_dead:
            self.__infection -= 1
            if self.__infection < 1:
                self.__has_immunity = True
                self.__infection = 0

    def dead(self):
        '''return whether ball is dead or not'''
        if self.isInfected():
            self.__death_clock -= 1
            if self.__death_clock < 0:
                self.__death_clock = -2
                self.__is_dead = True
                self.__infection = 0

    def isInfected(self):
        '''return whether this ball is infected or not'''
        return self.__infection >= 1

    def isDead(self):
        '''return whether this ball is dead or not, if __death_clock > 1 then true'''
        return self.__death_clock <= -1

    def isRecovered(self):
        '''return whether this ball is recovered or not'''
        return self.__has_immunity

class ball_handler():

    def __init__(self, w, h, num_balls, at_risk_pop, inf_pop):
        self.balls = [ball(random.randint(0, w), random.randint(0, h), 6) for _ in range(num_balls)]

        # infects population
        for i, b in enumerate(self.balls):
            if i < len(self.balls) * inf_pop:
                b.infect()

        # gives at risk status to portion of population
        for i, b in enumerate(self.balls):
            if i < len(self.balls) * at_risk_pop:
                b.risk()

    # creates lists for storing health status data
    health_history = []
    infected_history = []
    death_history = []
    recover_history = []


    def move(self, img):
        '''moves ball as well as where balls step towards recovery/death/none'''
        for b in self.balls:
            b.recover()
            b.dead()
            b.move(img)

        self.collision_handler(img)

    def collision_handler(self, img):
        '''function that causes balls to bounce off boundary'''

        h, w, _ = img.shape

        for b in self.balls:
            x = b.pos[0]
            y = b.pos[1]

            if y < b.radius or y > h - b.radius:
                b.velocity[1] *= -1
            if x < b.radius or x > w-b.radius:
                b.velocity[0] *= -1


        for i, b1 in enumerate(self.balls):
            for b2 in self.balls[i:]:
                x1 = b1.pos[0]
                x2 = b2.pos[0]
                y1 = b1.pos[1]
                y2 = b2.pos[1]
                distance = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
                tempvel = 0

                #if balls touch, they infect one another
                touching = distance <= (b1.radius + b2.radius)
                if b1.isDead() or b2.isDead():
                    pass;
                elif touching:
                    tempvel = b1.velocity
                    b1.velocity = b2.velocity
                    b2.velocity = tempvel
                    if not b1.isInfected() and not b2.isInfected():
                        pass;
                    elif b1.isInfected():
                        b2.infect()
                    elif b2.isInfected():
                        b1.infect()
                pass


    def draw(self, img):
        '''draws balls and edits health data'''
        infect = 0
        recovered = 0
        healthy = 0
        dead = 0

        for b in (self.balls):
            if b.isInfected():
                infect += 1
            elif b.isRecovered():
                recovered += 1
            elif b.isDead():
                dead += 1
            else:
                healthy += 1
            b.draw(img)

        # adds health status to lists
        self.health_history += [healthy]
        self.infected_history += [infect]
        self.death_history += [dead]
        self.recover_history += [recovered]


    def survivors(self):
        '''stops while loop once entire population dies or recovers'''
        x = 1
        for b in self.balls:
            if len(self.infected_history) == 0:
                pass
            elif len(self.infected_history) != 0:
                x = self.infected_history[len(self.infected_history)-1]
            return x > 0