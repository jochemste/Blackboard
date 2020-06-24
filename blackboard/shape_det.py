"""
Shape detection, using coordinates
"""
import math

class Shape_detector():
    shape: dict

    def __init__(self):
        self.shape = dict(x=None, y=None)

    def get_shape(self, x, y, margin=20):
        if self.is_line(x=x, y=y, margin=margin):
            return 'line'
        elif self.is_circle(x=x, y=y, margin=margin*2):
            return 'circle'
        else:
            return 'unknown'

    def is_circle(self, x, y, margin):
        if len(x) < 10:
            return False
        
        perc_step = 100/len(x)
        perc=0
        perc_x, perc_y = 0, 0
        radius_x = (max(x) - min(x)) / 2
        radius_y = (max(y) - min(y)) / 2

        if abs(radius_x-radius_y) > radius_x or \
           abs(radius_x-radius_y) > radius_y:
            return False
        
        radius = (radius_x+radius_y) / 2

        orig = dict(x=None, y=None)
        orig['x'] = ((max(x)-min(x))/2)+min(x)
        orig['y'] = ((max(y)-min(y))/2)+min(y)

        step = 2*math.pi/(max(x)-min(x))
        coords=dict(x=[], y=[])
        
        for i in range(len(x)):
            coords['x'].append(radius*math.cos(i*step)+orig['x'])
            coords['y'].append(radius*math.sin(i*step)+orig['y'])

            if abs(coords['x'][i]-x[i]) <= margin:
                perc_x+= perc_step
            if abs(coords['y'][i]-y[i]) <= margin:
                perc_y+= perc_step

        orig_new = dict(x=None, y=None)
        orig_new['x'] = ((max(coords['x'])-min(coords['x']))/2)+min(coords['x'])
        orig_new['y'] = ((max(coords['y'])-min(coords['y']))/2)+min(coords['y'])

        perc = (perc_x+perc_y) / 2
        #print('circle', perc, '%', 'x', perc_x, '%', 'y', perc_y, '%')
                
        if perc >= 80:
            self.shape = coords
            return True
        else:
            return False

    def is_line(self, x, y, margin):
        # y = a*x+b

        #print('x[0], x[-1], y[0], y[-1]')
        #print(x[0], x[-1], y[0], y[-1])
        
        perc_step = 100/len(x)
        perc=0

        y_extr = [y[0], y[-1]]
        x_extr = [x[0], x[-1]]


        slope = abs(y[-1]-y[0])/(abs(x[-1]-x[0]))

        if self.line_descends(y):
            slope *= -1
        if self.line_reversed(x):
            slope *= -1

        #slope = (y[-1]-y[0])/len(y)
        offset_y=y[0]
        y_line = []
        for x_line in x:
            y_line.append(slope*(x_line-x[0])+offset_y)

        #print(slope, '*(x[i]-', x[0], ')+', offset_y)
        #print('x[i]', 'y[i]', 'x[i]', 'y_line[i]')
        for i in range(len(x)):
            if abs(y_line[i]-y[i]) <= margin:
                perc += perc_step
            #print(x[i], y[i], x[i], y_line[i])

        print('line',perc)
        if perc > 80:
            self.shape = dict(x=x, y=y_line)
            return True
        else:
            return False
        

    def line_descends(self, y):
        if y[0] < y[-1]:
            #print('line descends')
            return True
        #print('line ascends')
        return False

    def line_reversed(self, x):
        if x[-1] > x[0]:
            return True
        return False

    def line_horiz(self, y):
        if y[0] == y[-1]:
            return True
        return False

    def line_vert(self, x):
        if x[0] == x[-1]:
            return True
        return False
