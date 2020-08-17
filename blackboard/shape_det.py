"""
Shape detection, using coordinates
"""
import math

class Shape_detector():
    shape: dict
    __shapes: dict
    __detect_shapes: list

    def __init__(self, *args, **kwargs):
        self.supported_shps = ['line', '', 'circle']
        self.shape = dict(x=None, y=None)
        self.__shapes = dict(line=None, triangle=None, circle=None)

        if 'detect' in kwargs:
            self.__detect_shapes = kwargs['detect']
        else:
            self.__detect_shapes = self.supported_shps

        for shape in self.__detect_shapes:
            if not(shape in self.supported_shps):
                ValueError("Shape not supported: "+str(shape))

    def get_shape(self, x, y, margin=20, margin_line=None, margin_circle=None,
                  margin_triangle=None):
        """
        Returns the shape name and sets a relative margin
        
        Parameters
        ----------
        x: list
            The list of x coordinates
        y: list
            The list of y coordinates
        margin: int
            The margin to be used for relative margin calculations
        
        Returns
        -------
        shape: str
            The name of the shape if detected. 
            If not a known shape, 'unknown' will be returned.
        """
        #relative_margin = margin*len(x)/200
        #relative_margin = margin*math.sqrt(len(x))/10
        self.percent = dict(line=0, triangle=0, circle=0)

        if not(margin_line == None):
            margin_line = margin*math.sqrt(self.get_line_length(x=x, y=y))/10
        else:
            margin_line = margin_line*math.sqrt(self.get_line_length(x=x, y=y))/10

        if not(margin_triangle == None):
            margin_triangle = margin*math.sqrt(self.get_line_length(x=x, y=y))/10
        else:
            margin_triangle = margin_triangle*math.sqrt(self.get_line_length(x=x, y=y))/10

        if not(margin_circle == None):
            margin_circle = margin+margin*math.sqrt(len(x))/5
        else:
            margin_circle = margin_circle+margin_circle*math.sqrt(len(x))/5
        
        
        print(margin_line, margin_triangle, margin_circle)
        shape = 'unknown'
        if not(len(x) == len(y)):
            print('ERROR: shape coordinate lengths do not match')
            return shape
        
        if ('line' in self.__detect_shapes) and \
           self.is_line(x=x, y=y, margin=margin_line):
            shape = 'line'
            self.shape=self.__shapes['line']

        if ('triangle' in self.__detect_shapes) and \
           self.is_triangle(x=x, y=y, margin=margin_triangle):
            if self.percent['triangle'] > self.percent['line']:
                shape = 'triangle'
                self.shape=self.__shapes['triangle']

        if ('circle' in self.__detect_shapes) and \
           self.is_circle(x=x, y=y, margin=margin_circle):
            if (self.percent['circle'] > self.percent['line']) and \
               (self.percent['circle'] > self.percent['triangle']):
                shape = 'circle'
                self.shape=self.__shapes['circle']
                
        print(self.percent, shape)
        return shape

    def is_line(self, x, y, margin):
        """
        Check if the given coordinates form a 
        linear shape within the given margin. If a linear shape is found, the corrected 
        shape is stored.
        
        Parameters
        ----------
        x: list
            The list of x coordinates
        y: list
            The list of y coordinates
        margin: int
            The margin to be used to allow shapes to deviate from a perfect form within 
            this margin. The margin is depicted in pixels, like the coordinates.
        
        Returns
        -------
        .boolean
            Returns if the coordinates form a line or not.
        """
        # y = a*x+b
        perc_step = 100/len(x)
        perc=0

        a, b = x, y

        # invert x and y coordinates for vertical lines
        if self.line_vert(x):
            #print('repeat process but process x instead of y')
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
        circular shape within the given margin. If a circular shape is found, the corrected 
        shape is stored.
        
        Parameters
        ----------
        x: list
            The list of x coordinates
        y: list
            The list of y coordinates
        margin: int
            The margin to be used to allow shapes to deviate from a perfect form within 
            this margin. The margin is depicted in pixels, like the coordinates.
        
        Returns
        -------
        .boolean
            Returns if the coordinates form a circle or not.
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
        #print('circle', perc, '%', ' margin:', margin)

        self.percent['circle'] = perc
        if perc >= 80:
            self.__shapes['circle'] = coords
            return True
        else:
            return False

    def is_triangle(self, x, y, margin):
        """
        Check if the given coordinates form a 
        triangular shape within the given margin. If a triangular shape is found, the corrected 
        shape is stored.
        
        Parameters
        ----------
        x: list
            The list of x coordinates
        y: list
            The list of y coordinates
        margin: int
            The margin to be used to allow shapes to deviate from a perfect form within 
            this margin. The margin is depicted in pixels, like the coordinates.
        
        Returns
        -------
        .boolean
            Returns if the coordinates form a triangle or not.
        """
        #2a/Pi arcsin(sin(2Pi/p * x))
        perc = 0
        perc_step = 100/len(x)

        print(y[0], y[-1])
        angle_a_coord = dict(x=None, y=min(y))
        angle_b_coord = dict(x=min(x), y=max(y))
        angle_c_coord = dict(x=max(x), y=max(y))

        for i in range(len(x)):
            if y[i]==min(y):
                angle_a_coord['x'] = x[i]
                break

        print('a: ', angle_a_coord)
        print('b: ', angle_b_coord)
        print('c: ', angle_c_coord)

        line_ab_og = dict(x=[], y=[])
        line_bc_og = dict(x=[], y=[])
        line_ca_og = dict(x=[], y=[])

        line_ab_new = dict(x=[], y=[])
        line_bc_new = dict(x=[], y=[])
        line_ca_new = dict(x=[], y=[])

        ############################FAULTY#########################################
        # Find the first of the original lines
        index=0
        for i in range(len(x)):
            line_ab_og['x'].append(x[i])
            line_ab_og['y'].append(y[i])
            if x[i] == angle_b_coord['x'] and \
               y[i] == angle_b_coord['y']:
                index=i
                break

        # Find the second of the original lines
        while not(x[index] == angle_c_coord['x'] and \
                  y[index] == angle_c_coord['y']):
            line_bc_og['x'].append(x[index])
            line_bc_og['y'].append(y[index])
            index += 1

        print(index, len(index))
        # Find the third of the original lines
        while not(x[index] == angle_a_coord['x'] and \
                  y[index] == angle_a_coord['y']):
            line_ca_og['x'].append(x[index])
            line_ca_og['y'].append(y[index])
            index += 1
        ########################################################################

        # slope for line ab
        try:
            slope_ab = abs(line_ab_og['x'][-1]-line_ab_og['x'][0])/ \
                abs(line_ab_og['y'][-1]-line_ab_og['y'][0])
        except ZeroDivisionError:
            slope_ab=0
            print('Zero division error occurred x[-1]=', line_ab_og['x'][-1],
                  'x[0]=', line_ab_og['x'][0])

        # slope for line bc
        try:
            slope_bc = abs(line_bc_og['x'][-1]-line_bc_og['x'][0])/ \
                abs(line_bc_og['y'][-1]-line_bc_og['y'][0])
        except ZeroDivisionError:
            slope_ab=0
            print('Zero division error occurred x[-1]=', line_bc_og['x'][-1],
                  'x[0]=', line_bc_og['x'][0])

        # slope for line ca
        try:
            slope_ca = abs(line_ca_og['x'][-1]-line_ca_og['x'][0])/ \
                abs(line_ca_og['y'][-1]-line_ca_og['y'][0])
        except ZeroDivisionError:
            slope_ab=0
            print('Zero division error occurred x[-1]=', line_ca_og['x'][-1],
                  'x[0]=', line_ca_og['x'][0])

        # calculate and check line ab
        if self.line_descends(line_ab_og['y']):
            slope_ab *= -1
        if self.line_reversed(line_ab_og['x']):
            slope_ab *= -1

        offset_ab=line_ab_og['y'][0]

        if slope == 0:
            step_ab = abs(max(line_ab_og['y'])-min(line_ab_og['y']))/len(line_ab_og['y'])
            for i in range(len(line_ab_og['y'])):
                line_ab_new['y'].append(min(line_ab_og['y'])+(i*step_ab))
                line_ab_new['x'].append(line_ab_og['x'])
        else:
            for x in line_ab_new['x']:
                line_ab_new['x'].append(x)
                line_ab_new['y'].append(slope_ab*(x-line_ab_og['x'][0])+offset_ab)

        for i in range(len(line_ab_og['x'])):
            if abs(line_ab_new['y'][i]-line_ab_og['y'][i]) <= margin:
                perc += perc_step

        # calculate and check line bc
        if self.line_descends(line_bc_og['y']):
            slope_bc *= -1
        if self.line_reversed(line_bc_og['x']):
            slope_bc *= -1

        offset_bc=line_bc_og['y'][0]

        if slope == 0:
            step_bc = abs(max(line_bc_og['y'])-min(line_bc_og['y']))/len(line_bc_og['y'])
            for i in range(len(line_bc_og['y'])):
                line_bc_new['y'].append(min(line_bc_og['y'])+(i*step_bc))
                line_bc_new['x'].append(line_bc_og['x'])
        else:
            for x in line_bc_new['x']:
                line_bc_new['x'].append(x)
                line_bc_new['y'].append(slope_bc*(x-line_bc_og['x'][0])+offset_bc)

        for i in range(len(line_bc_og['x'])):
            if abs(line_bc_new['y'][i]-line_bc_og['y'][i]) <= margin:
                perc += perc_step

        # calculate and check line ca
        if self.line_descends(line_ca_og['y']):
            slope_ca *= -1
        if self.line_reversed(line_ca_og['x']):
            slope_ca *= -1

        offset_ca=line_ca_og['y'][0]

        if slope == 0:
            step_ca = abs(max(line_ca_og['y'])-min(line_ca_og['y']))/len(line_ca_og['y'])
            for i in range(len(line_ca_og['y'])):
                line_ca_new['y'].append(min(line_ca_og['y'])+(i*step_ca))
                line_ca_new['x'].append(line_ca_og['x'])
        else:
            for x in line_ca_new['x']:
                line_ca_new['x'].append(x)
                line_ca_new['y'].append(slope_ca*(x-line_ca_og['x'][0])+offset_ca)

        for i in range(len(line_ca_og['x'])):
            if abs(line_ca_new['y'][i]-line_ca_og['y'][i]) <= margin:
                perc += perc_step

        self.percent['triangle'] = perc
        if perc >= 80:
            new_shape = dict(x=[], y=[])
            for i in range(len(line_ab_new['x'])):
                new_shape['x'].append(line_ab_new['x'][i])
                new_shape['y'].append(line_ab_new['y'][i])
            for i in range(len(line_bc_new['x'])):
                new_shape['x'].append(line_bc_new['x'][i])
                new_shape['y'].append(line_bc_new['y'][i])
            for i in range(len(line_ca_new['x'])):
                new_shape['x'].append(line_ca_new['x'][i])
                new_shape['y'].append(line_ca_new['y'][i])
            self.__shapes['triangle'] = new_shape
            return True

        return False

    def line_descends(self, y):
        """
        Check if line is sloping down or not.
        
        Parameters
        ----------
        y: list
            The list of y coordinates
        
        Returns
        -------
        .boolean
            Returns True if the line descends and False otherwise.
        """
        if y[0] < y[-1]:
            return True
        return False

    def line_reversed(self, x):
        """
        Check if line starts at a larger X than where it ends
        
        Parameters
        ----------
        x: list
            The list of x coordinates
        
        Returns
        -------
        .boolean
            Returns True if the line is reversed and False otherwise.
        """
        if x[-1] > x[0]:
            return True
        return False

    def line_horiz(self, y):
        """
        Check if line is horizontal
        
        Parameters
        ----------
        y: list
            The list of y coordinates
        
        Returns
        -------
        .boolean
            Returns True if the line is horizontal and False otherwise.
        """
        if y[0] == y[-1]:
            return True
        return False

    def line_vert(self, x):
        """
        Check if line is vertical or not
        
        Parameters
        ----------
        x: list
            The list of x coordinates
        
        Returns
        -------
        .boolean
            Returns True if the line is vertical and False otherwise.
        """
        vals=[]
        for val in x:
            if not(val in vals):
                vals.append(val)
        #print(len(vals), len(x), (len(vals)/len(x)*100))

        if ((len(vals)/len(x)*100) < 15) or (x[-1] == x[0]):
            #print('vertical')
            return True
        return False
            
    def get_line_length(self, x, y):
        """
        Calculates the length of a line
        
        Parameters
        ----------
        x: list
            The list of x coordinates
        y: list
            The list of y coordinates
        
        Returns
        -------
        result: str
            The length of the line.
        """
        x_length = max(x) - min(x)
        y_length = max(y) - min(y)

        result = math.sqrt((x_length**2)+(y_length**2))
        return result
