
class LogicError(Exception):
    
    def __str__(self):
        return self.message

class UnexpectedEndError(Exception):
    
    message = 'Unexpected end of statement'
    
    def __str__(self):
        return "Unexpected end of statement"


class UnexpectedTokenError(Exception):

    def __init__(self, token):
        self.token = token

    def __str__(self):
        return self.message


class ImmutableError(Exception):
    
    message = 'Cannot assign to immutable variable'

    def __init__(self, token):
        self.token = token
        
    def __str__(self):
        return self.message
