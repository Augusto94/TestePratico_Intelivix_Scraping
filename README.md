# TestePratico Intelivix Scraping


#### Augusto Rodrigues de lima
#### <arl4@cin.ufpe.br>

### Teste Prático Para a Chamada de Desenvolvedores - Time de Scraping

## Projeto

Um Crawler desenvolvido para extrair todas as informações de todos os produtos do site da Kabum.\
Foi criada uma spider que navega por todas as categorias e sub-categorias até o nível mais baixo para então acessar as páginas dos produtos e extrair suas informações requisitadas.\
Todas as informações solicitadas na descrição do teste foram capturadas no tipo de dado solicitado.\
Após capturar todas as informações referentes aos produtos, essas informações foram persistidas em um MongoDB.

## Pontos a serem destacados
O site da Kabum é muito bem estruturado, entretanto, na parte das especificações técnicas o site não apresenta um padrão para todos os produtos. Devido a isso, em poucos produtos algumas informações na parte de "características" podem estar faltosas. Mas são pouquíssimos os casos em que isso acontece.\
As dimensões dos produtos estão presentes na parte das específicações técnicas, o que dificulta a sua extração por falta de padrão. Alguns produtos vem com o campo dimensões no meio das especificações técnicas. Nesses produtos foi possível capturar.\
Os preços dos produtos na Kabum tem desconto quando o pagamento é feito via boleto, então, além do valor atual e do valor antigo (quando existia) também foi capturada a informação do valor á vista.

## Tempo despendido para o desenvolvimento

- Análise e escolha do site que seria feito o crawler e iniciação do projeto utilizando scrapy (3 horas)
- Capturar todas as informações de um único produto e realizar os devidos tratamentos (6 horas)
- Navegar pelas categorias até o menor nível possível (1 hora)
- Capturar as informações de todos produtos de uma página e realizar a paginação (2 horas)
- Persistir as informações no banco de dados MongoDB (2 horas)
- Revisão do código (6 horas)

#### Observação:

O tempo total estimado foi de aproximadamente 20 horas.\
Levando em conta os itens citados acima bem como o tempo para revisar o uso das ferramentas que foram utilizadas.

## Instruções para execução do projeto

É necessário ter instalado:
- Python 3 (Instalação pode ser feita via Anaconda para facilitar)\
https://docs.anaconda.com/anaconda/install
- Scrapy
```
conda install -c anaconda scrapy 
```
- MongoDB (Pode ser realiza a instalaço seguindo o tutorial que se encontra no link)
https://docs.mongodb.com/manual/tutorial/install-mongodb-on-ubuntu/
- pymongo
```
conda install -c anaconda pymongo
```

#### Executando o projeto
1. Clone o projeto:
```
git clone https://github.com/Augusto94/TestePratico_Intelivix_Scraping.git
```
2. Inicie o serviço do MongoDB:
```
sudo service mongod start
```
3. Entre na pasta do projeto e execute o seguinte comando para rodar a Spider:
```
cd TestePratico\
scrapy crawl kabum
```
4. Aguarde a execução do crawler (Isso pode levar um tempo ;) )
5. Ao término da execução da spider consultas no banco de dados já podem ser relizadas. 
6. Abra uma IDLE do python para realizar consultas (Terminal, Jupyter Notebook, etc).
7. Segue o exemplo de uma consulta:
```
import pymongo
client = pymongo.MongoClient()
db = client.products_kabum
collection = db.products_kabum
collection.find_one({'URL': 'https://www.kabum.com.br/cgi-local/site/produtos/descricao_ofertas.cgi?codigo=11652'})
```
