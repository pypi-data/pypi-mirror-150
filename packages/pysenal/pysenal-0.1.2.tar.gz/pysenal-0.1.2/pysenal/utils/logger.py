# -*- coding: UTF-8 -*-
import sys
import time
import logging


def get_logger(name, handler=logging.StreamHandler(sys.stderr), level=logging.DEBUG):
    """
    encapsulate get logger operation
    :param name: logger name
    :param handler: logger handler, default is stderr
    :param level: logger level, default is debug
    :return: logger
    """
    logger = logging.getLogger(name)
    handler.setFormatter(logging.Formatter('[%(asctime)s] [{}] %(message)s'.format(name)))
    handler.setLevel(level)
    logger.addHandler(handler)
    logger.setLevel(level)
    return logger


def log_time(logger=None, log_result=False, log_in_msg=False, request_stage='during'):
    """
    func used this decorator must satisfy following condition
    1. first parameter is dict, indicate the query instance with query_id and start_time
    2. If log_result is True, logger will print str result or key `log` value of dict result.
        Result in other data type will raise exception.
    :param logger: python logger object,
    :param log_result: whether log func return value
    :param log_in_msg: whether log time in msg
    :param request_stage: request stage, default is during
    :return:
    """
    if logger is None:
        logger = get_logger('default logger')

    def log_time_func(f):
        new_logger = logger

        def wrap(*args, **kwargs):
            if args and not isinstance(args[0], dict):
                if hasattr(args[0], 'logger'):
                    logger = args[0].logger
                else:
                    logger = new_logger
            else:
                logger = new_logger

            name = f.__name__

            start = time.time()
            ret = f(*args, **kwargs)
            step_time = time.time() - start
            step_time *= 1000

            info = {'_funcName': name,
                    'request_stage': request_stage,
                    'step_time': '{:.0f}ms'.format(step_time)}

            if log_in_msg:
                ret_str_tmpl = '[func_name:{}] [step_time:{}] [request_stage:{}]'
                ret_str = ret_str_tmpl.format(name, '{:.0f}ms'.format(step_time), request_stage)
            else:
                ret_str = ''

            if log_result:
                ret_str += ' ' + str(ret)
                
            ret_str = ret_str.strip()
            logger.info(ret_str, extra=info)
            return ret

        return wrap

    return log_time_func
