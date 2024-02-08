import numpy as np
from schemdraw.flow import Box, Connect
import math
from schemdraw.util import linspace

from schemdraw.segments import Segment
from schemdraw.elements import Element, Element2Term
from schemdraw.elements.switches import Switch

from schemdraw.types import ActionType, XY

from typing import Sequence, Union
from schemdraw.util import Point

gap = (math.nan, math.nan)  # Put a gap in a path


class Cylinder(Box):
    ''' Flowchart cylinder

        Args:
            w: Width of cylinder
            h: Height of cylinder
            d: depth of cylinder

        Anchors:
            * 16 compass points (N, S, E, W, NE, NNE, etc.)
    '''

    def __init__(self, w: float = 3, h: float = 2, d: float = 2, phi: float = 0, subframe: bool = False, **kwargs):
        super().__init__(w, h, **kwargs)
        while (0 > phi and phi > 360):
            if phi < 0:
                phi += 360
            else:
                phi -= 360

        phirad = phi * math.pi / 180
        dx = math.cos(phirad) * d
        dy = math.sin(phirad) * d

        X = -(w / 2) ** 2 * math.tan(phirad) / (math.sqrt((w / 2) ** 2 * math.tan(phirad) ** 2 + (h / 2) ** 2))
        Y = (h / 2) ** 2 / (math.sqrt((w / 2) ** 2 * math.tan(phirad) ** 2 + (h / 2) ** 2))

        dphi = math.acos(X / (w / 2)) - math.pi / 2

        self.segments = []

        t1 = linspace(math.pi / 2 + dphi, 3 * math.pi / 2 + dphi, num=25) if (phi > 270 or phi <= 90) \
            else linspace(-math.pi / 2 + dphi, math.pi / 2 + dphi, num=25)
        y = [(h / 2) * math.sin(t0) for t0 in t1]
        x = [(w / 2) * math.cos(t0) + w / 2 for t0 in t1]
        y.append(y[-1] + dy)
        x.append(x[-1] + dx)
        t2 = linspace(-math.pi / 2 + dphi, math.pi / 2 + dphi, num=25) if (phi > 270 or phi <= 90) \
            else linspace(math.pi / 2 + dphi, 3 * math.pi / 2 + dphi, num=25)
        y.extend([(h / 2) * math.sin(t0) + dy for t0 in t2])
        x.extend([(w / 2) * math.cos(t0) + w / 2 + dx for t0 in t2])
        y.append(y[0])
        x.append(x[0])
        self.segments.append(Segment(list(zip(x, y))))
        t3 = linspace(-math.pi / 2 + dphi, math.pi / 2 + dphi, num=25) if (phi > 270 or phi <= 90) \
            else linspace(math.pi / 2 + dphi, 3 * math.pi / 2 + dphi, num=25)
        y1 = ([(h / 2) * math.sin(t0) for t0 in t3])
        x1 = [(w / 2) * math.cos(t0) + w / 2 for t0 in t3]
        self.segments.append(Segment(list(zip(x1, y1))))
        if subframe:
            t4 = linspace(math.pi / 2 + dphi, 3 * math.pi / 2 + dphi, num=25) if (phi > 270 or phi <= 90) \
                else linspace(-math.pi / 2 + dphi, math.pi / 2 + dphi, num=25)
            y2 = ([(h / 2) * math.sin(t0) + dy for t0 in t4])
            x2 = [(w / 2) * math.cos(t0) + w / 2 + dx for t0 in t4]
            self.segments.append(Segment(list(zip(x2, y2)), ls="--"))

        self.anchors['center'] = (w / 2 + dx / 2, dy / 2)
        self.anchors['centerTop'] = (
            w / 2 + dx / 2 + w / 2 * math.cos(dphi + math.pi / 2), dy / 2 + h / 2 * math.sin(dphi + math.pi / 2))
        self.anchors['centerBot'] = (
            w / 2 + dx / 2 - w / 2 * math.cos(dphi + math.pi / 2), dy / 2 - h / 2 * math.sin(dphi + math.pi / 2))
        self.anchors['centerMain'] = (w / 2, 0)
        self.anchors['centerSub'] = (w / 2 + dx, dy)

        self.anchors['N'] = (w / 2, h / 2)
        self.anchors['S'] = (w / 2, -h / 2)
        self.anchors['W'] = (0, 0)
        self.anchors['E'] = (w, 0)
        self.anchors['subN'] = (w / 2 + dx, h / 2 + dy)
        self.anchors['subS'] = (w / 2 + dx, -h / 2 + dy)
        self.anchors['subE'] = (w + dx, dy)
        self.anchors['subW'] = (0 + dx, dy)

        self.anchors['NW'] = (w / 2 + w / 2 * math.cos(math.pi * 3 / 4), h / 2 * math.sin(math.pi * 3 / 4))
        self.anchors['SW'] = (w / 2 + w / 2 * math.cos(math.pi * 3 / 4), h / 2 * math.sin(math.pi * 5 / 4))
        self.anchors['NE'] = (w / 2 + w / 2 * math.cos(math.pi * 1 / 4), h / 2 * math.sin(math.pi * 3 / 4))
        self.anchors['SE'] = (w / 2 + w / 2 * math.cos(math.pi * 1 / 4), h / 2 * math.sin(math.pi * 5 / 4))

        self.anchors['subNW'] = (w / 2 + w / 2 * math.cos(math.pi * 3 / 4) + dx, h / 2 * math.sin(math.pi * 3 / 4) + dy)
        self.anchors['subSW'] = (w / 2 + w / 2 * math.cos(math.pi * 3 / 4) + dx, h / 2 * math.sin(math.pi * 5 / 4) + dy)
        self.anchors['subNE'] = (w / 2 + w / 2 * math.cos(math.pi * 1 / 4) + dx, h / 2 * math.sin(math.pi * 3 / 4) + dy)
        self.anchors['subSE'] = (w / 2 + w / 2 * math.cos(math.pi * 1 / 4) + dx, h / 2 * math.sin(math.pi * 5 / 4) + dy)

        self.anchors['NNW'] = (w / 2 + w / 2 * math.cos(math.pi * 5 / 8), h / 2 * math.sin(math.pi * 5 / 8))
        self.anchors['SSW'] = (w / 2 + w / 2 * math.cos(math.pi * 11 / 8), h / 2 * math.sin(math.pi * 11 / 8))
        self.anchors['NNE'] = (w / 2 + w / 2 * math.cos(math.pi * 3 / 8), h / 2 * math.sin(math.pi * 3 / 8))
        self.anchors['SSE'] = (w / 2 + w / 2 * math.cos(math.pi * 13 / 8), h / 2 * math.sin(math.pi * 13 / 8))

        self.anchors['subNNW'] = (
            w / 2 + w / 2 * math.cos(math.pi * 5 / 8) + dx, h / 2 * math.sin(math.pi * 5 / 8) + dy)
        self.anchors['subSSW'] = (
            w / 2 + w / 2 * math.cos(math.pi * 11 / 8) + dx, h / 2 * math.sin(math.pi * 11 / 8) + dy)
        self.anchors['subNNE'] = (
            w / 2 + w / 2 * math.cos(math.pi * 3 / 8) + dx, h / 2 * math.sin(math.pi * 3 / 8) + dy)
        self.anchors['subSSE'] = (
            w / 2 + w / 2 * math.cos(math.pi * 13 / 8) + dx, h / 2 * math.sin(math.pi * 13 / 8) + dy)

        self.anchors['WNW'] = (w / 2 + w / 2 * math.cos(math.pi * 7 / 8), h / 2 * math.sin(math.pi * 7 / 8))
        self.anchors['WSW'] = (w / 2 + w / 2 * math.cos(math.pi * 9 / 8), h / 2 * math.sin(math.pi * 9 / 8))
        self.anchors['ENE'] = (w / 2 + w / 2 * math.cos(math.pi * 1 / 8), h / 2 * math.sin(math.pi * 1 / 8))
        self.anchors['ESE'] = (w / 2 + w / 2 * math.cos(math.pi * 15 / 8), h / 2 * math.sin(math.pi * 15 / 8))

        self.anchors['subWNW'] = (
            w / 2 + w / 2 * math.cos(math.pi * 7 / 8) + dx, h / 2 * math.sin(math.pi * 7 / 8) + dy)
        self.anchors['subWSW'] = (
            w / 2 + w / 2 * math.cos(math.pi * 9 / 8) + dx, h / 2 * math.sin(math.pi * 9 / 8) + dy)
        self.anchors['subENE'] = (
            w / 2 + w / 2 * math.cos(math.pi * 1 / 8) + dx, h / 2 * math.sin(math.pi * 1 / 8) + dy)
        self.anchors['subESE'] = (
            w / 2 + w / 2 * math.cos(math.pi * 15 / 8) + dx, h / 2 * math.sin(math.pi * 15 / 8) + dy)


