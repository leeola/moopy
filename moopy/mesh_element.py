''''''

# Standard
# Related
# Local


class MeshElement(object):
    '''The base mesh element class.'''

    def __init__(self, mesh_item, *args, **kwargs):
        '''
        '''
        super(MeshElement, self).__init__(*args, **kwargs)
        
        #: The mesh item this element is contained within.
        self._mesh_item = mesh_item
    
    def _get_mesh_item():
        ''''''
        raise exceptions.NotImplementedError()
    
    mesh_item = property(
        _get_mesh_item,
        doc='''The mesh item that contains this mesh element.
        '''
    )


class Vertex(MeshElement):
    '''Instances of this class represent a single vertex.'''

    def __init__(self, mesh_item, *args, **kwargs):
        '''
        '''
        super(Vertex, self).__init__(*args, **kwargs)
     
