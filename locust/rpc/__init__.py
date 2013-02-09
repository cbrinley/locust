from collections import namedtuple
from locust.log import init_logger


#perhaps warning module is more appropriate but looks ugly, if there
#are functional changes as a result this can be reverted.
zmq_warn_msg1 = "Using pure Python socket RPC implementation instead of zmq. "
zmq_warn_msg2 = "This will not affect you if you're not running locust in distributed mode."
zmq_warn_msg3 = "If you are, we recommend you to install: pyzmq and gevent-zeromq"
try:
    import zmqrpc as rpc
except ImportError:
    init_logger.warning(zmq_warn_msg1)
    init_logger.warning(zmq_warn_msg2)
    init_logger.warning(zmq_warn_msg3)
    import socketrpc as rpc

Message = namedtuple("Message", ["type", "data", "node_id"])
