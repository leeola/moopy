#python
'''This example shows usage of the L{MoopyArguments 
<moopy.modo_session.ScriptOptions>} module.

What does it do? This is an extension of a hello world example, It will
simple reply (for example) "Hello, Mr. Smith." if given the name Smith and
told that the person is a male. If not told what sex, it will reply with
"Hello, Smith."

Below is a couple sample executions of the script from within modo:
 - @examples/script_arguments.py name=John sex=Male
 - @examples/script_arguments.py verbose=True n="John Doe"
 - @examples/script_arguments.py sex=Female "Jane Doe"
'''


import logging
import moopy.modo_session
moopy.modo_session.initialize(moopy_loglvl=logging.DEBUG)

# Create a ScriptArguments instance
script_arguments = moopy.modo_session.ScriptOptions()

# Add an argument for the name. This can be the first positional argument,
# the keyword argument "name", or the shorthand of that "n".
script_arguments.add_option(required=True, keywords=['name', 'n'],
                            allowed_types=[str])

# Add another argument, this one can be the second positional argument,
# or the keywords "sex" or "s". Note that each argument that is not given a 
# keyword and is flagged as positional is expected to be used in order, if at
# all. Remember though, keywords can be used in any order.
script_arguments.add_option(keywords=['sex', 's'],
                            choices=['male', 'female'])

# Finally, we add another argument that is _only_ triggered by the keywords
# "verbose" and "v". This is done by the positional=False declaration.
script_arguments.add_option(positional=False, keywords=['verbose', 'v'],
                            default=False, allowed_types=[bool, int])

# Now that we have setup what arguments we want this script to get, we tell
# the ScriptArguments instance to check if the user supplied whatever is
# required/expected.
# Note that if anything is not valid, an exception will be thrown to the user
# explaining what is wrong.
script_arguments.validate_options()
# If we get this far in the script, that means whatever the user gave this
# script for arguments is "valid", eg, nothing is the defies what rules you
# defined above, such as choices, or allowed_types.

# Now that we know whatever the user gave this script fits our rules, 
# we want to figure out what sex the user supplied. To do this we access
# the value of the argument.
# An argument can be accessed in one of two ways. By the positional index (if
# positional=True, which it is by default), or by the first keyword we
# gave as an option. Below we check for the male value by its positional index,
# and the female value by its keyword.
# Take note that these positional and keyword arguments do not in any way relate
# to what the user actually used to give you their sex (hehe). You don't really
# care how they give you their value right? This is strictly for your access
# to their value, so you don't have to try and figure out what they did.
sex_prefix = ''
if script_arguments[1] == 'male':
    sex_prefix = 'Mr. '
elif script_arguments['sex'] == 'female':
    sex_prefix = 'Ms. '
# Remember that it is only the first keyword we provide. If we had used the 
# second keyword we provide, "s", it would not be found. As an example, the
# following line would cause an error:
#elif script_arguments['s'] == 'female':


# After all that, we simply print the hello string. Lot of junk for a hello
# world, right?
print 'Hello, %s%s' % (sex_prefix, script_arguments['name'],)

# Here we have our little verbose call.
if script_arguments['verbose']:
    print (
        'So, you want me to be verbose? The question is, how verbose? I could '
        'ramble on for days but i assume you\'d get annoyed with that.. So what'
        ' do you really want?\nI mean.. seriously, what can i do to make you '
        'happy? Why on earth does it take so much these days to satisfy people.'
        '\nIn my generation, we used to appreciate everything in life. You '
        'never heard kids say "We\'re bored!". We went out and did things!'
        'No "Nintendo" or "Texting" for us. .. and on that same note, what the '
        'heck is twitter! Ugh.. i feel old.\n\nVerbose enough? :)'
    )
