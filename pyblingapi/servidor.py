#*************************************************************************#
# © 2021 Alexandre Defendi, Nexuz System                                  #
#     _   __                         _____            __                  #               
#    / | / /__  _  ____  ______     / ___/__  _______/ /____  ____ ___    #
#   /  |/ / _ \| |/_/ / / /_  /     \__ \/ / / / ___/ __/ _ \/ __ `__ \   #
#  / /|  /  __/>  </ /_/ / / /_    ___/ / /_/ (__  ) /_/  __/ / / / / /   #
# /_/ |_/\___/_/|_|\__,_/ /___/   /____/\__, /____/\__/\___/_/ /_/ /_/    #
#                                     /____/                              #
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).      #
#*************************************************************************#

from pyblingapi import tools

BLING_CATEGORIAS = 'categorias'
BLING_CATEGORIA = 'categoria'
BLING_CATEGORIAS_LOJA = 'categoriasLoja'
BLING_CATEGORIAS_LOJA_CATEG = 'categoriasLojaCateg'
BLING_CONTA_PAGAR = 'contapagar'
BLING_CONTA_RECEBER = 'contareceber'
BLING_CONTATOS = 'contatos'
BLING_CONTATO = 'contato'
BLING_CONTRATO = 'contrato'
BLING_DEPOSITO = 'deposito'
BLING_FORMA_PAGAMENTO = 'formapagamento'
BLING_LOGISTICA = 'logistica'
BLING_NOTAFISCAL = 'notafiscal'
BLING_NOTASFISCAIS = 'notafiscais'
BLING_NFCE = 'nfce'
BLING_NFSE = 'nfse'
BLING_ORDEM_PRODUCAO = 'ordemproducao'
BLING_PEDIDO = 'pedido'
BLING_PEDIDOS = 'pedidos'
BLING_SITUACAO = 'situacao'
BLING_PRODUTO = 'produto'
BLING_PRODUTOS = 'produtos'
BLING_PRODUTOS_FORNECEDOR = 'produtosfornecedor'
BLING_EVENTO_RASTREAMENTO = 'rastreamentoevento'
BLING_VINCULAR_RASTREAMENTO = 'rastreamentovincular'

URI = {
    'servidor': 'bling.com.br',
    BLING_CATEGORIAS: 'Api/v2/categorias',
    BLING_CATEGORIA: 'Api/v2/categoria/{idCategoria}',
    BLING_CATEGORIAS_LOJA: 'Api/v2/categoriasLoja/{idLoja}',
    BLING_CATEGORIAS_LOJA_CATEG: 'Api/v2/categoriasLoja/{idLoja}/{idCategoria}',
    BLING_CONTA_PAGAR: False,
    BLING_CONTA_RECEBER: False,
    BLING_CONTATOS: 'Api/v2/contatos',
    BLING_CONTATO: 'Api/v2/contato/{idContato}',
    BLING_CONTRATO: False,
    BLING_DEPOSITO: False,
    BLING_FORMA_PAGAMENTO: False,
    BLING_LOGISTICA: False,
    BLING_NOTAFISCAL: 'Api/v2/notafiscal/{numero}/{serie}',
    BLING_NOTASFISCAIS: 'Api/v2/notasfiscais',
    BLING_NFCE: False,
    BLING_NFSE: False,
    BLING_ORDEM_PRODUCAO: False,
    BLING_PEDIDO: 'Api/v2/pedido/{numero}',
    BLING_PEDIDOS: 'Api/v2/pedidos',
    BLING_PRODUTO: 'Api/v2/produto/{codigo}',
    BLING_PRODUTOS: 'Api/v2/produtos',
    BLING_PRODUTOS_FORNECEDOR: 'Api/v2/produto/{codigo}/{id_fornecedor}',
    BLING_SITUACAO: 'Api/v2/situacao/{modulo}',
    BLING_EVENTO_RASTREAMENTO: '',
    BLING_VINCULAR_RASTREAMENTO: '',
}


def localizar_uri(resource, method='GET'):
    dominio = URI['servidor']
    complemento = URI[resource]
    if method == 'POST':
        x = tools.find_nth(complemento, '/', 3)
        # x = (x-1) * (-1) if x > 1 else 0 
        complemento = complemento[:x]
    return "https://%s/%s" % (dominio, complemento)
