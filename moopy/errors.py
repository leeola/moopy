''''''

# Standard
# Related
# Local


class MoopyError(Exception):
    '''The base Moopy error.
    '''
    pass

class ChannelsError(MoopyError):
    '''The base channels error.
    '''
    pass

class ImproperMatchType(ChannelsError):
    '''
    '''
    
    def __init__(self, channel1, channel2, message=None):
        '''
        '''
        
        self.channel1 = channel1
        self.channel2 = channel2
        self.message = message
    
    def __str__(self):
        '''
        '''
        if self.message is not None:
            return '\n%s\nChannel #1: %s\nChannel #2: %s' % self.message

class ItemError(MoopyError):
    '''The base item error.
    '''
    pass

class ItemIDNonExistantError(ItemError):
    '''An item id does not exist.
    '''
    pass

class ItemIDNotClassTypeError(ItemError):
    '''An item id given to a specific Class constructor does not exist.
    '''
    pass

class ScriptOptionsError(MoopyError):
    '''The base script options error.'''

    def __init__(self, message):
        '''
        '''
        
        self.message = message
    
    def __str__(self):
        '''
        '''
        return '\n%s' % self.message

class ArgumentIsNotAChoice(ScriptOptionsError):
    '''An argument supplied was found within the list of accepted arguments.
    '''
    pass

class DuplicateArgumentSupplied(ScriptOptionsError):
    '''A keyword argument was given twice. This is thrown to prevent unintended
    behavior.
    '''
    pass

class InvalidArgumentFormatting(ScriptOptionsError):
    '''The arguments from modo given to a user script are formatted incorrectly.
    '''
    pass

class InvalidArgumentType(ScriptOptionsError):
    '''An argument supplied is not an accepted type for that argument.
    '''
    pass

class RequiredArgumentMissing(ScriptOptionsError):
    '''A required argument was not supplied in any form by the user.
    '''
    pass

