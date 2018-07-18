import hashlib
import inspect
import logging
from urllib.parse import urlparse, parse_qsl, urlencode, urlunparse

import gevent

def spawn(func,*args,**kwargs):
    """
    加入协称
    :param func:
    :param args:
    :param kwargs:
    :return:
    """
    return gevent.spawn(func,*args,**kwargs)


def get_logger(name):
    default_logger = logging.getLogger(name)
    default_logger.setLevel(logging.DEBUG)
    stream = logging.StreamHandler()
    stream.setLevel(logging.DEBUG)
    formatter = logging.Formatter("[%(levelname)s] %(asctime)s - %(message)s")
    stream.setFormatter(formatter)
    default_logger.addHandler(stream)
    return default_logger

logger = get_logger("myLogger")


def request_fingerprint(request):
    scheme, netloc, path, params, query, fragment = urlparse(request.url)
    #处理一下 把参数位置不一样的哈希一下
    keyvals = parse_qsl(query)
    keyvals.sort()
    query = urlencode(keyvals)
    canonicalize_url = urlunparse((
        scheme, netloc.lower(), path, params, query, fragment)
    )
    fpr = hashlib.sha1()
    fpr.update(canonicalize_url)
    return fpr.hexdigest()

def iter_children_classes(values,clazz):
    """
    判断是不是类，或者是不是子类，不能是DownloaderMiddleWare
    :param values:
    :param clazz:
    :return:
    """
    for obj in values:
        if inspect.isclass(obj) and issubclass(obj,clazz) and obj is not clazz:
            yield obj

def call_func(func,errback = None,callback = None,*args,**kwargs):
    """

    :param func:
    :param errback:
    :param callback:
    :param args:
    :param kwargs:
    :return:
    """
    try:
        result = func(*args,**kwargs)
    except Exception as exc:
        if errback:
            errback(exc)
    else:
        if callback:
            result = callback(result)
        return  result