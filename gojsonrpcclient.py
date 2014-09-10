
import time
import json
import socket
import itertools


class GoJsonRpcClient(object):
    def __init__(self, addr, port, name, retries=-1, max_sleep_time=32):
        """Construct an RPC client. 

        addr : string
            The server's address. 
        port : int
            The server's port. 
        name : string
            The name of the object we'll be calling on the other end. 
            When using the golang json-rpc server, functions are 
            prefixed with the object name and a dot: object.Function. 
            The name is simply prepended to the method requested. 
        retries : int
            The number of retries to attempt when connecting. If retries < 0
            then the code will retry forever. 
        max_sleep_time : float time in seconds
            Maximum sleep time in seconds. Each time the connection has to
            be retried, the sleep time between retries doubled until 
            it is greater than or equal to max_sleep_time. 
        """
        self._addr = addr
        self._port = port
        self._name = name
        self._retries = retries
        self._max_sleep_time = max_sleep_time
        self._id = itertools.count()
        self._sock = None
        self._do_connect()

        
    def _do_connect(self):
        sleep_time = 1
        retry = 0
        while 1:
            retry += 1
            try:
                self._sock = socket.create_connection((self._addr, self._port))
                return
            except Exception, ex:
                if retry == self._retries - 1:
                    raise ex
                else:
                    time.sleep(sleep_time)
                    if sleep_time < self._max_sleep_time:
                        sleep_time *= 2


    def _get_resp(self):
        strings = []
        while 1:
            s = self._sock.recv(4096)
            strings.append(s)
            if s[-1] == "\n":
                break
        return json.loads(" ".join(strings))


    def call(self, method, params):
        """Call the given method on the go server.
        
        method : string
            The name of the method to call. Note that the name given in the 
            constructor will be prepended to the name given here. Also recall
            that the method must be capitalized as per go regulations. 
        params : list or dict
            The standard go rpc server only allows a single argument for 
            exposed functions. 

        Return: 
            The "result" member of the returned dictionary if there was no 
            error. If an error occured, an exception is raised. 
        """
        _id = next(self._id)
        req = dict(id=_id, 
                   params=[params,], 
                   method=self._name + "." + method)
        req = json.dumps(req).encode()
        resp = None
        try:
            self._sock.sendall(req)
            resp = self._get_resp()
        except:
            self._do_connect()
            self._sock.sendall(req)
            resp = self._get_resp()
            
        if resp["error"] is not None:
            raise Exception(resp["error"])
        
        elif resp["id"] != _id:
            raise Exception("Mismatched message ids.")
        
        return resp["result"]
