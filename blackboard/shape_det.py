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
        elif self.is_triangle(x=x, y=y, margin=margin):
            return 'triangle'
        elif self.is_circle(x=x, y=y, margin=margin*2):
            return 'circle'
        else:
            return 'unknown'

    def is_line(self, x, y, margin):
        # y = a*x+b
        perc_step = 100/len(x)
        perc=0

        a, b = x, y

        if self.line_vert(x):
            print('repeat process but process x instead of y')
            a, b = y, x

        try:
            slope = abs(b[-1]-b[0])/(abs(a[-1]-a[0]))
        except ZeroDivisionError:
            slope=0
            print('Zero division error occurred a[-1]=', a[-1],
                  'a[0]=', a[0])
            
        if self.line_descends(b):
            slope *= -1
        if self.line_reversed(a):
            slope *= -1

        offset_b=b[0]
        b_line = []

        if slope == 0:
            y_step = abs(max(b)-min(b))/len(b)
            for i in range(len(b)):
                b_line.append(min(b)+(i*b_step))
        else:
            for a_line in a:
                b_line.append(slope*(a_line-a[0])+offset_b)

        for i in range(len(x)):
            if abs(b_line[i]-y[i]) <= margin:
                perc += perc_step

        #print('line',perc, '%')
        if perc > 80:
            self.shape = dict(x=x, y=b_line)
            return True
        else:
            #print('slope', slope, str(perc)+'%')
            for i in range(len(b_line)):
                pass#print('x', x[i], 'y', y[i], 'b_line', b_line[i])
            return False

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
        #print('circle', perc, '%')
                
        if perc >= 80:
            self.shape = coords
            return True
        else:
            return False

    def is_triangle(self, x, y, margin):
        #2a/Pi arcsin(sin(2Pi/p * x))
        perc_x, perc_y = 0, 0
        perc_step = 100/len(x)

        orig = dict(x=x[0], y=y[0])

        abc = dict(x=[], y=[])
        abc['x'].append(min(x))
        abc['y'].append(max(y))
        
        abc['x'].append(max(x))
        abc['y'].append(max(y))
        
        abc['x'].append(abs(max(x)-min(x))+min(x))
        abc['y'].append(min(y))

        perc = (perc_x + perc_y) / 2
        if perc > 80:
            self.shape = dict(x=x, y=y_line)
            return True

        return False

    def line_descends(self, y):
        if y[0] < y[-1]:
            return True
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
        vals=[]
        for val in x:
            if not(val in vals):
                vals.append(val)
        #print(len(vals), len(x), (len(vals)/len(x)*100))

        if ((len(vals)/len(x)*100) < 15) or (x[-1] == x[0]):
            print('vertical')
            return True
        return False
