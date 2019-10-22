import json
from kazoo.client import KazooClient
from kazoo.client import KazooState

ZK_POOLS = ["192.168.30.144:2181", "192.168.30.145:2181", "192.168.30.146:2181"]
ZK_PATH = "/test/services/"

def register_service(service_name, znode_name, znode_data, service_data=None):
    hosts_str = ",".join(ZK_POOLS)
    zk_client = KazooClient(hosts=hosts_str)
    zk_client.start()

    service_znode_str = ZK_PATH + service_name
    if not zk_client.exists(service_znode_str):
        zk_client.create(path=service_znode_str, value=service_data.encode(encoding='utf-8'), makepath=True)
    znode_str = "%s/%s" % (service_znode_str, znode_name)
    
    service_node = zk_client.get_children(path=service_znode_str, watch=service_watcher)

    if znode_name in service_node:
        zk_client.set(znode_str, json.dumps(znode_data).encode(encoding='utf-8'))
    else:
        zk_client.create(znode_str, json.dumps(znode_data).encode(encoding='utf-8'))
    
    zk_client.stop()

def service_watcher(state):
    pass

def my_listener(state):
    if state == KazooState.LOST:
        # Register somewhere that the session was lost
    elif state == KazooState.SUSPENDED:
        # Handle being disconnected from Zookeeper
    else:
        # Handle being connected/reconnected to Zookeeper

if __name__ == '__main__':
    register_service('students_services', 'node1', {'ip': '192.168.30.144', 'port': 50051},'students_services')