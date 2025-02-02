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

from core.cli.badges import badges
from core.base.storage import local_storage

from utils.shell.pseudo_shell import pseudo_shell

class sessions:
    def __init__(self):
        self.badges = badges()
        self.local_storage = local_storage()
        
        self.pseudo_shell = pseudo_shell()

    def add_session(self, session_property, session_module, session_host, session_port, session_object):
        if not self.local_storage.get("sessions"):
            self.local_storage.set("sessions", dict())

        session_id = 0
        if session_property in self.local_storage.get("sessions").keys():
            sessions = self.local_storage.get("sessions")
            session_id = len(sessions[session_property])
            sessions[session_property][int(session_id)] = {
                'module': session_module,
                'host': session_host,
                'port': session_port,
                'object': session_object
            }
        else:
            sessions = {
                session_property: {
                    int(session_id): {
                        'module': session_module,
                        'host': session_host,
                        'port': session_port,
                        'object': session_object
                    }
                }
            }
        
        self.local_storage.update("sessions", sessions)
        return session_id
    
    def check_session_exist(self, session_property, session_id):
        sessions = self.local_storage.get("sessions")
        if sessions:
            if session_property in sessions.keys():
                if int(session_id) in sessions[session_property].keys():
                    return True
        return False
    
    def spawn_interactive_connection(self, session_property, session_id):
        sessions = self.local_storage.get("sessions")
        if self.check_session_exist(session_property, session_id):
            self.badges.output_process("Interacting with session " + str(session_id) + "...")
            self.badges.output_success("Interactive connection spawned!")
            self.badges.output_information("Type commands below.\n")

            sessions[session_property][int(session_id)]['object'].interact()
        else:
            self.badges.output_error("Invalid session given!")
    
    def spawn_pseudo_shell(self, session_property, session_id):
        sessions = self.local_storage.get("sessions")
        if self.check_session_exist(session_property, session_id):
            execute_method = sessions[session_property][int(session_id)]['object'].send_command
            self.pseudo_shell.spawn_pseudo_shell(session_property, execute_method)
        else:
            self.badges.output_error("Invalid session given!")
    
    def close_session(self, session_property, session_id):
        sessions = self.local_storage.get("sessions")
        if self.check_session_exist(session_property, session_id):
            try:
                sessions[session_property][int(session_id)]['object'].close()
                del sessions[session_property][int(session_id)]
                
                if not sessions[session_property]:
                    del sessions[session_property]
                self.local_storage.update("sessions", sessions)
            except Exception:
                self.badges.output_error("Failed to close session!")
        else:
            self.badges.output_error("Invalid session given!")

    def get_session(self, session_property, session_id):
        sessions = self.local_storage.get("sessions")
        if self.check_session_exist(session_property, session_id):
            return sessions[session_property][int(session_id)]['object']
        return None
