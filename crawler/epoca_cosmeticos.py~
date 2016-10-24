from .network_traffic import HTTPTracing
import crawler
from lxml import html
import requests
import csv
class EpocaCosmeticos(object):

    BUTTON_LOAD = "//span[text()='MOSTRAR MAIS PRODUTOS']"
    AJAX_PAGINATION = "http://www.epocacosmeticos.com.br/buscapagina?"
    ITEMS_LINKS = "//a[@class='productImage']/@href"
    def __init__(self, filename):
        self.csvfile = open(filename, "w")
        self.writer = csv.writer(self.csvfile)
    
    def crawl(self, url):
        self.current_page = 1
        self.inspect_load(url)
        request = self.more_products()
        while request.status_code == requests.codes.ok:
            try:
                self.crawl_page(request)
                request = self.more_products()
            except:
                break

    def crawl_page(self, request):
        tree = html.fromstring(request.content)
        products = tree.xpath(self.ITEMS_LINKS)
        crawler.request_many(products,self.save_product)
    def inspect_load(self, url):
        with HTTPTracing(url) as tracing:
            driver = tracing.driver
            btn = driver.find_element_by_xpath(self.BUTTON_LOAD)
            btn.click()
            entries = tracing.wait_change_entry(self.AJAX_PAGINATION,4)
            self.ajax_request = entries[0]["request"]

    def save_product(self, product_url):
        r = requests.get(product_url)
        tree = html.fromstring(r.content)
        names = tree.xpath("//h1/div/text()")
        titles = tree.xpath("//title/text()")
        if names and titles:
            self.writer.writerow((names[0], titles[0], product_url))

    @property
    def cookies(self):
        cookies = self.ajax_request["cookies"]
        return {cookie["name"]:cookie["value"] for cookie in cookies}

    @property
    def headers(self):
        headers = self.ajax_request["headers"]
        return {header["name"]:header["value"] for header in headers}

    def more_products(self):
        url  = self.ajax_request["url"]
        url = url[:len(url)-1] + str(self.current_page)
        self.current_page += 1
        r = requests.get(url, cookies=self.cookies, headers=self.headers)
        return r