class Arc(Box):
    def __init__(self, theta1: float = 0, theta2: float = 90, r: float = 1, **kwargs):
        super().__init__(w=r * 2, h=r * 2, **kwargs)
        self.theta1 = theta1 * math.pi / 180
        self.theta2 = theta2 * math.pi / 180
        self.r = r
        self.segments = []
        t1 = linspace(self.theta1, self.theta2, num=100)
        y = [self.r * math.sin(t0) for t0 in t1]
        x = [self.r * math.cos(t0) + r for t0 in t1]
        self.segments.append(Segment(list(zip(x, y))))
        # self.anchors['center'] = (0, 0)


class Arc2(Box):
    def __init__(self, theta1: float = 0, arrow: str = None, theta2: float = 90, w: float = 2, h: float = 1, **kwargs):
        super().__init__(w, h, **kwargs)

        self.theta1 = theta1 * math.pi / 180
        self.theta2 = theta2 * math.pi / 180
        self.w = w
        self.h = h
        self.segments = []
        t1 = linspace(self.theta1, self.theta2, num=100)
        y = [(self.h / 2 * math.sin(t0)) for t0 in t1]
        x = [(self.w / 2 * math.cos(t0) + w / 2) for t0 in t1]

        self.segments.append(Segment(list(zip(x, y))))

        # self.anchors['center'] = (0, 0)


