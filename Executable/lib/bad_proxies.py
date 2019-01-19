# Date: 12/29/2018
# Author: Mohamed
# Description: Manages bad proxies

from .const import max_bad_proxies


class BadProxies(object):

    def __init__(self):
        self.proxies = []
    
    def __contains__(self, proxy):
        for _proxy in self.proxies:
            if _proxy.ip == proxy.ip and _proxy.port == proxy.port:
                return True 
        return False 

    def append(self, proxy):
        if len(self.proxies) >= max_bad_proxies:
            self.proxies.pop(0)
            
        self.proxies.append(proxy)

