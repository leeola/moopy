#python
'''This example shows the base usage of modopywrap, in the good ol hello world
format.'''

# Now we import the modo_connection module so that we can call the connection
# initializer.
import modopywrap.modo_connection

# Now we initialize the modo connection. This allows modopywrap to setup
# anything it needs, and pull any information from modo that it may need.
# This should always be done in the beginning of a script, after imports.
modopywrap.modo_connection.initialize()

# Now we print. The basic print is routed into modo's event logger. This is done
# at the initialization stage above.
print 'Hello World!'
