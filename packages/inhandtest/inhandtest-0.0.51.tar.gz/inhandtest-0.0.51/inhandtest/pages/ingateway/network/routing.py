# -*- coding: utf-8 -*-
# @Time    : 2023/5/23 14:19:02
# @Author  : Pane Li
# @File    : routing.py
"""
routing

"""
import allure
from inhandtest.tools import loop_inspector

from inhandtest.base_page.base_page import BasePage
from inhandtest.pages.ingateway.locators import IgLocators


class RoutingStatus(BasePage, IgLocators):

    def __init__(self, host: str, username: str, password: str, protocol='https',
                 port=443, model='IG902', language='en', page=None, locale: dict = None):
        super().__init__(host, username, password, protocol, port, model, language, page, locale=locale)
        IgLocators.__init__(self, page, locale)

    @allure.step('断言Routing Status状态')
    @loop_inspector('routing_status')
    def assert_routing_status(self, routing_type='all', **kwargs):
        """
        :param routing_type: 'all', 'connected_routing', 'static_routing', 'ospf', 'bgp', 'rip'
        :param kwargs:
               destination: 0.0.0.0
               netmask: 0.0.0.0
               gateway:
               interface: Gigabitethernet 0/1, Gigabitethernet 0/2, Bridge 1, Loopback 1
               distance: 255/0
               time:
               exist: True,False ex: exist=True # True:存在,False:不存在， 默认查询存在
        """

        if kwargs:
            self.access_menu('network.routing.routing_status')
            self.agg_in(self.network_locators.routing_locators, {'routing_type': routing_type}),
            exist = True if kwargs.get('exist') is None else kwargs.pop('exist')
            value = ''
            for cl_ in ('destination', 'netmask', 'interface', 'distance', 'time'):
                if kwargs.get(cl_):
                    value = value + kwargs.get(cl_)
                else:
                    value = value + '.*'
            if exist:
                return \
                    self.table_tr(self.network_locators.routing_table_locators, [('exist', value)], 'routing status')[0]
            else:
                return not \
                    self.table_tr(self.network_locators.routing_table_locators, [('exist', value)], 'routing status')[0]
        else:
            return True


class StaticRouting(BasePage, IgLocators):
    def __init__(self, host: str, username: str, password: str, protocol='https',
                 port=443, model='IG902', language='en', page=None, locale: dict = None):
        super().__init__(host, username, password, protocol, port, model, language, page, locale=locale)
        IgLocators.__init__(self, page, locale)

    @allure.step('配置Static Routing')
    def config_static_routing(self, **kwargs):
        """

        :param kwargs:
                routing: [($action, **kwarg)] ex: [('delete_all', )],
                    [('delete', '0.0.0.0Gigabitethernet 0/1')]
                    [('add', {'destination': '0.0.0.0', 'netmask': '0.0.0.0', 'interface': 'Gigabitethernet 0/1', 'gateway': '10.5.17.254','distance': 255, 'track_id': 1})]
                        add parameter:
                            destination:
                            netmask:
                            interface:
                            gateway:
                            distance:
                            track_id:
                            errors_text: str or list
                            cancel: True,False ex: cancel=True
                    [('edit', '0.0.0.0Gigabitethernet 0/1', {'destination': '1.1.1.1'})]
                    [('add', {'destination': '0.0.0.0', 'netmask': '10.5.24.97', 'interface': 'Gigabitethernet 0/1', 'is_exists': '10.5.24.97Gigabitethernet 0/1'})] 如果存在则不添加
                    [('edit', '10.5.24.97Gigabitethernet 0/1', {'destination': '1.1.1.1'})]
                submit: True,False ex: submit=True
                errors_text: 'ip_address_conflict' ex: errors_text='ip_address_conflict'
                success_tip: True ex: success_tip=True 提交后需要验证成功的提示框
                reset: True ex: reset=True
        :return:
        """
        self.access_menu('network.routing.static routing')
        if kwargs.get('success_tip'):
            kwargs.update({'success_tip': 'submit_success'})
        self.agg_in(self.network_locators.static_routing_locators, kwargs)
