# This file is placed in the Public Domain.


from ..objects import edit, keys, prt
from ..persist import last, write
from ..runtime import Cfg


def __dir__():
    return (
            "kcfg",
           )


__all__ = __dir__()


def kcfg(event):
    config = Cfg
    last(config)
    if not event.sets:
        event.reply(prt(
                        config,
                        keys(config)
                       )
                   )
    else: 
        edit(config, event.sets)
        write(config)
        event.reply('ok')
