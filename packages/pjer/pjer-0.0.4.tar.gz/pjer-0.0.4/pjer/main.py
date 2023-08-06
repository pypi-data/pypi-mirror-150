import turtle
class sprite():
    def __init__(self, model, speed):
      turtle.pencolor('#000000')
      self.model = model
      turtle.speed(speed)

    def create(self, x, y):
        self.id = {
          "x":x,
          "y":y
        }

    def draw(self,x,y, diffrence):
      turtle.penup()
      turtle.goto(x,y)
      turtle.pensize(diffrence)
      turtle.ht()
      for i in range(len(self.model)):
        if i==4 or i==8 or i==12:
          turtle.penup()
          turtle.back(4*diffrence)
          turtle.right(90)
          turtle.forward(diffrence)
          turtle.left(90)
        
        if self.model[i]==1:
          turtle.pendown()
          turtle.forward(0)
          turtle.penup()
          turtle.forward(diffrence)
        elif self.model[i]==0:
          turtle.penup()
          turtle.forward(diffrence)
        
        turtle.ht()

    def undraw(self,x,y,diffrence):
      turtle.penup()
      turtle.goto(x,y)
      turtle.pencolor('#ffffff')
      for i in range(len(self.model)):
        if i==4 or i==8 or i==12:
          turtle.penup()
          turtle.back(4*diffrence)
          turtle.right(90)
          turtle.forward(diffrence)
          turtle.left(90)
        
        if self.model[i]==1:
          turtle.pendown()
          turtle.forward(0)
          turtle.penup()
          turtle.forward(diffrence)
        elif self.model[i]==0:
          turtle.penup()
          turtle.forward(diffrence)
        
        turtle.ht()