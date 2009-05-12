''''''

# Standard
import sys
# Related
import lx
# Local
import errors


def initialize():
    '''Initializing ModoPyWrap will set a few things up for the lib, such as
    rerouting stdout into modo.'''
    
    # Reroute stdout to modo printing.
    sys.stdout = ModoPrinter()

class ModoPrinter(object):
    '''The purpose of this class is to be given to sys.stdout so that standard
    prints will be given to modo's event logger.
    '''
    
    def write(self, content_to_write):
        '''
        '''
        if content_to_write and content_to_write != '\n':
            lx.out('MPW Print: %s' % content_to_write)
