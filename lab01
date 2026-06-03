# Part 01
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *


import random


leftFlag = False
rightFlag = False
class RainDrops:

    def __init__(self):

        self.x = random.randint(0,1200)
        self.y = random.randint(0,900)

        self.speed = random.randint(5,50)
    

    def rainTransition(self):
        self.y = (self.y -self.speed)%900
        if leftFlag == True:
            self.x = (self.x -self.speed)%1200
        elif rightFlag == True:
            self.x = (self.x +self.speed)%1200
        else:
            pass
         


    def drawDrops(self):
        global leftFlag
        global rightFlag

        glVertex2f(self.x,self.y)

        if leftFlag == True:
            glVertex2f(self.x+self.speed,self.y+self.speed)
        elif rightFlag == True:
            glVertex2f(self.x-self.speed,self.y+self.speed)
        else:
            glVertex2f(self.x,self.y+self.speed)


rainObjectList = []

for rainDrops in range(500):
    rainObjectList.append(RainDrops())

def DrawRainDrops():

    glLineWidth(1)
    glColor3f(0.55, 0.6, 0.75)

    glBegin(GL_LINES)
    for objects in rainObjectList:
        objects.drawDrops()
    glEnd()

def animaterain():

    for objects in rainObjectList:
        objects.rainTransition()
    glutPostRedisplay()
 
def drawWindow(x,y,d):
    glLineWidth(5)
    glColor3f(0.0,0.0,0.0)
    glBegin(GL_LINES)
    if d=='v':
        glVertex2f(x,y)
        glVertex2f(x,y-80)
    elif d=='h':
        glVertex2f(x,y)
        glVertex2f(x+80,y)


    glEnd()




def drawSquare(x, y):
    glLineWidth(10) #pixel size. by default 1 thake
    glColor3f(0.4, 0.6, 1.0) # Color Of Wall

    # House Wall
    glBegin(GL_LINES)
    glVertex2f(x,y)
    glVertex2f(x,y-300)

    glVertex2f(x,y-300)
    glVertex2f(x+500,y-300)

    glVertex2f(x+500,y-300)
    glVertex2f(x+500,y)

    glVertex2f(x+500,y)
    glVertex2f(x,y)


    glEnd()

    # Coloring The House Square.
    colorShape(350,450,'wall')

    # Coloring The House Door.
    colorShape(550,300,'door')

    # Coloring The Windows
    colorShape(400,400,'window')
    colorShape(725,400,'window')

    # Axis of the left Window
    drawWindow(440,400,'v')
    drawWindow(400,360,'h')

    # Axis of the right Window
    drawWindow(765,400,'v')
    drawWindow(725,360,'h')

    # Door Nob
    glPointSize(10)
    glColor3f(0.0,0.0,0.0)

    glBegin(GL_POINTS)
    glVertex2f(640,220)
    glEnd()


def drawRoof(x,y):

    glColor3f(1.0, 0.99, 0.82)


    glBegin(GL_TRIANGLES)

    glVertex2f(x,y)
    glVertex2f(300,445)
    glVertex2f(900,445)
    
    glEnd()

def creatingTrees():

    glColor3f(0.0, 0.4, 0.0)
    glBegin(GL_TRIANGLES)
    for lines in range(0,1200,50):
        glVertex2f(lines+50,450)

        glVertex2f(lines-50,350)
        glVertex2f(lines+100,350)


    glEnd()

def colorShape(x,y,typeOf='square'):

    if typeOf=='wall':
        dec = 300
        length =500
        glColor3f(0.4, 0.6, 1.0)

    else:
        glColor3f(1.0, 1.0, 1.0)

        if typeOf == 'door':
            dec = 155
            length = 100
        elif typeOf == 'window':
            dec = 80
            length = 80

    glLineWidth(1)
    glBegin(GL_LINES)
    
    for lines in range(length):
        glVertex2f(x+lines,y)
        glVertex2f(x+lines,y-dec)


    glEnd()


