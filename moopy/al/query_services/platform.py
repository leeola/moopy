'''
'''

# Standard
# Related
import lx
# Local


#: Just for the sake of reducing repeated code, we define a global service
#: object here.
_service_object = lx.Service('platformservice')

select = _service_object.select

def list_roots():
    '''Return a tuple of all the roots found in platformservice.'''
    return _service_object.query()

def get_appbuild():
    ''''''
    return int(_service_object.query('appbuild'))

def get_appname():
    ''''''
    return _service_object.query('appname')

def get_appversion():
    ''''''
    return int(_service_object.query('appversion'))

def get_expiresin():
    '''
    @note: This needs to be tested by someone with the trial, to see if
    it can always be converted to an int.
    '''
    return _service_object.query('expiresin')

def get_iseval():
    ''''''
    if _service_object.query('iseval') == '1':
        return True
    return False

def get_importpaths():
    ''''''
    return _service_object.query('importpaths')

def get_isheadless():
    ''''''
    if _service_object.query('isheadless') == '1':
        return True
    return False

def get_licensedto():
    ''''''
    return _service_object.query('licensedto')

def get_numlicenses():
    ''''''
    return int(_service_object.query('numlicenses'))

def get_osname():
    ''''''
    return _service_object.query('osname')

def get_ostype():
    ''''''
    return _service_object.query('ostype')

def get_osversion():
    ''''''
    return _service_object.query('osversion')

def get_paths():
    ''''''
    return _service_object.query('paths')

def get_serialnumber():
    ''''''
    return int(_service_object.query('serialnumber'))

