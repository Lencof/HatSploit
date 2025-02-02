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

import random
import requests

from core.base.config import config

from requests.packages.urllib3.exceptions import InsecureRequestWarning

class http:
    def __init__(self):
        self.config = config()

        self.http_client = requests.request
        requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
    
    #
    # Functions to manipulate responses
    #
    
    def generate_fake_response(self, reason):
        fake_response = requests.models.Response()
        
        fake_response.code = ""
        fake_response.error_type = ""
        fake_response.reason = reason
        fake_response.status_code = 0
        fake_response.headers = dict()
        
        return fake_response
    
    #
    # Functions to manipulate User-Agent
    #
    
    def new_user_agent(self):
        file = open(self.config.path_config['base_paths']['data_path'] + 'utils/http/http/user_agents.txt')
        user_agents = list(filter(None, file.read().split('\n')))
        
        file.close()
        
        number = random.randint(0, len(user_agents))
        return user_agents[number]
    
    def get_user_agent_header(self):
        user_agent = self.new_user_agent()
        headers = {
            'User-Agent': user_agent
        }
        
        return headers
    
    #
    # Functions to check URL stability
    #
    
    def check_url_access(self, url, path="/", ssl=False, user_agent=True, timeout=10):
        response = self.http_request("HEAD", url, path, None, ssl, user_agent, timeout)
        
        if response.status_code != 0:
            return True
        
        if "aborted" in response.reason:
            response = self.http_request("GET", url, path, None, ssl, user_agent, timeout)
            
            if response.status_code != 0:
                return True
        return False
    
    #
    # HTTP requests
    #

    def http_request(self, method, url, path, data=None, ssl=False, user_agent=True, timeout=10):
        if self.get_url_port(url) == 443:
            url = self.normalize_url(url, True)
        else:
            url = self.normalize_url(url, ssl)
        url = self.add_path_to_url(url, path)
        
        headers = None
        if user_agent:
            headers = self.get_user_agent_header()
        
        try:
            response = self.http_client(method=method, url=url, data=data, headers=headers, timeout=timeout, verify=False, allow_redirects=False)
        except Exception as e:
            return self.generate_fake_response(str(e))
        return response
    
    #
    # Functions to parse host and port
    #
    
    def format_host_and_port(self, host, port):
        return host + ':' + str(port)
    
    #
    # Functions to parse URL
    #
    
    def craft_url(self, host, port, ssl=False):
        url = host + ':' + port
        return self.normalize_url(url, ssl)
    
    def get_url_port(self, url):
        url = self.strip_scheme(url, True).split(':')
        if len(url) == 2:
            return int(url.split(':')[1])
        return None
        
    def get_url_host(self, url):
        url = self.strip_scheme(url, True).split(':')
        if len(url) == 2:
            return url.split(':')[0]
        return None
    
    def strip_scheme(self, url, strip_path=False):
        url = url.replace('http://', '', 1)
        url = url.replace('https://', '', 1)
        if strip_path:
            url = url.split('/')[0]
        return url
    
    def add_http_to_url(self, url):
        url = self.strip_scheme(url)
        url = 'http://' + url
        return url
    
    def add_https_to_url(self, url):
        url = self.strip_scheme(url)
        url = 'https://' + url
        return url
    
    def add_path_to_url(self, url, path):
        if not path.startswith('/'):
            path = '/' + path
            
        if url.endswith('/'):
            path = path[1:]
            
        return url + path
    
    def normalize_url(self, url, ssl=False):
        if ssl:
            return self.add_https_to_url(url)
        return self.add_http_to_url(url)
