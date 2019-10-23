import etcd3
import time
import datetime

ETCD_WATCH_COUNT = 0

def pait_log(char):
    def print_line(func):
        def printing(text):
            print (char * 15)
            func(text)
            print (char * 15)
        return printing
    return print_line

def print_line1(func):
    def printing(text):
        print ("*" * 15)
        func(text)
        print ("*" * 15)
    return printing

def print_line2(func):
    def printing(text):
        print ("~" * 15)
        func(text)
        print ("~" * 15)
    return printing

#@pait_log('=')
@print_line1
@print_line2
def log(text):
    print ("now is %s" % text)

def log1(text):
    print ("now is %s" % text)

if __name__ == '__main__':
    #etcd = etcd3.client(host='192.168.30.144', port=2379, ca_cert="etcd/ca.pem", cert_cert="etcd/client.pem",cert_key='etcd/client-key.pem')
    log(datetime.datetime.now())
    a = print_line1(print_line2(log1))
    a(datetime.datetime.now())
    etcd = etcd3.client(host='192.168.30.144', port=2379, ca_cert="etcd/ca.pem", cert_cert="etcd/client.pem",cert_key='etcd/client-key.pem')

    #with etcd.lock('/key') as locker:
    #    print(etcd.get('/key'))
    #    etcd.put("/key", "locked by vscode")
    #    print(etcd.get('/key').value)
    # cancel watch
    



