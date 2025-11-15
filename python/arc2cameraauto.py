import re
from time import sleep
import logging
import random
import math

def camera(t, transverse, bottomzoom, linezoom, steadyangle, topzoom, angle, easing, lastingtime):
    return f"camera({t:.0f},{transverse:.2f},{bottomzoom:.2f},{linezoom:.2f},{steadyangle:.2f},{topzoom:.2f},{angle:.2f},{easing},{lastingtime:.0f});"

class CameraSum:
  transverse, bottomzoom, linezoom, steadyangle, topzoom, angle = 0, 0, 0, 0, 0, 0
  @staticmethod
  def reset():
    CameraSum.transverse = 0
    CameraSum.bottomzoom = 0
    CameraSum.linezoom = 0
    CameraSum.steadyangle = 0
    CameraSum.topzoom = 0
    CameraSum.angle = 0

class CameraBuffer:
  lastms = 0
  lastduration = 0
  transverse, bottomzoom, linezoom, steadyangle, topzoom, angle = 0, 0, 0, 0, 0, 0
  @staticmethod
  def reset():
    CameraBuffer.transverse = 0
    CameraBuffer.bottomzoom = 0
    CameraBuffer.linezoom = 0
    CameraBuffer.steadyangle = 0
    CameraBuffer.topzoom = 0
    CameraBuffer.angle = 0




def arc2camera(arc):
    arcre = re.compile("(?P<indent> *?)arc\((?P<t1>\d+),(?P<t2>\d+),(?P<x1>-?\d+\.\d+),(?P<x2>-?\d+\.\d+),(?P<easing>[bsio]+),(?P<y1>-?\d+\.\d+),(?P<y2>-?\d+\.\d+),(?P<color>[\-\d]+),(?P<fx>[a-z]+),(?P<is_trace>[a-z]+)\)")
    match = arcre.match(arc)
    if not match:
      return ""
    matchgroup = match.groupdict()
    t1 = int(matchgroup["t1"])
    t2 = int(matchgroup["t2"])
    lastingtime = t2 - t1
    if lastingtime == 0:
      lastingtime = 1
    x1 = float(matchgroup["x1"])
    x2 = float(matchgroup["x2"])
    dx = x2 - x1
    y1 = float(matchgroup["y1"])
    y2 = float(matchgroup["y2"])
    dy = y2 - y1
    easing: str = matchgroup["easing"]
    color = int(matchgroup["color"])
    is_trace = matchgroup["is_trace"] == "true"
    cameraeasing = "l"
    if easing.startswith("si"): cameraeasing = "qo"
    if easing.startswith("so"): cameraeasing = "qi"
    if easing.startswith("b"): cameraeasing = "s"
    if is_trace:
      if t1 == t2:
        CameraSum.reset()
        return camera(t1, 0, 0, 0, 0, 0, 0, "reset", 1)
      else:
        ret = camera(t1,
        -CameraSum.transverse,
        -CameraSum.bottomzoom,
        -CameraSum.linezoom,
        -CameraSum.steadyangle,
        -CameraSum.topzoom,
        -CameraSum.angle,
        cameraeasing, lastingtime)
        CameraSum.reset()
        return ret

    if color == 0:
        if x1 == 0.0 and y1 == -0.2:
          random.seed(t1)
          deg = random.uniform(0,360)
          rad = math.radians(deg)
          xcos = math.cos(rad)
          xsin = math.sin(rad)
          outdx = xcos * dx + xsin * dx
          outdy = -xsin * dx + xcos * dx
          CameraSum.transverse += outdx * 450
          CameraSum.bottomzoom += outdy * 450
          return camera(t1, outdx * 450, outdy * 450, 0, 0, 0, 0, cameraeasing, lastingtime)
        else:
          CameraSum.transverse += dx * 850
          CameraSum.bottomzoom += dy * 450
          if len(easing) == 4:
            cameraeasing2 = "?"
            if easing.endswith("si"): cameraeasing2 = "qo"
            if easing.endswith("so"): cameraeasing2 = "qi"
            if cameraeasing != cameraeasing2:
              return camera(t1, dx * 850, 0, 0, 0, 0, 0, cameraeasing, lastingtime) + "\n" + camera(t1, 0, dy * 450, 0, 0, 0, 0, cameraeasing2, lastingtime)
            else:
              return camera(t1, dx * 850, dy * 450, 0, 0, 0, 0, cameraeasing, lastingtime)
          else:
            return camera(t1, dx * 850, dy * 450, 0, 0, 0, 0, cameraeasing, lastingtime)
    if color == 1:
        if y1 != -0.2:
          CameraSum.linezoom += dy * 1000
          CameraSum.angle += dx * 100
          return camera(t1, 0, 0, dy * 1000, 0, 0, dx * 100, cameraeasing, lastingtime)
        else:
          dx *= 3
          steadymultiplier = 1
          anglemultiplier = -2.6457513110645907
          CameraSum.steadyangle += dx * steadymultiplier
          CameraSum.angle += dx * anglemultiplier
          return camera(t1, 0, 0, 0, dx * steadymultiplier, 0, dx * anglemultiplier, cameraeasing, lastingtime)
    CameraSum.steadyangle += dx * 100
    CameraSum.topzoom += dy * 100
    return camera(t1, 0, 0, 0, dx * 100, dy * 100, 0, cameraeasing, lastingtime)



def conv():
  print("Converting.")
  CameraSum.reset()
  affinfd = open("3.aff", "r")
  affoutfd = open("camera.txt", "w")
  lines = affinfd.read().splitlines()
  for l in lines:
    if l.startswith("camera"): continue
    camcmd = arc2camera(l)
    # if camcmd != l:
    #   affoutfd.write(l + "\n")
    affoutfd.write(camcmd + "\n")
  affinfd.close()
  affoutfd.close()

conv()

