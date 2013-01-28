import os,sys,time,traceback
from kazoo.client import KazooClient
from kazoo.protocol.states import KazooState
from kazoo.handlers.gevent import SequentialGeventHandler
from locust.exception import RescheduleTask
from locust.exception import ResponseError
from locust import events
from baseclient import BaseClient
from baseclient import BaseContextManager


#supporting decorators
def require_state(state):
  '''This decorator can be used to ensure the client is in
     the provided state before allowing the decorated function
     to run. If not the function will be rescheduled.
     This decorator assumes it is wrapping an object instance
     method with self._state of type kazoo.protocol.states.KazooState
  '''
  def rs_callable_capture(func):
    def require_state_decorator(self,*args,**kwargs):
      if self._state != state:
        err = "Zookeeper connection is not in correct state to execute function: "
        err += "%s. Requires %s Found %s. Rescheduling this task."
        err = err % (func,state,self._state)
        raise RescheduleTask(err)
      else: return func(self,*args,**kwargs)
    return require_state_decorator
  return rs_callable_capture

def record_stats(func):
  def record_stats_decorator(*args,**kwargs):
    request = {}
    request["method"] = func.__name__
    request["name"] = args[1] #TODO fix this, temporary hack for demo
    request["response_time"] = 0
    request["content_size"] = 0 #TODO find some valid way of measuring this.
    start = time.time()
    ret = func(*args,**kwargs)
    end = time.time()
    response_time["response_time"] = int(end - start) * 1000
    events.request_success.fire(
      request_meta["method"],
      request_meta["name"],
      request_meta["response_time"],
      request_meta["content_size"],
    )
    return ret



class ZookeeperResponseContextManager(BaseContextManager):
  exception_class = ResponseError


class ZookeeperSession(BaseClient):
  conext_manager = ZookeeperResponseContextManager
  loose_policy = {}
  strict_policy = {}

  def __init__(self,server_list='127.0.0.1:2181',*args,**kwargs):
    super(ZookeeperSession,self).__init__(*args,**kwargs)
    self.session_policy = "loose_policy"
    self._zookeeper_client = None 
    self.server_list = server_list

  def set_session_policy(self,session_policy="loose"):
    '''prototype not currenlty used.
    '''
    self.session_policy = session_policy+"_policy"

  def connect(self,*args,**kwargs):
    '''See http://kazoo.readthedocs.org/en/latest/api/client.html
     for details regarding available options. Any provided client
     start() parameters provided will override defaults.
    '''
    defaults = {
      "hosts" : self.server_list,
      "handler" : SequentialGeventHandler()
    }
    defaults.update(getattr(self,self.session_policy))
    defaults.update(kwargs)
    self._state = KazooState.LOST
    self._zookeeper_client = KazooClient(**defaults)
    self._zookeeper_client.add_listener(self._state_tracker)
    watchable = self._zookeeper_client.start_async()
    watchable.wait(30)
    if not self._zookeeper_client.connected:
      err = "Could not connect to Zookeeper server(s) %(server_list)s" % defaults
      raise ResponseError(err)

  @require_state(KazooState.CONNECTED)
  @record_stats
  def ensure_path(self,path,watcher=None):
    self._zookeeper_client.ensure_path(path,watcher)
    
  def _state_tracker(self,state):
    self._state = state

  def __del__(self):
    if isinstance(self._zookeeper_client, KazooClient):
      self._zookeeper_client.stop() 


