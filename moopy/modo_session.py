''''''

# Standard
import inspect
import logging
import shlex
import sys
# Related
import lx
# Local
import errors

#: An instance of L{SessionInfo} created by L{initialize}
session_info = None

def convert_string_to_object(string_to_convert):
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

def initialize(moopy_loglvl=logging.WARNING, moopy_logfile=None,
               loglvl=logging.WARNING, logfile=None, stdout_modo=True,
               trace_this=None):
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

    #if session_info.keyword_arguments is not None:
        ## Now we set the moopy log level. If the user defined one, use his.
        #if session_info.keyword_arguments.has_key('moopy_loglvl'):
            #moopy_loglvl = log_levels[
                #session_info.keyword_arguments['moopy_loglvl'].lower()]
        ## If the user defined a file to log to, grab that value.
        #if session_info.keyword_arguments.has_key('moopy_logfile'):
            #moopy_logfile = session_info.keyword_arguments['moopy_logfile']

        ## The same as above, except for the root logger, aka, the script logger.
        #if session_info.keyword_arguments.has_key('loglvl'):
            #loglvl = log_levels[
                #session_info.keyword_arguments['loglvl'].lower()]
        #if session_info.keyword_arguments.has_key('logfile'):
            #logfile = session_info.keyword_arguments['logfile']

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

def parse_script_arguments(script_arguments):
    '''This function will take a string like object and parse the contents
    into a list and a dictionary, and return them inside of a tuple.

    The list is comprised of all arguments which do not contain an equal sign,
    and are then assumed to be I{positional} arguments. The dictionary returns
    all arguments which contain an equals sign and is then populated by those
    arguments in a key=value pair form.

    @param script_arguments: A string containing "script arguments". Some
    examples below.

    ScriptArgument:
        5 7 toggle=false
    Returns:
        ([5, 7], {'toggle':False})

    ScriptArgument:
        .7 color=orange something else
    Returns:
        ([0.7, 'something', 'else'], {'color':'orange'})
    '''

    if script_arguments is None:
        return ([], {},)

    # First we parse the arguments with shlex.
    split_arguments = shlex.split(script_arguments)

    # Now take the parsed args, and loop through each item and split them
    # into two lists. self.arguments and self.keyword_arguments.
    # We also convert every arg, key, and value into the proper python
    # object.
    positional_arguments = []
    keyword_arguments = {}

    # Store the convert function locally for speed.
    convert_string = convert_string_to_object

    for split_argument in split_arguments:
        if '=' in split_argument:
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

    return (positional_arguments, keyword_arguments)

