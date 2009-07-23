''''''

# Standard
# Related
# Local


def get_selection_type():
    '''Return the Selection class which matches whatever the user selection
    is currently set up.'''
    
    raise NotImplementedError()


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

    def get_current_selection(self, replace=False):
        '''Get the current selection inside of modo and add it into this
        selection instance.
        
        @param replace: Entirely replace whatever selection this selection 
        instance contains with whatever is in modo.
        '''
        
        raise NotImplementedError()
    
    def make_active(self):
        '''Make this selection instance the current selection in modo.'''
        raise NotImplementedError()

class ElementSelection(Selection):
    '''The base class for the element selection types.'''
    
    def __init__(self, *args, **kwargs):
        ''''''
        super(ElementSelection, self).__init__(*args, **kwargs)

class PolygonSelection(ElementSelection):
    ''''''
    
    def __init__(self, *args, **kwargs):
        ''''''
        super(PolygonSelection, self).__init__(*args, **kwargs)
        
        raise NotImplementedError()

class VertexSelection(ElementSelection):
    ''''''
    
    def __init__(self, *args, **kwargs):
        ''''''
        super(PolygonSelection, self).__init__(*args, **kwargs)
        
        raise NotImplementedError()

class EdgeSelection(ElementSelection):
    ''''''
    
    def __init__(self, *args, **kwargs):
        ''''''
        super(PolygonSelection, self).__init__(*args, **kwargs)
        
        raise NotImplementedError()

class MaterialSelection(Selection):
    ''''''
    
    def __init__(self, *args, **kwargs):
        ''''''
        super(MaterialSelection, self).__init__(*args, **kwargs)
        
        raise NotImplementedError()
