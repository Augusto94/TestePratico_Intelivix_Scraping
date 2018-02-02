
XPATHS = {
    'itens': "//li[contains(@data-trackcheckoutcontainer, 'true')]",
    'nome': ".//div[contains(@class, 'bui-product__name')]/a/span/text()",
    'preco': ".//div[@class='bui-price']/a/span[contains \
              (@class, 'bui-price__value button-tab-links--green')]/text()",
    'loja': ".//div[@class='bui-product__store']/a/span/text()",
    'link': ".//div[contains(@class, 'bui-product__action-button')]/a/@href"
}
