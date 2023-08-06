# This file is placed in the Public Domain.
# pylint: disable=C0114,C0115,C0116,W0703


import inspect
import sys


from .errored import Errors
from .logging import Logging
from .message import Message
from .objects import Object, copy


def __dir__():
    return (
            'Commands',
           )


MODNAMES = {
            'cmd': 'nopaths.modules.cmd',
            'err': 'nopaths.modules.err',
            'flt': 'nopaths.modules.flt',
            'fnd': 'nopaths.modules.fnd',
            'cfg': 'nopaths.modules.irc',
            'dlt': 'nopaths.modules.irc',
            'met': 'nopaths.modules.irc',
            'mre': 'nopaths.modules.irc',
            'pwd': 'nopaths.modules.irc',
            'log': 'nopaths.modules.log',
            'mod': 'nopaths.modules.mod',
            'dpl': 'nopaths.modules.rss',
            'nme': 'nopaths.modules.rss',
            'rem': 'nopaths.modules.rss',
            'rss': 'nopaths.modules.rss',
            'sts': 'nopaths.modules.sts',
            'dne': 'nopaths.modules.tdo',
            'tdo': 'nopaths.modules.tdo',
            'thr': 'nopaths.modules.thr',
            'upt': 'nopaths.modules.upt',
            'ver': 'nopaths.modules.ver'
           }


class Commands(Object):

    cmds = Object()
    modnames = copy(Object(), MODNAMES)
    modules = None
    ondemand = True

    @staticmethod
    def add(cmd, func) -> None:
        setattr(Commands.cmds, cmd, func)
        setattr(Commands.modnames, cmd, func.__module__)

    @staticmethod
    def handle(evt) -> Message:
        evt.parse(evt.txt)
        func = getattr(Commands.cmds, evt.cmd, None)
        if Commands.ondemand and not func:
            modname = getattr(Commands.modnames, evt.cmd, None)
            if modname:
                if modname in sys.modules:
                    mod = sys.modules[modname]
                if not mod:
                    Logging.debug(f"load {modname}")
                    mod = getattr(
                                  Commands.modules,
                                  modname.split(".")[-1],
                                  None
                                 )
                func = getattr(mod, evt.cmd, None)
        if func:
            try:
                func(evt)
                evt.show()
            except Exception as ex:
                Errors.handle(ex)
        evt.ready()
        return evt

    @staticmethod
    def scan(mod) -> None:
        for _key, cmd in inspect.getmembers(mod, inspect.isfunction):
            if 'event' in cmd.__code__.co_varnames:
                Commands.add(cmd.__name__, cmd)
