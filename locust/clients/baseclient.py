

class BaseClient(object):
  '''BaseClient is currently a place holder to put
     common logic for all clients. Currently it does
     nothing
  '''
  pass


class BaseContextManager(object):
    '''For now same as BaseClient
    '''
    exception_class = None

    def __init__(self,exception_class):
        self._is_reported = False

    def __enter__(self):
        return self

    def __exit__(self, exc, value, traceback):
        if self._is_reported:
            # if the user has already manually marked this response as failure or success
            # we can ignore the default haviour of letting the response code determine the outcome
            return exc is None
        
        if exc:
            if isinstance(value, self.exception_class):
                self.failure(value)
            else:
                return False
        else:
            self.success()
            return True

    def success(self):
        ''' custom success reporting code here.
        '''
        pass

    def failure(self,exc):
        ''' custom failure reporting code here.
        '''
        pass