class Queue(Element2Term):
    def __init__(self, *d,
                 double: bool = False,
                 headwidth: float = 0.15, headlength: float = 0.25,
                 qsize: float = 1,
                 arrow: str = None,
                 **kwargs):
        super().__init__(*d, arrowlength=headlength,
                         arrowwidth=headwidth, arrow=arrow,
                         **kwargs)
        self.headlength = headlength
        self.headwidth = headwidth
        self.arrow = arrow
        self.qsize = qsize

        self.segments.append(Segment([(0, 0), gap, (qsize, 0)],
                                     arrow=self.arrow,
                                     arrowlength=self.headlength,
                                     arrowwidth=self.headwidth
                                     ))
        qsegsize = self.qsize / 4
        x1 = [0, 0 + 4 * qsegsize, 0 + 4 * qsegsize, 0]
        y1 = [0 + qsegsize, 0 + qsegsize, 0 - qsegsize, 0 - qsegsize]
        x1.append(x1[0])
        y1.append(y1[0])
        self.segments.append(Segment(list(zip(x1, y1))))
        self.segments.append(Segment([(0 + 3 * qsegsize, 0 + qsegsize), (0 + 3 * qsegsize, 0 - qsegsize)]))
        self.segments.append(Segment([(0 + 2 * qsegsize, 0 + qsegsize), (0 + 2 * qsegsize, 0 - qsegsize)]))
        self.segments.append(Segment([(0 + qsegsize, 0 + qsegsize), (0 + qsegsize, 0 - qsegsize)]))


class SwitchClosed(Switch):
    def __init__(self, *d,
                 action: ActionType = None,
                 **kwargs,
                 ):
        """Closed switch"""
        super().__init__(*d, action=action, **kwargs)

        self.segments[0] = (Segment([(0, 0), gap, (0.12 * 2, .1), (1 - 0.12 * 2, .1), gap, (1, 0)]))


class Interrupt(Element2Term):
    def __init__(self, *d, arrow: str = "<-", **kwargs):
        super().__init__(*d, **kwargs)
        self.segments.append(Segment([(0, 0), (-0.2, 0.2)], arrow=arrow))


