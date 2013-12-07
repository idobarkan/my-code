import socket, time

def open_tcp_connections(num_connections, host, port):
    t0 = time.time()
    for _ in xrange(num_connections):
        s = socket.socket()
        s.connect((host, port))
        _data = s.recv(1024)
        s.close()
    return time.time() - t0

def open_as_many_tcp_connections(period_sec, host, port):
    start_time = time.time()
    connection_opened = 0
    while time.time() - start_time <= period_sec:
        s = socket.socket()
        s.connect((host, port))
        connection_opened += 1
        _data = s.recv(1024)
        s.close()
    return connection_opened