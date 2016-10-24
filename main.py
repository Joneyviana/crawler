from  crawler.epoca_cosmeticos  import EpocaCosmeticos

categorias = ["perfumes","maquiagem",
              "dermocosmeticos","tratamentos",
              "corpo-e-banho","unhas"]

url = "http://www.epocacosmeticos.com.br/"

epoca_cosmeticos = EpocaCosmeticos("products.csv")

for categoria in categorias:
    epoca_cosmeticos.crawl(url+categoria)
