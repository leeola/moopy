'''
'''

# Standard
import logging
# Related
import lx
# Local


#: Just for the sake of reducing repeated code, we define a global service
#: object here.
_service_object = lx.Service('layerservice')

logger = logging.getLogger('moopy')
select = _service_object.select
query = _service_object.query

def _convert_strings_to_ints(strings):
    '''A small utility function for converting a tuple of strings into
    integers, note that this also converts a single string into an integer and
    puts it inside of a list.'''
    
    if strings is None:
        return None
    
    # If it is a string, it is a single vert.
    if type(strings) == str:
        return [int(strings)]
    
    # This _needs_ to be faster. Log a debug warning and do it slowly for now.
    # I'm avoiding premature optimization. :)
    logger.debug('APO: al.query_services.layer._convert_strings_to_ints()')
    
    def convert_to_int(numeric_string):
        ''''''
        return int(numeric_string)
    
    return map(convert_to_int, strings)


def list_roots():
    '''Return a tuple of all the roots found in layerservice.'''
    return query()

def list_attributes(root_attribute):
    '''Return a tuple of all the attributes found within a .'''
    return query(root_attribute)

def get_clip_indicies():
    ''''''
    return _convert_strings_to_ints(query('clips'))

def get_clip_name(clip_index):
    ''''''
    select('clip.name', str(clip_index))
    return query('clip.name')

def get_clip_path(clip_index):
    ''''''
    select('clip.file', str(clip_index))
    return query('clip.file')

def get_layer_groups():
    ''''''
    return query('layer_groups')

def get_layer_id():
    ''''''
    return query('layer.id')

def get_layer_name():
    ''''''
    return query('layer.name')

def get_texture_clipfile(texture_index):
    ''''''
    select('texture.clipfile', str(texture_index))
    return query('texture.clipfile')

def get_texture_index(texture_id):
    ''''''
    select()
    total_textures = query('texture.N')

    for i in range(total_textures):
        select('texture.id', str(i))
        if query('texture.id') == texture_id:
            return i
    
    # If the texture_id is not found, raise a NotImplemented for now.
    raise NotImplementedError()

def get_uv_pos(vertex_index, uv_map_name=None):
    ''''''
    if uv_map_name is not None:
        raise NotImplementedError()
    
    # I think this is just vert indices.. i think.
    # Also, i'm doing this twice because of a weird problem.
    # The first query, results in a different position than the 2nd query.
    # If i call select twice, that issue doesn't appear. Later this needs
    # to be fixed.
    select('uv.pos', str(vertex_index))
    select('uv.pos', str(vertex_index))
    return query('uv.pos')

def get_vert_indices():
    ''''''
    select('selected')
    return _convert_strings_to_ints(query('verts'))

def get_vert_pos(vert_index):
    ''''''
    select('vert.pos', str(vert_index))
    return query('vert.pos')

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
