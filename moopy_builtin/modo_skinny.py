#python
'''Modo Skinny is a script which takes a series of image maps (which are
tied to images) and converts them to mesh weights to be used as deformations
for character animation.
'''

if os.environ.has_key('WINGDB_ACTIVE'):
    del os.environ['WINGDB_ACTIVE']
import wingdbstub

# Standard
import logging
import os
# Related
import moopy.item
import moopy.mesh_element
import moopy.modo_session
# Local


moopy.modo_session.initialize()

logger = logging.getLogger('script')

# First, setup the script options.
script_options = moopy.modo_session.ScriptOptions()
script_options.add_option(default=False, allowed_types=[bool],
                          keywords=['symmetry', 'sym'])
script_options.add_option(default=False, allowed_types=[bool],
                          keywords=['base_weight', 'base'])
script_options.add_option(default=False, allowed_types=[bool],
                          keywords=['create_deformers', 'def'])
script_options.add_option(default=False, allowed_types=[bool],
                          keywords=['replace_weight_maps', 'rep_maps'])
script_options.validate_options()

# Create an item collection
mesh_items = moopy.item.ItemCollection()

# Add the active mesh items.
mesh_items.add_selected(item_type=moopy.item.Mesh)

if len(mesh_items) == 0:
    raise NotImplemented()

elif len(mesh_items) > 1:
    raise NotImplemented()

# Get the selected mesh item.
mesh_item = mesh_items[0]

def get_images(uv_map):
    '''Get a list of images to use with this script. Returned as a list
    of paths.'''
    
    image_maps = moopy.item.ItemCollection()
    image_maps.add_selected(item_type=moopy.item.ImageMap)
    
    if len(image_maps) == 0:
        raise NotImplemented()
    
    image_map_paths = []
    
    for image_map in image_maps:
        logger.debug('Handling image map "%r"' % image_map)
        
        image_map_uv = image_map.uv_map
        
        if image_map_uv != uv_map:
            logger.info(
                'Not using image map "%s" because it is not using the '
                'selected UV Map.' % image_map_uv
            )
            
            image_maps.remove(image_map)
            continue
        
        image_map_paths.append(image_map.clip.path)
    
    return image_map_paths

def get_uv_map(mesh_item):
    '''Get the uv map we are going to work with.'''
    # Get a VMap collection of the mesh item's UVs.
    uv_maps = moopy.vertex_maps.VMapCollection(mesh_item)
    uv_maps.update_selected(weight=False, morph=False, other=False)
    
    if len(uv_maps) == 0:
        raise NotImplemented()
    
    elif len(uv_maps) > 1:
        raise NotImplemented()
    
    # Get the uv_map.
    return uv_maps[0]

def get_vertex_uv_positions(mesh_item):
    '''Get the uv positions of each vertex and return a dict where the
    keys are the vert IDs, and the keys are a tuple of U and V values.'''
    
    if 0:
        # A little bit for WingIDE Autocomplete.
        assert isinstance(mesh_item, moopy.item.Mesh)
        
    raise NotImplemented()
