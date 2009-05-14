'''
'''

# Standard
import exceptions
# Related
# Local
import al.query_services.layer
import al.commands.item


def get_item_by_name(name):
    ''''''
    raise exceptions.NotImplementedError()

def get_item_by_id(item_id):
    ''''''
    raise exceptions.NotImplementedError()

def instance_item(item):
    ''''''
    raise exceptions.NotImplementedError()

class Item(object):
    '''The base layer item. Not indended for direct use, but feel free to
    inherit it.
    '''

    def __init__(self, *args, **kwargs):
        '''
        '''
        super(Item, self).__init__(*args, **kwargs)

        # Add default values for all the properties, incase one of you
        # crazy kids decides to inherit from Item.
        self._channels = None
        self._layer_id = None
        self._name = None
        self._visibility = None

    def __str__(self):
        '''
        '''
        return '%s:%s' % (self.layer_id, self.name)

    def _get_channels(self):
        ''''''
        raise exceptions.NotImplementedError()

    channels = property(
        _get_channels,
        doc='''The channels object for this object.
        '''
    )

    def _get_layer_id(self):
        ''''''
        return self._layer_id

    layer_id = property(
        _get_layer_id,
        doc='''The layer id of the item.
        '''
    )    

    def _get_name(self):
        ''''''
        return self._name

    def _set_name(self, value):
        ''''''
        raise exceptions.NotImplementedError()

    name = property(
        _get_name,
        _set_name,
        doc='''The name of the item, human readable.
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

    def __init__(self, name=None):
        '''
        '''
        super(Mesh, self).__init__(name)

        # Create the mesh with the given name.
        al.commands.item.create_mesh(name)

        # Select the active layer, which should be the newly created mesh.
        al.query_services.layer.select_layer_main()

        # Grab information about that layer and store it in this object.
        self._layer_id = al.query_services.layer.get_layer_id()
        self._name = al.query_services.layer.get_layer_name()

