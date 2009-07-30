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

def get_all_image_map_ids():
    ''''''
    return get_all_item_ids('imageMap')

def get_all_item_ids(item_type):
    ''''''
    items = []
    total_items = query('%s.N' % item_type)
    for i in range(total_items):
        select(item_type, str(i))
        items.append(query('%s.id' % item_type))
        
    if items:
        return items
    else:
        return None

def get_all_texture_ids():
    ''''''
    return get_all_item_ids('imageMap')

def get_item_children(item_id):
    '''Modo Equivalent: query sceneservice item.children ? item_id'''
    
    select('item.children', item_id)
    return query('item.children')

def get_item_id(index, item_type='item'):
    '''Modo Equivalent: query sceneservice item.id ? index'''
    
    select('%s.id' % item_type, str(index))
    return query('%s.id' % item_type)

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
