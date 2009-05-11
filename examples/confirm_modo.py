#python
''''''

# Standard
import os
import sys
# Here we are appending the local path of modopywrap. This is not needed
# normally because you'll have modo_wrapper in your scripts dir.
sys.path.append(os.path.abspath('..'))
# Related
# Local
import modopywrap.modo

# Here we call a function which grabs information from modo to see if it is
# compatible with this specific version of modopywrap.
# modopywrap will raise a number of exceptions for any problems found,
# such as not being able to import lx.
modopywrap.modo.check_modo()