# This file is placed in the Public Domain.
# flake8: noqa: F401
# pylama:ignore=W0611


"""there are no paths modules


use an alias for easier typing::

    $ alias np="python3 -m nopaths"

list of commands::

    $ np cmd
    cmd,err,flt,sts,thr,upt

start a console::

    $ np -c
    >

start additional modules::

    $ np mod=<mod1,mod2> -c
    >

list of modules::

    $ np mod
    cmd,err,flt,fnd,irc,log,mod,rss,sts,tdo,thr,upt

start as daemon::

    $ np mod=cmd,irc,rss -d
    $

*irc*

    $ np cfg server=<server>
    $ np cfg channel=<channel>
    $ np cfg nick=<nick>

*sasl*

    $ np pwd <nsnick> <nspass>
    $ np cfg password=<frompwd>

*rss*

    $ np rss <url>
    $ np dpl <str_in_url> <i1,i2>
    $ np rem <str_in_url>
    $ np nme <str_in_url> <name>


**COMMANDS**

    cmd - commands
    cfg - irc configuration
    dlt - remove a user
    dpl - sets display items
    ftc - runs a fetching batch
    fnd - find objects
    flt - instances registered
    log - log some text
    mdl - genocide model
    met - add a user
    mre - displays cached output
    nck - changes nick on irc
    now - genocide stats
    pwd - sasl nickserv name/pass
    rem - removes a rss feed
    req - reconsider
    rss - add a feed
    slg - slogan
    thr - show the running threads
    tpc - genocide stats into topic

"""


__author__ = "No Paths <nopaths@proton.me>"


from . import cmd, err, flt, fnd, irc, log, mod, rss, sts, tdo
from . import thr, upt, ver


def __dir__():
    return (
            "cmd",
            "err",
            "flt",
            "fnd",
            "irc",
            "log",
            "mod",
            "rss",
            "sts",
            "tdo",
            "thr",
            "upt",
            'ver'
           )


__all__ = __dir__()
