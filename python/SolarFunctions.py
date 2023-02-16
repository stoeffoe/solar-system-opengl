from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *

from math import sqrt, sin, cos, atan, pi
from PIL import Image

# function to handle texture loading, returns GLUT's textureID
def loadTexture(fileLocation):
    img = Image.open(fileLocation) 
    glPixelStorei(GL_UNPACK_ALIGNMENT, 1)
    textureID = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, textureID)
    glTexParameter(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glTexParameter(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, img.size[0], img.size[1], 0, GL_RGB, GL_UNSIGNED_BYTE, img.tobytes())
    glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_MODULATE)

    return textureID


def magnitude(vector):  # calculates the magnitude (length) of the vector
    return sqrt( sum( map(lambda x: x*x, vector) ) )


def subtract(vectorA, vectorB): # subtracts two vectors (for directions and distances)
    return tuple( map( lambda x, y: x-y, vectorA, vectorB) )


# calculates the angle of a vector on the XZ plane (like looking from the top down)
def angleOfXZplane(vector):
    dx, dy, dz = vector

    if (dx != 0): angle = atan(dy/dx)   
    else: angle = pi/2     # prevent divide by 0 error

    if (dx < 0):                    # different calculation for
        if (dy < 0): angle -= pi   # each quadrant
        else: angle += pi

    return angle
