# Example 6.4: Flow field following

from PVector import *
from Particle import *
from math import *
from Simplex import *

def constrain(amt, low, high):
        if amt < low: return low
        elif amt > high: return high
        else: return amt

def map(value, in_from, in_to, out_from, out_to):
    out_range = out_to-out_from
    in_range = in_to-in_from
    in_val = value-in_from
    val=(float(in_val)/in_range)*out_range
    out_val = out_from+val
    return out_val


class Vehicle:
    def __init__(self, x, y):
        self.acceleration = PVector(0, 0)
        self.velocity = PVector(random(-3,3), random(-3,3))
        self.location = PVector(x, y)
        self.r = 3.
        self.maxspeed = 4.
        self.maxforce = 0.15
    
    def update(self):
        self.velocity.add(self.acceleration)
        self.velocity.limit(self.maxspeed)
        self.location.add(self.velocity)
        self.acceleration.mult(0)
    
    def applyForce(self, force):
        self.acceleration.add(force)
    
    def seek(self, target):
        desired = PVector.subStatic(target, self.location)
        desired.normalize()
        desired.mult(self.maxspeed)
        steer = PVector.subStatic(desired, self.velocity)
        steer.limit(self.maxforce)
        self.applyForce(steer)
    
    def arrive(self, target):
        desired = PVector.subStatic(target, self.location)
        d = desired.mag()
        desired.normalize()
        if(d < 100):
            m = map(d, 0, 100, 0, self.maxspeed)
            desired.mult(m)
        else:
            desired.mult(self.maxspeed)
        steer = PVector.subStatic(desired, self.velocity)
        steer.limit(self.maxforce)
        self.applyForce(steer)
    
    def follow(self, flow):
        desired = flow.lookup(self.location)
        desired.mult(self.maxspeed)
        steer = PVector.subStatic(desired, self.velocity)
        steer.limit(self.maxforce)
        self.applyForce(steer)
        
    def boundaries(self, d):
        desired = False
        
        if(self.location.x < d):
            desired = PVector(self.maxspeed, self.velocity.y)
        elif(self.location.x > WIDTH-d):
            desired = PVector(-self.maxspeed, self.velocity.y)
        
        if(self.location.y < d):
            desired = PVector(self.velocity.x, self.maxspeed)
        elif(self.location.y > HEIGHT-d):
            desired = PVector(self.velocity.x, -self.maxspeed)
        
        if(desired):
            desired.normalize()
            desired.mult(self.maxspeed)
            steer = PVector.subStatic(desired, self.velocity)
            steer.limit(self.maxforce)
            self.applyForce(steer)
            
    def display(self):
        theta = self.velocity.heading() + pi/2
        fill(0,6)
        stroke(0)
        push()
        translate(self.location.x, self.location.y)
        rotate(radians = theta*-1)
        beginpath(0, -self.r*2)
        lineto(-self.r, self.r*2)
        lineto(self.r, self.r*2)
        endpath()
        pop()
    
    def run(self):
        self.update()
        self.display()

class FlowField:
    def __init__(self, r):
        self.resolution = r
        self.cols = WIDTH/self.resolution
        self.rows = HEIGHT/self.resolution
        self.field = [[]]*self.cols
        self.init()
    
    def init(self):
        xoff = 0.
        for i in range(self.cols):
            yoff = 0.
            for j in range(self.rows):
                noise = octave_noise_2d(4, 0.5, 10, xoff, yoff)
                theta = map(noise, -0.5, 0.5, 0, pi*2)
                self.field[i].append(PVector(cos(theta), sin(theta)))
                yoff += 0.1
        xoff += 0.1
        
    def lookup(self, lookup):
        column = int(constrain(lookup.x/self.resolution, 0, self.cols-1))
        row = int(constrain(lookup.y/self.resolution, 0, self.rows-1))
        return self.field[column][row]


speed(60)        
size(400, 400)
background(1)

def setup():
    global f, r, v
    r = 10
    f = FlowField(r)
    v = Vehicle(WIDTH/2, HEIGHT/2)
    
def draw():
    global f, r, v
    v.follow(f)
    v.run()
    
    nofill()
    stroke(0)


