'''This module specifically relates to querying information from modo.
'''

# Standard
# Related
import lx
# Local


_sceneservice_object = lx.Service('sceneservice')

def get_all_item_ids(item_type='item'):
    '''Get all the item id's the active scene.
    
    @param item_type: The item types you wish to have returned, if any.
    '''
    items = []
    total_items = _sceneservice_object.query('%s.N' % item_type)
    # Store the item.id string so that it isn't calculated every iteration.
    item_id_string = '%s.id' % item_type
    for i in range(total_items):
        _sceneservice_object.select(item_type, str(i))
        items.append(_sceneservice_object.query(item_id_string))
        
    if items:
        return items
    else:
        return None

def get_selected_item_ids(item_type='item'):
    '''Get the selected item id's the active scene.
    
    @param item_type: The item types you wish to have returned, if any.
    '''
    items = []
    total_items = _sceneservice_object.query('%s.N' % item_type)
    # Store the item.id string so that it isn't calculated every iteration.
    item_id_string = '%s.id' % item_type
    for i in range(total_items):
        _sceneservice_object.select(item_type, str(i))
        if not not _sceneservice_object.query('item.isSelected'):
            items.append(_sceneservice_object.query(item_id_string))
        
    if items:
        return items
    else:
        return None

def get_item_mtype(item_id):
    ''''''
    
    _sceneservice_object.select('item.type', item_id)
    return _sceneservice_object.query('item.type')

def get_item_mtypes():
    '''Return all of the possible mtypes from modo.'''
    
    return _sceneservice_object.query('types')
