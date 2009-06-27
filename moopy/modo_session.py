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

class ScriptOptions(object):
    '''The ScriptOptions class allows modo scripts to require positional
    arguments, keyword arguments, and even set the required type for them.'''
    
    def __init__(self, argument_string=None):
        ''''''
        
        # The arguments this ScriptOptions instance contains.
        # Remember that these can be supplied to the class directly, or by modo
        self.parsed_arguments = {}
        # The options held in ScriptArguments instance, stored in dict form.
        self.options = None
        # A set of all the keywords provided to this ScriptOptions instance.
        self.all_option_keywords = None
        # The total positional arguments held within this class.
        self.total_positional_options = 0
        # The total unique arguments this script contains.
        # An example of unique is "f" and "file", 2 arguments, but one unique
        # since they both result in the same value.
        self.total_unique_options = 0
        
        if argument_string is not None:
            # If the class was given a manual argument string.
            
            self.argument_string = argument_string
        else:
            # Since the argument_string is not supplied, ask modo for the real
            # string.
            
            self.argument_string = lx.arg()
        
        if not self.argument_string:
            # If the argument string is empty, replace the value with None
                
            self.argument_string = None
    
    def __getitem__(self, key):
        ''''''
        
        return self.arguments[key]
    
    def add_argument(self, default=None, required=False, allowed_types=None,
                     positional=True, keywords=None, choices=None):
        '''Add an argument to this ScriptArguments instance.
        
        @param default: The default value this argument will use.
        
        @param required: If True this function will raise an exception if not
        provided with a value in one of the supplied methods.
        
        @param allowed_types: A list of object types. If provided, the argument
        given must match atleast ONE of the types provided.
        
        @param positional: If true, this argument can accept a positional
        argument as its value. If false, only keyword arguments (matching
        one of the supplied keywords) are accepted.
        
        @param keywords: A list of strings that this argument can use.
        
        @options: If given, the value of this argument must exactly match one
        of the given options.
        
        @raise errors.DuplicateArgumentSupplied: Raised if a duplicate argument
        is given to {self.add_arguments}.
        '''
        
        # If there is an intersection of all_keywords and the newly supplied
        # keywords, raise an exception.
        if self.all_keywords.intersection(keywords):
            raise errors.DuplicateArgumentSupplied(
                'Argument: %s' % self.all_keywords.intersection(keywords)
            )
        
        # Calculate this arguments positional index (if any)
        # This is done by iterating backwards over the list of arguments until
        # one is found to have an argument index. That index plus one is used
        # for this arguments index.
        if positional:
            # Store the index of this positional argument
            argument_index = self.positional_count
            
            # Increase the count of positional arguments.
            self.positional_count += 1
        else:
            # This option is not storing a positional argument.
            argument_index = None
        
        argument_makeup = {
            'index':argument_index,
            'default':default,
            'allowed_types':allowed_types,
            'positional':positional,
            'keywords':keywords,
            'required':required,
            'options':options,
        }
        
        logging.getLogger('moopy').debug('Appending a script argument with the '
                                         'values "%s"' % argument_makeup)
        
        # Append the script keywords to the keywords list, so we can
        # check it against what the user supplied later on.
        self.all_keywords.update(keywords)
        
        # Add the argument dict to the self.arguments list.
        self.arguments.append(argument_makeup)
        
        # Update the total arguments count.
        self.total_unique_arguments += 1
    
    def convert_string(string_to_convert):
        '''This is a utility function used to convert string arguments into
        the Python object equivalent.
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
    
    def parse(self):
        '''
        '''
        
        if self.argument_string is None:
            # If there is no argument string, there's nothing to parse.
            
            return (None, None,)
        
        # First we parse the arguments with shlex.
        split_arguments = shlex.split(self.argument_string)
        
        # Now take the parsed args, and loop through each item and split them
        # into two lists. self.arguments and self.keyword_arguments.
        # We also convert every arg, key, and value into the proper python
        # object.
        positional_arguments = []
        keyword_arguments = {}
        
        # Store the convert function locally for speed.
        convert_string = self.convert_string
        
        for split_argument in split_arguments:
            if '=' in raw_argument:
                # If there is a = character, its a kw_arg
                
                split_kw_argument = split_argument.split('=', 1)
                
                # Both the key and the value, we use
                # convert_argument_value() to make sure the objects are
                # their intended type.
                key = convert_string(split_kw_argument[0])
                value = convert_string(split_kw_argument[1])
                
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
                # If there is no = character, its a positional argument.
                
                positional_arguments.append(convert_string(split_argument))
        
        if not positional_arguments:
            # For clean python, if arguments is empty make it None
            
            positional_arguments = None
        if not keyword_arguments:
            # Same as above.
            
            keyword_arguments = None
        
        self.positional_arguments = arguments
        self.keyword_arguments = keyword_arguments
        
        map(self.parse_argument, self.arguments)
    
    def parse_argument(self, argument):
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
        
        pass
