

import scrapy
import csv

from scrapy.http import Request

from buscape.spiders.constants import XPATHS


class SmartphonesSpider(scrapy.Spider):
    name = "smartphones"
    allowed_domains = ["buscape.com.br"]
    start_urls = (
        'https://www.buscape.com.br/celular-e-smartphone',
    )

    def parse(self, response):  
        url_default = ('https://www.buscape.com.br/'
                       'celular-e-smartphone?pagina={}'.format)
        for i in range(1,89):
            url = url_default(str(i))
            yield Request(
                url=url,
                callback=self.extrair_dados
            )

    def extrair_dados(self, response):
        itens = response.xpath(XPATHS['itens'])
        for item in itens:
            nome = item.xpath(XPATHS['nome']).extract_first()
            preco = item.xpath(XPATHS['preco']).extract_first()
            if preco:
                preco = preco.replace(
                    'R$ ', '').replace('.', '').replace(',', '.')
            loja = item.xpath(XPATHS['loja']).extract_first()
            link = item.xpath(XPATHS['link']).extract_first()
            if not nome or not preco or not loja or not link:
                continue

            inserir = [nome.encode(
                "utf-8"), preco.encode("utf-8"),
                loja.encode("utf-8"), link.encode("utf-8")]
            with open(r'csv_produtos.csv', 'a') as csvfile:
                writer = csv.writer(csvfile, delimiter='|',
                                    quoting=csv.QUOTE_MINIMAL)
                writer.writerow(inserir)
