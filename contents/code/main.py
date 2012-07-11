#
# Copyright (c) 2012, Henrik N. Jensen
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met: 
#
# 1. Redistributions of source code must retain the above copyright notice, this
#    list of conditions and the following disclaimer. 
# 2. Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution. 
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR
# ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
# ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#

from PyKDE4 import plasmascript
from PyKDE4.plasma import Plasma
from PyKDE4.kdeui import KIcon, KMessageBox
from random import choice
from string import ascii_letters, digits

#
# XXX: Generate random word
#
#
def random_generator(size=10):
    if size > 50:
        size = 50
    return ''.join(choice(ascii_letters + digits) for x in range(size))

#
# KRunner
#
class PasswordRunner(plasmascript.Runner):
 
    def init(self):
        self.addSyntax(Plasma.RunnerSyntax("rnd :q:", "Copy password to clipboard"))
 
    def match(self, context):
        
        # Password
        password = 0

        # Check if context is valid
        if not context.isValid():
            return
        
        data = context.query()
 
        # Match keyword!
        if not data.startsWith("rnd "):
             return
        
        # Length
        if data.length < 3:
            return

        # Trim size
        data = data[3:]
        data = data.trimmed()
        
        # Input validation
        try:
            password = random_generator(int(data))
        except ValueError:
            error = Plasma.QueryMatch(self.runner)
            error.setText("Random only accepts ints")
            error.setType(Plasma.QueryMatch.InformationalMatch)
            error.setIcon(KIcon("dialog-error"))
            context.addMatch(" ", error)
            return

        #
        # Plasma action, that sends data to krunner
        #
        m = Plasma.QueryMatch(self.runner)
        m.setText("Random: '%s'" % password)
        m.setData(password)
        m.setType(Plasma.QueryMatch.InformationalMatch)
        m.setIcon(KIcon("dialog-password"))
        context.addMatch(password, m)


    def run(self, context, match):
        # TODO:
        #  Close runner on match
        #
        pass

def CreateRunner(parent):
    return PasswordRunner(parent)
