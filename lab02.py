import random
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

W_Width, W_Height = 600,650
catcher_GoingLeft = 0
downWardSpeed = 0

r,g,b=random.uniform(0.0, 1.0),random.uniform(0.0, 1.0),random.uniform(0.0, 1.0)
c_r, c_g, c_b = 1.0, 1.0, 1.0

xPositon = random.randint(-600, 600)

gameOver = False
gamePause = False

score = 0

def allInOneZoneConverter(x, y, zone, toOriginal=False):
    if zone == 0:
        return x, y

    elif zone == 1:
        return (y, x) if not toOriginal else (y, x)

    elif zone == 2:
        return (y, -x) if not toOriginal else (-y, x)

    elif zone == 3:
        return (-x, y) if not toOriginal else (-x, y)

    elif zone == 4:
        return (-x, -y) if not toOriginal else (-x, -y)

    elif zone == 5:
        return (-y, -x) if not toOriginal else (-y, -x)

    elif zone == 6:
        return (-y, x) if not toOriginal else (y, -x)

    elif zone == 7:
        return (x, -y) if not toOriginal else (x, -y)

    else:
        return -1, -1

def findOutZone(x1,y1,x2,y2):

    delX = x2 - x1
    delY = y2 - y1

    if(abs(delX) > abs(delY)) or (abs(delX) == abs(delY)):

        if (delX>=0) and (delY>=0):
            return 0
        if (delX>=0) and (delY<0): 
            return 7
        if(delX<0) and (delY<0):
            return 4
        if(delX<0) and (delY>=0): 
            return 3
            
    elif(abs(delX) < abs(delY)):

        if (delX>0) and (delY>=0):
            return 1
        if (delX>=0) and (delY<0): 
            return 6
        if(delX<0) and (delY<0):
            return 5
        if(delX<0) and (delY>=0): 
            return 2
    return -1
      

def midPointLine(x1,y1,x2,y2):
    dx = x2 - x1
    dy = y2 - y1
    d = 2 * dy - dx
    incX = 2*dy
    incY = 2*dy-2*dx

    newZones = []
    newZones.append((x1, y1))


    while x1 <= x2:
        if d > 0:
            y1 += 1
            d += incY

        else:
            d += incX
        x1 += 1
        
        newZones.append((x1, y1))

    return newZones

def theEightWaySymmetry(x1, y1, x2, y2):
    findZone = findOutZone(x1, y1, x2, y2)
    
    x1not , y1not = allInOneZoneConverter(x1, y1,findZone)

    x2not, y2not = allInOneZoneConverter(x2, y2,findZone)

    newPoints = midPointLine(x1not, y1not, x2not, y2not)

    return (newPoints,findZone)



def drawDiamnod(x1,y1,x2,y2):
    global r, g, b
    newPoints,findZone = theEightWaySymmetry(x1, y1, x2, y2)

    glPointSize(1) 
    glBegin(GL_POINTS)
    glColor3f(r,g,b)

    for point in newPoints:
        x, y = point
        x, y = allInOneZoneConverter(x, y, findZone, toOriginal=True)
       
        glVertex2f(x, y)

    glEnd()

def animateDiamond():
    global downWardSpeed, xPositon, r, g, b, catcher_GoingLeft,gameOver,score,c_r, c_g, c_b
    if not gameOver:

        if not gamePause:

            downWardSpeed += 1+(score*0.5)

            catcher_y = -1130

            if -downWardSpeed <= catcher_y:

                if (-150 + catcher_GoingLeft <= xPositon + 10) and (250 + catcher_GoingLeft >= xPositon - 10):
                
                    downWardSpeed = 0
                    xPositon = random.randint(-600, 600)
                    r, g, b = random.uniform(0, 1), random.uniform(0, 1), random.uniform(0, 1)
                    score += 1
                
                    print(f"Score: {score}")

                else:
                    gameOver = True
                    print()
                    print("Onek khelso, Tomar Khela shesh :)")
                    print(f"Tomar Final Score: {score}")

                    c_r, c_g, c_b = 1.0, 0.0, 0.0
                    r,g,b = 0.0, 0.0, 0.0
                    catcher_GoingLeft = 0
        
    glutPostRedisplay()


def drawCatcher(x1, y1, x2, y2):
    global c_r, c_g, c_b

    newPoints,findZone = theEightWaySymmetry(x1, y1, x2, y2)

    glPointSize(2) 
    glBegin(GL_POINTS)
    glColor3f(c_r, c_g, c_b)
    for point in newPoints:
        x, y = point
        x, y = allInOneZoneConverter(x, y, findZone, toOriginal=True)
       
        glVertex2f(x, y)

    glEnd()

def drawLeftArrow(x1, y1, x2, y2):

    newPoints,findZone = theEightWaySymmetry(x1, y1, x2, y2)

    glPointSize(2) 
    glBegin(GL_POINTS)
    glColor3f(0.0,1.0,1.0)
    for point in newPoints:
        x, y = point
        x, y = allInOneZoneConverter(x, y, findZone, toOriginal=True)
       
        glVertex2f(x, y)

    glEnd()

def drawCross(x1, y1, x2, y2):

    newPoints,findZone = theEightWaySymmetry(x1, y1, x2, y2)

    glPointSize(2) 
    glBegin(GL_POINTS)
    glColor3f(1.0,0.0,0.0)
    for point in newPoints:
        x, y = point
        x, y = allInOneZoneConverter(x, y, findZone, toOriginal=True)
       
        glVertex2f(x, y)

    glEnd()


