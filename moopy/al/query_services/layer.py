'''
'''

# Standard
# Related
import lx
# Local


#: Just for the sake of reducing repeated code, we define a global service
#: object here.
_service_object = lx.Service('layerservice')

def list_roots():
    '''Return a tuple of all the roots found in layerservice.'''
    return _service_object.query()

def get_all_vert_indices():
    ''''''
    return _service_object.query('verts ? all')

def get_layer_groups():
    ''''''
    return _service_object.query('layer_groups')

def get_layer_id():
    ''''''
    return _service_object.query('layer.id')

def get_layer_name():
    ''''''
    return _service_object.query('layer.name')

def get_selected_vert_indices():
    ''''''
    return _service_object.query('verts ? selected')

def get_unselected_vert_indices():
    ''''''
    return _service_object.query('verts ? unselected')

def get_visible_vert_indices():
    ''''''
    return _service_object.query('verts ? visible')

def select(*selectors):
    ''''''
    _service_object.select(*selectors)

def select_layer_all():
    ''''''
    select('layer', 'all')

def select_layer_bg():
    ''''''
    select('layer', 'bg')

def select_layer_fg():
    ''''''
    select('layer', 'fg')

def select_layer_id(layer_id):
    ''''''
    select('layer.id', layer_id)

def select_layer_main():
    ''''''
    select('layer', 'main')

def select_layer_name(name):
    ''''''
    select('layer.name', name)
