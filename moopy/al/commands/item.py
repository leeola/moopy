'''
'''

# Standard
# Related
import lx
# Local


def create_mesh(name=None, mask=None):
    ''''''
    command = 'item.create mesh'
    if name is not None:
        command += ' name:%s' % name
    if mask is not None:
        command += ' mask:%s' % name
    lx.eval(command)
