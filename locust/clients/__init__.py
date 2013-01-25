'''
all clients need to be explicitly imported here.
Not fancy but sure not to have odd bugs. I'm looking
at you __import__
'''
from httpclient import HttpSession


'''
client_index is a lookup table that allows associating one or more
common names with a given client. Example "web" and "http" are
synonyms for HttpSession client.
'''
client_index = {
  HttpSession : ["web","http","HttpSession"],
}



def client_loader(client_type):
  '''BaseClient client_loader(client_type = str)
     client_type is some common name defined for a 
     given client type. See client_index doc.
  '''
  for client_impl,names in client_index.items():
    if client_type in names:
      return client_impl
  
