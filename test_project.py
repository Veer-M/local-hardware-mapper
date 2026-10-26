import socket
import pytest
from network_mapper import scan, probe

def test_actual_local_listener():
    with socket.socket() as server:
        server.bind(('127.0.0.1',0))
        server.listen(8)
        port = server.getsockname()[1]
        assert probe('127.0.0.1',[port],0.1) == [port]
        assert scan('127.0.0.1/32',[port],0.1,1) == [{'ip':'127.0.0.1','ports':[port]}]

@pytest.mark.parametrize('network',['8.8.8.8/32','192.168.0.0/16','::1/128'])
def test_reject_scope(network):
    with pytest.raises(ValueError):
        scan(network)
