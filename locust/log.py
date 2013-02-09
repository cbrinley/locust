import logging
from logging.handlers import MemoryHandler
import sys

def setup_logging(loglevel, logfile):
    global init_handler
    numeric_level = getattr(logging, loglevel.upper(), None)
    if numeric_level is None:
        raise ValueError("Invalid log level: %s" % loglevel)
    
    log_format = "[%(asctime)s] %(levelname)s/%(name)s: %(message)s"
    logging.basicConfig(level=numeric_level, filename=logfile, format=log_format)
    init_handler.setTarget(logging.root)
    init_handler.flush()

    
    sys.stderr = StdErrWrapper()
    sys.stdout = StdOutWrapper()

stdout_logger = logging.getLogger("stdout")
stderr_logger = logging.getLogger("stderr")

class StdOutWrapper(object):
    """
    Wrapper for stdout
    """
    def write(self, s):
        stdout_logger.info(s.strip())

class StdErrWrapper(object):
    """
    Wrapper for stderr
    """
    def write(self, s):
        stderr_logger.error(s.strip())

# set up logger for the statistics tables
console_logger = logging.getLogger("console_logger")
# create console handler
sh = logging.StreamHandler()
sh.setLevel(logging.INFO)
# formatter that doesn't include anything but the message
sh.setFormatter(logging.Formatter('%(message)s'))
console_logger.addHandler(sh)
console_logger.propagate = False

# configure python-requests log level
requests_log = logging.getLogger("requests")
requests_log.setLevel(logging.WARNING)

#logger to handle initial startup messages in a pretty way
#messages are buffered so that when user issues: locust --help
#they don't get ugly warnings.
#this log handler is flushed in setup__logging
init_logger = logging.getLogger("initialize")
init_logger.setLevel(logging.DEBUG)
init_handler = MemoryHandler(1000,flushLevel=logging.DEBUG) 
init_logger.addHandler(init_handler)

