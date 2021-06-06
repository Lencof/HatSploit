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

from core.lib.module import Module
from utils.tcp import TCPClient


class HatSploitModule(Module, TCPClient):
    details = {
        'Name': "ADB Installation Checker",
        'Module': "auxiliary/android/checker/check_adb_installation",
        'Authors': [
            'Ivan Nikolsky (enty8080)'
        ],
        'Description': "Check if remote Android device has ADB installation.",
        'Comments': [
            ''
        ],
        'Platform': "android",
        'Risk': "low"
    }

    options = {
        'RHOST': {
            'Description': "Remote host.",
            'Value': None,
            'Type': "ip",
            'Required': True
        }
    }

    def run(self):
        remote_host = self.parse_options(self.options)

        self.output_process(f"Checking {remote_host}...")
        if self.check_tcp_port(remote_host, 5555):
            self.output_success("Target device may has ADB installation!")
        else:
            self.output_warning("Looks like target device has no ADB installation.")
