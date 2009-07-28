'''
'''

# Standard
# Related
import lx
# Local


#: Just for the sake of reducing repeated code, we define a global service
#: object here.
_service_object = lx.Service('sceneservice')

query = _service_object.query
select = _service_object.select

def list_roots():
    '''Return a tuple of all the roots found in sceneservice.'''
    
    select()
    return query()

def list_attributes(root_attribute):
    '''Return a tuple of all the attributes found within a .'''
    
    select()
    return query(root_attribute)

def get_item_name(item_id):
    '''Modo Equivalent: query sceneservice item.name ? item_id'''
    
    select('item.name', item_id)
    return query('item.name')

def get_item_type(item_id):
    '''Modo Equivalent: query sceneservice item.type ? item_id'''
    
    select('item.type', item_id)
    return query('item.type')

def get_is_type(item_id):
    '''Modo Equivalent: query sceneservice isType ? item_id'''
    
    select('isType', item_id)
    return not not query('isType')

def get_scene_selection(item_type='all'):
    '''Modo Equivalent: query sceneservice selection ? item_type'''
    
    select('selection', item_type)
    return query('selection')

def get_types():
    '''Modo Equivalent: query sceneservice types ? '''
    
    select()
    return query('types')
