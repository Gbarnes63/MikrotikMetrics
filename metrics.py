import time
import urllib3
import asyncio

class Metrics:
    def __init__(self, client):
        self.client = client

    async def latency_check(self):
        print(f'Collecting latency stats for {self.client.ip}')
        ping_targets = [
            {'name': 'Google', 'address': '8.8.8.8'},
            {'name': 'Cloudflare', 'address': '1.1.1.1'},
            {'name': 'Facebook', 'address': 'facebook.com'},
            {'name': 'Quad9', 'address': '9.9.9.9'},
            {'name': 'MyDigitalOcean', 'address': '10.0.20.1'},
            {'name': 'Webmasters-DNS', 'address': '196.10.148.37'},
            {'name': 'Cisco Primary DNS', 'address': '208.67.222.222'},
            {'name': 'Cisco Secondary DNS', 'address': '208.67.220.220'}
        ]

        latency_dict = {}

        try:
            for target in ping_targets:
                ping_data = await self.client.net_console_cmd('ping', f'{{"address":"{target["address"]}","count":"1"}}')
                ping_result = ping_data[0]

                if 'packet-loss' not in ping_result:
                    print(f"Error: 'packet-loss' key not found in {ping_result}")
                    continue
                if ping_result.get('packet-loss') == '100':
                    pass
                else:
                    latency = float(f"{ping_result['time'].split('ms')[0]}.{ping_result['time'].split('ms')[1][:-2]}")
                    latency_dict[target['name']] = latency

            return {'latency_metrics': latency_dict}

        except (urllib3.exceptions.MaxRetryError, ConnectionError):
            print('Connection error during ping request')
            time.sleep(1.5)
        except Exception as err:
            print('Caught unknown error while querying MikroTik for latency data:', err)
            time.sleep(1.5)

    async def interface_collect(self):
        interface_data = {}
        print(f'Collecting interface stats for {self.client.ip}')

        try:
            for data in await self.client.net_query('interface'):
                interface_name = data['name']
                rx_byte = data['rx-byte']
                tx_byte = data["tx-byte"]

                interface_data[interface_name] = {
                    "interface": interface_name,
                    "rx-byte": float(rx_byte),
                    "tx-byte": float(tx_byte) * -1
                }

            return {'interface_metrics': interface_data}

        except Exception as err:
            print('Caught unknown error while querying MikroTik for interface data:', err)
            time.sleep(1.5)

    async def consumption_collect(self):
        consumption_dict = {}
        print(f'Collecting data consumption stats for {self.client.ip}')

        try:
            for data in await self.client.net_query('ip kid-control device'):
                rx_byte = data['bytes-down']
                tx_byte = data["bytes-up"]

                device_name = data['name'] if data['name'] else data['ip-address']
                consumption_dict[device_name] = {
                    "user": device_name,
                    "rx-byte": float(rx_byte),
                    "tx-byte": float(tx_byte) * -1
                }

            return {'consumption_metrics': consumption_dict}

        except Exception as err:
            print('Caught unknown error while querying MikroTik for consumption data:', err)
            time.sleep(1.5)