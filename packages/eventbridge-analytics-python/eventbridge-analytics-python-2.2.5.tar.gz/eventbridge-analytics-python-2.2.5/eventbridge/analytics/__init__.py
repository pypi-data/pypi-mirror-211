
from eventbridge.analytics.version import VERSION
from eventbridge.analytics.client import Client

__version__ = VERSION

"""Settings."""
source_id = Client.DefaultConfig.source_id
event_bus_name = Client.DefaultConfig.event_bus_name
on_error = Client.DefaultConfig.on_error
debug = Client.DefaultConfig.debug
send = Client.DefaultConfig.send
sync_mode = Client.DefaultConfig.sync_mode
max_queue_size = Client.DefaultConfig.max_queue_size
max_retries = Client.DefaultConfig.max_retries
access_key = Client.DefaultConfig.access_key
secret_access_key = Client.DefaultConfig.secret_access_key
region_name = Client.DefaultConfig.region_name
session_token = Client.DefaultConfig.session_token

default_client = None


def track(*args, **kwargs):
    """Send a track call."""
    return _proxy('track', *args, **kwargs)


def identify(*args, **kwargs):
    """Send a identify call."""
    return _proxy('identify', *args, **kwargs)


def group(*args, **kwargs):
    """Send a group call."""
    return _proxy('group', *args, **kwargs)


def alias(*args, **kwargs):
    """Send a alias call."""
    return _proxy('alias', *args, **kwargs)


def page(*args, **kwargs):
    """Send a page call."""
    return _proxy('page', *args, **kwargs)


def screen(*args, **kwargs):
    """Send a screen call."""
    return _proxy('screen', *args, **kwargs)


def flush():
    """Tell the client to flush."""
    _proxy('flush')


def join():
    """Block program until the client clears the queue"""
    _proxy('join')


def shutdown():
    """Flush all messages and cleanly shutdown the client"""
    _proxy('flush')
    _proxy('join')


def _proxy(method, *args, **kwargs):
    """Create an analytics client if one doesn't exist and send to it."""
    global default_client
    if not default_client:
        default_client = Client(source_id=source_id,
                                event_bus_name=event_bus_name, debug=debug,
                                max_queue_size=max_queue_size,
                                send=send, on_error=on_error,
                                max_retries=max_retries,
                                sync_mode=sync_mode,
                                access_key=access_key,
                                secret_access_key=secret_access_key,
                                region_name=region_name,
                                session_token=session_token)

    fn = getattr(default_client, method)
    return fn(*args, **kwargs)
