'''
'''

# Standard
# Related
# Local


#: Just for the sake of reducing repeated code, we define a global service
#: object here.
_service_object = lx.Service('sceneservice')

def list_roots():
    '''Return a tuple of all the roots found in sceneservice.'''
    return _service_object.query()

def list_attributes(root_attribute):
    '''Return a tuple of all the attributes found within a .'''
    return _service_object.query('%s ?' % root_attribute)

def get_is_type(item_type):
    '''Modo Equivalent: query sceneservice isType ? item_type'''
    
    return not not _service_object.query('isType ? %s' % item_type)

def get_scene_selection(item_type='all'):
    '''Modo Equivalent: query sceneservice selection ? item_type'''
    
    return _service_object.query('selection ? %s' % item_type)

def get_types():
    '''Modo Equivalent: query sceneservice types ? '''
    
    _service_object.query('types')
