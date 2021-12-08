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

# from pyblingapi import tools
from pyblingapi.errors import BlingApiResourceMethodError

METHOD_POST = 'POST'
METHOD_GET = 'GET'
METHOD_PUT = 'PUT'
METHOD_DELETE = 'DELETE'

BLING_CAMPOSCUSTOMIZADOS = 'camposcustomizados'
BLING_CATEGORIAS = 'categorias'
BLING_CATEGORIA = 'categoria'
BLING_CATEGORIA_ID = 'categoria_id'
BLING_CATEGORIAS_LOJA = 'categoriasLoja'
BLING_CATEGORIAS_LOJA_CATEG = 'categoriasLojaCateg'
BLING_CONTA_PAGAR = 'contapagar'
BLING_CONTA_PAGAR_ID = 'contapagar_id'
BLING_CONTA_RECEBER = 'contareceber'
BLING_CONTA_RECEBER_ID = 'contareceber_id'
BLING_CONTATOS = 'contatos'
BLING_CONTATO = 'contato'
BLING_CONTATO_CPF_CNPJ = 'contato_cpf_cnpj'
BLING_CONTRATO = 'contrato'
BLING_CONTRATO_ID = 'contrato_id'
BLING_CTE = 'cte'
BLING_CTE_NUMBER_SERIE = 'cte_number_serie'
BLING_CTE_LANCAMENTO_CONTAS = 'cte_lancamento_contas'
BLING_DEPOSITO = 'deposito'
BLING_DEPOSITO_ID = 'deposito_id'
BLING_FORMA_PAGAMENTO = 'formapagamento'
BLING_FORMA_PAGAMENTO_ID = 'formapagamento_id'
BLING_GRUPO_PRODUTOS = 'grupoprodutos'
BLING_GRUPO_PRODUTOS_ID = 'grupoprodutos_id'
BLING_LOGISTICA_SERVICO = 'logisticaservicos'
BLING_LOGISTICA_ID_SERVICO = 'logistica_id_servico'
BLING_NFCE = 'nfce'
BLING_NFCE_NUMBER_SERIE = 'nfce_number_serie'
BLING_NFE = 'nfe'
BLING_NFE_NUMBER_SERIE = 'nfe_number_serie'
BLING_NFSE = 'nfse'
BLING_NFSE_NUMBER = 'nfse_number'
BLING_ORDENS_PRODUCAO = 'ordensproducao'
BLING_ORDEM_PRODUCAO = 'ordemproducao'
BLING_PEDIDO = 'pedido'
BLING_PEDIDOS = 'pedidos'
BLING_PEDIDO_COMPRA = 'pedidocompra'
BLING_PEDIDOS_COMPRA = 'pedidoscompra'
BLING_PRODUTO = 'produto'
BLING_PRODUTOS = 'produtos'
BLING_PRODUTOS_FORNECEDOR = 'produtosfornecedor'
BLING_PRODUTO_LOJA = 'produtoloja'
BLING_FORNECEDOR_PRODUTOS = 'produtosfornecedores'
BLING_FORNECEDOR_PRODUTO = 'produtofornecedor'
BLING_PROPOSTA_COMERCIAL = 'propostacomercial'
BLING_PROPOSTAS_COMERCIAIS = 'propostascomerciais'

BLING_SITUACAO = 'situacao'
BLING_EVENTO_RASTREAMENTO = 'rastreamentoevento'
BLING_VINCULAR_RASTREAMENTO = 'rastreamentovincular'

