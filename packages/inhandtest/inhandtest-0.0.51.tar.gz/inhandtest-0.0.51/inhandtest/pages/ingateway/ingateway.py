# -*- coding: utf-8 -*-
# @Time    : 2023/5/15 16:09:27
# @Author  : Pane Li
# @File    : ingateway.py
"""
ingateway

"""
from playwright.sync_api import Page
from inhandtest.base_page.base_page import BasePage
from inhandtest.pages.ingateway.edge_computing.edge_computing import EdgeComputing
from inhandtest.pages.ingateway.network.network import Network
from inhandtest.pages.ingateway.overview.overview import Overview
from inhandtest.pages.locale import in_setting
from inhandtest.telnet import Telnet


class InGateway(BasePage):

    def __init__(self, host: str, super_user: str, super_password: str, page: Page = None, model='IG902',
                 language='en', protocol='https', port=443, username='adm', password='123456', telnet=True):
        super().__init__(host, username, password, protocol, port, model, language, page, locale=in_setting)
        if telnet:
            self.telnet = Telnet(model, host, super_user, super_password)
        else:
            self.telnet = None
        if self.language == 'en':
            self.telnet.send_cli(command='language English', type_='user')
        else:
            self.telnet.send_cli(command='language Chinese', type_='user')
        self.login()
        self.overview = Overview(host, username, password, protocol, port, model, language, self.page,
                                 locale=self.locale)
        self.network: Network = Network(host, username, password, protocol, port, model, language, self.page,
                                        locale=self.locale)
        self.edge = EdgeComputing(host, username, password, protocol, port, model, language, self.page,
                                  locale=self.locale)


if __name__ == '__main__':
    import logging
    file_handler = logging.FileHandler('./log1.log')
    console_handler = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)
    logging.basicConfig(level=logging.DEBUG, handlers=[file_handler, console_handler])
    file_handler.setLevel(logging.DEBUG)
    console_handler.setLevel(logging.INFO)
    with InGateway('10.5.24.96', 'inhand', '64391099@inhand') as device:
        device.network.dhcp.config_dhcp(
            static_ip_setting=[('add', {"ip_address": '10.5.24.97', 'mac_address': '00:00:00:00:00:01'})],
            submit=True)
        device.page.wait_for_timeout(5 * 1000)
