from collections import defaultdict
import json
import time
from browsermobproxy import Server
from selenium import webdriver
import getpass
user = getpass.getuser()
path = "/home/"+user+"/Downloads/browsermob-proxy-2.1.2/bin/browsermob-proxy"

class HTTPTracing(object):
    """create HTTP archive file"""

    def __init__(self, url):
        """initial setup"""
        self.browser_mob = path
        self.server = self.driver = self.proxy = None
        self.traffic_for_domain = []
        self.url = url
    def __start_server(self):
        """prepare and start server"""
        self.server = Server(self.browser_mob)
        self.server.start()
        self.proxy = self.server.create_proxy()

    def __enter__(self):
        self.__start_server()
        self.driver = webdriver.Firefox(proxy=self.proxy.selenium_proxy())
        self.driver.implicitly_wait(10)
        self.driver.get(self.url)
        self.proxy.new_har(self.url,
            options={'captureHeaders':True, 'captureCookies':True})

        return self

    @property
    def entries(self):
        return self.proxy.har["log"]["entries"]


    def wait_change_entry(self, url, duration=2):
        num_loops = duration/0.1
        count = 0
        har = self.proxy.har
        entry = har["log"]["entries"]
        while count <= num_loops and not self.url_in_entry(url):
            time.sleep(0.1)
            count += 1
        return self.f_entries

    def url_in_entry(self, base_url):
        self.f_entries = list(filter(lambda x: base_url in x["request"]["url"],
                                     self.entries))
        return self.f_entries

    def __exit__(self, exc_type, exc_val, exc_tb):
        """stop server and driver"""
        self.server.stop()
        self.driver.quit()
