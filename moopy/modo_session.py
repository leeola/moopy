''''''

# Standard
import logging
import shlex
import sys
# Related
import lx
# Local
import errors

#: An instance of L{SessionInfo} created by L{initialize}
session_info = None

def initialize(moopy_loglvl=logging.WARNING, moopy_logfile=None,
               loglvl=logging.WARNING, logfile=None, stdout_modo=True):
    '''Initializing Moopy will set a few things up for the lib, such as
    rerouting stdout into modo and creating a L{SessionInfo} object.
    
    @param moopy_loglvl: Set the loglevel for moopy, internally.
    Note that it will be overriden by the client value, if given.
    
    @param moopy_logfile: Set the logfile for moopy, internally.
    Note that it will be overriden by the client value, if given.
    
    @param loglvl: Set the loglvl for client scripts.
    Note that it will be overriden by the client value, if given.
    
    @param logfile: Set the logfile for client scripts.
    Note that it will be overriden by the client value, if given.
    '''
    if stdout_modo:
        # Reroute stdout to modo printing.
        sys.stdout = ModoPrinter()
    
    # Create a session info instance, and assign it to the module level object.
    global session_info
    session_info = SessionInfo()
    
    log_levels = {
        'debug': logging.DEBUG,
        'info': logging.INFO,
        'warning': logging.WARNING,
        'error': logging.ERROR,
        'critical': logging.CRITICAL
    }
    
    if session_info.keyword_arguments is not None:
        # Now we set the moopy log level. If the user defined one, use his.
        if session_info.keyword_arguments.has_key('moopy_loglvl'):
            moopy_loglvl = log_levels[
                session_info.keyword_arguments['moopy_loglvl'].lower()]
        # If the user defined a file to log to, grab that value.
        if session_info.keyword_arguments.has_key('moopy_logfile'):
            moopy_logfile = session_info.keyword_arguments['moopy_logfile']
        
        # The same as above, except for the root logger, aka, the script logger.
        if session_info.keyword_arguments.has_key('loglvl'):
            loglvl = log_levels[
                session_info.keyword_arguments['loglvl'].lower()]
        if session_info.keyword_arguments.has_key('logfile'):
            logfile = session_info.keyword_arguments['logfile']
    
    # Create/get both the moopy and script loggers
    script_logger = logging.getLogger()
    moopy_logger = logging.getLogger('Moopy')
    
    # Create handlers for both loggers
    script_handler = logging.StreamHandler(sys.stdout)
    moopy_handler = logging.StreamHandler(sys.stdout)
    
    # Create formatter, its important that it starts with "Moopy Script Log", or
    # "Moopy Log" so that it is formatted properly when printed to modo.
    script_formatter = logging.Formatter(
        'Moopy Script Log: %(levelname)s - %(message)s')
    moopy_formatter = logging.Formatter(
        'Moopy Log: %(levelname)s - %(message)s')
    
    # Add the formatters to the handlers.
    script_handler.setFormatter(script_formatter)
    moopy_handler.setFormatter(moopy_formatter)
    
    # Add the handlers
    script_logger.addHandler(script_handler)
    moopy_logger.addHandler(moopy_handler)
    
    # Set the log levels.
    script_logger.setLevel(loglvl)
    moopy_logger.setLevel(moopy_loglvl)
    
    # Finally, repeat the log steps above if the user defined any file loggers.
    if logfile is not None:
        # For now if the user gives a bad file, let the loggers throw the
        # exceptions.
        script_file_handler = logging.FileHandler(logfile)
        script_file_formatter = logging.Formatter(
            'Moopy Script Log: [%(asctime)s] %(levelname)s - %(message)s')
        
        script_file_handler.setFormatter(script_file_formatter)
        script_logger.addHandler(script_file_handler)
        
    if moopy_logfile is not None:
        # Same as above.
        moopy_file_handler = logging.FileHandler(moopy_logfile)
        moopy_file_formatter = logging.Formatter(
            'Moopy Log: [%(asctime)s] %(levelname)s - %(message)s')
        
        moopy_file_handler.setFormatter(moopy_file_formatter)
        moopy_logger.addHandler(moopy_file_handler)
    
    moopy_logger.debug('Session initialization complete.')
        

class SessionInfo(object):
    '''This class stores information about the "modo session". On initialization
    (usually done via L{initialize}), it inspects modo for collection of
    information.
    '''

    def __init__(self):
        '''
        '''
        
        # First we parse the arguments with shlex.
        raw_arguments = shlex.split(lx.arg())
        
        # Now take the parsed args, and loop through each item and split them
        # into two lists. self.arguments and self.keyword_arguments.
        # We also convert every arg, key, and value into the proper python
        # object.
        arguments = []
        keyword_arguments = {}
        def convert_string(string_to_convert):
            '''We use this function to quickly convert a string into an int,
            float, or bool. If it is found to not be a bool, int, or float,
            the string is returned unedited.
            '''
            try:
                if '.' in string_to_convert:
                    return float(string_to_convert)
                else:
                    return int(string_to_convert)
            except ValueError:
                if string_to_convert.lower() == 'true':
                    return True
                if string_to_convert.lower() == 'false':
                    return False
                else:
                    return string_to_convert
                
        for raw_argument in raw_arguments:
            if '=' in raw_argument:
                # If there is a = character, its a kw_arg
                
                split_raw_argument = raw_argument.split('=', 1)
                
                # Both the key and the value, we use
                # convert_string() to make sure the objects are their intended
                # type.
                key = convert_string(split_raw_argument[0])
                value = convert_string(split_raw_argument[1])
                
                if keyword_arguments.has_key(key):
                    # If the key is already defined, raise an exception
                    # instead of simply overriding it.
                    raise errors.InvalidArgumentSupplied(
                        'The key "%s" was used twice with the following '
                        'values:\n  #1: "%s"\n  #2: "%s"' % (
                            key, keyword_arguments[key], value))
                
                # Now we add this keyword arg to the keyword_arguments object.
                keyword_arguments[key] = value
            else:
                arguments.append(convert_string(raw_argument))
        
        if not arguments:
            # For clean python, if arguments is empty make it None
            
            arguments = None
        if not keyword_arguments:
            # Same as above.
            
            keyword_arguments = None
        
        self.arguments = arguments
        self.keyword_arguments = keyword_arguments

class ModoPrinter(object):
    '''The purpose of this class is to be given to sys.stdout so that standard
    prints will be given to modo's event logger.
    '''
    
    def write(self, content_to_write):
        '''
        '''
        if content_to_write and content_to_write != '\n':
            if (content_to_write.startswith('Moopy Log') or
                content_to_write.startswith('Moopy Script Log')):
                lx.out(content_to_write)
            else:
                lx.out('Moopy Print: %s' % content_to_write)
