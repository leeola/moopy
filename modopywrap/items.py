'''
'''

# Standard
import exceptions
# Related
# Local


def get_item_by_name(name):
    ''''''
    raise exceptions.NotImplementedError()

def get_item_by_id(item_id):
    ''''''
    raise exceptions.NotImplementedError()

class Item(object):
    '''
    '''

    def __init__(self, *args, **kwargs):
        '''
        '''
        pass
    
    def _get_channels(self):
        ''''''
        raise exceptions.NotImplementedError()
    
    def _set_channels(self, value):
        '''Setting the channels property will match one items channels to
        another item.
        @raise 
        '''
        raise exceptions.NotImplementedError()
    
    channels = property(
        _get_channels,
        _set_channels,
        doc='''The channels object for this object.
        '''
    )
    
    def _get_visibility(self):
        ''''''
        raise exceptions.NotImplementedError()
    
    def _set_visibility(self, value):
        ''''''
        raise exceptions.NotImplementedError()
    
    visibility = property(
        _get_visibility,
        _set_visibility,
        doc='''The visibility of the item, not to be confused with L{the alpha
        of the item. <self.channels.alpha>}.
        '''
    )
    
    def add_child(self, item):
        '''Make this item the parent of the given item.
        '''
        raise exceptions.NotImplementedError()
    
    def add_children(self, items):
        '''Make this item the parent of the given items
        '''
        map(self.add_child, items)
    
    def get_child_by_id(self, layer_id):
        '''
        '''
        raise exceptions.NotImplementedError()
    
    def get_child_by_index(self, index):
        '''
        '''
        raise exceptions.NotImplementedError()
    
    def get_child_by_name(self, name):
        '''
        '''
        raise exceptions.NotImplementedError()
    
    def get_parent(self):
        '''
        '''
        raise exceptions.NotImplementedError()
    
    def rename(self, name):
        '''
        '''
        raise exceptions.NotImplementedError()
    
    def set_parent(self, parent):
        '''
        '''
        raise exceptions.NotImplementedError()

class Mesh(Item):
    '''
    '''

    def __init__(self, name=None, instance=None):
        '''
        '''
        super(Mesh, self).__init__(name, instance)
        
        raise exceptions.NotImplementedError()

        