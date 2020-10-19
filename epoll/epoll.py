import select
import server
import socket

EOL0 = b'\n'
EOL1 = b'\n\n'
EOL2 = b'\n\r\n'
class EpollServer(server.Server):
    def __init__(self, addr, port):
        server.Server.__init__(self, addr, port, "tcp")
        self.epoll = select.epoll()
    
    def start_server(self):
        self.bind()
        self.listen()
        self.server_end.setblocking(False)
        self.register_fd(self.server_end.fileno(), select.EPOLLIN)

    def register_fd(self, fd, event_mask):
        self.epoll.register(fd, event_mask)
    
    def unregister_fd(self, fd):
        self.epoll.unregister(fd)

    def modify_setting(self, fd, event_mask):
        self.epoll.modify(fd, event_mask)

    def poll(self):
        return self.epoll.poll(maxevents=100)
    
    def close(self):
        self.unregister_fd(self.server_end.fileno())
        self.epoll.close()
        super(EpollServer, self).close()

def epoll_LT(efd):
    events = efd.poll()
    for fd, event in events:
        if fd == efd.server_end.fileno():
            connection, address = efd.accept()
            connection.setblocking(False)
            efd.register_fd(connection.fileno(), select.EPOLLIN)
            connections[connection.fileno()] = connection
        elif event & select.EPOLLHUP and fd in connections:
            efd.unregister_fd(fd)
            connections[fd].close()
            del connections[fd]
        elif event & select.EPOLLIN and fd in connections:
            receive_byte = b""
            while True:
                data = connections[fd].recv(1024)
                if data:
                    receive_byte += data
                    print(receive_byte)
                    if EOL0 in receive_byte or EOL1 in receive_byte or EOL2 in receive_byte:
                        messages[fd] = receive_byte.decode("utf-8")
                        break
                else:
                    break
            efd.modify_setting(fd, select.EPOLLOUT)
        elif event& select.EPOLLOUT and fd in connections:
            connections[fd].send("got it message {} from {}:{}\n".format(messages[fd], connections[fd].getpeername()[0], connections[fd].getpeername()[1]).encode("utf-8"))
            efd.modify_setting(fd, select.EPOLLIN)

def epoll_ET(efd):
    events = efd.poll()
    for fd, event in events:
        if fd == efd.server_end.fileno():
            try:
                while True:
                    connection, address = efd.accept()
                    connection.setblocking(False)
                    efd.register_fd(connection.fileno(), select.EPOLLIN | select.EPOLLET)
                    connections[connection.fileno()] = connection
            except socket.error:
                pass
        elif (event & select.EPOLLHUP or event & select.EPOLLERR) and fd in connections:
            efd.unregister_fd(fd)
            connections[fd].close()
            del connections[fd]
        elif event & select.EPOLLIN and fd in connections:
            receive_byte = b""
            while True:
                data = connections[fd].recv(1024)
                if data:
                    receive_byte += data
                    print(receive_byte)
                    if EOL0 in receive_byte or EOL1 in receive_byte or EOL2 in receive_byte:
                        messages[fd] = receive_byte.decode("utf-8")
                        break
                else:
                    break
            efd.modify_setting(fd, select.EPOLLOUT | select.EPOLLET)
        elif event& select.EPOLLOUT and fd in connections:
            connections[fd].send("got it message {} from {}:{}\n".format(messages[fd], connections[fd].getpeername()[0], connections[fd].getpeername()[1]).encode("utf-8"))
            efd.modify_setting(fd, select.EPOLLIN | select.EPOLLET)

            
if __name__ == "__main__":
    s = EpollServer("0.0.0.0", 8881)
    s.start_server()

    connections = {}
    messages = {}
    try:
        while True:
            epoll_ET(s)
    finally:
        s.close()

    