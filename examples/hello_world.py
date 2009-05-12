#python
'''This example shows the base usage of modopywrap, in the good ol hello world
format.'''

# Now we import the modo_session module so that we can call the session
# initializer.
import modopywrap.modo_session

# Now we initialize the modo session. This allows modopywrap to setup
# anything it needs, and pull any information from modo that it may need.
# This should always be done in the beginning of a script, after imports.
modopywrap.modo_session.initialize()

# Now we print. The basic print is routed into modo's event logger. This is done
# at the initialization stage above.
print 'Hello World!'

# Here we say hello in the logger! (With critical importance)
import logging
logging.critical('Hello World!')
