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

import socketserver

from core.lib.module import HatSploitModule

from utils.tcp.tcp import tcp

from data.modules.auxiliary.multi.sniffer.user_agent_sniffer.core.handler import handler

class HatSploitModule(HatSploitModule):
    tcp = tcp()

    handler = handler

    details = {
        'Name': "User Agent Sniffer",
        'Module': "auxiliary/multi/sniffer/user_agent_sniffer",
        'Authors': [
            'enty8080'
        ],
        'Description': "Sniff User-Agent through URL.",
        'Dependencies': [
            ''
        ],
        'Comments': [
            ''
        ],
        'Risk': "medium"
    }

    options = {
        'LHOST': {
            'Description': "Local host.",
            'Value': tcp.get_local_host(),
            'Type': "ip",
            'Required': True
        },
        'LPORT': {
            'Description': "Local port.",
            'Value': 80,
            'Type': "port",
            'Required': True
        },
        'FOREVER': {
            'Description': "Start http server forever.",
            'Value': "no",
            'Type': "boolean",
            'Required': False
        }
    }

    def start_server(self, local_host, local_port, forever):
        try:
            httpd = socketserver.TCPServer((local_host, int(local_port)), self.handler)
            self.badges.output_process("Starting http server on port " + local_port + "...")
            if forever.lower() in ['yes', 'y']:
                while True:
                    self.badges.output_process("Listening for connections...")
                    httpd.handle_request()
            else:
                self.badges.output_process("Listening for connections...")
                httpd.handle_request()
        except Exception:
            self.badges.output_error("Failed to start http server on port " + local_port + "!")

    def run(self):
        local_host, local_port, forever = self.parser.parse_options(self.options)
        self.start_server(local_host, local_port, forever)
