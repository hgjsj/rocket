from kubernetes import client, config, watch
import sys, getopt

def add_srv_in_ingress(api, srv):
    ingress = api.read_namespaced_ingress("test-ingress", "default")
    srv_name = srv.metadata.name
    port = srv.spec.ports[0].port

    ingress_paths = ingress.spec.rules[0].http.paths
    
    if srv_name not in [ingress_path.backend.service_name for ingress_path in ingress_paths]:
        backend = client.NetworkingV1beta1IngressBackend(srv_name, port)
        path = "/%s" % srv_name
        ingress_paths.append(client.NetworkingV1beta1HTTPIngressPath(backend=backend, path=path))
        api.patch_namespaced_ingress("test-ingress", "default", ingress)


def delete_srv_in_ingress(api, srv):
    ingress = api.read_namespaced_ingress("test-ingress", "default")
    srv_name = srv.metadata.name

    ingress_paths = ingress.spec.rules[0].http.paths

    for ingress_path in ingress_paths:
        if srv_name == ingress_path.backend.service_name:
            ingress_paths.remove(ingress_path)
            break
    if (len(ingress_paths) != 0):
        api.patch_namespaced_ingress("test-ingress", "default", ingress)
    else:
        print("last path can't delete")
    

def main(host_cluster=None, access_token=None):

    if host_cluster and access_token:
        remote_config = client.Configuration()
        remote_config.host = host_cluster
        remote_config.verify_ssl = False
        remote_config.api_key = {"authorization": "Bearer " + access_token}
        api_client = client.ApiClient(remote_config)
    else:
        # run this script in pod
        config.load_incluster_config()
        api_client = None
    core_api = client.CoreV1Api(api_client)
    network_api = client.NetworkingV1beta1Api(api_client)
    w = watch.Watch()

    for event in w.stream(core_api.list_service_for_all_namespaces, watch=True, label_selector="export-type=ingress-nginx"):
        print(event)
        if event['type'] == "ADDED":
            add_srv_in_ingress(network_api, event['object'])
        elif event['type'] == "DELETED":
            delete_srv_in_ingress(network_api, event['object'])
        
    # Do calls  
    #print("Listing pods with their IPs:")
    #ret = v1.list_pod_for_all_namespaces(watch=False)
    #svcs = v1.list_service_for_all_namespaces(watch=False)
    #ingresses = v2.list_ingress_for_all_namespaces(watch=False)
    
    #for s in ingresses.items:
    #    print(s)

def usage():
    print("k8s_operator.py -h -t --help\n-h: kubernetes cluster server with port -t: access token")

if __name__ == "__main__":
    opts, args = getopt.getopt(sys.argv[1:], "h:t:", ["help"])
    host_cluster = None
    access_token = None
    for opt, arg in opts:
        if opt == "--help":
            usage()
            sys.exit()
        if opt == "-h":
            host_cluster = arg
        if opt == "-t":
            access_token = "eyJhbGciOiJSUzI1NiIsImtpZCI6IiJ9.eyJpc3MiOiJrdWJlcm5ldGVzL3NlcnZpY2VhY2NvdW50Iiwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudC9uYW1lc3BhY2UiOiJrdWJlLXN5c3RlbSIsImt1YmVybmV0ZXMuaW8vc2VydmljZWFjY291bnQvc2VjcmV0Lm5hbWUiOiJyZXNvdXJjZS1vcGVyYXRvci10b2tlbi1xOGpnNiIsImt1YmVybmV0ZXMuaW8vc2VydmljZWFjY291bnQvc2VydmljZS1hY2NvdW50Lm5hbWUiOiJyZXNvdXJjZS1vcGVyYXRvciIsImt1YmVybmV0ZXMuaW8vc2VydmljZWFjY291bnQvc2VydmljZS1hY2NvdW50LnVpZCI6IjE3ZDRlNWZkLWQ3YjItNGZhNS1hZjFjLWMwMzFmYjg0ZTQxYiIsInN1YiI6InN5c3RlbTpzZXJ2aWNlYWNjb3VudDprdWJlLXN5c3RlbTpyZXNvdXJjZS1vcGVyYXRvciJ9.FNLh-aoo4RBeDnOo0oafUc2BOQxb5nV4ItMnhw-kaGcciou4NAn9_nCoM2AyV5P7wrbtXyFvf6_CiC6XqnerGX9VgK7mPDN2cWzDAgWY0jzUbheyB0UQgliRWjOFmbhudif86hjG1Auzy5qJ6Nn81-CyyIIchLYxpasxnRyNAgEPRmMS2OOctCAJV8Syr_tgbs1PIHIPynZTFLeA0y0QKZFfwAAa2TyKWlKJ8OZCUcjFCEb-1fdxDM9lXYS7vkPgogHIWQAOK5uB7XSC53qTB-R83bi3-Pi7L2iPVfXi3YqOA97KsDgcuqLpSIvQBK_fwpdHHP_tBZZ5WNvnCehweQ"
    
    main(host_cluster,access_token)