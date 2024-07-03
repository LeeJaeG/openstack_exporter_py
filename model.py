from pydantic import BaseModel, Field
from typing import List, Optional, Union

class MemoryDetails(BaseModel):
    used: int
    maximum: int

class CPUDetails(BaseModel):
    utilisation: Optional[float]
    id: int
    time: int

class DiskDetails(BaseModel):
    read_requests: int
    errors_count: int
    read_bytes: int
    write_requests: int
    write_bytes: int

class NICDetails(BaseModel):
    rx_packets: int
    rx_drop: int
    tx_octets: int
    tx_errors: int
    tx_drop: int
    rx_octets: int
    rx_rate: Optional[float]
    rx_errors: int
    mac_address: str
    tx_packets: int
    tx_rate: Optional[float]

class Location(BaseModel):
    cloud: str
    region_name: str
    zone: Optional[str]
    project: Optional[dict]

class ServerDetails(BaseModel):
    has_config_drive: bool
    state: str
    driver: str
    hypervisor: str
    hypervisor_os: str
    uptime: int
    num_cpus: int
    num_disks: int
    num_nics: int
    memory_details: MemoryDetails
    cpu_details: List[CPUDetails]
    disk_details: List[DiskDetails]
    nic_details: List[NICDetails]
    id: Optional[str]
    name: Optional[str]
    location: Location

class OpenstackInstanceMetrics:
    def instance_data():
        return {
        "uptime": "Openstack_Instance_Uptime",
        "num_cpus": "Openstack_Instance_CPU_Nums",
        "num_disks": "Openstack_Instance_Disk_Nums",
        "num_nics": "Openstack_Instance_NIC_Nums",
        }
        
    def disk_data():
        return {
        "disk": "Openstack_Instance_Root_Disk_Size",
        "ephemeral": "Openstack_Instance_Ephemeral_Disk_Size"
        }
        
    def cpu():
        return {
        # "CPU_UTIL": "Openstack_Instance_CPU_Util",
        "time": "Openstack_Instance_CPU_Time"
        }
        
    def memory():
        return {
        "used": "Openstack_Instance_Memory_Used",
        "maximum": "Openstack_Instance_Memory_Maximum"
        }
        
    def disk():
        return {
        "read_requests": "Openstack_Instance_Disk_Read_Requests",
        "errors_count": "Openstack_Instance_Disk_Errors_Count",
        "read_bytes": "Openstack_Instance_Disk_Read_Bytes",
        "write_requests": "Openstack_Instance_Disk_Write_Requests",
        "write_bytes": "Openstack_Instance_Disk_Write_Bytes"
        }
        
    def nic():
        return {
        "rx_packets": "Openstack_Instance_NIC_RX_Packets",
        "rx_octets": "Openstack_Instance_NIC_RX_Octets",
        "rx_errors": "Openstack_Instance_NIC_RX_Errors",
        "rx_drop": "Openstack_Instance_NIC_RX_Drop",
        "tx_packets": "Openstack_Instance_NIC_TX_Packets",
        "tx_octets": "Openstack_Instance_NIC_TX_Octets",
        "tx_errors": "Openstack_Instance_NIC_TX_Errors",
        "tx_drop": "Openstack_Instance_NIC_TX_Drop",
        }





