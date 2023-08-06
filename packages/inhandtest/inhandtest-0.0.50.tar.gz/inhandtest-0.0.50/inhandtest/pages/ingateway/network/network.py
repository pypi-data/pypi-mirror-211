# -*- coding: utf-8 -*-
# @Time    : 2023/5/17 13:23:17
# @Author  : Pane Li
# @File    : network.py
"""
network

"""
from inhandtest.pages.ingateway.network.firewall import Acl, Nat
from inhandtest.pages.ingateway.network.network_interface import Cellular, Ethernet, Bridge, Lan, Wan, Wlan, Loopback
from inhandtest.pages.ingateway.network.network_services import Dhcp, Dns, Gps, HostList
from inhandtest.pages.ingateway.network.routing import RoutingStatus, StaticRouting
from inhandtest.pages.ingateway.network.vpn import Vpn


class Network:

    def __init__(self, host: str, username: str, password: str, protocol='https',
                 port=443, model='IG902', language='en', page=None, locale: dict = None):
        self.ethernet: Ethernet = Ethernet(host, username, password, protocol, port, model, language, page, locale)
        self.cellular: Cellular = Cellular(host, username, password, protocol, port, model, language, page, locale)
        self.bridge: Bridge = Bridge(host, username, password, protocol, port, model, language, page, locale)
        self.wlan: Wlan = Wlan(host, username, password, protocol, port, model, language, page, locale)
        self.wan: Wan = Wan(host, username, password, protocol, port, model, language, page, locale)
        self.lan: Lan = Lan(host, username, password, protocol, port, model, language, page, locale)
        self.loopback: Loopback = Loopback(host, username, password, protocol, port, model, language, page, locale)
        self.dhcp: Dhcp = Dhcp(host, username, password, protocol, port, model, language, page, locale)
        self.dns: Dns = Dns(host, username, password, protocol, port, model, language, page, locale)
        self.gps: Gps = Gps(host, username, password, protocol, port, model, language, page, locale)
        self.host_list: HostList = HostList(host, username, password, protocol, port, model, language, page, locale)
        self.routing_status: RoutingStatus = RoutingStatus(host, username, password, protocol, port, model, language,
                                                           page, locale)
        self.static_routing: StaticRouting = StaticRouting(host, username, password, protocol, port, model, language,
                                                           page, locale)
        self.acl: Acl = Acl(host, username, password, protocol, port, model, language, page, locale)
        self.nat: Nat = Nat(host, username, password, protocol, port, model, language, page, locale)
        self.vpn: Vpn = Vpn(host, username, password, protocol, port, model, language, page, locale)
