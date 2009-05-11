#python
''''''

# Standard
import os
import sys
# Here we are appending the local path of modo wrapper. This is not needed
# normally because you'll have modo_wrapper in your scripts dir.
sys.path.append(os.path.abspath('..'))
# Related
# Local
import modo_wrapper.modo

# Here we call a function which grabs information from modo to see if it is
# compatible with this specific version of modo_wrapper.
# modo_wrapper will raise a number of exceptions for any problems found,
# such as not being able to import lx.
modo_wrapper.modo.check_modo()