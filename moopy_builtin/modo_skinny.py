#python
'''
'''

# Standard
import logging
import os
# Related
import png
import moopy.item
import moopy.modo_session
import moopy.select
import moopy.al.commands.vertex_map
# Local
moopy.modo_session.initialize(moopy_loglvl=logging.DEBUG, loglvl=logging.DEBUG)

logger = logging.getLogger('script')

# First, setup the script options. xSymmetry is the only one currently.
script_options = moopy.modo_session.ScriptOptions()
script_options.add_option(default=False, allowed_types=[bool],
                          keywords=['xSymmetry', 'xSym'])
script_options.validate_options()

# Get the selected vertices, if any.
vertex_collection = moopy.select.get_selected_vertices()

# If there are no vertices.. fail not implemented. Later i'll add a
# "get all vertices" utility.
if vertex_collection is None:
    logger.debug('No Vertices Selected, Using All.')
    raise NotImplementedError()

logger.debug('Total Vertices: %s' % len(vertex_collection))

# Create a general dict where we'll store a bunch of general info.
vertex_info = {}

# Also, for symmetry, store the verts positions. We can then later, invert
# the numeric value to get the symmetrical vertex. And if it doesn't exist,
# the world explodes.
symmetry_verts = {}

# Loop through all the verts and get their u & v positions.
for vertex in vertex_collection:
    uv_pos = vertex.uv_position()
    world_pos = vertex.position()
    vertex_info[vertex.index] = {
        'u':uv_pos[0],
        'v':uv_pos[1],
        'total_weight':0.0 # Also, add a default "total_weight" for later.
    }
    symmetry_verts[world_pos[0]] = vertex

# Create a dict where we'll store the weight information we get
# from the images. We store it in this way because of how we write the weights.
# Format:
#weight_information = {
    #'im a weight name':{
        #185:0.1, The Weight Indices, and the weight values.
        #186:0.3,
        #187:0.5,
    #},
#}
weight_information = {}
ordered_weight_names = []

def parse_image(path):
    ''''''
    file_name = os.path.basename(path)

    logger.debug('Loading %s' % path)

    # Load the image
    png_reader = png.Reader(filename=path)

    # Read it.
    (image_width, image_height,
     image_pixels, image_metadata) = png_reader.read()

    logger.debug('Loaded %s, Size:%sx%s' % (
        file_name, image_width, image_height))

    weight_information[file_name] = {}
    ordered_weight_names.append(file_name)
    
    # For every vertex, look up its position.
    for vertex_index in vertex_info:

        x = int(image_width * vertex_info[vertex_index]['u'])
        y = int(image_height - image_height * 
                vertex_info[vertex_index]['v'])

        pixel_index = x + (y - 1) * image_width

        pixel_alpha = float(image_pixels[pixel_index * 4 + 3]) / 255.0

        weight_information[file_name][vertex_index] = pixel_alpha

    logger.debug(
        'Image %s resulted in the following weights:' % file_name)
    logger.debug(str(weight_information[file_name]))

# Grab the scene's image maps, in shader order.
poly_render = moopy.item.PolyRender(
    moopy.item.get_id_by_index(0, item_type='polyRender')
)
#poly_render = moopy.item.PolyRender('polyRender007')
image_maps = poly_render.children.filter_type(moopy.item.ImageMap)

# Now for the _SLOW_ part. Loop through each clip, load the image into python,
# and start grabbing verts.
for image_map in image_maps:
    parse_image(image_map.clip_path)

for weight_name in ordered_weight_names:
    # Now because this is an early and ugly test,
    # we simply mass create all the weight maps we need.
    # So i hope you don't have any with the same name.. :)
    moopy.al.commands.vertex_map.new_weight_map(weight_name)

    # After creation, they are automatically selected so now we work with
    # that. Loop through all the verts and start assigning weights
    # for this map.
    for (vertex_index,
         vertex_weight_value) in weight_information[weight_name].items():

        total_weight = vertex_info[vertex_index]['total_weight']

        if total_weight >= 1.0:
            # If the total is already 1.0, we can just skip this vert and
            # go to the next.
            continue
        elif total_weight + vertex_weight_value > 1.0:
            # If adding this value to the total is more than 1.0, find the
            # amount it is over by (overage), and subtract the weight_value
            # by the overage.
            overage = (vertex_weight_value + total_weight) - 1.0
            vertex_weight_value -= overage

        logger.debug('Vert: %s, Value: %s, Map %s' % (
            vertex_index, vertex_weight_value, weight_name))

        vertex_collection.by_index(vertex_index).set_weight(
            weight_name, vertex_weight_value)

        # Also, add this to whatever the total is.
        vertex_info[vertex_index]['total_weight'] += vertex_weight_value

# Now we have assigned all the vertices with values coorisponding to the
# images, but there are still many with no image color, and therefor
# no weight. Apply all these with whatever weight fills them to 1.0 weight in
# a last weightmap called "base_weight" (hopefully no one has an image like
# this.. hmm.. lol)
moopy.al.commands.vertex_map.new_weight_map('base_weight')

for vertex_index in vertex_info:

    total_weight = vertex_info[vertex_index]['total_weight']

    if total_weight >= 1.0:
        continue

    difference = 1.0 - total_weight

    vertex_collection.by_index(vertex_index).set_weight(
        'base_weight', difference)

# This dumpy test is done.. i think :)
print 'Script Completed Successfully!'
