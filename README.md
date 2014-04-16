gojsonrpcclient
===============

A python library for communicating with a golang json rpc server. 

Usage: 

from gojsonrpcclient import GoJsonRpcClient
client = GoJsonRpcClient("localhost", 8000, "Server")
client.call("ExposedMethod", { "Mass": 1, "Velocity": 32.8 })

