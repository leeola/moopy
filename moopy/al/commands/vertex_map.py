'''
'''

# Standard
# Related
import lx
# Local


def new_weight_map(name, initial_value=None):
    ''''''
    if initial_value is not None:
        lx.eval('vertMap.new %s type:wght '
                'init_value:true value:%s' % (name, initial_value))
    else:
        lx.eval('vertMap.new %s type:wght init:false' % name)

def set_vertex_value(weight_name, vertex_index, weight_value):
    ''''''
    lx.eval('vertMap.setVertex {%s} weight 0 %s %s' % (
        weight_name, vertex_index, weight_value))
