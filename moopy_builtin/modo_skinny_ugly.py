#python
'''The "ugly" version of this script was basically written quickly with no
real focus on the code being readable, clean, etc. It was written to test the
concept of modo skinny.

Because of the hastened testing, this file is buggy and not intended
for any real use. See L{<modo_skinny>} for the real file.
'''

# Standard
import logging
import os
# Related
import lx
import moopy.item
import moopy.modo_session
import moopy.select
import moopy.al.commands.vertex_map
# Local
moopy.modo_session.initialize()

logger = logging.getLogger('script')

# First, setup the script options. xSymmetry is the only one currently.
script_options = moopy.modo_session.ScriptOptions()
script_options.add_option(default=False, allowed_types=[bool],
                          keywords=['xSymmetry', 'xSym'])
script_options.add_option(default=False, allowed_types=[bool],
                          keywords=['base_weight', 'base'])
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

# Loop through all the verts and get their u & v positions.
for vertex in vertex_collection:
    uv_pos = vertex.uv_position()
    world_pos = vertex.position()
    vertex_info[vertex.index] = {
        'u':uv_pos[0],
        'v':uv_pos[1],
        'x_pos':world_pos[0],
        'total_weight':0.0, # Also, add a default "total_weight" for later.
        'highest_weight':0.0,
        'highest_weight_maps':[], 
        'weights':[], # This is just used for debugging. We append each write.
    }

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

def parse_image_with_pil(path):
    ''''''
    import PIL.Image
    
    file_name = os.path.basename(path)

    logger.debug('Loading %s' % path)

    # Load the image
    image = PIL.Image.open(path)
    image_width, image_height = image.size
    
    logger.debug('Loaded %s' % (file_name))

    weight_information[file_name] = {}
    ordered_weight_names.append(file_name)
    
    # For every vertex, look up its position.
    for vertex_index in vertex_info:

        x = int(image_width * vertex_info[vertex_index]['u'])
        y = int(image_height - image_height * vertex_info[vertex_index]['v'])
        
        if x == image_height:
            x -= 1
        if y == image_height:
            y -= 1
        
        pixel_alpha = image.getpixel((x, y))[3] / 255.0
        
        weight_information[file_name][vertex_index] = pixel_alpha

    logger.debug(
        'Image %s resulted in the following weights:' % file_name)
    logger.debug(str(weight_information[file_name]))
    

def parse_image_with_pngpy(path):
    ''''''
    import png
    
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
    parse_image_with_pil(image_map.clip_path)

def assign_weights_to_map(weight_name, side=None):
    ''''''
    
    source_weight_name = weight_name
    
    if side == 'left':
        weight_name = 'L_%s' % weight_name
    elif side == 'right':
        weight_name = 'R_%s' % weight_name
    
    for (vertex_index,
         vertex_weight_value) in weight_information[source_weight_name].items():
        
        # This is a horrendous implementation of weighting symmetry.
        # On the real version of the script, this will be vastly improved.
        # For now though, its quick, its dirty, and it gets the job done.
        if side == 'left' and vertex_info[vertex_index]['x_pos'] < 0:
            continue
        elif side == 'right' and vertex_info[vertex_index]['x_pos'] > 0:
            continue
        elif side is not None and vertex_info[vertex_index]['x_pos'] == 0:
            vertex_weight_value = vertex_weight_value / 2
        
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
        vertex_info[vertex_index]['weights'].append(
            '%s:%s' % (weight_name, vertex_weight_value))
        
        # If this value is the highest this vert has been assigned yet,
        # store it.
        highest_weight = vertex_info[vertex_index]['highest_weight']
        if vertex_weight_value > highest_weight:
            vertex_info[vertex_index]['highest_weight'] = vertex_weight_value
            vertex_info[vertex_index]['highest_weight_maps'] = [weight_name]
        elif vertex_weight_value == highest_weight:
            vertex_info[vertex_index]['highest_weight_maps'].append(
                weight_name)
            

for weight_name in ordered_weight_names:
    # Now because this is an early and ugly test,
    # we simply mass create all the weight maps we need.
    # So i hope you don't have any with the same name.. :)
    
    if script_options['xSymmetry']:
        moopy.al.commands.vertex_map.new_weight_map('L_%s' % weight_name)
        assign_weights_to_map(weight_name, 'left')
        lx.eval('deform.mapadd')
        moopy.al.commands.vertex_map.new_weight_map('R_%s' % weight_name)
        assign_weights_to_map(weight_name, 'right')
        lx.eval('deform.mapadd')
    else:
        moopy.al.commands.vertex_map.new_weight_map(weight_name)
        assign_weights_to_map(weight_name)
        lx.eval('deform.mapadd')


if script_options['base_weight']:
    moopy.al.commands.vertex_map.new_weight_map('base_weight')
    
    for vertex_index in vertex_info:
    
        total_weight = vertex_info[vertex_index]['total_weight']
    
        if total_weight >= 1.0:
            continue
    
        difference = 1.0 - total_weight
    
        vertex_collection.by_index(vertex_index).set_weight(
            'base_weight', difference)
    
    lx.eval('deform.mapadd')
else:
    
    for vertex_index in vertex_info:
    
        total_weight = vertex_info[vertex_index]['total_weight']
        highest_weight = vertex_info[vertex_index]['highest_weight']
        highest_weight_maps = vertex_info[vertex_index]['highest_weight_maps']
    
        if total_weight >= 1.0:
            continue
    
        difference = (1.0 - total_weight) / float(len(highest_weight_maps))
     
        logger.debug('Supplementing "%s", total:%s, diff:%s, vert:%s' % (
            highest_weight_maps, total_weight, difference, vertex_index))
        
        added_weight = highest_weight + difference
        
        # 228, 229, 230 are some bad ones.
        if vertex_index == 195:
            pass
        
        for weight_name in highest_weight_maps:
            vertex_collection.by_index(vertex_index).set_weight(
                weight_name, added_weight)
            
            vertex_info[vertex_index]['total_weight'] += difference
            vertex_info[vertex_index]['weights'].append(
                '%s:%s' % (weight_name, difference))
    

# This dumpy test is done.. i think :)
print 'Script Completed Successfully!'
