'''
'''

# Standard
# Related
import lx
# Local


def create(shader_type):
    '''Create a new shader and add it to the current shader context.
    '''
    return lx.eval('shader.create %s' % shader_type)
    
def create_image_map():
    '''Create a new image map and add it to the current shader context.
    '''
    return lx.eval('shader.create imageMap')
