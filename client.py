import aiohttp
import ssl

class Client:
    def __init__(self, ip, username, password, cert):
        self.ip = ip
        self.auth = aiohttp.BasicAuth(username, password)
        self.cert = cert

    async def net_query(self, query):
        ssl_context = ssl.create_default_context()
        ssl_context.check_hostname = False
        ssl_context.verify_mode = ssl.CERT_NONE
        async with aiohttp.ClientSession(auth=self.auth) as session:
            query = query.replace(' ', '/')
            url = f'https://{self.ip}/rest/{query}'
            async with session.get(url, ssl=ssl_context) as response:
                data = await response.json()
                return data

    async def net_console_cmd(self, cmd, json_data):
        ssl_context = ssl.create_default_context()
        ssl_context.check_hostname = False
        ssl_context.verify_mode = ssl.CERT_NONE

        headers = {
            'Content-type': 'application/json',
            'Accept': 'application/json'
        }
        async with aiohttp.ClientSession(auth=self.auth) as session:
            url = f'https://{self.ip}/rest/{cmd}'
            async with session.post(url, data=json_data, headers=headers, ssl=ssl_context) as response:
                data = await response.json()
                return data