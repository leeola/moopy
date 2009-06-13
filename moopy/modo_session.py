''''''

# Standard
import copy
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

class ScriptArguments(object):
    '''The ScriptArguments class allows modo scripts to require arguments,
    keyword arguments, and even set the required type for them.'''
    
    def __init__(self):
        ''''''
        
        self.arguments = []
        self.values = []
    
    def __getitem__(self, index):
        ''''''
        
        return self.values[index]
    
    def add(self, default=None, required=False, allowed_types=None,
            keyword_only=False, keywords=None, options=None):
        ''''''
        
        # Calculate this arguments non-keyword index (if any)
        # This is done by iterating backwards over the list of arguments until
        # one is found to have an argument index. That index plus one is used
        # for this arguments index.
        if not keyword_only:
            
            # This is just a hack. When 401 hits, this can be removed in favor
            # of the builtin reversed()
            rev_arguments = copy.copy(self.arguments)
            rev_arguments.reverse()
            logging.getLogger('moopy').warning(
                'Moopy is using a function from python 2.3. Remove '
                'list.reverse() in favor of reversed()')
        
            for argument in rev_arguments:
                if argument['index'] is not None:
                    argument_index = argument['index'] + 1
                    break
            else:
                # If we get here, then the loop ran through without finding
                # Any other arguments with indexes. This means that this is
                # the first non-keyword argument, so assign it an index of 0.
                argument_index = 0
        else:
            argument_index = None
        
        argument_makeup = {
            'index':argument_index,
            'default':default,
            'allowed_types':allowed_types,
            'keyword_only':keyword_only,
            'keywords':keywords,
            'required':required,
            'options':options,
        }
        
        logging.getLogger('moopy').debug('Appending a script argument with the '
                                         'values "%s"' % argument_makeup)
        
        # Append the script keywords to the valid keywords list, so we can
        # check it against what the user supplied later on.
        self.valid_keywords += keywords
        # Same as above, except for non-kw arguments.
        if not keyword_only:
            self.total_sarguments += 1
        
        self.arguments.append(argument_makeup)
    
    def validate(self):
        ''''''
        if len(session_info.arguments) > self.total_arguments:
            # Calculate the total extra arguments
            total_extra_arguments =  (
                len(session_info.arguments) - self.total_arguments)
            
            raise errors.TooManyArguments(
                'There are too many non-keyword arguments given. Offending '
                'arguments: %s' % session_info.arguments[total_extra_arguments:]
            )
        
        map(self.validate_argument, self.arguments)
    
    def validate_argument(self, argument):
        ''''''
        
        # Store some argument parameters locally, to reduce dict lookups.
        keywords = argument['keywords']
        allowed_types = argument['allowed_types']
        argument_value = None
        
        # First we attempt to find this arguments value.
        if keywords is not None:
            # The scripter has provided kw-arguments for the user.
            if session_info.keyword_arguments is not None:
                # The user provided kwargs
                for keyword in keywords:
                    if session_info.keyword_arguments.has_key(keyword):
                        if argument_value is not None:
                            # If the argument_value has already been assigned,
                            # we raise a failure signalling that the user used
                            # duplicate keywords.
                            raise errors.DuplicateArgumentSupplied(
                                'The argument which contains (but not limited '
                                'to) the key "%s" was used atleast twice with '
                                'the following values:\n  #1: "%s"\n  #2: '
                                '"%s"' % (
                                    keyword, argument_value,
                                    session_info.keyword_arguments[keyword]))
                        argument_value = session_info.keyword_arguments[keyword]
        else:
            if argument['keyword_only']:
                # If the argument is keyword only, but has no keywords given,
                # raise an error. Note that this is strictly a scripting error
                # by the programmer/scripter.
                raise InvalidArgumentFormatting(
                    ''
                )
        
        if not argument['keyword_only']:
            if (session_info.arguments is not None and 
                argument['index'] < len(session_info.arguments)):
                # If the index of this function is smaller than the total
                # functions we know that this argument's value is in
                # the non-keyword arguments.
                if argument_value is not None:
                    # If the argument_value has already been assigned,
                    # we raise a failure signalling that the user used
                    # duplicate keywords.
                    raise errors.DuplicateArgumentSupplied(
                        'The key "%s" was used in conjunction with its'
                        'non-keyword argument, these contained the values' % (
                            keyword, argument_value,
                            session_info.keyword_arguments[keyword]))
                argument_value = session_info.arguments[argument['index']]
        
        def ordinal_suffix(integer):
            # This is just a little tool function for the following exception
            # messages.. i should probably put this somewhere useful..
            ''''''
            def return_th():
                return 'th'
            def return_st():
                return 'st'
            def return_nd():
                return 'nd'
            def return_rd():
                return 'rd'
            
            ordinal_dict = {
                11:return_th,
                12:return_th,
                13:return_th,
                1:return_st,
                2:return_nd,
                3:return_rd,
            }
            
            large_mod = integer % 100
            if ordinal_dict.has_key(large_mod):
                return ordinal_dict[large_mod]()
            
            small_mod = integer % 10
            if ordinal_dict.has_key(small_mod):
                return ordinal_dict[small_mod]()
            
            return 'th'
        
        if argument_value is None and argument['required']:
            # If the argument was not given by the user, but it is required,
            # fail it.
            if keywords is not None and not argument['keyword_only']:
                raise errors.RequiredArgumentMissing(
                    'An argument was not supplied with a value it required. '
                    'This can be the %s%s non-keyword argument, or the '
                    'following keyword-arguments: %s' % (
                        argument['index']+1,
                        ordinal_suffix(argument['index']+1), keywords,)
                )
            elif keywords is not None and argument['keyword_only']:
                raise errors.RequiredArgumentMissing(
                    'An argument was not supplied with a value it required. '
                    'The argument must be one of the following keyword-'
                    'arguments: %s' % keywords
                )
            elif keywords is None:
                raise errors.RequiredArgumentMissing(
                    'An argument was not supplied with a value it required. '
                    'The argument must be the %s non-keyword '
                    'argument.' % ordinal_suffix(argument['index'])
                )
        
        if argument_value is not None:
            if (argument['options'] is not None and
                argument_value not in argument['options']):
                if argument['keyword_only']:
                    raise errors.ArgumentIsNotAnOption(
                        'The argument which has the keywords "%s" has a '
                        'value that is not in the list of accepted options. '
                        'Options: %s' % (
                            keywords, argument['options'])
                    )
                else:
                    raise errors.ArgumentIsNotAnOption(
                        'The %s%s argument (or keyword-args: %s) is not in '
                        'the list of accepted options. Options: %s' % (
                            argument['index']+1,
                            ordinal_suffix(argument['index']+1),
                            argument['options'])
                    )
            
            if (argument['allowed_types'] is not None 
                and type(argument_value) not in argument['allowed_types']):
                
                if argument['keyword_only']:
                    raise errors.InvalidArgumentType(
                        'The argument which has the keywords "%s" was '
                        'expected to be of type(s) "%s"' % (
                            keywords,
                            argument['allowed_types'])
                    )
                else:
                    raise errors.InvalidArgumentType(
                        'The %s%s argument (or keyword-args: %s) was '
                        'expected to be of type(s) "%s"' % (
                            argument['index']+1,
                            ordinal_suffix(argument['index']+1), keywords,
                            argument['allowed_types'])
                    )
        
        # Now that we're all done, and a value has been supplied, store that
        # value in this class, so it can be accessed directly from this class
        # (if desired)
        self.values.append(argument_value)

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
                    raise errors.DuplicateArgumentSupplied(
                        'The key "%s" was used atleast twice with the '
                        'following values:\n  #1: "%s"\n  #2: "%s"' % (
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
