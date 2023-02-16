from OpenGL.GLU import *
from OpenGL.GL import *

from SolarFunctions import*
from math import sin, cos, radians


class Camera:

    def __init__(self,focusingObject = None, distance = 1, skyboxTextureID = 0):
        self.skyboxTextureID = skyboxTextureID        
        self.focusingObject = focusingObject    # the planet 
        self.pitch = 0     
        self.yaw = 0                
        self.distance = distance    # viewing distance from the planet; used for zooming in and out
        self._position = (0,0,0)    
        glMatrixMode(GL_PROJECTION)
        gluPerspective(90, 1.777, .1, 3000)    # adds perspective view
        # (FOV, Screen ratio (1920/1080), near clipping plane, far clipping plane)

        self._quadric = gluNewQuadric()         # used for drawing a sphere with a texture
        gluQuadricDrawStyle(self._quadric, GLU_FILL)
        gluQuadricTexture(self._quadric, GL_TRUE)
        gluQuadricNormals(self._quadric, GLU_SMOOTH)


    def update(self, elapsedTime):
        self.focusingObject.update(elapsedTime)
        x = sin(radians(self.yaw)) * cos(radians(self.pitch)) * self.distance + self.focusingObject.position[0] 
        z = cos(radians(self.yaw)) * cos(radians(self.pitch)) * self.distance + self.focusingObject.position[2]
        y = sin(radians(self.pitch)) * self.distance + self.focusingObject.position[1]
        # turn the polar coördinates (pitch, yaw, distance) into cartesian coördinates (x,y,z) to tell opengl where to draw the camera
        self._position = (x,y,z)

        self._updateCamera()
        self._drawSkyBox()

    def _updateCamera(self):
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()    # clear the old camera matrix
        gluLookAt(*self._position, *self.focusingObject.position, 0, 1, 0)
                # (lookFrom,       lookAt,                       upVector)

    def _drawSkyBox(self):
        glMatrixMode(GL_MODELVIEW)
        glPushMatrix()
        glDepthMask(GL_FALSE)                          # draws skybox as last 'behind all objects' 
        glDisable(GL_LIGHTING)  
        glBindTexture(GL_TEXTURE_2D, self.skyboxTextureID)
        glTranslate(*self._position)                   # skybox wraps around the camera
        glRotate(90, 1, 0, 0)                     # rotate to make the image stand up right
        gluSphere(self._quadric, 2, 50, 50)   # simple sphere with a texture
        glDepthMask(GL_TRUE)   
        glEnable(GL_LIGHTING)
        glPopMatrix()
