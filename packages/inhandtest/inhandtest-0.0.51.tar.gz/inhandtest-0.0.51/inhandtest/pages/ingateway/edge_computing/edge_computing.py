# -*- coding: utf-8 -*-
# @Time    : 2023/5/25 15:33:58
# @Author  : Pane Li
# @File    : edge_computing.py
"""
edge_computing

"""
from inhandtest.pages.ingateway.edge_computing.python_edge_computing import PythonEdgeComputing, DockerManager


class EdgeComputing:

    def __init__(self, host: str, username: str, password: str, protocol='https',
                 port=443, model='IG902', language='en', page=None, locale: dict = None):
        self.python_edge_computing: PythonEdgeComputing = PythonEdgeComputing(host, username, password, protocol, port,
                                                                              model, language, page, locale)
        self.docker_manager: DockerManager = DockerManager(host, username, password, protocol, port, model, language,
                                                           page, locale)
