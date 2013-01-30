'''
utility functions to be of general use.
'''

class Decorators(object):
		@staticmethod
		def decorator(fn):
			'''takes a standalone function and makes it a decorator.
				 used to keep you code looking cleaner. decorators can 
				 be kinda ugly to look at.
				 :param fn: function to turn into a decorator. function must\
				 accept the target of decoration as its first argument.
				 Usage pattern is as follows:

				 from utils import Decorators
				 
				 @Decorators.decorator
				 def my_logging_decorator(decoratored,*args,**kwargs):
				   log.info("calling %s" % decorated)
				   return decorated(*args,**kwargs)

				 @my_logging_decorator
				 def do_work(worker):
				   return worker.work()
			'''
			def decorator_wrapper(decorated_function):
				def stand_in_decorator(*args,**kwargs):
					'''This is the function that will actually be the 
					   decorator we see if we were to inspect the target.
					   From our example:
					   print do_work 
					   <function stand_in_decorator at 0x023AB8B0>
					'''
					return fn(decorated_function,*args,**kwargs)
				return stand_in_decorator
			return decorator_wrapper


		@staticmethod
		def instance_decorator(fn):
			'''syntax sugar. it clearly marks the
			   decorator as only useful on a instance method
			   as it will require a reference to "self"
			'''
			return Decorators.decorator(fn)

		@staticmethod
		def options_decorator(fn):
			'''this decorator will allow your function to
			   be called with or without keyword arguments:
			   NOTE: positional arguments are not supported.
			   @optional_args_decorator
			   def mydec(decorated,options,*args,**kwargs):
			     decorator_keyword_arg = options.get('myKeyword',"kw_default")
			     #do conditional stuff
			     return decorated(*args,**kwargs)

			   @mydec
			   def foo():

			   and 

			   @mydec(some_kw_args=1234)
			   def foo():

			   will work without the ugyly setup code. you
			   must still check if your arguments are None type.
			'''
			def decorator_wrapper(*decorated_function,**decorator_kwargs):
				if decorator_kwargs:
					def accepts_callable(decorated_function):
						def stand_in_decorator(*args,**kwargs):
							return fn(decorated_function,decorator_kwargs,*args,**kwargs)
						return stand_in_decorator
					return accepts_callable
				else:
					def stand_in_decorator(*args,**kwargs):
						return fn(decorated_function[0],decorator_kwargs,*args,**kwargs)
					return stand_in_decorator
			return decorator_wrapper
