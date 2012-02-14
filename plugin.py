###
# Copyright (c) 2012, Henry Donnay
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
#   * Redistributions of source code must retain the above copyright notice,
#     this list of conditions, and the following disclaimer.
#   * Redistributions in binary form must reproduce the above copyright notice,
#     this list of conditions, and the following disclaimer in the
#     documentation and/or other materials provided with the distribution.
#   * Neither the name of the author of this software nor the name of
#     contributors to this software may be used to endorse or promote products
#     derived from this software without specific prior written consent.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED.  IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

###

import supybot.utils as utils
from supybot.commands import *
import supybot.plugins as plugins
import supybot.ircutils as ircutils
import supybot.callbacks as callbacks
import supybot.dbi as dbi

class nickRecord(dbi.Record):
    __fields__ = ['twitternick', 'ircnick']

class nickDB(plugins.DbiChannelDB):
    class DB(dbi.DB):
        Record = nickRecord
        def add(self, twitternick, ircnick):
            record = self.Record(twitternick=twitternick, ircnick=ircnick)
            super(self.__class__, self).add(record)
        def getTwitter(self, ircnick):
            for pair in super(self.__class__, self).list(self):
                if pair.ircnick is ircnick:
                    return pair.twitternick.strip()
        def list(self):
            return list(self)

NICKDB = plugins.DB('nick', {'flat': nickDB})

class gameRecord(dbi.Record):
    __fields__ = ['game', 'nicklist']

class gameDB(plugins.DbiChannelDB):
    class DB(dbi.DB):
        Record = gameRecord
        def add(self, game, nicklist):
            record = self.Record(game=game, nicklist=nicklist)
            super(self.__class__, self).add(record)
        def getUsers(self, game):
            for pair in super(self.__class__, self).list(self):
                if pair.game is game:
                    return pair.nicklist.split()
        def gameExists(self, game):
            for pair in super(self.__class__, self).list(self):
                if pair.game is game:
                    return True
            return False
        def list(self):
            return list(self)

GAMEDB = plugins.DB('game', {'flat': nickDB})

class Lebowski(callbacks.Plugin):
    """This plugin provides some cool things for users."""
    threaded = True

    def __init__(self, irc):
        self.__parent = super(Lebowski, self)
        self.__parent.__init__(irc)
        self.nickdb = NICKDB()
        self.gamedb = GAMEDB()

    def add(self, irc, msg, args, ircnick, twitternick):
        """<ircnick> <twitternick>

        Associate two nicks across services."""
        chan = msg.args[0]
        try:
            self.nickdb.add(chan, twitternick, ircnick)
        except:
            irc.reply("You dun goofed")
        else:
            irc.reply("Added association")
    add = wrap(add, ['nick', 'something'])

    def list(self, irc, msg, args):
        """takes no arguments

        List known associations."""
        chan = msg.args[0]
        irc.reply( "Known nicks:")
        for nick in self.nickdb.list(chan):
            irc.reply("    " + nick.ircnick.strip() + " -> " + nick.twitternick.strip())
    list = wrap(list)

    def funny(self, irc, msg, args):
        """takes no arguments

        Soothes your fragile ego."""
        irc.reply( "lololololol. That was quite funny." )
    funny = wrap(funny)

    def gameadd(self, irc, msg, args, game, ircnick):
        """<game> <ircnick>

        Adds the <ircnick> to the list for <game>."""
        if (self.gamedb.gameExists(game)):
            self.gamedb.add(game, self.gamedb.getUsers+" "+ircnick)
        else:
            self.gamedb.add(game, ircnick)
    gameadd = wrap(gameadd, ['something', 'something'])

    def hadoken(self, irc, msg, args):
        """takes no arguments

        Let everyone know that they should come get beat up by Guile."""
        users = self.gamedb.getUsers(chan, "SSFIVAE")
        twitternicks = []
        for nick in users:
            twitternicks.append(self.nickdb.getTwitter(nick))

        twitterstr = 'post HADOKEN! ' + " ".join(twitternicks)
        ircstring = 'MY FIGHT MONEY! ' + " ".join(users)

        irc.reply(ircstring)
        self.Proxy(irc.irc, msg, callbacks.tokenize(twitterstr))
    hadoken = wrap(hadoken)

Class = Lebowski


# vim:set shiftwidth=4 softtabstop=4 expandtab textwidth=79:
