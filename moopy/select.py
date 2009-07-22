''''''

# Standard
# Related
# Local


def get_current_selection():
    '''Get a L{Selection} instance representing the current selection.'''
    raise exceptions.NotImplementedError()

class Selection(object):
    '''A representation of a B{potential} selection. Ie, what ever this class
    contains as a selection is not directly related to the current selection
    in modo.
    
    To make a Selection instance the current modo selection,
    call L{self.make_active}
    '''

    def __init__(self, *args, **kwargs):
        ''''''
        super(Selection, self).__init__(*args, **kwargs)

    def make_active(self):
        '''Make this selection instance the current selection in modo.'''
        raise exceptions.NotImplementedError()
