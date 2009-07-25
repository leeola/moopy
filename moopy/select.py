''''''

# Standard
# Related
# Local


CENTER_SELECTION = 'CENTER_SELECTION'
EDGE_SELECTION = 'EDGE_SELECTION'
ITEM_SELECTION = 'ITEM_SELECTION'
MATERIAL_SELECTIO = 'MATERIAL_SELECTIO'
PIVOT_SELECTION = 'PIVOT_SELECTION'
POLYGON_SELECTION = 'POLYGON_SELECTION'
VERTEX_SELECTION = 'VERTEX_SELECTION'

def get_selection_type():
    '''
    '''
    raise NotImplementedError()

def get_selected_edges():
    ''''''
    raise NotImplementedError()

def get_selected_vertices():
    '''Get the selected vertices.
    
    @return: A vertex collection, or None if none are selected.
    '''
    raise NotImplementedError()

def set_selection_type():
    '''
    '''
    raise NotImplementedError()

def set_selected_edges():
    ''''''
    raise NotImplementedError()
