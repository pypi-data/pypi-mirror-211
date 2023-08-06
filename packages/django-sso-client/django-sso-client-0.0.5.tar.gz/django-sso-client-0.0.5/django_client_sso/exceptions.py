
class Exception401(Exception):
    def __init__(self,mensage):
        self.message = "Unauthorized user or invalidate token"
        
    def __str__(self):
        return self.mensage
    

class Exception403(Exception):
    def __init__(self):
        self.message = "Unauthorized access to this resource"
        
    def __str__(self):
        return self.mensage