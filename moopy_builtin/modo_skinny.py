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
mesh_items.update_selected(item_type=moopy.item.Mesh)

