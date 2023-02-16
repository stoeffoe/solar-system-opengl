from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *
glutInit()

from PIL import Image
from time import sleep

from SolarFunctions import *
from Planet import *
from Camera import *

moveSensitivity = .3
zoomSensitivity = .5

planets = []
stars = []

timeMultiplier = 86400 # 24*60*60 =86400 seconds; 1 day takes 1 real second




mouseLookingaround = False
def mouseButtonEvent(button, state, x, y):
    global mouseLockPos, mouseLookingaround

    if (state == GLUT_DOWN):
        if (button == GLUT_RIGHT_BUTTON):       # right mouse button lets the user move the camera
            glutSetCursor(GLUT_CURSOR_NONE)
            mouseLockPos = (x,y)
            mouseLookingaround = True           # boolean enables camera movement in mouseMoveEvent

        elif (button == 3): # scollwheel up
            if (camera.distance > 2):
                camera.distance -= zoomSensitivity
            else:
                camera.distance = 2

        elif (button == 4): # scollwheel down
            camera.distance += zoomSensitivity

    else:
        if (button == GLUT_RIGHT_BUTTON):
            glutSetCursor(GLUT_CURSOR_INHERIT)
            mouseLookingaround = False



def mouseMoveEvent(x, y):
    if (mouseLookingaround):

        xoffset = (mouseLockPos[0] - x) * moveSensitivity
        yoffset = (y - mouseLockPos[1]) * moveSensitivity

        camera.yaw += xoffset
        camera.pitch += yoffset

        if (camera.pitch > 89):         # prevents camera from
            camera.pitch = 89          # flipping upside down
        elif (camera.pitch < -89):
            camera.pitch = -89

        glutWarpPointer(*mouseLockPos)  # locks the mouse in place



objectFocusIndex = 0
def keyboardEvent(key, x, y):
    global objectFocusIndex, timeMultiplier

    if (key == GLUT_KEY_LEFT):
        timeMultiplier /= 1.2   # slows time

    elif (key == GLUT_KEY_RIGHT):
        timeMultiplier *= 1.2   # speeds time

    elif (key == GLUT_KEY_UP):
        objectFocusIndex = (objectFocusIndex + 1) % len(allObjects)  # focusses camera on the next planet in the list
        camera.focusingObject = allObjects[objectFocusIndex]

    elif (key == GLUT_KEY_DOWN):
        objectFocusIndex = (objectFocusIndex - 1) % len(allObjects) 
        camera.focusingObject = allObjects[objectFocusIndex]



lastTime = 0
simulationTime = 0
def display():
    global simulationTime, lastTime
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    timeStamp = glutGet(GLUT_ELAPSED_TIME)        
    timeInterval = timeStamp - lastTime        
    lastTime = timeStamp

    simulationTime += timeInterval * timeMultiplier   # timeMultiplier speeds or slows the simulation

    camera.update(simulationTime)   

    glLight(GL_LIGHT0, GL_SPECULAR, [.3, .3, .3])       
    glMaterial(GL_FRONT_AND_BACK, GL_SHININESS, 15)
    for planet in planets:
        planetSunlightVector = subtract(stars[0].position, planet.position)     # renders the light on the planet
        glLight(GL_LIGHT0, GL_POSITION, planetSunlightVector)                  # coming from the 1st star

        planet.draw(simulationTime)


    glLight(GL_LIGHT0, GL_SPECULAR, [2, 2, .9])         # super bright light
    glMaterial(GL_FRONT_AND_BACK, GL_SHININESS, 1)     # that hurts your eyes
    for star in stars:
        sunLightCameraVector = subtract(camera._position, star.position)   # light has to point to the camera
        glLight(GL_LIGHT0, GL_POSITION, sunLightCameraVector)             # so it seems like the star emits in all directions

        star.draw(simulationTime)


    glutSwapBuffers()   # does the display magic





# //------------- OPENGL setup ------------------//

glutInitDisplayMode(GLUT_DEPTH)
glutInitWindowSize(glutGet(GLUT_SCREEN_WIDTH), glutGet(GLUT_SCREEN_HEIGHT))
glutCreateWindow(b"Solar system")
glutFullScreen()

glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
glEnable(GL_BLEND)
glEnable(GL_LINE_SMOOTH)
glEnable(GL_DEPTH_TEST)

glEnable(GL_TEXTURE_2D)

glutDisplayFunc(display)
glutIdleFunc(glutPostRedisplay)

glutMotionFunc(mouseMoveEvent)
glutMouseFunc(mouseButtonEvent)
glutSpecialFunc(keyboardEvent)
glutKeyboardFunc(keyboardEvent)

glEnable(GL_LIGHTING)
glEnable(GL_RESCALE_NORMAL)
glEnable(GL_LIGHT0)

glLight(GL_LIGHT0, GL_DIFFUSE, [3, 3, 3])
glLight(GL_LIGHT0, GL_AMBIENT, [0.3, 0.3, 0.3])
glMaterial(GL_FRONT_AND_BACK, GL_SPECULAR, [1, 1, 1])
glLightModeli(GL_LIGHT_MODEL_COLOR_CONTROL, GL_SEPARATE_SPECULAR_COLOR)

glMatrixMode(GL_MODELVIEW)



# //------------- objects setup ------------------//

sun = Planet(50, (0,0,0), 648, 7.3, None, 0, loadTexture(r"..\textures\sun.jpg"))
stars = [sun]

mercury = Planet(2, (0,14,70), 1408, 2.1, sun, 2100, loadTexture(r"..\textures\mercury.jpg"))
venus = Planet(4, (100,10,0), 2802, 177.3, sun, 5390, loadTexture(r"..\textures\venus.jpg"))
earth = Planet(6, (0,0,-140), 24, 23.5, sun, 8770, loadTexture(r"..\textures\earth.jpg"))
moon = Planet(1, (0,2,-150), 655.72, 1.5, earth, 660, loadTexture(r"..\textures\moon.jpg"))
mars = Planet(3, (-180,5,0), 25, 25.0, sun, 16500, loadTexture(r"..\textures\mars.jpg"))
jupiter = Planet(23, (0,20,260), 10, 3.1, sun, 100000, loadTexture(r"..\textures\jupiter.jpg"))
saturn = Planet(22, (380,30,0), 11, 26.7, sun, 260000, loadTexture(r"..\textures\saturn.jpg"))
uranus = Planet(12, (0,0,-520), 17, 98.0, sun, 740000, loadTexture(r"..\textures\uranus.jpg"))
neptune = Planet(10, (-660,0,0), 16, 28.3, sun, 1440000, loadTexture(r"..\textures\neptune.jpg"))

planets = [mercury, venus, earth, moon, mars, jupiter, saturn, uranus, neptune]


camera = Camera(planets[0], 5, loadTexture(r"..\textures\stars.jpg"))

allObjects = planets + stars

# //----------------------------------------------//


glutMainLoop() # loops display function
