from kazoo.client import KazooClient
from baseclient import BaseClient

class ZookeeperSession(BaseClient):
	def __init__(self,server_list,*args,**kwargs):
		self.zk_client = None 
		self.server_list = server_list

  def connect(self,*args,**kwargs):
  	'''See http://kazoo.readthedocs.org/en/latest/api/client.html
  	   for details regarding available options. "Hosts" parameter
  	   is not required if this is being executed via the command
  	   line interface. It may be overridden explicitly here.
  	'''
  	if "hosts" not in kwargs: kwargs["hosts"] = self.server_list
	  self.zk_client = KazooClient(**kwargs)

	def ensure_path(self,path): pass