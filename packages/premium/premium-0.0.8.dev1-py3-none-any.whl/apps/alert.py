#!/usr/bin/env python
import random, requests
from collections import defaultdict
from functools import reduce
import codefast as cf


class Bark(object):
    @classmethod
    def alert(cls, title: str, message: str) -> bool:
        host = 'http://ddot.fun:8080/tcimavY6omAS9dzL5zZVmZ'
        ins = 'https://s3.bmp.ovh/imgs/2022/04/08/2b5acc67a703e510.jpeg'
        host = f'{host}/{title}/{message}?icon={ins}'
        host = host.replace(' ', '%20')
        cf.info('alert', host)
        requests.get(host)
        return True