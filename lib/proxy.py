# Date: 12/28/2018
# Author: Mohamed
# Description: Proxy

import time


class Proxy(object):
    def __init__(self, ip: str, port: int) -> None:
        self.__ip = ip
        self.__port = port
        self.__total_used = 0
        self.__total_passed = 0
        self.__last_used = None

    @property
    def addr(self) -> dict:
        self.__total_used += 1
        self.__last_used = time.time()

        addr = f"{self.__ip}:{self.__port}"
        return {"http": f"http://{addr}", "https": f"http://{addr}"}

    def incr_success(self) -> None:
        """Incremented when proxy works"""
        self.__total_passed += 1

    def decr_usage(self) -> None:
        """Takes away usage data for this session"""
        self.__total_used = 0
        self.__total_passed = 0

    def info(self) -> dict:
        return {
            "ip": self.__ip,
            "port": self.__port,
            "last_used": self.__last_used,
            "total_used": self.__total_used,
            "total_passed": self.__total_passed,
        }
