from incv_client.ius.ip_city import IPCityClient


class IUSClient:
    def __init__(self, union):
        self.__union = union

    @property
    def ip_city(self):
        return IPCityClient(self.__union)
