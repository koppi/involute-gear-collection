#!/usr/bin/env python
#
# pip install dxfgrapper
#

import dxfgrabber
import math
import sys

# SVG TEMPLATES

SVG_PREAMBLE = \
'<svg xmlns="http://www.w3.org/2000/svg" ' \
'version="1.1" viewBox="{0} {1} {2} {3}">\n'

# SVG_MOVE_TO = 'M {0} {1:.2f} '
# SVG_LINE_TO = 'L {0} {1:.2f} '
# SVG_ARC_TO  = 'A {0} {1:.2f} {2} {3} {4} {5:.2f} {6:.2f} '

SVG_MOVE_TO = 'M {0} {1} '
SVG_LINE_TO = 'L {0} {1} '
SVG_ARC_TO  = 'A {0} {1} {2} {3} {4} {5} {6} '

SVG_PATH = \
'<path d="{0}" fill="none" stroke="{1}" stroke-width="{2:.2f}" />\n'

SVG_LINE = \
'<line x1="{0}" y1="{1}" x2="{2}" y2="{3}" stroke="{4}" stroke-width="{5:.2f}" />\n'

SVG_CIRCLE = \
'<circle cx="{0}" cy="{1}" r="{2}" stroke="{3}" stroke-width="{4}" fill="none" />\n'

# SVG DRAWING HELPERS

def angularDifference(startangle, endangle):
  result = endangle - startangle
  while result >= 360:
    result -= 360
  while result < 0:
    result += 360
  return result

def moveTo(point):
    return SVG_MOVE_TO.format(point.x,height-point.y)

def lineTo(point):
    return SVG_LINE_TO.format(point.x,height-point.y)

def pathStringFromPoints(points):  
  pathString = SVG_MOVE_TO.format(*points[0])
  for i in range(1,len(points)):
    pathString += SVG_LINE_TO.format(*points[i])
  return pathString

# CONVERTING TO SVG

def handleEntity(svgFile, e):
  # TODO: handle colors and thinckness
  # TODO: handle elipse and spline and some other types
  
  if isinstance(e, dxfgrabber.entities.Line):      
    svgFile.write(SVG_LINE.format(
      e.start[0], e.start[1], e.end[0], e.end[1],
      'black', 1          
    ))

  elif isinstance(e, dxfgrabber.entities.LWPolyline):
    pathString = pathStringFromPoints(e)
    if e.is_closed:
      pathString += 'Z'
    svgFile.write(SVG_PATH.format(pathString, 'black', 1))
    
  elif isinstance(e, dxfgrabber.entities.Circle):
    svgFile.write(SVG_CIRCLE.format(e.center[0], e.center[1],
      e.radius, 'black', 1))

  elif isinstance(e, dxfgrabber.entities.Arc):
    
    # compute end points of the arc
    x1 = e.center[0] + e.radius * math.cos(math.pi * e.startangle / 180)
    y1 = e.center[1] + e.radius * math.sin(math.pi * e.startangle / 180)
    x2 = e.center[0] + e.radius * math.cos(math.pi * e.endangle / 180)
    y2 = e.center[1] + e.radius * math.sin(math.pi * e.endangle / 180)

    pathString  = SVG_MOVE_TO.format(x1, y1)
    pathString += SVG_ARC_TO.format(e.radius, e.radius, 0,
      int(angularDifference(e.startangle, e.endangle) > 180), 1, x2, y2)

    svgFile.write(SVG_PATH.format(pathString, 'black', 1))
  elif isinstance(e, dxfgrabber.entities.Insert):
    # TODO: handle group instances
    pass
#end: handleEntity

minx = sys.maxint
maxx = -sys.maxint -1

miny = sys.maxint
maxy = -sys.maxint -1

def bounds(x, y):
  global minx
  global maxx
  global miny
  global maxy
  
  minx = min(minx, x)
  maxx = max(maxx, x)
  miny = min(miny, y)
  maxy = max(maxy, y)

def dxf_bounds_entity(e):
  if isinstance(e, dxfgrabber.entities.Line):
    #        print("%d, %d" % (e.start[0], e.start[1]))
    bounds(e.start[0], e.start[1])
    bounds(e.end[0], e.end[1])
    
  elif isinstance(e, dxfgrabber.entities.LWPolyline):
    linePoints = []
    for i in range(0, len(e)):
      #            print("%d, %d" % (e[i][0], e[i][1]))
      bounds(e[i][0], e[i][1])
    
  elif isinstance(e, dxfgrabber.entities.Arc):
  #        print("%d, %d" % (e.center[0], e.center[1]))
    bounds(e.center[0] + math.cos(d2r(e.startangle))*e.radius, e.center[1] + math.sin(d2r(e.startangle))*e.radius)
    bounds(e.center[0] + math.cos(d2r(e.endangle))*e.radius, e.center[1] + math.sin(d2r(e.endangle))*e.radius)
  
  elif isinstance(e, dxfgrabber.entities.Circle):
    bounds(e.center[0] - e.radius, e.center[1] - e.radius)
    bounds(e.center[0] + e.radius, e.center[1] + e.radius)
  
  else:
    print("dxf_bounds_entity: warning: not implemented: %s" % (e))

def dxf_bounds(es):
  for entity in es:
    dxf_bounds_entity(entity)
                
def saveToSVG(svgFile, dxfData):

  es = [entity for entity in dxfData.entities]

  dxf_bounds(es)
  
  minX = minx
  minY = miny
  maxX = maxx
  maxY = maxy
  
  # TODO: also handle groups
  svgFile.write(SVG_PREAMBLE.format(
    minX, minY, maxX - minX, maxY - minY))

  for entity in dxfData.entities:
    #layer = dxfData.layers[entity.layer]
    #if layer.on:
    #if layer.on and not layer.frozen:
      handleEntity(svgFile, entity)
     
  svgFile.write('</svg>\n')
#end: saveToSVG

if __name__ == '__main__':
  # TODO: error handling
  if len(sys.argv) < 2:
    sys.exit('Usage: {0} file-name'.format(sys.argv[0]))

  filename = sys.argv[1]

  dxfData = dxfgrabber.readfile(filename)

  svgName = '.'.join(filename.split('.')[:-1] + ['svg'])
  svgFile = open(svgName, 'w')

  saveToSVG(svgFile, dxfData)

  print("dxf2svg %s %s" % (filename, svgName))

  svgFile.close()
#end: __main__

