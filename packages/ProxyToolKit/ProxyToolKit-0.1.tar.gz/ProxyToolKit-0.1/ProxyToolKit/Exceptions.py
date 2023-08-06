

class InavalidProxyData(Exception):
    def __init__(self):
        self.message = '\n\nInvalidProxyData: Invalid Proxy Data , This error must be due to invalid type of proxys list'

    def __str__(self):
        return self.message


class PathError(Exception):
    def __init__(self) :
        self.message = '\n\nPathError  Invalid Path'
    def __str__(self) -> str:
        return self.message
    

class NetworkError(Exception):
    def __init__(self) :
        self.message = '\n\nNetworkError:  NetWork Connection is too bad or No Connection'
    def __str__(self):
        return self.message
    

class ModuleError(Exception):
    def __init__(self):
        self.message = '\n\nModuleError: Module Not Found OR Error occured when Connecting with Moduels'
    def __str__(self) :
        return self.message
    
class RequirementsError(Exception):
    def __init__(self,) :
        self.message = '\n\n RequirementsError: System doesn\'t meet Requirements '
    def __str__(self):
        return self.message
    
    

