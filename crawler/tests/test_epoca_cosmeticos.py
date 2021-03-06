#!/usr/bin/env python3
from crawler.epoca_cosmeticos import EpocaCosmeticos
import requests
from unittest.mock import patch
import subprocess
import os
import time
PRODUCT ={
   'url':"http://www.epocacosmeticos.com.br/argan-oil-lola-cosmetics-oleo-anti-frizz/p",
   'name':"Argan Oil Lola Cosmetics - Óleo Anti-Frizz - 60ml",
   'title' : 'Argan Oil Lola Cosmetics - Óleo Anti-Frizz - Época Cosméticos'
}
epoca = EpocaCosmeticos("products.csv")

URLS = ['http://google.com/',
       'http://facebook.com/',
       'http://youtube.com/',
       'http://medium.com/',
       'http://quora.com/'
        ]


class TestEpocaCosmeticos:

    def test_inspect_load(self):
        epoca.inspect_load("http://www.epocacosmeticos.com.br/cabelos")
        assert epoca.ajax_request
        assert epoca.AJAX_PAGINATION in epoca.ajax_request["url"]

    def test_more_products(self):
        epoca.ajax_request = {
            "url":"https://www.facebook.com/?page_numbe=2",
            'cookies':[],
            'headers':[],
        }
        epoca.current_page = 1
        request = epoca.more_products()
        assert isinstance(request,requests.models.Response)

    def test_cookies(self):
        epoca.ajax_request = {
            'cookies':[{"value":25,"name":"idade"},
                     {"value":"joney","name":"nome"}]}
        assert epoca.cookies == {"idade":25,"nome":"joney"}

    def test_headers(self):
        epoca.ajax_request = {
            'headers':[{"value":"bytes","name":"Accept-Ranges"},
                     {"value":"close","name":"Connection"}]}
        print( epoca.headers)
        assert epoca.headers == {"Connection":"close","Accept-Ranges":"bytes"}

    @patch("crawler.request_many")
    def test_crawl_page(self, mock_req):
        dirname = os.path.dirname(__file__)
        process = subprocess.Popen(["python",dirname+"/server/base_server.py"])
        time.sleep(2)
        epoca.ITEMS_LINKS ="//li/a/@href"
        r = requests.get("http://localhost:8081/")
        epoca.crawl_page(r)
        mock_req.assert_called_with(URLS, epoca.save_product)
        process.terminate()

    @patch("csv.writer")
    def test_save(self, mock_csv):
        epoca = EpocaCosmeticos("products.csv")
        epoca.save_product(PRODUCT['url'])
        epoca.writer.writerow.assert_called_with((
            PRODUCT['name'],PRODUCT["title"],PRODUCT['url']))




