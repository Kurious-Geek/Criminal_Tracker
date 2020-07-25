from os import path
import sys


if getattr(sys, 'frozen', False):
    image_directory = path.join(path.dirname(sys.executable), 'images')
else:
    image_directory = path.dirname(__file__)

ctracker_32 = path.join(image_directory, 'ctracker_logo-32x20.gif')
ctracker_64 = path.join(image_directory, 'ctracker_logo-64x45.gif')