def createBackground(x,y):

    glColor3f(0.545, 0.271, 0.075)

    glLineWidth(10)

    glBegin(GL_LINES)
    for lines in range(1200):
        glVertex2f(x+lines,y)
        glVertex2f(x+lines,y-400)


    glEnd()

shades =0.0

def drawSky():

    glColor3f(shades,shades,shades)
    glLineWidth(10)

    glBegin(GL_LINES)
    for lines in range(1200):
        glVertex2f(lines,400)
        glVertex2f(lines,900)

    glEnd()


def dayNight(eventlistner,x,y):
    global shades,leftFlag,rightFlag
    
    if eventlistner == GLUT_KEY_UP:
        if shades <1.25:
            shades+=0.25
        else:
            print("Din toh hysei bhai ar koto.")
    elif eventlistner == GLUT_KEY_DOWN:
        if shades >0.0:
            shades-=0.25
        else:
            print("Ar kalo kora possible na eitai raat.")

    if eventlistner==GLUT_KEY_RIGHT:
        if(leftFlag == True):
            leftFlag = False
           

        elif(leftFlag == False):
            rightFlag =True

    if eventlistner==GLUT_KEY_LEFT:
        if(rightFlag == True):
            rightFlag = False
            
            
        elif(rightFlag == False):
            leftFlag =True


    glutPostRedisplay()



def iterate():
    glViewport(0, 0, 1200, 900)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0.0, 1200, 0.0, 900, 0.0, 1.0)
    glMatrixMode (GL_MODELVIEW)
    glLoadIdentity()

def showScreen():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    iterate()
    glColor3f(1.0, 1.0, 0.0) #konokichur color set (RGB)
    #call the draw methods here

    drawSky()
    createBackground(0,400)
    creatingTrees()

    drawSquare(350,450)
    drawRoof(600,650)

    DrawRainDrops()
    
    glutSwapBuffers()



glutInit()

glutInitDisplayMode(GLUT_RGBA)

glutInitWindowSize(1200, 900) #window size
glutInitWindowPosition(400, 50)

wind = glutCreateWindow(b"Ek guccho kodom haate, Bhijte Chai Tomar sathe") #window name
glutDisplayFunc(showScreen)

glutIdleFunc(animaterain)

glutSpecialFunc(dayNight)

glutMainLoop()


# Part 02

# from OpenGL.GL import *
# from OpenGL.GLUT import *
# from OpenGL.GLU import *
# import random
# import time

# createdObjects = []
# speed = 0.05

# pauseToggle = False
# blinkToggle = False
# clickToggle = False

# endTime = 0


# class Pointers:


#     def __init__(self,x,y):

#         global speed

#         self.x,self.y=x,y
#         self.r,self.g,self.b = random.uniform(0.0,1.0),random.uniform(0.0,1.0),random.uniform(0.0,1.0)

#         self.randomX = random.choice([speed,-speed])
#         self.randomY = random.choice([speed,-speed])

#         self.tempX = random.choice([speed,-speed])
#         self.tempY =random.choice([speed,-speed])


#         self.tempr,self.tempg,self.tempb =random.uniform(0.0,1.0),random.uniform(0.0,1.0),random.uniform(0.0,1.0)

#     def createPoint(self):
    
#         glColor3f(self.r,self.g,self.b)

#         glVertex2f(self.x,self.y)
    
#     def pointReflections(self):
      

#         self.x += self.randomX
#         self.y += self.randomY

#         if self.x <0 or self.x>1200:
#             self.randomX = self.randomX * -1

#         if self.y <0 or self.y>900:
#             self.randomY = self.randomY * -1

# def drawPoint():

#     glPointSize(10)
#     glBegin(GL_POINTS)

#     for objectPoints in createdObjects:
        
#         objectPoints.createPoint()

#     glEnd()