class Cube(Box):
    ''' Flowchart Cube
        Args:
            w: Width of cube
            h: Height of cube
            d: depth of cube
            phi: angle of depth
        Anchors:
            * 16 compass points (N, S, E, W, NE, NNE, etc.)
    '''

    def __init__(self, w: float = 3, h: float = 2, d: float = 2, phi: float = 30, **kwargs):
        super().__init__(w, h, **kwargs)
        while (0 > phi or phi > 360):
            if phi < 0:
                phi += 360
            else:
                phi -= 360
        print(phi)
        phirad = phi * math.pi / 180
        d = abs(math.sin(phirad) * d)

        dx = math.cos(phirad) * d
        dy = math.sin(phirad) * d
        if phi <= 90 and phi >= 0:
            x = [0, dx, dx + w, dx + w, w, w, 0]
            y = [h / 2, dy + h / 2, dy + h / 2, dy - h / 2, -h / 2, h / 2, h / 2]
            self.segments.append(Segment([(w, h / 2), (w + dx, h / 2 + dy)]))
        elif phi > 90 and phi <= 180:
            x = [w, dx + w, dx, dx, 0, 0, w]
            y = [h / 2, dy + h / 2, dy + h / 2, dy - h / 2, -h / 2, h / 2, h / 2]
            self.segments.append(Segment([(0, h / 2), (dx, h / 2 + dy)]))
        elif phi > 180 and phi <= 270:
            x = [0, dx, dx, dx + w, w, 0, 0]
            y = [h / 2, dy + h / 2, dy - h / 2, dy - h / 2, -h / 2, -h / 2, h / 2]
            self.segments.append(Segment([(0, -h / 2), (dx, -h / 2 + dy)]))
        else:
            x = [w, dx + w, dx + w, dx, 0, w, w]
            y = [h / 2, dy + h / 2, dy - h / 2, dy - h / 2, -h / 2, -h / 2, h / 2]
            self.segments.append(Segment([(w, -h / 2), (dx + w, -h / 2 + dy)]))
        self.segments.append(Segment(list(zip(x, y))))


class Ellipse(Box):
    ''' Flowchart ellipse

        Args:
            w: Width of ellipse
            h: Height of ellipse

        Anchors:
            * 16 compass points (N, S, E, W, NE, NNE, etc.)
    '''

    def __init__(self, w: float = 3, h: float = 2, **kwargs):
        super().__init__(w, h, **kwargs)
        self.segments = []
        # There's no ellipse Segment type, so draw one with a path Segment
        t = linspace(0, math.pi * 2, num=50)
        y = [(h / 2) * math.sin(t0) for t0 in t]
        x = [(w / 2) * math.cos(t0) + w / 2 for t0 in t]
        x[-1] = x[0]
        y[-1] = y[0]  # Ensure the path is actually closed
        self.segments.append(Segment(list(zip(x, y))))
        sinpi4 = math.sin(math.pi / 4)
        cospi4 = math.cos(math.pi / 4)
        sinpi8 = math.sin(math.pi / 8)
        cospi8 = math.cos(math.pi / 8)
        self.anchors['SE'] = (w / 2 + w / 2 * cospi4, -h / 2 * sinpi4)
        self.anchors['SW'] = (w / 2 - w / 2 * cospi4, -h / 2 * sinpi4)
        self.anchors['NW'] = (w / 2 - w / 2 * cospi4, h / 2 * sinpi4)
        self.anchors['NE'] = (w / 2 + w / 2 * cospi4, h / 2 * sinpi4)
        self.anchors['ENE'] = (w / 2 + w / 2 * cospi8, h / 2 * sinpi8)
        self.anchors['WNW'] = (w / 2 - w / 2 * cospi8, h / 2 * sinpi8)
        self.anchors['ESE'] = (w / 2 + w / 2 * cospi8, -h / 2 * sinpi8)
        self.anchors['WSW'] = (w / 2 - w / 2 * cospi8, -h / 2 * sinpi8)
        self.anchors['NNE'] = (w / 2 + w / 2 * sinpi8, h / 2 * cospi8)
        self.anchors['NNW'] = (w / 2 - w / 2 * sinpi8, h / 2 * cospi8)
        self.anchors['SSE'] = (w / 2 + w / 2 * sinpi8, -h / 2 * cospi8)
        self.anchors['SSW'] = (w / 2 - w / 2 * sinpi8, -h / 2 * cospi8)


