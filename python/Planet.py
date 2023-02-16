from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *

from SolarFunctions import*
from math import sqrt, sin, cos, atan, pi

class Planet():

    def __init__(self, radius = 1, position = (0,0,0), dayPeriod = 0, tiltAngle = 0, orbitPlanet = None, orbitPeriod = 0, textureID = 0):
        self.radius = radius
        self.position = position
        self.dayPeriod = dayPeriod  # hours
        self.tiltAngle = tiltAngle   # degrees
        self.setOrbit(orbitPlanet)   
        self.orbitPeriod = orbitPeriod # hours
        self.textureID = textureID

        self._quadric = gluNewQuadric() # quadric used for mapping a texture on a sphere
        gluQuadricDrawStyle(self._quadric, GLU_FILL)
        gluQuadricTexture(self._quadric, GL_TRUE)
        gluQuadricNormals(self._quadric, GLU_SMOOTH)


    def setOrbit(self, orbitPlanet):

        if (orbitPlanet != None):
            self.orbitRadiusVector = subtract(self.position, orbitPlanet.position)
            self.distanceXZradius = magnitude((self.orbitRadiusVector[0], self.orbitRadiusVector[2])) # distance between planets
            self.angleXZplane = angleOfXZplane(self.orbitRadiusVector)  # gets the current angle between its orbiting planet
            self.startAngle = self.angleXZplane # saves the angle it begins with

        self.orbitPlanet = orbitPlanet

    def update(self, elapsedTime):

        if (self.orbitPlanet):
            start = self.startAngle
            radius = self.distanceXZradius
            dy = self.orbitRadiusVector[1]

            # planet only truly orbits on the XZ plane around a planet 
            self.angleXZplane = self.startAngle + (elapsedTime / (self.orbitPeriod * 3600000)) * -2 * pi
            # angle (radians) =                  (current time / time an orbit takes (*3600000 to seconds)) = the percentage of the orbit circle it has traveled
                                                                                                            # times the perimeter of a circle gives the angle in radians
                                                                                                            # (plus the startoffset)
            angle = self.angleXZplane       

            # the vertical movement is a cosine of the current angle times the vertical radius for a simple and fluid up and down motion
            y = cos(angle - start) * dy + self.orbitPlanet.position[1]

            x = cos(angle) * radius + self.orbitPlanet.position[0]
            z = sin(angle) * radius + self.orbitPlanet.position[2]

            self.position = (x,y,z)



    def draw(self, elapsedTime):

        angle = (elapsedTime / (self.dayPeriod * 3600000)) * 360 # glRotate uses degrees instead of radians

        self.update(elapsedTime)

        glBindTexture(GL_TEXTURE_2D, self.textureID)
        glMatrixMode(GL_MODELVIEW)
        glPushMatrix()
        glTranslate(*self.position)         # set position
        glRotate(self.tiltAngle, 0, 0, 1)    # apply tilt 
        glRotate(angle, 0, 1, 0)              # rotate planet around its own axis
        glRotate(90, 1, 0, 0)                  # put the planet upright
        gluSphere(self._quadric, self.radius, 50, 50) # draws the planet
        glPopMatrix()
