import socket
import datetime
from concurrent.futures import ThreadPoolExecutor

PROTO = {
    "tcp": socket.SOCK_STREAM,
    "udp": socket.SOCK_DGRAM
}

thread_pool = ThreadPoolExecutor(2)

def proceed_client(client_fd, addr):
    while True:
        recv_str = client_fd.recv(1024).decode("utf-8")
        print(recv_str)
        if recv_str.startswith("bye"):
            client_fd.close()
            break
        send_str = "received %s from %s port %d on %s" % (recv_str, addr[0], addr[1], datetime.datetime.now())
        client_fd.send(send_str.encode("utf-8"))

class Server(object):
    def __init__(self, addr, port, protocal="tcp"):
        self.port = port
        self.addr = addr
        self.server_end = socket.socket(socket.AF_INET, PROTO[protocal])
    
    def bind(self):
        self.server_end.bind(( self.addr, self.port))

    def listen(self):
        self.server_end.listen()

    def accept(self):
        return self.server_end.accept()

    def read(self):
        return self.server_end.recvfrom(1024)

    def write(self, addr):
        self.server_end.sendto(b"ok1",addr)

    def close(self):
        self.server_end.close()

if __name__ == "__main__":
    s = Server("0.0.0.0", 8880)
    s.bind()
    s.listen()
    task_list = []
    while True:
        client, addr = s.accept()
        task_list.append(thread_pool.submit(proceed_client, client, addr))
        #data, addr = s.read()
        #print(data)
        #print(addr)
        #s.write(addr)
        #print(client.recv(1024))
        #client.send(b"ok")

        #client.close()
    s.close()
        