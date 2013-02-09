from collections import namedtuple
from locust.log import init_logger


#perhaps warning module is more appropriate but looks ugly, if there
#are functional changes as a result this can be reverted.
pretty_spaces = " " * len("[WARNING] ")
zmq_warn_msg =  "Using pure Python socket RPC implementation instead of zmq. "
zmq_warn_msg += "\n%sThis will not affect you if you're not running locust in "
zmq_warn_msg += "distributed mode,\n%sbut if you are, "
zmq_warn_msg += "we recommend you to install "
zmq_warn_msg += "the python packages: pyzmq and gevent-zeromq"
zmq_warn_msg = zmq_warn_msg % (pretty_spaces,pretty_spaces)
try:
    import zmqrpc as rpc
except ImportError:
    init_logger.warning(zmq_warn_msg)
    import socketrpc as rpc

Message = namedtuple("Message", ["type", "data", "node_id"])
