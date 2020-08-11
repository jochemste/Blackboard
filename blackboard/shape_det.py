"""
Shape detection, using coordinates
"""
import math

class Shape_detector():
    shape: dict
    __shapes: dict

    def __init__(self):
        self.shape = dict(x=None, y=None)
        self.__shapes = dict(line=None, triangle=None, circle=None)

    def get_shape(self, x, y, margin=20):
        """
        Returns the shape name
        """
        #relative_margin = margin*len(x)/200
        #relative_margin = margin*math.sqrt(len(x))/10
        self.percent = dict(line=0, triangle=0, circle=0)
        
        relative_margin = margin*math.sqrt(self.get_line_length(x=x, y=y))/10
        rel_margin_circ = margin*math.sqrt(len(x))/5
        shape = 'unknown'
        if not(len(x) == len(y)):
            print('ERROR: shape coordinate lengths do not match')
            return shape
        if self.is_line(x=x, y=y, margin=relative_margin):
            shape = 'line'
            self.shape=self.__shapes['line']
        if self.is_triangle(x=x, y=y, margin=relative_margin):
            if self.percent['triangle'] > self.percent['line']:
                shape = 'triangle'
                self.shape=self.__shapes['triangle']
        if self.is_circle(x=x, y=y, margin=rel_margin_circ):
            if (self.percent['circle'] > self.percent['line']) and \
               (self.percent['circle'] > self.percent['triangle']):
                shape = 'circle'
                self.shape=self.__shapes['circle']
                
        print(self.percent, shape)
        return shape

    def is_line(self, x, y, margin):
        """
        Check if the given coordinates form a 
        linear shape within the given margin
        """
        # y = a*x+b
        perc_step = 100/len(x)
        perc=0

        a, b = x, y

        # invert x and y coordinates for vertical lines
        if self.line_vert(x):
            print('repeat process but process x instead of y')
            a, b = y, x

        # check for zero division in slope calculations
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
            b_step = abs(max(b)-min(b))/len(b)
            for i in range(len(b)):
                b_line.append(min(b)+(i*b_step))
        else:
            for a_coord in a:
                b_line.append(slope*(a_coord-a[0])+offset_b)

        for i in range(len(x)):
            if abs(b_line[i]-b[i]) <= margin:
                perc += perc_step

        #print('line',perc, '%')
        self.percent['line']=perc
        if perc >= 80:
            if x == a:
                self.__shapes['line'] = dict(x=a, y=b_line)
            else:
                self.__shapes['line'] = dict(x=b_line, y=a)
            return True
        else:
            #print('margin: ', margin, ' slope: ', slope)
            for i in range(len(b_line)):
                #print('a', a[i], 'b', b[i], 'b_line', b_line[i])
                pass
            return False

    def is_circle(self, x, y, margin):
        """
        Check if the given coordinates form a 
        circular shape within the given margin
        """
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
        print('circle', perc, '%', ' margin:', margin)

        self.percent['circle'] = perc
        if perc >= 80:
            self.__shapes['circle'] = coords
            return True
        else:
            return False

    def is_triangle(self, x, y, margin):
        """
        Check if the given coordinates form a 
        triangular shape within the given margin
        """
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
        self.percent['triangle'] = perc
        if perc > 80:
            self.__shapes['triangle'] = dict(x=x, y=y_line)
            return True

        return False

    def line_descends(self, y):
        """
        Check if line is sloping down or not
        """
        if y[0] < y[-1]:
            return True
        return False

    def line_reversed(self, x):
        """
        Check if line starts at a larger X than where it ends
        """
        if x[-1] > x[0]:
            return True
        return False

    def line_horiz(self, y):
        """
        Check if line is horizontal
        """
        if y[0] == y[-1]:
            return True
        return False

    def line_vert(self, x):
        """
        Check if line is vertical or not
        """
        vals=[]
        for val in x:
            if not(val in vals):
                vals.append(val)
        #print(len(vals), len(x), (len(vals)/len(x)*100))

        if ((len(vals)/len(x)*100) < 15) or (x[-1] == x[0]):
            print('vertical')
            return True
        return False
            
    def get_line_length(self, x, y):
        """
        Calculates the length of a line
        """
        x_length = max(x) - min(x)
        y_length = max(y) - min(y)

        result = math.sqrt((x_length**2)+(y_length**2))
        return result
