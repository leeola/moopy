''''''

# Standard
# Related
# Local
import moopy.al.query_services.layer


class Clip(object):
    '''A representation of a single clip item.
    
    @todo: Convert this class to use the sceneservice's clip.
    '''

    def __init__(self, clip_index, *args, **kwargs):
        ''''''
        super(Clip, self).__init__(*args, **kwargs)
        
        self._index = clip_index
    
    def __getitem__(self, key):
        ''''''
        return Clip(self._index)
    
    def __repr__(self):
        ''''''
        return "<class 'moopy.image.Clip', index:%s, name:%s>" % (
            self._index, self.name)
    
    def __str__(self):
        ''''''
        return 'Clip, Index "%s", Name: %s' % (self._index, self.name)
    
    def _get_index(self):
        ''''''
        return self._index
    
    index = property(
        _get_index,
        doc='''The index of the mesh element.
        '''
    )
    
    def _get_path(self):
        ''''''
        return moopy.al.query_services.layer.get_clip_path(self._index)
    
    def _set_path(self, value):
        ''''''
        raise NotImplementedError()
    
    path = property(
        _get_path,
        _set_path,
        doc='''
        '''
    )    
    
    def _get_name(self):
        ''''''
        return moopy.al.query_services.layer.get_clip_name(self._index)
    
    def _set_name(self, value):
        ''''''
        raise NotImplementedError()
    
    name = property(
        _get_name,
        _set_name,
        doc='''
        '''
    )
    

class ClipCollection(object):
    '''A collection of clips. Astouding naming convention right?'''

    def __init__(self, clip_indices, *args, **kwargs):
        ''''''
        super(ClipCollection, self).__init__(*args, **kwargs)
        
        #: A iterable object containing the indices of this clip collection.
        self._indices = clip_indices
    
    def __getitem__(self, key):
        ''''''
        return Clip(self._indices[key])

    def __len__(self):
        ''''''
        return len(self._indices)
    
    def __repr__(self):
        ''''''
        return "<class 'moopy.mesh_element.ClipCollection', index:%s>" % (
            self._index)
    
    def __str__(self):
        ''''''
        return 'Clip Collection, Index "%s"' % (self._index)
    
    def _get_indices(self):
        ''''''
        return self._indices
    
    indices = property(
        _get_indices,
        doc='''A list of the clip indices contained within this collection.
        '''
    )
