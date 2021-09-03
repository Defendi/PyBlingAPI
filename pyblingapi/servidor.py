# © 2021 Alexandre Defendi, Nexuz System
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
#    _   __                         _____            __               
#   / | / /__  _  ____  ______     / ___/__  _______/ /____  ____ ___ 
#  /  |/ / _ \| |/_/ / / /_  /     \__ \/ / / / ___/ __/ _ \/ __ `__ \
# / /|  /  __/>  </ /_/ / / /_    ___/ / /_/ (__  ) /_/  __/ / / / / /
#/_/ |_/\___/_/|_|\__,_/ /___/   /____/\__, /____/\__/\___/_/ /_/ /_/ 
#                                     /____/                          

BLING_CATEGORIAS = 'categorias'
BLING_CATEGORIA = 'categoria'
BLING_CATEGORIA_LOJAS = 'categoriasLoja'
BLING_CONTA_PAGAR = 'contapagar'
BLING_CONTA_RECEBER = 'contareceber'
BLING_CONTATO = 'contato'
BLING_CONTRATO = 'contrato'
BLING_DEPOSITO = 'deposito'
BLING_FORMA_PAGAMENTO = 'formapagamento'
BLING_LOGISTICA = 'logistica'
BLING_NFE = 'nfe'
BLING_NFCE = 'nfce'
BLING_NFSE = 'nfse'
BLING_ORDEM_PRODUCAO = 'ordemproducao'
BLING_PEDIDO = 'pedido'
BLING_PRODUTO = 'produto'
BLING_EVENTO_RASTREAMENTO = 'rastreamentoevento'
BLING_VINCULAR_RASTREAMENTO = 'rastreamentovincular'

URI = {
    'servidor': 'bling.com.br',
    BLING_CATEGORIAS: 'Api/v2/categorias',
    BLING_CATEGORIA: 'Api/v2/categoria/{idCategoria}',
    BLING_CATEGORIA_LOJAS: 'Api/v2/',
    BLING_CONTA_PAGAR: 'Api/v2/',
    BLING_CONTA_RECEBER: 'Api/v2/',
    BLING_CONTATO: 'Api/v2/contato',
    BLING_CONTRATO: 'Api/v2/',
    BLING_DEPOSITO: 'Api/v2/',
    BLING_FORMA_PAGAMENTO: 'Api/v2/',
    BLING_LOGISTICA: 'Api/v2/',
    BLING_NFE: 'Api/v2/',
    BLING_NFCE: 'Api/v2/',
    BLING_NFSE: 'Api/v2/',
    BLING_ORDEM_PRODUCAO: 'Api/v2/',
    BLING_PEDIDO: 'Api/v2/',
    BLING_PRODUTO: 'Api/v2/produto',
    BLING_EVENTO_RASTREAMENTO: 'Api/v2/',
    BLING_VINCULAR_RASTREAMENTO: 'Api/v2/',
}


def localizar_uri(resource):
    dominio = URI['servidor']
    complemento = URI[resource]
    return "https://%s/%s" % (dominio, complemento)
