# -*- coding: utf-8 -*-
import scrapy


class KabumSpider(scrapy.Spider):
    name = "kabum"
    start_urls = ['https://www.kabum.com.br/']
    #Entra em cada categoria do Site da Kabum
    def parse(self, response):
        menu = response.xpath('//*[@id="menu_left"]/div[@class="texto_categoria"]/p[@class="bot-categoria"]/a/@href').extract()
        for cat in menu:
            yield scrapy.Request(
            url = cat,
            callback = self.parse_sub
            )


    #Entra em cada Subcategoria da categoria que esta executando
    def parse_sub(self, response):
        subs = response.xpath('//div[@id="menu_left"]/div[@class="texto_categoria"][1]/p[@class="bot-categoria"]/a/@href').extract()
        for sub in subs:
            yield scrapy.Request(
            url = sub,
            callback = self.parse_item
            )
        cat = response.xpath('//*[@id="menu_left"]/div[@class="icone_categoria_azul"]/h2/text()').extract()[0]
        self.log(cat)

    #Na página das subcategorias, entra em cada produto da página e realiza a paginação para pegar todos os produtos
    def parse_item(self, response):
        itens = response.xpath('//div[@id="BlocoConteudo"]/div[2]/div[@class="box_page"]/div[@class="listagem-box"]/div/span/a/@href').extract()
        raiz = response.url
        if raiz[-2:] == "30":
            raiz = raiz[:-35]
        for prod in itens:
            yield scrapy.Request(
            url = prod,
            callback = self.parse_details
            )

        #Tratamento de Paginação
        proxima_pagina = response.xpath('//div[@class="listagem-paginacao"]/form[@name="listagem"]//tr/td/a/@href').extract_first()
        if proxima_pagina:
            new_url = raiz + proxima_pagina
            yield scrapy.Request(
            url = new_url,
            callback = self.parse_item
            )

    #Em cada produto extrai as informações para colocar no MongoDB e cada item capturado exibe uma mensagem de log
    def parse_details(self, response):
        #Variáveis auxiliares
        marca = ""
        aux = ""
        aux2 = 0
        caracteristicas = []
        lstLine = []
        dic = {}
        line = ""
        dim = {}


        detalhe = response.xpath("//div[@id='pag-detalhes']")
        #Captura a url, nome, descrição e categoria da página do produto
        url = response.url
        nome = response.xpath('//div[@id="titulo_det"]/h1/text()').extract()[0].strip()
        descricao = detalhe.xpath('//p[@itemprop="description"]/text()').extract()
        if descricao:
            descricao = descricao[0]
        else:
            descricao = ""
        categoria = response.xpath('//div[@id="menu_left"]/div[@class="icone_categoria_azul"]/h2/text()').extract()[0]

        #Captura a Marca do Produto que esta presente nas especificaçẽos técnicas
        #Faz o tratamento da String para extrair somento nome da marca (retirando o termo "- Marca: ")
        marcaLista = detalhe.xpath('//div[@class="content_tab"][1]/p/text()').extract()
        while marca == "" and aux2 < len(marcaLista):
            if "Marca:" in marcaLista[aux2]:
                marca = marcaLista[aux2]
            aux2 += 1
        if marca != "":
            marca = marca.split(":")[1][1:].strip("\xa0")

        #Captura a navegação
        #Faz o tratamento para pegar somente a string (sem o " >")
        navegacao = response.xpath('//div[@class="links_det"]/ol/li/a/text()').extract()
        tratamento = lambda nav: [nav[0:-2] for nav in navegacao]
        navegacao = tratamento(navegacao)

        #O nome do vendedor é Default
        vendedor = "Kabum"

        #Captura o preço antigo do procuto se houver
        #Verifica se o produto esta em promoção
        precoAntigo = detalhe.xpath('//div[@class="preco_antigo"]/text()').extract()
        #Se estiver em promoção a captura do preço se dar por um xpath diferente do padrão
        if not precoAntigo:
            precoAntigo = detalhe.xpath('//div[@class="preco_antigo-cm"]/text()').extract()
        if precoAntigo:
            precoAntigo = precoAntigo[0][6:-4].replace(".","").replace(",",".")
        else:
            precoAntigo = ''

        #Captura o preço do produto sem descontos
        #Verifica se o produto esta em promoção
        precoPrazo = detalhe.xpath('//div[@class="preco_normal"]/text()').extract()
        #Se estiver em promoção a captura do preço se dar por um xpath diferente do padrão
        if len(precoPrazo) == 0:
            precoPrazo = detalhe.xpath('//div/div[2]/div[2]/div[3]/div[2]/span/strong/text()').extract()
        #Realiza o tratamento para extrair somente o valor no tipo Float
        if len(precoPrazo) != 0:
            precoPrazo = precoPrazo[0].split("$ ")
            precoPrazo = float(precoPrazo[1].split("\n")[0].replace(".","").replace("," , "."))
        else:
            precoPrazo = ''

        #Captura o preço com desconto (pagamento à vista)
        #Verifica se o produto esta em promoção
        precoAVista = detalhe.xpath('//span[@class="preco_desconto"]/span/span/strong/text()').extract()
        #Se estiver em promoção a captura do preço se dar por um xpath diferente do padrão
        if len(precoAVista) == 0:
            precoAVista = detalhe.xpath('//div/div[2]/div[2]/div[3]/div[4]/span[1]/text()').extract()
        #Realiza o tratamento para extrair somente o valor no tipo Float
        if len(precoAVista) != 0:
            precoAVista = float(precoAVista[0].split("$ ")[1][0:-1].replace(".", "").replace(",","."))
        else:
            precoAVista = ''
        #Captura as imagem principal e imagens secundàrias
        imagemPrincipal = detalhe.xpath('//div[@id="fotoG"]/div/section/div/ul/li[1]/img[1]/@src').extract_first()
        imagensSecundarias = detalhe.xpath('//div[@id="slider"]/ul[@class="slides"]/li/img/@src').extract()

        #Captura as características do produto (Os valores que possuem o campo "chave: valor")
        #Realiza o tratamento e insere no dicionário, após isso insere o dicionário na lista (formando o list dict)
        #Como as dimensões estão nas caracteristicas, faço o tratamento para capturar as dimensões se houver
        values = detalhe.xpath('//div/div[@class="tab_"]/div[@class="content_tab"]/p//text()').extract()
        for i in range(len(values)):
            if (len(values[i]) >= 2) and (values[i][0] == "-" or values[i][1] == "-"):
                line = values[i][2:]
                if ":" in line:
                    line = line.replace("\xa0","")
                    lstLine = line.split(":")
                    if lstLine[1]:
                        if lstLine[1][0] == " ":
                            lstLine[1] = lstLine[1][1:]
                    dic[lstLine[0].replace(".","")] = lstLine[1].replace(".",",").strip("\xa0")
                    key = list(dic.keys())[0]
                    if ("Dimensões" in key) or ("Dimensão" in key):
                        dim = dic
                    else:
                        caracteristicas.append(dic)
                    dic = {}



        yield {
            "URL": url,
            "Nome": nome,
            "Descrição": descricao,
            "Categoria": categoria,
            "Marca": marca,
            "Navegação": navegacao,
            "Nome_Vendedor": vendedor,
            "Valor": precoAVista,
            "Valor_Parcelado": precoPrazo,
            "Valor_Antigo": precoAntigo,
            "Imagem_Principal": imagemPrincipal,
            "Imagens_Secudarias": imagensSecundarias,
            "Caracteristicas": caracteristicas,
            "Dimensões": dim,
        }
        self.log('\n--------------ITEM CAPTURADO--------------\n')
