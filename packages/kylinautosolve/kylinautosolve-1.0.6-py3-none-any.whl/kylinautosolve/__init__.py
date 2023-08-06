# __init__.py

from .client import KylinAutosolveClient
from .client import KylinAutosolveError
from .client import AlreadyStartedError, NotStartedError, RemoteError, RequestAbortedError, StoppedError
from .client import CreateTaskRequest, GetTaskResultRequest, CancelTaskRequest
from .service import KylinAutosolveService
from .pb import kylinautosolve_pb2 as KylinAutosolveProto

# Version of the kylin autosolve client package
__version__ = "1.0.6"
