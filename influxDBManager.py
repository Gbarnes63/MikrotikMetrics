from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS

class InfluxDBWriter:
    def __init__(self, url, token, org):
        self.client = InfluxDBClient(url=url, token=token, org=org)
        self.write_api = self.client.write_api(write_options=SYNCHRONOUS)

    def write_interface_metrics(self, client_ip, interface_data):
        for interface_name, data in interface_data.items():
            point = Point("interface_metrics") \
                .tag("client", client_ip) \
                .tag("interface", data['interface']) \
                .field("rx-byte", data['rx-byte']) \
                .field("tx-byte", data['tx-byte'])
            self.write_api.write(bucket="InterfaceStat", record=point, write_precision=WritePrecision.MS)

    def write_latency_metrics(self, client_ip, latency_data):
        for service, latency in latency_data.items():
            point = Point("latency_metrics") \
                .tag("client", client_ip) \
                .tag("service", service) \
                .field("latency", latency)
            self.write_api.write(bucket="LatencyStat", record=point, write_precision=WritePrecision.MS)

    def write_consumption_metrics(self, client_ip, consumption_data):
        for device, data in consumption_data.items():
            point = Point("consumption_metrics") \
                .tag("client", client_ip) \
                .tag("device", data['user']) \
                .field("rx-byte", data['rx-byte']) \
                .field("tx-byte", data['tx-byte'])
            self.write_api.write(bucket="UsrConsumptionStat", record=point, write_precision=WritePrecision.MS)