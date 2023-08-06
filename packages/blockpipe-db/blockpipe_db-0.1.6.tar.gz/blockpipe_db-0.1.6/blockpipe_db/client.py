import socket
import msgpack
import pandas as pd
from hexbytes import HexBytes

from .msg import GetLogs1Request


_DEFAULT_HOST = 'blockpipe_db_host'
_DEFAULT_PORT = 5555


class BufferedSocket:
    def __init__(self, sock):
        self.sock = sock
        self.buffer = b''

    def read_exact(self, num_bytes):
        while len(self.buffer) < num_bytes:
            new_data = self.sock.recv(4096)
            if not new_data:
                raise IOError("Could not receive enough data")
            self.buffer += new_data

        result, self.buffer = self.buffer[:num_bytes], self.buffer[num_bytes:]
        return result


class Client:
    def __init__(self, host: str = _DEFAULT_HOST, port: int = _DEFAULT_PORT):
        self.host = host
        self.port = port

    def load_event_df(
        self, address: str, topic0: str, network: str = 'ethereum_mainnet',
        from_block_number: int = 0, from_log_index: int = 0, limit: int = 100,
    ) -> pd.DataFrame:
        q = GetLogs1Request(
            network=network,
            address=HexBytes(address),
            topic0=HexBytes(topic0),
            from_block_number=from_block_number,
            from_log_index=from_log_index,
            limit=limit,
        )
        s = socket.socket()
        s.connect((self.host, self.port))
        data = q.to_bytes()
        s.sendall(len(data).to_bytes(4, 'big'))
        s.sendall(data)
        buf_read = BufferedSocket(s)
        data = []
        while True:
            nb = buf_read.read_exact(4)
            sz = int.from_bytes(nb, 'big')
            e = buf_read.read_exact(sz)
            v = msgpack.unpackb(e)
            if 'Done' in v:
                break
            data.append(v['DataFrame'])
        return pd.DataFrame(data, columns=[
            'log_index', 'tx_index', 'tx_hash', 'block_hash', 'block_number', 'block_timestamp',
            'address', 'data', 'topic0', 'topic1', 'topic2', 'topic3',
        ])
