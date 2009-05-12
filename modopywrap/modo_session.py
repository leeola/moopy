''''''

# Standard
import sys
import logging
# Related
import lx
# Local
import errors

#: An instance of L{SessionInfo} created by L{initialize}
session_info = None

def initialize():
    '''Initializing ModoPyWrap will set a few things up for the lib, such as
    rerouting stdout into modo and creating a L{SessionInfo} object.'''
    
    # Reroute stdout to modo printing.
    sys.stdout = ModoPrinter()
    
    # Create a session info instance, and assign it to the module level object.
    global session_info
    session_info = SessionInfo()
    
    # Set the logger to be used in MPW.
    logger = logging.getLogger()
    logging_handler = logging.StreamHandler(sys.stdout)
    
    # Create formatter, its important that it starts with "MPW Log", so
    # that it is formatted properly when printed to modo.
    logging_formatter = logging.Formatter(
        'MPW Log: %(name)s - %(levelname)s - %(message)s')
    
    # Now add the formatter and then the logger.
    logging_handler.setFormatter(logging_formatter)
    logger.addHandler(logging_handler)

class SessionInfo(object):
    '''This class stores information about the "modo session". On initialization
    (usually done via L{initialize}), it inspects modo for collection of
    information.
    '''

    def __init__(self):
        '''
        '''
        # I'll be adding this soon.
        pass

class ModoPrinter(object):
    '''The purpose of this class is to be given to sys.stdout so that standard
    prints will be given to modo's event logger.
    '''
    
    def write(self, content_to_write):
        '''
        '''
        if content_to_write and content_to_write != '\n':
            if content_to_write.startswith('MPW Log'):
                lx.out(content_to_write)
            else:
                lx.out('MPW Print: %s' % content_to_write)
