import etcd3
import time


ETCD_WATCH_COUNT = 0
if __name__ == '__main__':
    etcd = etcd3.client(host='192.168.30.144', port=2379, ca_cert="etcd/ca.pem", cert_cert="etcd/client.pem",cert_key='etcd/client-key.pem')

    with etcd.lock('/key') as locker:
        etcd.put("/key", "locked by command")
        time.sleep(30)
        print(etcd.get('/key'))
    # cancel watch
    



