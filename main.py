import time
from prometheus_client import start_http_server, Gauge
import openstack
import concurrent.futures
from model import OpenstackInstanceMetrics, ServerDetails

conn = openstack.connect(cloud='openstack')


openstack_instance_metrics = OpenstackInstanceMetrics
instance_gauges = {}


def prometheus_instance_Gauge(name, documentation, value, instance_id, instance_name, instance_cluster_id):
    if name not in instance_gauges:
        instance_gauges[name] = Gauge(name, documentation, ['instance_id', 'instance_name', 'instance_cluster_id'])
    instance_gauges[name].labels(instance_id=instance_id, instance_name=instance_name,
                                  instance_cluster_id=instance_cluster_id).set(value)


def prometheus_instance_nic_Gauge(name, documentation, value, instance_id, instance_name, instance_cluster_id,
                                  nic_mac_address):
    if name not in instance_gauges:
        instance_gauges[name] = Gauge(name, documentation,
                                      ['instance_id', 'instance_name', 'instance_cluster_id', 'nic_mac_address'])
    instance_gauges[name].labels(instance_id=instance_id, instance_name=instance_name,
                                  instance_cluster_id=instance_cluster_id, nic_mac_address=nic_mac_address).set(value)


def process_server(server):
    server_id = server['id']
    server_name = server['name']
    # diskio=nova.servers.diagnostics(server_id)
    # a=conn.compute.get_hypervisor('986fa384-22c2-4624-90f5-d93058e9412b')
    # print(server)
    if server['metadata']:
        server_cluster_id = server['metadata']['cluster_id']
    else:
        server_cluster_id = ''
    server_diagnostics = conn.compute.get_server_diagnostics(server_id)
    server_details = ServerDetails(**server_diagnostics)
    

    for key, value in openstack_instance_metrics.instance_data().items():
        prometheus_instance_Gauge(value, key, getattr(server_details, key), server_id, server_name, server_cluster_id)

    for key, value in openstack_instance_metrics.disk_data().items():
        prometheus_instance_Gauge(value, key, getattr(server.flavor, key), server_id, server_name, server_cluster_id)

    for key, value in openstack_instance_metrics.cpu().items():
        cputime = sum(getattr(cpu_detail, key) for cpu_detail in server_details.cpu_details)
        prometheus_instance_Gauge(value, key, cputime, server_id, server_name, server_cluster_id)

    for key, value in openstack_instance_metrics.memory().items():
        prometheus_instance_Gauge(value, key, getattr(server_details.memory_details, key), server_id, server_name,
                                  server_cluster_id)

    for key, value in openstack_instance_metrics.disk().items():
        for disk_detail in server_details.disk_details:
            prometheus_instance_Gauge(value, key, getattr(disk_detail, key), server_id, server_name, server_cluster_id)


    for key, value in openstack_instance_metrics.nic().items():
        for nic_detail in server_details.nic_details:
            prometheus_instance_nic_Gauge(value, key, getattr(nic_detail, key), server_id, server_name,
                                          server_cluster_id, nic_detail.mac_address)


if __name__ == '__main__':
    start_http_server(18080)

    while True:
        time.sleep(3)
        server_list = list(conn.compute.servers(all_projects=True))

        with concurrent.futures.ThreadPoolExecutor() as executor:
            executor.map(process_server, server_list)
