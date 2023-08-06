# This file is placed in the Public Domain.


from ..command import Commands
from ..objects import keys


## COMMANDS


def cmd(event):
    event.reply(','.join(sorted(keys(Commands.modnames))))
