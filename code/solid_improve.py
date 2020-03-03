class Const(object):

    def __setattr__(self, key, value):
        if key in self.__dict__:
            raise Exception('Change invalid')
        if not key.isupper():
            raise Exception('Change invalid')

        self.__dict__[key] = value

import sys

sys.modules[__name__] = Const()