class SineWave(Element):
    ''' Sine wave

        Args:
            w: Width of sine wave
            h: Height of sine wave
            segments: Number of segments to draw the sine wave with

        Anchors:
            * 16 compass points (N, S, E, W, NE, NNE, etc.)
    '''

    def __init__(self, *d,
                 double: bool = False,
                 headwidth: float = 0.15, headlength: float = 0.25,
                 arrow: str = None,
                 numsegments: int = 1000,
                 amp: float = 1,
                 freq: float = 1,
                 phase: float = 0,

                 **kwargs):
        super().__init__(*d, arrowlength=headlength,
                         arrowwidth=headwidth, arrow=arrow,
                         **kwargs)
        self.headlength = headlength
        self.headwidth = headwidth
        self.arrow = arrow
        self.amplitude = amp
        self.frequency = freq
        self.phase = phase
        self.numsegments = numsegments

    def to(self, xy: XY, dx: float = 0, dy: float = 0) -> 'Element':
        ''' Specify ending position

            Args:
                xy: Ending position of element
                dx: X-offset from xy position
                dy: Y-offset from xy position
        '''
        xy = Point(xy)
        self._userparams['to'] = Point((xy.x + dx, xy.y + dy))
        return self

    def delta(self, dx: float = 0, dy: float = 0) -> 'Element':
        ''' Specify change in position '''
        self._userparams['delta'] = Point((dx, dy))
        return self

    def _place(self, dwgxy: XY, dwgtheta: float, **dwgparams) -> tuple[Point, float]:
        ''' Calculate absolute placement of Element '''
        self._dwgparams = dwgparams
        if not self._cparams:
            self._buildparams()

        xy: Point = Point(self._cparams.get('at', dwgxy))
        to: Point = Point(self._cparams.get('to', Point((xy.x + 3, xy.y))))
        delta = self._cparams.get('delta', None)
        if delta is not None:
            dx, dy = delta
        else:
            dx = to.x - xy.x
            dy = to.y - xy.y


        # define coordinates of a sine wave between (0,0) and (dx, dy)

        dist = math.sqrt(dx ** 2 + dy ** 2)
        x = np.linspace(0, dist, self.numsegments)
        #draw one period sine wave from 0 to dist
        sine_y = self.amplitude * np.sin(1/dist * 2 * math.pi * self.frequency * x + self.phase)
        #rotate x by theta
        theta = math.atan2(dy, dx)
        sine_x = x * math.cos(theta)
        sine_y = x * math.sin(theta) + sine_y

        self.segments.append(Segment(list(zip(sine_x, sine_y))))
        if self.arrow is not None:
            #get the direction of the arrow
            arrow_theta = math.atan2(sine_y[-1] - sine_y[-2], sine_x[-1] - sine_x[-2])
            #find point on the sine wave where the arrow should end
            arrow_x = sine_x[-1] + self.headlength * math.cos(arrow_theta)
            arrow_y = sine_y[-1] + self.headlength * math.sin(arrow_theta)
            #draw the arrow
            self.segments.append(Segment([(sine_x[-1], sine_y[-1]), (arrow_x, arrow_y)],
                                         arrow=self.arrow,
                                         arrowlength=self.headlength,
                                         arrowwidth=self.headwidth))


        self.params['theta'] = 0
        self.params['lblloc'] = 'mid'
        self.anchors['start'] = Point((0, 0))
        self.anchors['end'] = Point((dx, dy))
        self.params['drop'] = Point((dx, dy))
        valign = 'bottom'
        halign = 'left'
        vofst = 0.1

        self.params['lblofst'] = vofst
        self.params['lblalign'] = (halign, valign)
        return super()._place(dwgxy, dwgtheta, **dwgparams)

