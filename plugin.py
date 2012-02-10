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
        def nicks(self):
            return list(self)

NICKDB = plugins.DB('nick', {'flat': nickDB})

class Lebowski(callbacks.Plugin):
    """This plugin provides some cool things for users."""
    threaded = True

    def __init__(self, irc):
        self.__parent = super(Lebowski, self)
        self.__parent.__init__(irc)
        self.db = NICKDB()

    def add(self, irc, msg, args, ircnick, twitternick):
        """<ircnick> <twitternick>

        Associate two nicks across services."""
        self.db.add(twitternick, ircnick)
    add = wrap(add, ['text', 'text'])

    def list(self, irc, msg, args):
        """takes no arguments

        List known associations."""
        irc.reply( ", ".join(self.db.nicks))
    list = wrap(list)

    def hadoken(self, irc, msg, args):
        """takes no arguments

        Let everyone know that they should come get beat up by Guile."""
        users = {'Newfie':'@HWHQNewfie', 'C4':'@ceephour', 'that_guy':'@nliadm'}
        twitterstr = 'post HADOKEN! ' + " ".join(users.values())
        ircstring = 'MY FIGHT MONEY! ' + " ".join(users.keys())

        irc.reply(ircstring)
        self.Proxy(irc.irc, msg, callbacks.tokenize(twitterstr))
    hadoken = wrap(hadoken)

Class = Lebowski


# vim:set shiftwidth=4 softtabstop=4 expandtab textwidth=79:
