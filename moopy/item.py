'''
'''

# Standard
# Related
# Local
import errors
import al.commands.item
import al.commands.shader
import al.query_services.scene
import al.query_services.layer


def get_item_by_name(name):
    ''''''
    raise NotImplementedError()

def get_item_by_id(item_id):
    ''''''
    raise NotImplementedError()

def get_item_class_from_id(item_id):
    '''Return the Class of the object type.'''
    type_switch = {
        'imageMap':ImageMap,
    }
    
    item_type = al.query_services.scene.get_item_type(item_id)
    
    if not type_switch.has_key(item_type):
        raise NotImplementedError()
    else:
        return type_switch[item_type]
    

class Item(object):
    '''The base item. Not indended for direct use, but feel free to
    inherit it.
    '''

    def __init__(self, item_id, *args, **kwargs):
        '''
        '''
        super(Item, self).__init__(*args, **kwargs)
        
        self._channels = None
        self._item_id = item_id
        self._mtype = None
        self._mtype_label = None
        
        # If this fails, we can assume the item_id does not exist.
        try:
            self._name = al.query_services.scene.get_item_name(item_id)
        except:
            errors.ItemIDNonExistantError('ItemID: %s' % item_id)
    
    def __repr__(self):
        '''
        '''
        return "<class 'moopy.item.Item', name:%s>" % (self.name)

    def __str__(self):
        '''
        '''
        return 'Item, Name %s' % (self.name)

    def _get_channels(self):
        ''''''
        raise exceptions.NotImplementedError()

    channels = property(
        _get_channels,
        doc=''' The channels object for this object.
        '''
    )
    
    def _get_mtype(self):
        ''''''
        return self._mtype
    
    mtype = property(
        _get_mtype,
        doc=''' The string type, as found in modo.
        '''
    )
    
    def _get_mtype_label(self):
        ''''''
        return self._mtype_label
    
    mtype_label = property(
        _get_mtype_label,
        doc=''' The human readable label of the item type.
        '''
    )
    
    def _get_name(self):
        ''''''
        return self._name
    
    def _set_name(self, value):
        ''''''
        raise NotImplementedError()
    
    name = property(
        _get_name,
        _set_name,
        doc='''The name of the item in modo.
        '''
    )    
    
    def instance(self, name=None):
        ''''''
        raise NotImplementedError()
    
    def select(self, add=False):
        ''''''
        raise NotImplementedError()
        

class ImageMap(Item):
    '''An image map, as seen in the shader tree.'''

    def __init__(self, item_id, *args, **kwargs):
        ''''''
        super(ImageMap, self).__init__(item_id, *args, **kwargs)
        
        if al.query_services.scene.get_item_type(item_id) != 'imageMap':
            errors.ItemIDNotClassTypeError('ItemID:%s is not an ImageMap.')
        
        self._type = 'imageMap'
        self._label = 'Image Map'

    def __repr__(self):
        '''
        '''
        return "<class 'moopy.item.ImageMap', name:%s>" % (self.name)

    def __str__(self):
        '''
        '''
        return 'Image Map, Name %s' % (self.name)
    
    @classmethod
    def new(cls, name=None):
        '''Create a new image map and return that object.'''
        raise NotImplementedError()
        
        item_id = al.commands.shader.create_image_map()
        
        image_map = cls(item_id)
        
        if name is not None:
            image_map.name = name
        
        return image_map

class SceneItem(Item):
    '''The base scene item. Not indended for direct use, but feel free to
    inherit it.
    '''

    def __init__(self, *args, **kwargs):
        '''
        '''
        super(SceneItem, self).__init__(*args, **kwargs)

        # Add default values for all the properties, incase one of you
        # crazy kids decides to inherit from Item.
        self._layer_id = None
        self._visibility = None

    def __repr__(self):
        '''
        '''
        return "<class 'moopy.item.SceneItem', layer_id:%s, name:%s>" % (
            self.layer_id, self.name)

    def __str__(self):
        '''
        '''
        return 'Scene Item, Name %s' % (self.name)

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


class ItemCollection(object):
    '''A collection of items.'''

    def __init__(self, ids, *args, **kwargs):
        '''
        @param ids: An iterable object containing string IDs of each item
        to be in this collection. Note that if any IDs given are not valid,
        they will not fail until accessed.
        '''
        super(ItemCollection, self).__init__(*args, **kwargs)
        
        #: An iterable object of string IDs.
        self._ids = ids
        #: This serves as cache for the items contained in this class.
        #: That way there is no need to continually create new objects for
        #: each item.
        self._item_cache = dict.fromkeys(ids)
    
    def __repr__(self):
        '''
        '''
        return "<class 'moopy.item.ItemCollection', name:%s, len:%s>" % (
            self.name, self.__len__())

    def __str__(self):
        '''
        '''
        return 'Scene Item, Name %s' % (self.name)
    
    def __len__(self):
        ''''''
        return len(self._ids)
    
    def __getitem__(self, item_id):
        ''''''
        if self._item_cache[item_id] is None:
            item = get_item_class_from_id(item_id)(item_id)
            self._item_cache[item_id] = item
            return item
        else:
            return self._item_cache[item_id]
    
    def new_of_type(self, item_class):
        '''Create a new collection from this collection, of the type
        defined in the param:item_class.
        '''
        raise NotImplementedError()
        
