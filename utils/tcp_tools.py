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

import time
import socket
import telnetlib

from core.badges import badges
from core.exceptions import exceptions

class tcp_tools:
    def __init__(self):
        self.badges = badges()
        self.exceptions = exceptions()
        
        self.client = None

    #
    # Functions to connect or disconnect
    #
        
    def connect(self, client):
        self.client = telnetlib.Telnet()
        self.client.sock = client
        
    def disconnect(self):
        self.client.close()
        
    #
    # Functions to send and recv from client and to client
    #
    
    def send(self, buffer):
        if self.client:
            self.client.write(buffer)
            
    def recv(self):
        if self.client:
            time.sleep(0.1)
            output = self.client.read_very_eager()
            
            return output
        return None
        
    #
    # Functions to send system commands to client
    #

    def send_command(self, command, wait=False):
        if self.client:
            buffer = command.encode()
            self.send(buffer)
            
            if wait:
                output = self.client.sock.recv(1024)
                _ = self.recv().decode().strip()
                output = output.decode().strip()
            else:
                output = self.recv().decode()
                output = output.strip()
            
            return output
        return None
        
    #
    # Functions to manipulate 
    #
        
    def start_server(self, local_host, local_port):
        self.badges.output_process("Binding to " + local_host + ":" + local_port + "...")
        try:
            server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            server.bind((local_host, int(local_port)))
            server.listen(1)
        except Exception:
            self.badges.output_error("Failed to bind to " + local_host + ":" + local_port + "!")
            raise self.exceptions.GlobalException
        return server