# def SpecialListner(event,x,y):
#     global speed

#     if event == GLUT_KEY_UP:
#         for objectPoints in createdObjects:
#             if objectPoints.randomX<2 or objectPoints.randomY<2:
#                 objectPoints.randomX*=2
#                 objectPoints.randomY*=2
#                 print("speed x 2")
#             else:
#                 print("Increment Limit Reached")

#     if event == GLUT_KEY_DOWN:
#         for objectPoints in createdObjects:
#             if objectPoints.randomX >0 or objectPoints.randomY>0:
#                 objectPoints.randomX/=2
#                 objectPoints.randomY/=2
#                 print("Speed / 2")
#             else:
#                 print("Decrement objectPoints Reached")

  
#     glutPostRedisplay()

# def KeyBoardListner(event,x,y):
#     global speed,pauseToggle
#     if event == b' ' and pauseToggle == False:
#         for objectPoints in createdObjects:
#             objectPoints.tempX = objectPoints.randomX
#             objectPoints.tempY = objectPoints.randomY
#             objectPoints.randomX = 0
#             objectPoints.randomY = 0
#         pauseToggle = True
#         print("It's magic, it's magic")

#     elif event == b' ' and pauseToggle == True:
#         for objectPoints in createdObjects:
#             objectPoints.randomX = objectPoints.tempX
#             objectPoints.randomY = objectPoints.tempY
#         pauseToggle = False
#         print("It's magic, it's magic")
      
# def mouseListner(eventlistner,state,x,y):
#     global blinkToggle, clickToggle

#     if (eventlistner == GLUT_RIGHT_BUTTON) and (state == GLUT_DOWN):
#         createdObjects.append(Pointers(x,900-y))

#     if (eventlistner == GLUT_LEFT_BUTTON) and (state == GLUT_DOWN):
#         clickToggle  = not clickToggle

#         if clickToggle == False:
#             for objectPoints in createdObjects:

#                 objectPoints.r,objectPoints.g,objectPoints.b = objectPoints.tempr,objectPoints.tempg,objectPoints.tempb
            
        
#     glutPostRedisplay()


# def animatePointer():

#     for objectPoints in createdObjects:
#         objectPoints.pointReflections()

# def animateBlinking():
#     global blinkToggle, clickToggle,endTime

#     if clickToggle:
#         ctime = time.time()
#         if (ctime-endTime)>=0.8:

#             blinkToggle = not blinkToggle
#             endTime = ctime

#             for obj in createdObjects:
#                 if blinkToggle == True:
#                     obj.tempr,obj.tempg,obj.tempb = obj.r,obj.g,obj.b
#                     obj.r,obj.g,obj.b =0.0,0.0,0.0
#                 else:
#                     obj.r,obj.g,obj.b = obj.tempr,obj.tempg,obj.tempb 

# def iterate():
#     glViewport(0, 0, 1200, 900)
#     glMatrixMode(GL_PROJECTION)
#     glLoadIdentity()
#     glOrtho(0.0, 1200, 0.0, 900, 0.0, 1.0)
#     glMatrixMode (GL_MODELVIEW)
#     glLoadIdentity()

# def showScreen():
#     glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
#     glLoadIdentity()
#     iterate()

#     drawPoint()
#     glutSwapBuffers()

# def idleFunctions():
#     animatePointer()
#     animateBlinking()
#     glutPostRedisplay()


# glutInit()
# glutInitDisplayMode(GLUT_RGBA)
# glutInitWindowSize(1200, 900) #window size
# glutInitWindowPosition(400, 50)
# wind = glutCreateWindow(b"Edhar Chala main udhar Chala") #window name
# glutDisplayFunc(showScreen)
# glutIdleFunc(idleFunctions)

# glutMouseFunc(mouseListner)
# glutSpecialFunc(SpecialListner)
# glutKeyboardFunc(KeyBoardListner)


# glutMainLoop()
