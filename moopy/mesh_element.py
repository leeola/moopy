''''''

# Standard
import logging
# Related
import lx
# Local
import moopy.al.commands.select
import moopy.al.commands.vertex_map
import moopy.al.query_services.layer

logger = logging.getLogger('moopy')

class MeshElement(object):
    '''The base mesh element class.'''

    def __init__(self, element_index, *args, **kwargs):
        '''
        '''
        super(MeshElement, self).__init__(*args, **kwargs)
        
        self._index = element_index
    
    def __repr__(self):
        ''''''
        return "<class 'moopy.mesh_element.MeshElement', index:%s>" % (
            self._index)
    
    def __str__(self):
        ''''''
        return 'Mesh Element, Index "%s"' % (self._index)
    
    def _get_mesh_item(self):
        ''''''
        raise exceptions.NotImplementedError()
    
    mesh_item = property(
        _get_mesh_item,
        doc='''The mesh item that contains this mesh element.
        '''
    )
    
    def _get_index(self):
        ''''''
        return self._index
    
    index = property(
        _get_index,
        doc='''The index of the mesh element.
        '''
    )

class Vertex(MeshElement):
    '''A representation of a single vertex.'''

    def __init__(self, vertex_index, *args, **kwargs):
        '''
        '''
        super(Vertex, self).__init__(vertex_index, *args, **kwargs)
    
    def __repr__(self):
        ''''''
        return "<class 'moopy.mesh_element.Vertex', index:%s>" % (
            self._index)
    
    def __str__(self):
        ''''''
        return 'Mesh Vertex, Index "%s"' % (self._index)
    
    @classmethod
    def new(self):
        ''''''
        raise NotImplementedError()
    
    def uv_position(self, map_name=None):
        '''This method of accessing the U & V coordinates of a vertex will
        probably be deprecated at some point.
        '''
        
        if map_name is not None:
            raise NotImplementedError()
        
        return moopy.al.query_services.layer.get_uv_pos(self._index, map_name)
    
    def position(self):
        '''This method of accessing the global position of a vertex will
        be deprecated at some point soon.
        '''
        
        return moopy.al.query_services.layer.get_vert_pos(self._index)
    
    def set_weight(self, map_name, weight):
        '''
        Again, this method will get nixed in favor of an OOP approach.
        '''
        moopy.al.commands.vertex_map.set_vertex_value(
            map_name, self._index, weight)

class MeshElementCollection(object):
    '''The base mesh element collection class.'''
    
    def __init__(self, element_indices, *args, **kwargs):
        '''
        '''
        super(MeshElementCollection, self).__init__(*args, **kwargs)
        
        #: A iterable object containing the indices of this element collection.
        self._indices = element_indices
    
    def __len__(self):
        ''''''
        return len(self._indices)
    
    def __repr__(self):
        ''''''
        return "<class 'moopy.mesh_element.MeshElementCollection', len:%s>" % (
            self.__len__())
    
    def __str__(self):
        ''''''
        return 'Mesh Element Collection, Total Elements %s' % (self.__len__())
    
    def _get_indices(self):
        ''''''
        return self._indices
    
    indices = property(
        _get_indices,
        doc='''A list of the mesh element indices contained within this
        collection.
        '''
    )

class VertexCollection(MeshElementCollection):
    '''A collection of vertices'''
    
    def __init__(self, vertex_indices, *args, **kwargs):
        '''
        '''
        super(VertexCollection, self).__init__(vertex_indices, *args, **kwargs)
    
    def __getitem__(self, key):
        ''''''
        return Vertex(self._indices[key])
    
    def __repr__(self):
        ''''''
        return "<class 'moopy.mesh_element.VertexCollection', len:%s>" % (
            self.__len__())
    
    def __str__(self):
        ''''''
        return 'Vertex Collection, Total Vertices %s' % (self.__len__())

    def by_index(self, index):
        '''Get a vertex by it's index.'''
        return Vertex(index)
