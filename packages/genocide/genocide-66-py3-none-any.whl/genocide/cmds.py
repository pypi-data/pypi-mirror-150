# This file is placed in the Public Domain.


"commands"


import threading
import time


from hdl import Bus, Commands, starttime
from irc import Config
from obj import Class, Db, Object, edit, find, fntime, format, get, last, save, update
from rpt import elapsed
from rss import Fetcher, Rss
from thr import getname
from usr import User


class Log(Object):

    def __init__(self):
        super().__init__()
        self.txt = ""


Class.add(Log)


def cmd(event):
    event.reply(",".join(sorted(Commands.cmd)))


def dlt(event):
    if not event.args:
        event.reply("dlt <username>")
        return
    selector = {"user": event.args[0]}
    for _fn, o in find("user", selector):
        o._deleted = True
        save(o)
        event.reply("ok")
        break


def dpl(event):
    if len(event.args) < 2:
        event.reply("dpl <stringinurl> <item1,item2>")
        return
    db = Db()
    setter = {"display_list": event.args[1]}
    names = Class.full("rss")
    if names:
        _fn, o = db.lastmatch(names[0], {"rss": event.args[0]})
        if o:
            edit(o, setter)
            save(o)
            event.reply("ok")


def flt(event):
    try:
        index = int(event.args[0])
        event.reply(Bus.objs[index])
        return
    except (KeyError, TypeError, IndexError, ValueError):
        pass
    event.reply(" | ".join([getname(o) for o in Bus.objs]))


def fnd(event):
    if not event.args:
        db = Db()
        res = ",".join(
            sorted({x.split(".")[-1].lower() for x in db.types()}))
        if res:
            event.reply(res)
        else:
            event.reply("no types yet.")
        return
    bot = event.bot()
    otype = event.args[0]
    res = list(find(otype))
    if bot.cache:
        if len(res) > 3:
            bot.extend(event.channel, [x[1].txt for x in res])
            bot.say(event.channel, "%s left in cache, use !mre to show more" % bot.cache.size())
            return
    nr = 0
    for _fn, o in res:
        txt = "%s %s %s" % (str(nr), format(o), elapsed(time.time()-fntime(_fn)))
        nr += 1
        event.reply(txt)
    if not nr:
        event.reply("no result")


def ftc(event):
    res = []
    thrs = []
    fetcher = Fetcher()
    fetcher.start(False)
    thrs = fetcher.run()
    for t in thrs:
        res.append(t.join())
    if res:
        event.reply(",".join([str(x) for x in res]))
        return


def met(event):
    if not event.args:
        event.reply("met <userhost>")
        return
    user = User()
    user.user = event.rest
    user.perms = ["USER"]
    save(user)
    event.reply("ok")


def log(event):
    if not event.rest:
        event.reply("log <txt>")
        return
    o = Log()
    o.txt = event.rest
    save(o)
    event.reply("ok")


def nme(event):
    if len(event.args) != 2:
        event.reply("name <stringinurl> <name>")
        return
    selector = {"rss": event.args[0]}
    nr = 0
    got = []
    for _fn, o in find("rss", selector):
        nr += 1
        o.name = event.args[1]
        got.append(o)
    for o in got:
        save(o)
    event.reply("ok")


def rem(event):
    if not event.args:
        event.reply("rem <stringinurl>")
        return
    selector = {"rss": event.args[0]}
    nr = 0
    got = []
    for _fn, o in find("rss", selector):
        nr += 1
        o._deleted = True
        got.append(o)
    for o in got:
        save(o)
    event.reply("ok")


def rss(event):
    if not event.args:
        event.reply("rss <url>")
        return
    url = event.args[0]
    if "http" not in url:
        event.reply("i need an url")
        return
    res = list(find("rss", {"rss": url}))
    if res:
        return
    o = Rss()
    o.rss = event.args[0]
    save(o)
    event.reply("ok")


def thr(event):
    result = []
    for t in sorted(threading.enumerate(), key=lambda x: x.getName()):
        if str(t).startswith("<_"):
            continue
        o = Object()
        update(o, vars(t))
        if get(o, "sleep", None):
            up = o.sleep - int(time.time() - o.state.latest)
        else:
            up = int(time.time() - starttime)
        result.append((up, t.getName()))
    res = []
    for up, txt in sorted(result, key=lambda x: x[0]):
        res.append("%s (%s)" % (txt, elapsed(up)))
    if res:
        event.reply(" ".join(res))
