'''
utility functions to be of general use.
'''

def decorator(fn):
  '''this function will convert a vanilla python
     function into a decorator. This allows for
     much cleaner decorator definitions and 
     easy extension to support optional parameters
     without having to update all usage sites.
     the generated decorator will have the following
     properties:
      * it may used to decorate target functions
        with or with out optional arguments. See
        below for example.
      * the decorated callable is passed as the
        first argument to the vanilla function.
      * any optional parameters specified  in the
        decorator use are passed as a the second
        argument to the vanilla function. The type
        of this argument is dictionary.
      * any arguments to the decorated function are
        passed as the remaining arguments to the 
        vanilla function and can be captured with
        standard *args,**kwargs syntax.
      
      === USAGE ===
      
      from utils import decorator
      
      @decorator
      def log_call(target,options,*args,**kwargs):
        "I log all calls to decorated functions."
        level = options.get("level","INFO")
        fname = target.__name__
        log_function_call(fname,level,phase="entry",*args,**kwargs)
        ret = target(*args,**kwargs)
        log_function_call(fname,level,phase="exit")
        return ret

      @log_call(level="DEBUG")
      def latent_call(arg1,arg2):
        #do latent stuff

      @log_call
      def highly_latent_call(arg3,optional_arg=None)
        #do highly latent stuff

  '''
  '''=== Code Comments ===
     #1 This returns a function which may accept either a callable
        as is the standard case for decorators or a set of options
        which is the case for some decorators.

     #2 if kwargs was found we now know we are evaluating usage of 
        a decorator with options provided.
     #3 since we have now consumed the optional arguments we must 
        now return a function that can consume a callable. aka 
        the standard decorator pattern.
     #4 when inspecting the code this will be the function that is
        observed as the "bound method":
  Example from python shell:
  >>> myobj = MyObject() #where MyObject.bar has had decorator applied.
  >>> myobj.bar
  <bound method MyObject.stand_in_decorator of <__main__.MyObject object at 0x02566BF0>>
     #5 We see that no options were passed. Proceed with standard
        decorator pattern. See line item #4
     #6 Of note, decorated_function is a tuple due to the *decorated_function
        syntax used in decorator_wrapper definition. Pull off the 
        first element of this tuple and pass this as vanilla function
        as though it was a traditional decorator.
  '''
  def decorator_wrapper(*decorated_function,**decorator_kwargs): #1
    if decorator_kwargs: #2
      def accepts_callable(decorated_function): #3
        def stand_in_decorator(*args,**kwargs): #4
          return fn(decorated_function,decorator_kwargs,*args,**kwargs)
        return stand_in_decorator
      return accepts_callable
    else: #5
      def stand_in_decorator(*args,**kwargs): #4
        return fn(decorated_function[0],decorator_kwargs,*args,**kwargs) #6
      return stand_in_decorator
  return decorator_wrapper

