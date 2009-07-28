''''''

# Standard
# Related
# Local
import moopy.image
import moopy.mesh_element
import moopy.al.query_services.layer


CENTER_SELECTION = 'CENTER_SELECTION'
EDGE_SELECTION = 'EDGE_SELECTION'
ITEM_SELECTION = 'ITEM_SELECTION'
MATERIAL_SELECTIO = 'MATERIAL_SELECTIO'
PIVOT_SELECTION = 'PIVOT_SELECTION'
POLYGON_SELECTION = 'POLYGON_SELECTION'
VERTEX_SELECTION = 'VERTEX_SELECTION'

def get_all_clips():
    ''''''
    
    clip_indices = moopy.al.query_services.layer.get_clip_indicies()
    
    if clip_indices is None:
        return None
    
    return moopy.image.ClipCollection(clip_indices)

def get_selected_edges():
    ''''''
    raise NotImplementedError()

def get_selected_vertices():
    '''Get the selected vertices.
    
    @return: A vertex collection, or None if none are selected.
    '''
    selected_indices = moopy.al.query_services.layer.get_vert_indices()
    
    if selected_indices is None:
        return None
    
    return moopy.mesh_element.VertexCollection(selected_indices)

def get_selection_type():
    '''
    '''
    raise NotImplementedError()

def set_selected_edges():
    ''''''
    raise NotImplementedError()

def set_selection_type():
    '''
    '''
    raise NotImplementedError()
