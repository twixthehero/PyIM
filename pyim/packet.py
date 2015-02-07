"""
The structure of packets looks like this:

packet id   | sender id | dest id   | data
1 byte      | 1 byte    | 1 byte    | x bytes
"""

ID_PING = b"\0"
ID_MSG = b"\1"
ID_NAME = b"\2"