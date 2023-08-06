# -*- coding: UTF-8 -*-
import logging

from pysenal.utils.logger import *


def test_get_logger():
    logger = get_logger('test_logger')
    assert logger.name == 'test_logger'


def test_log_time():
    class T(object):
        def __init__(self):
            self.logger = get_logger('test_logger', level=logging.INFO)

        @log_time(log_in_msg=True)
        def test(self):
            a = 1

        @log_time(log_result=True)
        def test1(self):
            return 10

    @log_time(log_in_msg=True)
    def test_time():
        a = 1

    assert T().test() is None
    assert T().test1() == 10
    assert test_time() is None
