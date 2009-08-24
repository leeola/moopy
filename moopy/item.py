'''
'''

# Standard
# Related
# Local
import errors
import al.commands.item
import al.commands.shader
import al.query
import al.query_services.scene
import al.query_services.layer


def get_id_by_index(index, item_type=None):
    ''''''
    if item_type is not None:
        return al.query_services.scene.get_item_id(index, item_type)
    else:
        return al.query_services.scene.get_item_id(index)

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
        'mesh':Mesh,
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
    _mtype = None
    _mtype_label = None

    def __init__(self, item_id, *args, **kwargs):
        '''
        '''
        super(Item, self).__init__(*args, **kwargs)
        
        self._channels = None
        self._item_id = item_id
        
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
    
    def _get_children(self):
        ''''''
        children = list(
            al.query_services.scene.get_item_children(self._item_id))
        children.reverse()
        return ItemCollection(children)
    
    def _set_children(self, value):
        ''''''
        raise NotImplementedError()
    
    children = property(
        _get_children,
        _set_children,
        doc='''
        '''
    )
    
    def _get_item_id(self):
        ''''''
        return self._item_id
    
    item_id = property(
        _get_item_id,
        doc=''' The item ID.
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
    
    def instance(self, name=None):
        ''''''
        raise NotImplementedError()
    
    def select(self, add=False):
        ''''''
        raise NotImplementedError()
        

class ImageMap(Item):
    '''An image map, as seen in the shader tree.'''
        
    _mtype = 'imageMap'
    _mtype_label = 'Image Map'

    def __init__(self, item_id, index=None, *args, **kwargs):
        ''''''
        super(ImageMap, self).__init__(item_id, *args, **kwargs)
        
        self._index = index
        
        if al.query_services.scene.get_item_type(item_id) != 'imageMap':
            errors.ItemIDNotClassTypeError('ItemID:%s is not an ImageMap.')

    def __repr__(self):
        '''
        '''
        return "<class 'moopy.item.ImageMap', name:'%s'>" % (self.name)

    def __str__(self):
        '''
        '''
        return "Image Map, Name '%s'" % (self.name)
    
    def _get_clip_path(self):
        ''''''
        return al.query_services.layer.get_texture_clipfile(self.index)
    
    def _set_clip_path(self, value):
        ''''''
        raise NotImplementedError()
    
    clip_path = property(
        _get_clip_path,
        _set_clip_path,
        doc='''A path of the clipfile (if any) that this instance contains.
        
        @important: This is an expensive property to get, if index is None.
        This is because the layerservice query currently (and unfortunately)
        required to get the clipfile information, requires the index. To
        understand why needing the index could be expensive, read the docs
        of L{<self.index>}
        '''
    )
    
    def _get_index(self):
        ''''''
        return al.query_services.layer.get_texture_index(self._item_id)
    
    def _set_index(self, value):
        ''''''
        raise NotImplementedError()
    
    index = property(
        _get_index,
        _set_index,
        doc='''The index of the texture in the shader tree.
        
        @important: that this object often is created without knowledge of
        the index. So if we don't have it, we must loop through all textures
        until we run into this image map's ID. A very expensive procedure.
        '''
    )
    
    @classmethod
    def new(cls, name=None):
        '''Create a new image map and return that object.'''
        # Create the image map.
        al.commands.shader.create_image_map()
        # Get the item id
        item_id = al.query_services.scene.get_scene_selection('imageMap')
        # Create the instance
        image_map = cls(item_id)
        # Rename it if needed.
        if name is not None:
            image_map.name = name
        # Return it.
        return image_map

class PolyRender(Item):
    ''''''

    _mtype = 'polyRender'
    _mtype_label = 'Poly Render'
    
    def __init__(self, item_id, *args, **kwargs):
        ''''''
        super(PolyRender, self).__init__(item_id, *args, **kwargs)
        
        if al.query_services.scene.get_item_type(item_id) != 'polyRender':
            raise errors.ItemIDNotClassTypeError(
                'ItemID:%s is not a PolyRender.')


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
            self._layer_id, self._name)

    def __str__(self):
        '''
        '''
        return 'Scene Item, Name %s' % (self._name)

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

class Mesh(SceneItem):
    ''''''

    _mtype = 'mesh'
    _mtype_label = 'Mesh'
    
    def __init__(self, item_id, *args, **kwargs):
        ''''''
        super(Mesh, self).__init__(item_id, *args, **kwargs)
        
        if al.query_services.scene.get_item_type(item_id) != 'mesh':
            raise errors.ItemIDNotClassTypeError(
                'ItemID:%s is not a Mesh Item.')

    def __repr__(self):
        '''
        '''
        return "<class 'moopy.item.Mesh', layer_id:%s, name:'%s'>" % (
            self._layer_id, self._name)

    def __str__(self):
        '''
        '''
        return 'Mesh Item, Name %s' % (self._name)



class ItemCollection(object):
    '''A collection of items.'''

    def __init__(self, ids=None, *args, **kwargs):
        '''
        '''
        super(ItemCollection, self).__init__(*args, **kwargs)
        
        if ids is not None:
            #: An iterable object of string IDs.
            self._ids = set(ids)
            #: This serves as cache for the items contained in this class.
            #: That way there is no need to continually create new objects for
            #: each item.
            self._item_cache = dict.fromkeys(ids)
        else:
            self._ids = []
            self._item_cache = {}
    
    def __repr__(self):
        '''
        '''
        return "<class 'moopy.item.ItemCollection', len:%s>" % (self.__len__())

    def __str__(self):
        '''
        '''
        return 'Item Collection, len:%s' % (self.__len__())
    
    def __len__(self):
        ''''''
        return len(self._ids)
    
    def __getitem__(self, index):
        ''''''
        try:
            item_id = self._ids[index]
            if self._item_cache.has_key(item_id):
                return self._item_cache[item_id]
            else:
                item = get_item_class_from_id(item_id)(item_id)
                self._item_cache[item_id] = item
                return item
        except IndexError:
            raise IndexError()
        
    def add_item(self, item):
        '''Add an item to this collection.'''
        
        self._ids += item.item_id
        self._item_cache[item.item_id] = item
    
    def filter_type(self, item_type):
        '''Return a new item collection based on any item matching the type
        given to this method.'''
        
        matching_item_ids = []
        
        for item_id in self._ids:
            if (al.query_services.scene.get_item_type(item_id) == 
                item_type._mtype):
                matching_item_ids.append(item_id)
        
        return ItemCollection(matching_item_ids)
    
    def update(self, collection):
        '''Add a collection to this collection, ignoring any duplicates.'''
        
        self._ids = list(set(collection._ids).union(self._ids))
        self._item_cache.update(collection._item_cache)
    
    def update_selected(self, item_type=None):
        '''Add the selected items to this collection, ignoring any duplicates.
        '''
        
        if item_type is None:
            item_ids = al.query.get_selected_item_ids(item_type._mtype)
        else:
            item_ids = al.query.get_selected_item_ids(item_type._mtype)
        
        if item_ids is not None:
            self._ids = list(set(item_ids).union(self._ids))
        
