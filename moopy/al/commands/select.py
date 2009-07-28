'''
'''

# Standard
# Related
import lx
# Local


def vert_map(name, map_type, mode):
    '''Select a vertex map.
    
    @param map_type: The type of vertex map. Can be one of the following
    values:
        'wght', 'subd', 'txuv', 'morf', 'spot',
        'rgb', 'rgba', 'pick', 'norm', 'epck'
    @param mode: How the select is preformed, eg, replaces, adds, etc. Can be
    one of the following values:
        'replace', 'add', 'remove'
    '''
    lx.eval('select.vertexMap name:"%s" type:%s mode:%s' % (name,
                                                            map_type,
                                                            mode))
