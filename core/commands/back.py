#!/usr/bin/env python3

#
# MIT License
#
# Copyright (c) 2020-2021 EntySec
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#

from core.lib.command import HatSploitCommand

from core.modules.modules import modules
from core.base.storage import local_storage

class HatSploitCommand(HatSploitCommand):
    modules = modules()
    local_storage = local_storage()
    
    details = {
        'Category': "module",
        'Name': "back",
        'Description': "Return to the previous module.",
        'Usage': "back",
        'MinArgs': 0
    }

    def run(self, argc, argv):
        if self.modules.check_current_module():
            self.local_storage.set("current_module_number", self.local_storage.get("current_module_number") - 1)
            self.local_storage.set("current_module", self.local_storage.get("current_module")[0:-1])
            if not self.local_storage.get("current_module"):
                self.local_storage.set("current_module_number", 0)