URI = {
    'servidor': 'bling.com.br',
    
    METHOD_GET: {
        BLING_CAMPOSCUSTOMIZADOS: 'Api/v2/camposcustomizados/{modulo}',
        BLING_CATEGORIA: 'Api/v2/categorias',
        BLING_CATEGORIA_ID: 'Api/v2/categoria/{idCategoria}',
        BLING_CATEGORIAS_LOJA: 'Api/v2/categoriasLoja/{idLoja}',
        BLING_CATEGORIAS_LOJA_CATEG: 'Api/v2/categoriasLoja/{idLoja}/{idCategoria}',
        BLING_CONTATO: 'Api/v2/contatos',
        BLING_CONTATO_CPF_CNPJ: 'Api/v2/contato/{cpf_cnpj}',
        BLING_CONTA_PAGAR: 'Api/v2/contaspagar',
        BLING_CONTA_PAGAR_ID: 'Api/v2/contaspagar/{idContaPagar}',
        BLING_CONTA_RECEBER: 'Api/v2/contasreceber',
        BLING_CONTA_RECEBER_ID: 'Api/v2/contareceber/{id}',
        BLING_CONTRATO: 'Api/v2/contratos',
        BLING_CONTRATO_ID: 'Api/v2/contrato/{id}',
        BLING_CTE: 'Api/v2/ctes',
        BLING_CTE_NUMBER_SERIE: 'Api/v2/cte/{numero}/{serie}',
        BLING_DEPOSITO: 'Api/v2/depositos',
        BLING_DEPOSITO_ID: 'Api/v2/deposito/{id}',
        BLING_FORMA_PAGAMENTO: 'Api/v2/formaspagamento',
        BLING_FORMA_PAGAMENTO_ID: 'Api/v2/formapagamento/{id}',
        BLING_GRUPO_PRODUTOS: 'Api/v2/gruposprodutos',
        BLING_GRUPO_PRODUTOS_ID: 'Api/v2/grupoprodutos/{id}',
        BLING_LOGISTICA_SERVICO: 'Api/v2/logisticas/servicos',
        BLING_LOGISTICA_ID_SERVICO: 'Api/v2/logistica/{id}/servicos',
        BLING_NFCE: 'Api/v2/nfces',
        BLING_NFCE_NUMBER_SERIE: 'Api/v2/nfce/{numero}/{serie}',
        BLING_NFE: 'Api/v2/notasfiscais',
        BLING_NFE_NUMBER_SERIE: 'Api/v2/notafiscal/{numero}/{serie}',
        BLING_NFSE: 'Api/v2/notasservico',
        BLING_NFSE_NUMBER: 'Api/v2/notaservico/{numero}',
        BLING_ORDEM_PRODUCAO: 'Api/v2/ordensproducao/page={page}',
        BLING_ORDEM_PRODUCAO: 'Api/v2/ordemproducao/{numero}',
        BLING_PEDIDO: 'Api/v2/pedido/{numero}',
        BLING_PEDIDOS: 'Api/v2/pedidos',
        BLING_PEDIDO_COMPRA: 'v2/pedidocompra/{numero}',
        BLING_PEDIDOS_COMPRA: 'Api/v2/pedidoscompra',
        BLING_PRODUTO: 'Api/v2/produto/{codigo}',
        BLING_PRODUTOS: 'Api/v2/produtos',
        BLING_PRODUTOS_FORNECEDOR: 'Api/v2/produto/{codigo}/{id_fornecedor}',
        BLING_PRODUTO_LOJA: 'Api/v2/produto/{codigo}',
        BLING_FORNECEDOR_PRODUTOS: 'Api/v2/produtosfornecedores',
        BLING_FORNECEDOR_PRODUTO: 'Api/v2/produtofornecedor/{id}',
    },
    METHOD_POST: {
        BLING_CATEGORIA: 'Api/v2/categoria',
        BLING_CATEGORIAS_LOJA: 'Api/v2/categoriasLoja/{idLoja}',
        BLING_CONTATO: 'Api/v2/contato',
        BLING_CONTA_PAGAR: 'Api/v2/contapagar',
        BLING_CONTA_RECEBER: 'Api/v2/contareceber',
        BLING_CONTRATO: 'Api/v2/contratos',
        BLING_CTE: 'Api/v2/cte',
        BLING_CTE_LANCAMENTO_CONTAS: 'Api/v2/cte/lancamento/contas/{id}',
        BLING_DEPOSITO: 'Api/v2/deposito',
    },
    METHOD_PUT: {
        BLING_CATEGORIA: 'Api/v2/categoria/{idCategoria}',
        BLING_CATEGORIAS_LOJA: 'Api/v2/categoriasLoja/{idLoja}/{idCategoria}',
        BLING_CONTATO: 'Api/v2/contato/{idContato}',
        BLING_CONTA_PAGAR: 'Api/v2/contapagar/{id}',
        BLING_CONTA_RECEBER: 'Api/v2/contareceber/{id}',
        BLING_CONTRATO: 'Api/v2/contrato/{id}',
        BLING_CTE: '/Api/v2/cte/{id}',
        BLING_DEPOSITO: 'Api/v2/deposito/{id}',
    },
    METHOD_DELETE: {
        BLING_CONTRATO: 'Api/v2/contrato/{id}',
        BLING_CTE: 'Api/v2/cte/estorno/contas/{id}',
    },
    
    # BLING_FORMA_PAGAMENTO: False,
    # BLING_LOGISTICA: False,
    # BLING_NOTAFISCAL: 'Api/v2/notafiscal/{numero}/{serie}',
    # BLING_NOTASFISCAIS: 'Api/v2/notasfiscais',
    # BLING_NFCE: False,
    # BLING_NFSE: False,
    # BLING_ORDEM_PRODUCAO: False,
    # BLING_SITUACAO: 'Api/v2/situacao/{modulo}',
    # BLING_EVENTO_RASTREAMENTO: '',
    # BLING_VINCULAR_RASTREAMENTO: '',
}


def localizar_uri(resource, method='GET'):
    dominio = URI['servidor']
    try:
        complemento = URI[method][resource]
    except:
        raise BlingApiResourceMethodError(resource,method)
    
    # if method == 'POST':
    #     x = tools.find_nth(complemento, '/', 3)
    #     # x = (x-1) * (-1) if x > 1 else 0 
    #     complemento = complemento[:x]
    return "https://%s/%s" % (dominio, complemento)
