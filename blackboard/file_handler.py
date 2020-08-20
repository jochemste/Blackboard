#!/usr/bin/python3

"""
Classes to help simplify handling file reading/writing
"""

class File_handler():
    """
    Class to simplify file reading and writing

    A class to help simplify reading and writing to a file

    Attributes
    ----------
    __fd: str
        The file descriptor
    __filters: list
        The list of filters to filter file data
    __data: list
        A list which holds the data, read from a file
    __data_filt: list
        A list which holds the filtered data, read from a file

    Methods
    -------
    __init__(self, fd)
        Constructor, initialises members and creates file

    read_data(self)
        Reads data from __fd

    clear_file(self)
        Clears all contents from a file

    write_data(self, data)
        Writes data into a file

    count_lines(self)
        Counts the lines in a file

    set_filters(self, filters)
        Sets the filters for file data

    filter_data(self, filters, startswith='', endswith='')
        Filter data and store it in __data_filt

    get_fdata_lvalue(self, letter: str)
        Gets the filtered data

    create_file(self)
        Creates the file
    """
    __fd: str
    __filters: list
    __data: list
    __data_filt: list

    def __init__(self, fd):
        """
        Constructor, initialises members and creates file
        
        The class constructor, which initialises all members and creates 
        a file if it does not exist.
        
        Parameters
        ----------
        fd: str
            The file descriptor
        """
        self.__fd=fd
        self.__filters=[]
        self.__data=[]
        self.__data_filt=[]
        self.create_file()
        
    def read_data(self):
        """
        Reads data from __fd
        
        Reads the data after opening the __fd and stores
        it in __data, which is returned
        
        Returns
        -------
        self.__data: list
            A list of data, read from the file
        """
        self.__data=[]
        with open(self.__fd, 'r') as fd:
            for line in fd:
                self.__data.append(line)
        return self.__data

    def clear_file(self):
        """
        Clears all contents from a file
        
        Truncates the file at the very beginning, resulting in an empty file
        """
        with open(self.__fd, 'w') as fd:
            fd.truncate(0)

    def write_data(self, data):
        """
        Writes data into a file
        
        Writes the contents of data into the file
        
        Parameters
        ----------
        data: list
            A list of data to write into a file
        """
        with open(self.__fd, 'w') as fd:
            for d in data:
                fd.write(d)

    def count_lines(self):
        """
        Counts the lines in a file
        
        Counts the number of lines written in a file by reading all data 
        from a file and counting the elements.
        
        Returns
        -------
        cnt
            The number of lines
        """
        cnt=0
        with open(self.__fd, 'r') as fd:
            for line in fd:
                cnt +=1
        return cnt

    def set_filters(self, filters):
        """
        Sets the filters for file data
        
        Sets the filters to be used to get filtered data from a file
        
        Parameters
        ----------
        filters: list
            A list of filters
        """
        self.__filters=[]
        for filter in filters:
            self.__filters.append(filter)
    
    def filter_data(self, filters, startswith='', endswith=''):
        """
        Filter data and store it in __data_filt
        
        Filters the data, retrieved from a file and stored in data and 
        stores it in __data_filt
        
        Parameters
        ----------
        filters: list
            List of filters to use
        startswith='': str
            Extra filter to make sure a line begins with (a) certain character(s)
        endswith='': str
            Extra filter to make sure a line ends with (a) certain character(s)
        """
        self.set_filters(filters)

        for line in self.__data:
            if line.startswith(startswith) and line.endswith(endswith):
                include=True
                for filt in self.__filters:
                    if(not(filt in line)):
                        include=False
                        break
                if include:
                    self.__data_filt.append(line)
    
    def get_fdata_lvalue(self, letter: str):
        """
        Gets the filtered data
        
        Gets the filtered data, further filtered with the 
        specified letter
        
        Parameters
        ----------
        letter: str
            The letter to look for in the filtered data
        
        Returns
        -------
        values: list
            The list of values
        """
        values=[]
        for line in self.__data_filt:
            parts=line.split(' ')
            for part in parts:
                if part.startswith(letter):
                    values.append(part.split(letter)[1])
                    break
        return values

    def create_file(self):
        """
        Creates the file
        
        Opens the file if it exists. If not, an exception is 
        thrown and the file is created
        """
        try:
            file=open(self.__fd, 'r')
        except:
            file=open(self.__fd, 'w')

#example
if __name__ == '__main__':

    fd='../../rpi/src/data_files/data16.txt'
    filters=['Fri Apr  3']
    f=File_handler(fd)
    f.read_data()
    f.filter_data(filters, 'N:')

    print('\n'.join(f.get_fdata_lvalue('T')))
    print(len(f.get_fdata_lvalue('T')))

    average = 0
    for d in f.get_fdata_lvalue('T'):
        average+=float(d)
    average/=len(f.get_fdata_lvalue('T'))

    print('Average='+str(average))

    
