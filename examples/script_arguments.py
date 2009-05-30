#python
'''This example shows usage of the L{MoopyArguments 
<moopy.modo_session.ScriptArguments>} module.

What does it do? This is an extension of a hello world example, It will
simple reply (for example) "Hello, Mr. Smith." if given the name Smith and
told that the person is a male. If not told what sex, it will reply with
"Hello, Smith."'''


import moopy.modo_session
# Initialize the modo session.
moopy.modo_session.initialize()

# Create a ScriptArguments instance
script_arguments = moopy.modo_session.ScriptArguments()

# Add an argument for the name. This can be the first non-keyword argument,
# the keyword argument "name", or the shorthand of that "n".
script_arguments.add(required=True, keywords=['name', 'n'],
                     allowed_types=[str])

# Add another argument, this one can be the second non-keyword argument,
# or the keywords "sex" or "s". Note that each argument that is not flagged
# as keyword_only is expected to be used in order, if at all. Remember though,
# keywords can be used in any order.
script_arguments.add(keywords=['sex', 's'],
                     options=['male', 'female'])

# Finally, we add another argument that is only triggered by the keywords
# "verbose" and "v".
script_arguments.add(keyword_only=True, keywords=['verbose', 'v'],
                     default=False, allowed_types=[bool, int])

# Now that we have setup what arguments we want this script to get, we tell
# the ScriptArguments instance to check if the user supplied whatever is
# required/expected.
# Note that if anything is not valid, an exception will be thrown to the user
# explaining what is wrong.
script_arguments.validate()

# If the user supplies male or female this is overwritten with that. If not, it
# is still used, but empty.
sex_prefix = ''
if script_arguments[1] == 'male':
    sex_prefix = 'Mr. '
elif script_arguments[1] == 'female':
    sex_prefix = 'Ms. '

# Since the arg setup above is fairly redundant with the wide array of options,
# eg, the user has 3 options for providing his/her name,
# ScriptArguments allows you to access the user supplied values in the order
# added as arguments to ScriptArguments.
# For example, if the user runs "@/path/required_arguments.py name=John", how
# do you know that the user did that? He could have done 
# "@/path/required_arguments.py n=John" or "@/path/required_arguments.py John".
# Without ScriptArguments you would have to check session_info.arguments and
# session_info.keyword_arguments. With ScriptArguments all you have to do
# is access the first argument given to the ScriptArguments instance.
# For example:
print 'Hello, %s%s' % (sex_prefix, script_arguments[0],)

# Here we have our little verbose call. Notice that we again are accessing the
# 3rd argument given to script_arguments, despite the 'verbose' argument being
# a keyword only argument.
if script_arguments[2]:
    print (
        'So, you want me to be verbose? The question is, how verbose? I could '
        'ramble on for days but i assume you\'d get annoyed with that.. So what'
        ' do you really want? I mean.. seriously, what can i do to make you '
        'happy? Why on earth does it take so much these days to satisfy people.'
        '\nIn my generation, we used to appreciate everything in life. You '
        'never heard kids say "We\'re bored!". We went out and did things!'
        'No "Nintendo" or "Texting" for us. .. and on that same note, what the '
        'heck is twitter! Ugh.. i feel old.\n\nVerbose enough? :)'
    )
