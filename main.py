import asyncio
import os
import time
from apscheduler.schedulers.background import BackgroundScheduler
from client import Client
from metrics import Metrics
from influxDBManager import InfluxDBWriter

# Define clients
clients = [
    Client("172.16.255.1", "Gb@m1kr0ut3r", "xxx", "cert_export_SSLTESTv2.crt"),
    Client("10.0.0.2", "Gb@m1kr0ut3r", "xxx", "cert_export_SSLTESTv2.crt")
]

# InfluxDB configuration
influxdb_writer = InfluxDBWriter(url=os.getenv("INFLUXDB_URL"), token = os.getenv("INFLUXDB_TOKEN"), org=os.getenv("INFLUXDB_ORG"))

async def collect_metrics(client):
    metrics_collector = Metrics(client)
    metrics_data = await asyncio.gather(
        metrics_collector.interface_collect(),
        metrics_collector.latency_check(),
        metrics_collector.consumption_collect()
    )

    for data in metrics_data:
        if 'interface_metrics' in data:
            influxdb_writer.write_interface_metrics(client.ip, data['interface_metrics'])
        elif 'latency_metrics' in data:
            influxdb_writer.write_latency_metrics(client.ip, data['latency_metrics'])
        elif 'consumption_metrics' in data:
            influxdb_writer.write_consumption_metrics(client.ip, data['consumption_metrics'])

async def collect_metrics_for_all_clients():
    # Run collection for all clients concurrently
    await asyncio.gather(*[collect_metrics(client) for client in clients])

def test():
    start = time.time()
    asyncio.run(collect_metrics_for_all_clients())
    end = time.time()
    print(f"Time taken: {end - start} seconds")

def schedule_data_collection():
    scheduler = BackgroundScheduler()
    scheduler.add_job(test, 'interval', seconds=5)
    scheduler.start()

    try:
        while True:
            time.sleep(0.1)
    except KeyboardInterrupt:
        scheduler.shutdown()

if __name__ == '__main__':
    schedule_data_collection()