def drawEntireCross():
    drawCross(525, 575, 575, 525)
    drawCross(525, 525, 575, 575)

def drawPlayButton(x1, y1, x2, y2):

    newPoints,findZone = theEightWaySymmetry(x1, y1, x2, y2)

    glPointSize(2) 
    glBegin(GL_POINTS)
    glColor3f(1.0,1.0,0.0)
    for point in newPoints:
        x, y = point
        x, y = allInOneZoneConverter(x, y, findZone, toOriginal=True)
       
        glVertex2f(x, y)

    glEnd()

def drawEntirePlayButton():
    drawPlayButton(-20, 580, -20, 500)
    drawPlayButton(-20, 580, 20, 540)
    drawPlayButton(-20, 500, 20, 540)



def drawPauseButton(x1, y1, x2, y2):

    newPoints,findZone = theEightWaySymmetry(x1, y1, x2, y2)

    glPointSize(2) 
    glBegin(GL_POINTS)
    glColor3f(1.0,1.0,0.0)
    for point in newPoints:
        x, y = point
        x, y = allInOneZoneConverter(x, y, findZone, toOriginal=True)
       
        glVertex2f(x, y)

    glEnd()

def drawEntirePauseButton():
    drawPauseButton(-20, 570, -20, 530)
    drawPauseButton(20, 570, 20, 530)


def drawEntireLeftArrow():
    drawLeftArrow(-600,550,-500,550)
    drawLeftArrow(-600,550,-580,570)
    drawLeftArrow(-600,550,-580,530)


def drawEntireDiamond():
    global downWardSpeed,xPositon

    drawDiamnod(xPositon, 600-downWardSpeed, xPositon+10, 590-downWardSpeed)
    drawDiamnod(xPositon, 600-downWardSpeed, xPositon-10, 590-downWardSpeed)
    drawDiamnod(xPositon-10, 590-downWardSpeed, xPositon, 580-downWardSpeed)
    drawDiamnod(xPositon, 580-downWardSpeed, xPositon+10, 590-downWardSpeed)


def drawEntireCatcher():

    drawCatcher(-100+catcher_GoingLeft , -600, 200+catcher_GoingLeft , -600) 
    drawCatcher(-150+catcher_GoingLeft, -550, 250+catcher_GoingLeft , -550) 
    drawCatcher(200+catcher_GoingLeft, -600, 250+catcher_GoingLeft , -550) 
    drawCatcher(-150+catcher_GoingLeft, -550, -100+catcher_GoingLeft , -600)


def specialKeys(key, x, y):
    global catcher_GoingLeft
    if not gameOver and not gamePause:
        if key == GLUT_KEY_LEFT:
            if catcher_GoingLeft > -450:
                catcher_GoingLeft-=50
            else:
                print("Onek soraisos left a, thaam eibar.")
        if key == GLUT_KEY_RIGHT:
            if catcher_GoingLeft < 350:
                catcher_GoingLeft+=50 #basically going right
            else:
                print("Onek soraisos right a, thaam eibar.")


    glutPostRedisplay()
   
def mouseListner(button, state, x, y):
    global gamePause,gameOver, score, downWardSpeed, xPositon, r, g, b, c_r, c_g, c_b

    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:

        if (275 <= x <= 332) and (30 <= y <= 107):
            gamePause = not gamePause

        elif (540 <= x <= 570) and (40 <= y <= 85):
            glutLeaveMainLoop()

        elif (14<=x<=71) and (40 <= y <= 85):
            print("Abar Khelaa Shuru koro...")
            gamePause = False
            gameOver = False
            score = 0
            downWardSpeed = 0
            xPositon = random.randint(-500, 500)
            r, g, b = random.uniform(0, 1), random.uniform(0, 1), random.uniform(0, 1)
            c_r, c_g, c_b = 1.0, 1.0, 1.0
            glutPostRedisplay()
        
def display():
    global gamePause, gameOver
   
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    glClearColor(0,0,0,0);

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
   
    glMatrixMode(GL_MODELVIEW)
  
    glLoadIdentity()
  
    gluLookAt(0,0,500,	0,0,0,	0,1,0)
    glMatrixMode(GL_MODELVIEW)

    drawEntireCatcher()
    drawEntireDiamond()
    drawEntireLeftArrow()
    drawEntireCross()
 
    
    if not gamePause and not gameOver:
        drawEntirePauseButton()
    else:
        drawEntirePlayButton()

   

    glutSwapBuffers()


def init():
   
    glClearColor(0,0,0,0)
    
    glMatrixMode(GL_PROJECTION)
  
    glLoadIdentity()
  
    gluPerspective(104,	1,	1,	1000.0)
  


glutInit()

glutInitWindowSize(W_Width, W_Height)

glutInitWindowPosition(400, 0)

glutInitDisplayMode(GLUT_DEPTH | GLUT_DOUBLE | GLUT_RGB)

wind = glutCreateWindow(b"Diamond Digger")
init()

glutSpecialFunc(specialKeys)
glutMouseFunc(mouseListner)

glutDisplayFunc(display)

glutIdleFunc(animateDiamond) 

glutMainLoop()
