#python
''''''

# Standard
# Related
# Local
import modopywrap # Importing the main lib will check if it can find modo.
import modopywrap.modo

modopywrap.modo.initialize_modo_connection()

print 'Yup, its working!'