
class Action():
    """
    A class to define aspects of user actions to be used in both GUI and CLI applications
    """
    def __init__(self, *args, **kwargs):
        self.type_ = ''
        self.name = ''
        self.keys_used = ''
        self.description = ''
        self.coords = []

        arg = 'type_'
        if arg in kwargs:
            self.type_=kwargs[arg]

        arg = 'name'
        if arg in kwargs:
            self.name=kwargs[arg]

        arg = 'keys_used'
        if arg in kwargs:
            self.keys_used=kwargs[arg]

        arg = 'description'
        if arg in kwargs:
            self.description=kwargs[arg]

        arg = 'coords'
        if arg in kwargs:
            self.coords=kwargs[arg]

    
class ActionLog():
    """
    A class to store performed user actions, as defined by class Action   
    """
    def __init__(self):
        """
        Initialises the variables
        """
        self.actions = []

    def add(self, *args, **kwargs):
        action = Action()

        arg = 'type_'
        if arg in kwargs:
            action.type_ = kwargs[arg]

        arg = 'name'
        if arg in kwargs:
            action.name = kwargs[arg]

        arg = 'keys_used'
        if arg in kwargs:
            action.keys_used = kwargs[arg]

        arg = 'description'
        if arg in kwargs:
            action.description = kwargs[arg]

        arg = 'coords'
        if arg in kwargs:
            action.coords = kwargs[arg]

        self.actions.append(action)

    def delete(self, *args, **kwargs):
        if 'index' in kwargs:
            self.actions.pop(kwargs['index'])
        elif 'type_' in kwargs:
            for i in range(len(self.actions)):
                if self.actions[i].type_ == kwargs['type_']:
                    self.actions.pop(i)
        elif 'name' in kwargs:
            for i in range(len(self.actions)):
                if self.actions[i].name == kwargs['name']:
                    self.actions.pop(i)
        elif 'keys_used' in kwargs:
            for i in range(len(self.actions)):
                if self.actions[i].keys_used == kwargs['keys_used']:
                    self.actions.pop(i)
        elif 'description' in kwargs:
            for i in range(len(self.actions)):
                if self.actions[i].description == kwargs['description']:
                    self.actions.pop(i)
        elif 'coords' in kwargs:
            for i in range(len(self.actions)):
                if self.actions[i].coords == kwargs['coords']:
                    self.actions.pop(i)
        else:
            raise ValueError('Unspecified argument(s)')

    def get(self, *args, **kwargs):
        if 'index' in kwargs:
            return self.actions[kwargs['index']]
        elif 'type_' in kwargs:
            for i in range(len(self.actions)):
                if self.actions[i].type_ == kwargs['type_']:
                    return self.actions[i]
        elif 'name' in kwargs:
            for i in range(len(self.actions)):
                if self.actions[i].name == kwargs['name']:
                    return self.actions[i]
        elif 'keys_used' in kwargs:
            for i in range(len(self.actions)):
                if self.actions[i].keys_used == kwargs['keys_used']:
                    return self.actions[i]
        elif 'description' in kwargs:
            for i in range(len(self.actions)):
                if self.actions[i].description == kwargs['description']:
                    return self.actions[i]
        elif 'coords' in kwargs:
            for i in range(len(self.actions)):
                if self.actions[i].coords == kwargs['coords']:
                    return self.actions[i]
