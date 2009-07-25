''''''

# Standard
# Related
# Local


class MeshElement(object):
    '''The base mesh element class.'''

    def __init__(self, element_index, *args, **kwargs):
        '''
        '''
        super(MeshElement, self).__init__(element_index, *args, **kwargs)
        
        
        raise exceptions.NotImplementedError()
    
    def _get_mesh_item():
        ''''''
        raise exceptions.NotImplementedError()
    
    mesh_item = property(
        _get_mesh_item,
        doc='''The mesh item that contains this mesh element.
        '''
    )
    
    def _get_index():
        ''''''
        raise exceptions.NotImplementedError()
    
    def _set_index():
        ''''''
        raise exceptions.NotImplementedError()
    
    index = property(
        _get_index,
        _set_index,
        doc='''The index of the mesh element.
        '''
    )

class Vertex(MeshElement):
    '''A representation of a single vertex.'''

    def __init__(self, vertex_index, *args, **kwargs):
        '''
        '''
        super(Vertex, self).__init__(vertex_index, *args, **kwargs)


class MeshElementCollection(object):
    '''The base mesh element collection class.'''
    
    def __init__(self, element_indices, *args, **kwargs):
        '''
        '''
        super(MeshElementCollection, self).__init__(
            element_indices, *args, **kwargs)
        
class VertexCollection(object):
    '''A collection of vertices'''

    
    def __init__(self, vertex_indices, *args, **kwargs):
        '''
        '''
        super(VertexCollection, self).__init__(vertex_indices, *args, **kwargs)

