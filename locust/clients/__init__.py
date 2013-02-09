
import logging
from locust.log import init_logger
from locust.exception import LocustError

'''
import_manifest:
describes where to import clients from and how to expose 
those clients via the CLI. i.e. the alias for the client.

Structure:
  import_manifest is a dict with two distinct entry 
  types per client/Session class

  Entry1: the module name and class name to attempt import
  modulename : classname | [classname1,classname2,...]

  Entry2: the aliases for the class that can be used at CLI
  <classname>_alias: [list,of,names,this,class,can,be,called]


Structure Detail:
  modulename:
    the module component of a from clause in a standard 
    import statement. example: `from foo.bar import baz`
    foo.bar is the <modulename> in this case.

  classname:
    the class to import from the above module or an 
    iterable containing the name of all classes to
    import.

<classname>_alias = a list of human friendly names that
                     can be used as argument to -T param
                     via CLI locust command.
'''

import_manifest = {
  "httpclient" : ["HttpSession","HttpsSession"],
  "HttpSession_alias" : ["web","http","HttpSession"],
  "HttpsSession_alias" : ["https","sslweb","HttpsSession"],


  "zookeeperclient" : "ZookeeperSession",
  "zookeeperclient_alias" : ["zookeeper","zk","ZookeeperSession"],
}


######################## PUBLIC METHODS #############################
loaded_clients = {}
def client_loader(client_alias):
  '''BaseClient client_loader(client_type = str)
     client_type is some common name defined for a 
     given client type. See client_index doc.
  '''
  global loaded_clients
  logger = logging.getLogger(__name__)
  try:
    return loaded_clients[client_alias]
  except Exception, exc:
    logger.debug("%s encountered in clients.client_loader()" % exc)
    raise LocustError("No valid client type was specified.")



######################## INTERNAL LOGIC #############################
iterable = lambda x: hasattr(x,"__iter__") and x or [x]
do_import = lambda x,y: __import__(x,globals(),locals(),y)

def try_load(mod_name,class_name):
  global init_logger
  try:
    class_names = iterable(class_name)
    module_object = do_import(mod_name,class_names)
    out_names = []
    for name in class_names:
      if hasattr(module_object,name):
        out_names.append(name)
      else:
        init_logger.warning("%s was not found in %s." % (name,mod_name))
    return module_object,out_names
  except ImportError, exc:
    err1 = "An attempt to load client %s failed. " % class_name
    err2 = "A dependency of this client may not be installed."
    err3 = "REASON: %s" % str(exc) #spaces are for output formating.
    init_logger.warning(err1)
    init_logger.warning(err2)
    init_logger.warning(err3)
    return None,None
  except Exception,exc:
    #let users keep working even if some clients can't be loaded.
    #Assumption is the user is requesting a working client and 
    #shouldn't be prevented from running load tests because there 
    #is a busted client. If this proves to be trouble in practice 
    #simply remove this exception handler and the locust binary 
    #will error out early.
    init_logger.warning("Unable to load client %s." % class_name)
    init_logger.info(str(exc))
    return None,None

def update_loaded_clients(module_object,class_name):
  global import_manifest, loaded_clients, init_logger
  try:
    class_object = getattr(module_object,class_name)
    aliases = import_manifest[class_name+"_alias"]
    updates = dict( [(alias,class_object) for alias in aliases] )
    loaded_clients.update(updates)
  except:
    init_logger.warning("Unable to load client %s." % class_name)
    init_logger.info(str(exc))


def load_all_clients():
  global import_manifest
  #even though _alias is technically a class_name here
  #we treat it as mod_name because our view into import_manifest
  #is still somewhat opaque.
  for mod_name,class_names in import_manifest.items():
    if mod_name.endswith("_alias"): continue
    module_object,class_names = try_load(mod_name,class_names)
    if not module_object: continue
    for class_name in class_names:
      update_loaded_clients(module_object,class_name)

load_all_clients()