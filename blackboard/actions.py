
class Action():
    """
    A class to store performed user actions
    """

    def __init__(self):
        self.type_=[]

    def add(self, *args, **kwargs):
        if 'type_' in kwargs:
            self.type_.append(kwargs['type_'])
        if 'name' in kwargs:
            self.name.append(kwargs['name'])

    def delete(self, *args, **kwargs):
        if 'type_' in kwargs:
            pass

    def get(self, *args, **kwargs):
        pass
