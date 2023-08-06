class IPCityClient:
    def __init__(self, union):
        self.__union = union

    def search(self, ip: str):
        url = "{}/ius/ip_city/".format(self.__union.api_domain)
        data = {"ip": ip}
        return self.__union.web.post(url, json=data).json()