def trace_wrapper(trace_this):
    ''''''

    def get_trace_code(frame, context=1):
        '''This little bit comes from inspect.getframeinfo()'''
        if context > 0:
            start = lineno - 1 - context//2
            try:
                lines, lnum = inspect.findsource(frame)
            except IOError:
                lines = index = None
            else:
                start = max(start, 1)
                start = max(0, min(start, len(lines) - context))
                lines = lines[start:start+context]
                index = lineno - 1 - start
        else:
            lines = index = None

    try:
        trace_this()
    except:
        # Grab the current frame.
        frame_cursor = inspect.currentframe().f_back

        # Store all of the frames gathered.
        all_frame_info = []

        #inspect.getouterframes(frame_cursor)

        while True:
            # Continue looping through the frame cursor as it travels back
            # the stack.

            # Grab all relevant information from the current frame.
            frame_cursor_info = inspect.getframeinfo(frame_cursor)
            #frame_cursor_info['filename'] = frame_cursor.f_code.co_filename
            #frame_cursor_info['lineno'] = frame_cursor.f_lineno
            #frame_cursor_info['function'] = frame_cursor.f_code.co_name
            #frame_cursor_info['exception_type'] = frame_cursor.f_exc_type
            #frame_cursor_info['trace_function'] = frame_cursor.f_trace
            # Append information from each frame the cursor is on
            all_frame_info.append(frame_cursor_info)

            # Travel back on the stack.
            temp_frame_cursor = frame_cursor.f_back
            if temp_frame_cursor is None:
                break
            else:
                frame_cursor = temp_frame_cursor

        # Reverse the frame order.
        all_frame_info.reverse()

        for frame_info in all_frame_info:
            lx.out(frame_info)

        lx.out(sys.exc_type)
        lx.out(sys.exc_value)
        #lx.out('Boo: %s' % str(inspect.getframeinfo(frame_cursor)))

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
        '''The initilization process creates some default value initilization
        along with parsing the script arguments.

        @param argument_string: A possible override to the script arguments
        given to the script from modo. If given, no call to lx.arg() ever takes
        place and this is solely used as this script's arguments.
        @type argument_string: A string like object.
        '''

        # The arguments given to the script, where the keys are the
        # keywords and indexes of each option.
        self.arguments = {}
        # The options held in ScriptOptions instances, where each element is
        # a dict with keywords pertaining to data on that
        # option (choices, etc)
        self.options = []
        # A set of all the keywords provided to this ScriptOptions instance.
        self.all_option_keywords = set()
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

        # The raw arguments are those that have only been created but not
        # validated
        self.raw_positional_arguments, self.raw_keyword_arguments = parse_script_arguments(
            self.argument_string)

    def __getitem__(self, key):
        ''''''
        try: 
            return self.arguments[key]
        except KeyError:
            raise KeyError()

    def add_option(self, default=None, required=False, allowed_types=None,
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

        # If there is an intersection of all_option_keywords and the newly
        # supplied keywords, raise an exception.
        if self.all_option_keywords.intersection(keywords):
            raise errors.DuplicateArgumentSupplied(
                'Argument: %s' % self.all_option_keywords.intersection(keywords)
            )

        # Calculate this arguments positional index (if any)
        # This is done by iterating backwards over the list of arguments until
        # one is found to have an argument index. That index plus one is used
        # for this arguments index.
        if positional:
            # Store the index of this positional argument
            option_positional_index = self.total_positional_options

            # Increase the count of positional arguments.
            self.total_positional_options += 1
        else:
            # This option is not storing a positional argument.
            option_positional_index = None

        option_makeup = {
            'positional_index':option_positional_index,
            'default':default,
            'allowed_types':allowed_types,
            'positional':positional,
            'keywords':keywords,
            'required':required,
            'choices':choices,
        }

        logging.getLogger('moopy').debug('Appending a script argument with the '
                                         'values "%s"' % option_makeup)

        # Append the script keywords to the keywords list, so we can
        # check it against what the user supplied later on.
        self.all_option_keywords.update(keywords)

        # Add the argument dict to the self.arguments list.
        self.options.append(option_makeup)

        # Update the total arguments count.
        self.total_unique_options += 1

    def validate_options(self):
        '''Loop through all of the options call L{self.validate_option} on
        each one.
        '''

        map(self.validate_option, self.options)

    def validate_option(self, option):
        '''Check a single option to make sure it is valid against the
        script arguments in this instance. This means that there are no
        duplicate keywords, and possibly a positional, for this option,
        along with all other requirements the option posseses such as the
        object type, whether its required or not, etc.

        @note: This function could use a bit of recoding to make it cleaner and
        faster.
        '''
        
        # Store some argument parameters locally, to reduce dict lookups.
        option_keywords = option['keywords']
        option_allowed_types = option['allowed_types']
        options_argument_value = None

        raw_positional_arguments = self.raw_positional_arguments
        raw_keyword_arguments = self.raw_keyword_arguments

        # The following two objects represent the value of this option.
        # If the arg-value is supplied as a position argument, it is put
        # into pos_specific, and same goes for kw_specific.
        pos_specific_arg_value = None
        kw_specific_arg_value = None
        
        # Check the value of this options positional, if any.
        if option['positional']:
            # If this option is set to use a positional

            if (raw_positional_arguments is not None and 
                option['positional_index'] < len(raw_positional_arguments)):
                # If the index of this option is smaller than the total
                # arguments we know that this option's value is in
                # the positional arguments.

                pos_specific_arg_value = raw_positional_arguments[
                    option['positional_index']]

        # Check the value of this options keywords, if any.
        if option_keywords is not None:
            # The option has one or more keywords assigned to it.

            if raw_keyword_arguments is not None:
                # There is keyword arguments

                for option_keyword in option_keywords:
                    if raw_keyword_arguments.has_key(option_keyword):
                        # The raw kw-args contain this option_keyword.

                        if kw_specific_arg_value is not None:
                            # If the argument_value has already been assigned,
                            # we raise a failure signalling that the user used
                            # duplicate keywords.
                            raise errors.DuplicateArgumentSupplied(
                                'The argument which contains (but not limited '
                                'to) the key "%s" was used atleast twice with '
                                'the following values:\n  #1: "%s"\n  #2: '
                                '"%s"' % (
                                    keyword, kw_specific_arg_value,
                                    raw_keyword_arguments[
                                        option_keyword]))

                        kw_specific_arg_value = raw_keyword_arguments[
                            option_keyword]

                if (kw_specific_arg_value is not None
                    and pos_specific_arg_value is not None):
                    # If there is a kw_arg value found, and the positional
                    # argument value is found, then the user supplied both.

                    raise errors.DuplicateArgumentSupplied(
                        'The following two values both belong to the same '
                        'option.\n  #1: "%s"\n  #2: "%s"' % (
                            kw_specific_arg_value, pos_specific_arg_value)
                    )
        else:
            # The option has no keywords assigned to it.
            if not option['positional']:
                # If the option can not be positional but has no keywords given,
                # raise an error. To explain.. if it can't be positional.. and
                # it doesn't have any keywords.. how can it be assigned a value?
                # Note that this is strictly a scripting error
                # by the programmer/scripter.
                raise Exception(
                    'Scripter made a booboo.'
                )

        if pos_specific_arg_value is not None:
            options_argument_value = pos_specific_arg_value

        if kw_specific_arg_value is not None:
            options_argument_value = kw_specific_arg_value

        def ordinal_suffix(integer):
            '''
            # This is just a little tool function for the following exception
            # messages.. i should probably put this somewhere useful..
            '''

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

        if options_argument_value is None and option['default'] is not None:
            options_argument_value = option['default']
        
        if options_argument_value is None and option['required']:
            # If the argument was not given by the user, but it is required,
            # fail it in one of the following scenarios.

            if option_keywords is not None and option['positional']:
                # The option can be used as positional or by keyword
                raise errors.RequiredArgumentMissing(
                    'An argument was not supplied with a value it required. '
                    'This can be the %s%s positional argument, or the '
                    'following keyword-arguments: %s' % (
                        option['positional_index']+1,
                        ordinal_suffix(option['positional_index']+1),
                        option_keywords,)
                )
            elif option_keywords is not None and not option['positional']:
                # The option can only be used by keyword
                raise errors.RequiredArgumentMissing(
                    'An argument was not supplied with a value it required. '
                    'The argument must be one of the following keyword-'
                    'arguments: %s' % keywords
                )
            else:
                # The option can only be used by position
                raise errors.RequiredArgumentMissing(
                    'An argument was not supplied with a value it required. '
                    'The argument must be the %s%s positional '
                    'argument.' % (option['positional_index']+1,
                                   ordinal_suffix(
                                       option['positional_index']+1))
                )

        if options_argument_value is not None:
            # If there is a value, check one of the following scenarios for
            # problems.

            if (option['choices'] is not None and
                options_argument_value not in option['choices']):
                # If there are choices and the value doesn't match any choices

                if option_keywords is not None and option['positional']:
                    # The option can be used as positional or by keyword
                    raise errors.ArgumentIsNotAChoice(
                        'The argument which can be used as the following '
                        'keywords "%s", or as the %s%s positional argument '
                        ' has a value that is not in the list of accepted. '
                        'choices. Choices: %s' % (
                            option_keywords, 
                            option['positional_index']+1,
                            ordinal_suffix(option['positional_index']+1),
                            option['choices'])
                    )

                elif option_keywords is not None and not option['positional']:
                    # The option is not positional, and must be given keywords
                    raise errors.ArgumentIsNotAChoice(
                        'The argument which has the keywords "%s" has a '
                        'value that is not in the list of accepted choices. '
                        'Choices: %s' % (
                            option_keywords, option['choices'])
                    )
                else:
                    # The option is only positional
                    raise errors.ArgumentIsNotAChoice(
                        'The %s%s argument\'s value is not in '
                        'the list of accepted choices. Choices: %s' % (
                            option['positional_index']+1,
                            ordinal_suffix(option['positional_index']+1),
                            option['choices'])
                    )

            if (option['allowed_types'] is not None and 
                type(options_argument_value) not in option['allowed_types']):
                # Now we check if the argument type is within the boundries of
                # the allowed types. If any.

                raise errors.InvalidArgumentType(
                    'The argument "%s" is not an allowed type for this '
                    'option.' % (
                        option['allowed_types'])
                )

        if option['positional']:

            # Now that we're all done, and a value has been supplied, store
            # that value in this class, so it can be accessed directly from
            # this class instance (if desired).
            self.arguments[option['positional_index']] = options_argument_value

        if option_keywords is not None:

            # Now that we're all done, and a value has been supplied, store
            # that value in this class, so it can be accessed directly from
            # this class (if desired). Note that we could be assigning this a
            # second time, but this is seen as a feature. The scripter
            # has the freedom to access the user value in potentially two ways,
            # by index of the positional, or by this option's first keyword
            # he provided to the user.
            # Note that we "could" store all the keywords, but that would
            # be slow..er, and not all that useful.
            self.arguments[option_keywords[0]] = options_argument_value

class SessionInfo(object):
    '''This class stores information about the "modo session". On initialization
    (usually done via L{initialize}), it inspects modo for collection of
    information.
    '''

    def __init__(self):
        '''
        '''

        pass
