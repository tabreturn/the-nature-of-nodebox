# Example 1.8: Motion 101 (velocity and constant acceleration)

from math import sqrt

class PVector:
    def __init__(self, x_, y_):
        self.x = x_
        self.y = y_
        
    def add(self, v):
        self.x = self.x + v.x
        self.y = self.y + v.y

    def sub(self, v):
        self.x = self.x - v.x
        self.y = self.y - v.y
    
    def mult(self, n):
        self.x = self.x * n
        self.y = self.y * n
        
    def div(self, n):
        self.x = self.x / n
        self.y = self.y / n
        
    def mag(self):
        return sqrt(self.x*self.x + self.y*self.y)
        
    def normalize(self):
        m = self.mag()
        if(m != 0):
            self.div(m)
    
    def limit(self, max):
        if(self.mag() > max):
            self.normalize()
            self.mult(max)
         
class Mover:
    def __init__(self):
        self.location = PVector(WIDTH/2, HEIGHT/2)
        self.velocity = PVector(0, 0)
        self.acceleration = PVector(-0.001, 0.01)
        self.topspeed = 10
    
    def update(self):
        self.velocity.add(self.acceleration)
        self.velocity.limit(self.topspeed)
        self.location.add(self.velocity)
    
    def display(self):
        stroke(0)
        fill(0.6, 0.6)
        oval(self.location.x, self.location.y, 16, 16)
    
    def checkEdges(self):
        if(self.location.x > WIDTH):
            self.location.x = 0
        elif(self.location.x < 0):
            self.location.x = WIDTH
        
        if(self.location.y > HEIGHT):
            self.location.y = 0
        elif(self.location.y < 0):
            self.location.y = HEIGHT


speed(30)
size(200, 200)
background(1)

def setup():
    global mover
    mover = Mover()

def draw():
    global mover
    mover.update()
    mover.checkEdges()
    mover.display()


