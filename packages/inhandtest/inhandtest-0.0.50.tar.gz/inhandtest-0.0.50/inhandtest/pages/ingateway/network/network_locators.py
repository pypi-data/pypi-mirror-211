# -*- coding: utf-8 -*-
# @Time    : 2023/5/17 13:13:22
# @Author  : Pane Li
# @File    : network_locators.py
"""
network_locators

"""
from inhandtest.pages.ingateway.network.acl_locators import AclLocators
from inhandtest.pages.ingateway.network.bridge_locators import BridgeLocators
from inhandtest.pages.ingateway.network.cellular_locators import CellularLocators
from inhandtest.pages.ingateway.network.dhcp_locators import DhcpLocators
from inhandtest.pages.ingateway.network.dns_locators import DnsLocators
from inhandtest.pages.ingateway.network.ethernet_locators import EthernetLocators
from inhandtest.pages.ingateway.network.gps_locators import GpsLocators
from inhandtest.pages.ingateway.network.host_list_locators import HostListLocators
from inhandtest.pages.ingateway.network.l2tp_locators import L2tpLocators
from inhandtest.pages.ingateway.network.lan_locators import LanLocators
from inhandtest.pages.ingateway.network.loopback_locators import LoopbackLocators
from inhandtest.pages.ingateway.network.nat_locators import NatLocators
from inhandtest.pages.ingateway.network.routing_status_locators import RoutingStatusLocators
from inhandtest.pages.ingateway.network.static_routing_locators import StaticRoutingLocators
from inhandtest.pages.ingateway.network.wan_locators import WanLocators
from inhandtest.pages.ingateway.network.wlan_locators import WlanLocators


class NetworkLocators(EthernetLocators, CellularLocators, BridgeLocators, WlanLocators, WanLocators, LanLocators,
                      LoopbackLocators, DhcpLocators, DnsLocators, GpsLocators, HostListLocators,
                      RoutingStatusLocators, StaticRoutingLocators, AclLocators, NatLocators, L2tpLocators):
    pass
