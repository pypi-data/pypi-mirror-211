# This file is placed in the Public Domain.


from .utility import doskip, spl


def __dir__():
    return (
            'Logging',
           )


class Logging:

    skip = 'PING,PONG,PRIVMSG'
    verbose = False

    @staticmethod
    def debug(txt) -> None:
        if Logging.verbose and not doskip(txt, Logging.skip):
            Logging.raw(txt)

    @staticmethod
    def raw(txt) -> None:
        pass
