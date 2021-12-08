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

import os
import logging
import requests

from lxml import etree
from pyblingapi.xml import render_xml
from pyblingapi.servidor import localizar_uri, METHOD_DELETE, METHOD_GET, METHOD_POST, METHOD_PUT
from pyblingapi.errors import BlingApiRequestError, BlingApiDateSelectError, BlingApiTypeContactError, BlingApiMethodError,\
                              BlingStateError
from pyblingapi.tools import checkData, StateInList, SELECTDATEDATATYPE, SEL_CONTRACT_STATE, SEL_BILLS_STATE

logger = logging.getLogger(__name__)

class BlingApi(object):

    def __init__(self, api_key, file_format='json'):
        self.api_key = api_key
        self.session = requests.Session()
        self.file_format = str(file_format).lower()

    # Métodos GET
    def getCamposCustomizados(self, module):
        """
        Função que Busca os campos customizados a partir do seu módulo.
        :param module: Módulo dos campos customizados que você deseja consultar (obrigatório). 
                       Utilizar o nome exibido na tabela de módulos.
        """
        uri = self._get_uri('camposcustomizados').format(modulo=module)
        resp = self._make_request('GET', uri)
        return resp

    def getSituation(self, module):
        """
        Função que Busca as situações a partir do seu módulo.
        :param module: Módulo das situações que você deseja consultar (obrigatório). 
                       Utilizar o nome exibido na tabela de módulos.
        """
        uri = self._get_uri('situacao').format(modulo=module)
        resp = self._make_request('GET', uri)
        return resp

    def getCategory(self, categoy_id=None):
        """
        Função que Busca todas as categorias de produtos.
        :param categoy_id: Busca uma categoria a partir do seu identificador (Opcional).
        """
        if bool(categoy_id):
            uri = self._get_uri('categoria_id').format(idCategoria=categoy_id)
        else:
            uri = self._get_uri('categoria')
        resp = self._make_request('GET', uri)
        return resp

    def getCategoryStore(self, store_id, category_id=None):
        """
        Função que Busca os todos os vínculos de categorias por loja.
        :param store_id: Identificador da loja (obrigatório).
        :param category_id: Identificador da categoria (opcional).
        """
        if bool(category_id):
            uri = self._get_uri('categoriasLojaCateg').format(idLoja=store_id,idCategoria=category_id)
        else:
            uri = self._get_uri('categoriasLoja').format(idLoja=store_id)
        resp = self._make_request('GET', uri)
        return resp

    def getBillsToPay(self, payment_id=None, issue_date=None, due_date=None, state=None, cnpj=None):
        """
        Função que Busca os todos os vínculos de categorias por loja.
        :param contact_id: Identificador da loja (opcional);
        :param id_type: Identificador da categoria (opcional);
        :param creation_date: periodo de ['dd/mm/aaaa','dd/mm/aaaa'] (opcional)
        :param modification_date: periodo de ['dd/mm/aaaa','dd/mm/aaaa'] (opcional)
        :param person_type: in ['F','J','E'] (opcional)
        Caso contact_id seja passado os outros valores serão ignorados.
        """
        filters = []
        if bool(payment_id):
            uri = self._get_uri('contapagar_id').format(idContaPagar=payment_id)
        else:
            uri = self._get_uri('contapagar')

            if issue_date:
                if checkData(SELECTDATEDATATYPE, issue_date):
                    filters.append('dataInclusao[{} TO {}]'.format(issue_date[0], issue_date[1]))
                else:
                    raise BlingApiDateSelectError()
            
            if due_date:
                if checkData(SELECTDATEDATATYPE, due_date):
                    filters.append('dataAlteracao[{} TO {}]'.format(due_date[0], due_date[1]))
                else:
                    raise BlingApiDateSelectError()
    
            if state:
                if StateInList(state,SEL_BILLS_STATE):
                    filters.append('situacao[{}]'.format(state))
                else:
                    raise BlingStateError()

            if cnpj:
                #TODO: Verificar se o cnpj é válido
                filters.append('situacao[{}]'.format(state))
    
        params = self._construct_params(filters)
        
        resp = self._make_request('GET', uri, params=params)
        return resp

    def getBillsToReceive(self, receive_id=None, issue_date=None, due_date=None, pay_date=None, state=None, cnpj=None):
        """
        Função que Busca os todos os vínculos de categorias por loja.
        :param receive_id: Identificador da Conta a Receber (opcional);
        :param id_type: Identificador da categoria (opcional);
        :param creation_date: periodo de ['dd/mm/aaaa','dd/mm/aaaa'] (opcional)
        :param modification_date: periodo de ['dd/mm/aaaa','dd/mm/aaaa'] (opcional)
        :param person_type: in ['F','J','E'] (opcional)
        Caso contact_id seja passado os outros valores serão ignorados.
        """
        filters = []
        if bool(receive_id):
            uri = self._get_uri('contareceber_id').format(idContaPagar=receive_id)
        else:
            uri = self._get_uri('contareceber')

            if issue_date:
                if checkData(SELECTDATEDATATYPE, issue_date):
                    filters.append('dataInclusao[{} TO {}]'.format(issue_date[0], issue_date[1]))
                else:
                    raise BlingApiDateSelectError()
            
            if due_date:
                if checkData(SELECTDATEDATATYPE, due_date):
                    filters.append('dataAlteracao[{} TO {}]'.format(due_date[0], due_date[1]))
                else:
                    raise BlingApiDateSelectError()

            if pay_date:
                if checkData(SELECTDATEDATATYPE, pay_date):
                    filters.append('dataPagamento[{} TO {}]'.format(pay_date[0], pay_date[1]))
                else:
                    raise BlingApiDateSelectError()
    
            if state:
                if StateInList(state,SEL_BILLS_STATE):
                    filters.append('situacao[{}]'.format(state))
                else:
                    raise BlingStateError()

            if cnpj:
                #TODO: Verificar se o cnpj é válido
                filters.append('situacao[{}]'.format(state))
    
        params = self._construct_params(filters)
        
        resp = self._make_request('GET', uri, params=params)
        return resp

    def getContact(self, contact_id=None, id_type=None, creation_date=None, modification_date=None, person_type=None):
        """
        Função que Busca os todos os vínculos de categorias por loja.
        :param contact_id: Identificador da loja (opcional);
        :param id_type: Identificador da categoria (opcional);
        :param creation_date: periodo de ['dd/mm/aaaa','dd/mm/aaaa'] (opcional)
        :param modification_date: periodo de ['dd/mm/aaaa','dd/mm/aaaa'] (opcional)
        :param person_type: in ['F','J','E'] (opcional)
        Caso contact_id seja passado os outros valores serão ignorados.
        """
        filters = []
        if bool(contact_id):
            uri = self._get_uri('contato').format(idContato=contact_id)

            if not bool(id_type) or id_type == 'cpf_cnpj':
                filters.append('identificador[1]')
            elif id_type == 'id':
                filters.append('identificador[2]')
        else:
            uri = self._get_uri('contatos')

            if creation_date:
                if checkData(SELECTDATEDATATYPE, creation_date):
                    filters.append('dataInclusao[{} TO {}]'.format(creation_date[0], creation_date[1]))
                else:
                    raise BlingApiDateSelectError()
            
            if modification_date:
                if checkData(SELECTDATEDATATYPE, modification_date):
                    filters.append('dataAlteracao[{} TO {}]'.format(modification_date[0], modification_date[1]))
                else:
                    raise BlingApiDateSelectError()
    
            if person_type:
                if person_type in ['F', 'J', 'E']:
                    filters.append('tipo[{}]'.format(type))
                else:
                    raise BlingApiTypeContactError()
    
        params = self._construct_params(filters)
        
        resp = self._make_request('GET', uri, params=params)
        return resp

    def getProduct(self, sku=None, creation_date=None, modification_date=None, creation_store_date=None, 
                         modification_store_date=None, type=None, state=None):
        """
        Função que busca um produto ou uma lista de produtos.
        :param sku: Código SKU do produto (opcional);
        :param creation_date: periodo de ['dd/mm/aaaa','dd/mm/aaaa'] (opcional)
        :param modification_date: periodo de ['dd/mm/aaaa','dd/mm/aaaa'] (opcional)
        :param creation_store_date: periodo de ['dd/mm/aaaa','dd/mm/aaaa'] (opcional)
        :param modification_store_date: periodo de ['dd/mm/aaaa','dd/mm/aaaa'] (opcional)
        :param type: in ['P','S'] P-Produto S-Serviço (opcional)
        :param state: in ['A','I'] A-Ativo I-Inativo (opcional)
        
        Caso sku seja passado os outros valores serão ignorados.
        """
        filters = []
        if bool(sku):
            uri = self._get_uri('produto').format(codigo=sku)
        else:
            uri = self._get_uri('produtos')

            if creation_date:
                if checkData(SELECTDATEDATATYPE, creation_date):
                    filters.append('dataInclusao[{} TO {}]'.format(creation_date[0], creation_date[1]))
                else:
                    raise BlingApiDateSelectError()
            
            if modification_date:
                if checkData(SELECTDATEDATATYPE, modification_date):
                    filters.append('dataAlteracao[{} TO {}]'.format(modification_date[0], modification_date[1]))
                else:
                    raise BlingApiDateSelectError()
    
            if creation_store_date:
                if checkData(SELECTDATEDATATYPE, creation_store_date):
                    filters.append('dataInclusaoLoja[{} TO {}]'.format(creation_store_date[0], creation_store_date[1]))
                else:
                    raise BlingApiDateSelectError()
            
            if modification_store_date:
                if checkData(SELECTDATEDATATYPE, modification_store_date):
                    filters.append('dataAlteracaoLoja[{} TO {}]'.format(modification_store_date[0], modification_store_date[1]))
                else:
                    raise BlingApiDateSelectError()

            if type:
                filters.append('tipo[{}]'.format(type))

            if state:
                filters.append('situacao[{}]'.format(state))
    
        params = self._construct_params(filters)
        
        resp = self._make_request('GET', uri, params=params)
        return resp

    def getProductBySupplier(self, sku, supplier_id):
        """
        Função que busca um produto pelo Fornecedor.
        :param sku: Código SKU do produto (obrigatorio);
        :param supplier_id: Identificador do fornecedor (obrigatorio)
        """
        uri = self._get_uri('produtosfornecedor').format(codigo=sku,id_fornecedor=supplier_id)
        resp = self._make_request('GET', uri)
        return resp

    def getProductSupplier(self, product_id=None, contact_id=None):
        """
        Função que busca um produto do Fornecedor.
        :param product_id: Código SKU do produto (obrigatorio);
        :param contact_id: Identificador do fornecedor (opcional)
        """
        filters = []
        if bool(product_id) and not bool(contact_id):
            uri = self._get_uri('produtofornecedor').format(codigo=product_id)
        else:
            uri = self._get_uri('produtosfornecedores')

            if product_id:
                filters.append('idProduto[{}]'.format(product_id))

            if contact_id:
                filters.append('idContato[{}]'.format(contact_id))

        params = self._construct_params(filters)
        resp = self._make_request('GET', uri)
        return resp

    def getSaleOrder(self, number=None, issued_date=None, change_date=None, expected_date=None, situation_id=None, contact_id=None):
        """
        Função que busca um Pedido de Venda ou uma lista de Pedidos de Venda.
        :param number: Número do Pedido (opcional);
        :param issued_date: periodo de ['dd/mm/aaaa','dd/mm/aaaa'] (opcional)
        :param change_date: periodo de ['dd/mm/aaaa','dd/mm/aaaa'] (opcional)
        :param expected_date: periodo de ['dd/mm/aaaa','dd/mm/aaaa'] (opcional)
        :param situation_id: in ['P','S'] P-Produto S-Serviço (opcional)
        :param contact_id: in ['A','I'] A-Ativo I-Inativo (opcional)
        
        Caso número seja passado é obrigatório a série e os outros valores serão ignorados.
        """
        filters = []
        if bool(number):
            uri = self._get_uri('pedido').format(numero=number)
        else:
            uri = self._get_uri('pedidos')

            if issued_date:
                if checkData(SELECTDATEDATATYPE, issued_date):
                    filters.append('dataEmissao[{} TO {}]'.format(issued_date[0], issued_date[1]))
                else:
                    raise BlingApiDateSelectError()

            if change_date:
                if checkData(SELECTDATEDATATYPE, change_date):
                    filters.append('dataAlteracao[{} TO {}]'.format(change_date[0], change_date[1]))
                else:
                    raise BlingApiDateSelectError()

            if expected_date:
                if checkData(SELECTDATEDATATYPE, expected_date):
                    filters.append('dataPrevista[{} TO {}]'.format(expected_date[0], expected_date[1]))
                else:
                    raise BlingApiDateSelectError()

            if situation_id:
                filters.append('idSituacao[{}]'.format(situation_id))

            if contact_id:
                filters.append('idContato[{}]'.format(contact_id))

        params = self._construct_params(filters)
        resp = self._make_request('GET', uri, params=params)
        return resp

    def getPurchaseOrder(self, number=None, issued_date=None, situation_id=None):
        """
        Função que busca um Pedido de Compra ou uma lista de Pedidos de Compra.
        :param number: Número do Pedido (opcional);
        :param issued_date: periodo de ['dd/mm/aaaa','dd/mm/aaaa'] (opcional)
        :param situation_id: in ['P','S'] P-Produto S-Serviço (opcional)
        """
        filters = []
        if bool(number):
            uri = self._get_uri('pedidocompra').format(numero=number)
        else:
            uri = self._get_uri('pedidoscompra')

            if issued_date:
                if checkData(SELECTDATEDATATYPE, issued_date):
                    filters.append('dataEmissao[{} TO {}]'.format(issued_date[0], issued_date[1]))
                else:
                    raise BlingApiDateSelectError()

            if situation_id:
                filters.append('idSituacao[{}]'.format(situation_id))

        params = self._construct_params(filters)
        resp = self._make_request('GET', uri, params=params)
        return resp

    def getWarehouses(self, warehouse_id=None):
        """
        Função que busca um determinado depósito ou todos os depósitos.
        :param warehouse_id: Identificador do depósito (opcional);
        """
        if bool(warehouse_id):
            uri = self._get_uri('deposito_id').format(id=warehouse_id)
        else:
            uri = self._get_uri('deposito')

        resp = self._make_request('GET', uri)
        return resp

    def getPaymentMethods(self, payment_method_id=None, description=None, fiscal_code=None, situation_id=None):
        """
        Função que busca um determinado depósito ou todos os depósitos.
        :param payment_method_id: Identificador do Método de Pagamento, inteiro (opcional);
        :param description: Descrição parcial do Método de Pagamento, texto (opcional);
        :param fiscal_code: Código Fiscal do Método de Pagamento, inteiro (opcional);
        :param situation_id: Situação  do Método de Pagamento, inteiro (opcional);
        """
        filters = []
        if bool(payment_method_id):
            uri = self._get_uri('formapagamento_id').format(id=payment_method_id)
        else:
            uri = self._get_uri('deposito')

        if description:
            filters.append('descricao[{}]'.format(description))

        if fiscal_code:
            filters.append('codigoFiscal[{}]'.format(fiscal_code))

        if situation_id:
            filters.append('situacao[{}]'.format(situation_id))

        params = self._construct_params(filters)
        resp = self._make_request('GET', uri, params=params)
        return resp

    def getProductGroup(self, product_group_id=None):
        """
        Função que busca um determinado Grupo de Produtos ou todos os Grupos de Produtos.
        :param product_group_id: Identificador do Grupo de Produtos, inteiro (opcional);
        """
        if bool(product_group_id):
            uri = self._get_uri('grupoprodutos_id').format(id=product_group_id)
        else:
            uri = self._get_uri('grupoprodutos')

        resp = self._make_request('GET', uri)
        return resp

    def getLogisticServices(self, logistic_id=None):
        """
        Função que busca todos os serviços da logistica.
        :param logistic_id: Identificador da logistica, inteiro (opcional);
        """
        if bool(logistic_id):
            uri = self._get_uri('logistica_id_servico').format(id=logistic_id)
        else:
            uri = self._get_uri('logisticaservicos')

        resp = self._make_request('GET', uri)
        return resp

    def getCTes(self, number=None, serie=None, issued_date=None):
        """
        Função que busca um Pedido de Venda ou uma lista de Pedidos de Venda.
        :param number: Número da CTe (opcional);
        :param serie: Série da CTe (opcional/obrigatorio)
        :param issued_date: periodo de ['dd/mm/aaaa','dd/mm/aaaa'] (opcional)
        
        Caso número seja passado é obrigatório a série e os outros valores serão ignorados.
        """
        filters = []
        if bool(number) and bool(serie):
            uri = self._get_uri('cte_number_serie').format(numero=number,serie=serie)
        else:
            uri = self._get_uri('cte')

            if issued_date:
                if checkData(SELECTDATEDATATYPE, issued_date):
                    filters.append('dataEmissao[{} TO {}]'.format(issued_date[0], issued_date[1]))
                else:
                    raise BlingApiDateSelectError()

        params = self._construct_params(filters)
        resp = self._make_request('GET', uri, params=params)
        return resp

    def getNFe(self, number=None, serie=None, issued_date=None, situation=None, type=None):
        """
        Função que busca uma Nota Fiscal ou uma lista de Notas Fiscais.
        :param number: Número da Nota (opcional);
        :param serie: Série da Nota (opcional/obrigatorio)
        :param issued_date: periodo de ['dd/mm/aaaa','dd/mm/aaaa'] (opcional)
        :param situation: in ['P','S'] P-Produto S-Serviço (opcional)
        :param type: in ['A','I'] A-Ativo I-Inativo (opcional)
        
        Caso número seja passado é obrigatório a série e os outros valores serão ignorados.
        """
        filters = []
        if bool(number) and bool(serie):
            uri = self._get_uri('nfe_number_serie').format(numero=number,serie=serie)
        else:
            uri = self._get_uri('nfe')

            if issued_date:
                if checkData(SELECTDATEDATATYPE, issued_date):
                    filters.append('dataEmissao[{} TO {}]'.format(issued_date[0], issued_date[1]))
                else:
                    raise BlingApiDateSelectError()

            if situation:
                filters.append('situacao[{}]'.format(situation))

            if type:
                filters.append('tipo[{}]'.format(type))

        params = self._construct_params(filters)
        resp = self._make_request('GET', uri, params=params)
        return resp

    def getNFCes(self, number=None, serie=None, issued_date=None, situation_id=None):
        """
        Função que busca todas as NFC-es emitidas ou uma determinada NFC-e.
        :param number: Número da NFC-e (opcional);
        :param serie: Série da NFC-e (opcional/obrigatorio)
        :param issued_date: periodo de ['dd/mm/aaaa','dd/mm/aaaa'] (opcional)
        :param situation_id: Situação conforme tabela (opcional)
        
        Caso número seja passado é obrigatório a série e os outros valores serão ignorados.
        """
        filters = []
        if bool(number) and bool(serie):
            uri = self._get_uri('nfce_number_serie').format(numero=number,serie=serie)
        else:
            uri = self._get_uri('nfce')

            if issued_date:
                if checkData(SELECTDATEDATATYPE, issued_date):
                    filters.append('dataEmissao[{} TO {}]'.format(issued_date[0], issued_date[1]))
                else:
                    raise BlingApiDateSelectError()
            if situation_id:
                filters.append('situacao[{}]'.format(situation_id))

        params = self._construct_params(filters)
        resp = self._make_request('GET', uri, params=params)
        return resp

    def getNFSes(self, number=None, issued_date=None, situation_id=None):
        """
        Função que busca todas as NFS-es emitidas ou uma determinada NFS-e.
        :param number: Número da NFS-e (opcional);
        :param serie: Série da NFS-e (opcional/obrigatorio)
        :param issued_date: periodo de ['dd/mm/aaaa','dd/mm/aaaa'] (opcional)
        :param situation_id: Situação conforme tabela (opcional)
        """
        filters = []
        if bool(number):
            uri = self._get_uri('nfse_number').format(numero=number)
        else:
            uri = self._get_uri('nfse')

            if issued_date:
                if checkData(SELECTDATEDATATYPE, issued_date):
                    filters.append('dataEmissao[{} TO {}]'.format(issued_date[0], issued_date[1]))
                else:
                    raise BlingApiDateSelectError()
            if situation_id:
                filters.append('situacao[{}]'.format(situation_id))

        params = self._construct_params(filters)
        resp = self._make_request('GET', uri, params=params)
        return resp

    def getProductionOrder(self,number=None,page=None):
        """
        Função que busca todas as Ordens de Produção.
        :param page: Número da página de retorno (de 100 em 100 ordens);
        """
        if bool(number):
            uri = self._get_uri('ordemproducao').format(numero=number)
        else:
            uri = self._get_uri('ordensproducao').format(page=page)

        resp = self._make_request('GET', uri)
        return resp

    def getProductStore(self, sku):
        """
        Função que retorna a loja vinculada ao produto.
        :param sku: Código do Produto (SKU);
        """
        uri = self._get_uri('produtoloja').format(numero=sku)

        resp = self._make_request('GET', uri)
        return resp

    def getCommercialProposal(self, number=None, issued_date=None, situation_id=None, contact_id=None):
        """
        Função que busca uma Proposta Comercial ou uma lista de Propostas Comerciais.
        :param number: Número da Proposta Comercial (opcional);
        :param issued_date: periodo de ['dd/mm/aaaa','dd/mm/aaaa'] (opcional)
        :param situation_id: in ['P','S'] P-Produto S-Serviço (opcional)
        :param contact_id: in ['A','I'] A-Ativo I-Inativo (opcional)
        """
        filters = []
        if bool(number):
            uri = self._get_uri('propostacomercial').format(numero=number)
        else:
            uri = self._get_uri('propostascomerciais')

            if issued_date:
                if checkData(SELECTDATEDATATYPE, issued_date):
                    filters.append('data[{} TO {}]'.format(issued_date[0], issued_date[1]))
                else:
                    raise BlingApiDateSelectError()

            if situation_id:
                filters.append('situacao[{}]'.format(situation_id))

            if contact_id:
                filters.append('idContato[{}]'.format(contact_id))

        params = self._construct_params(filters)
        resp = self._make_request('GET', uri, params=params)
        return resp

    def postContact(self, contact_id=None, **kwargs):
        """
        Função que Insere um contato ou altera um contato.
        :param contact_id: Identificador do contato (opcional).
        :param kwargs: Dict com informações para gerar o xml (obrigatório).
        Caso contact_id seja passado será realizado uma alteração, caso seja None o contato será criado.
        """
        if bool(contact_id):
            uri = self._get_uri('contato').format(idContato=contact_id)
        else:
            uri = self._get_uri('contato',method='POST')
        if "xml" not in kwargs:
            xml = self.render_xml_contact(**kwargs)
        else:
            xml = kwargs['xml']
        payload = {
            'xml': xml,
        }
        resp = self._make_request('POST', uri, data=payload)
        return resp

    def postProduct(self, sku=None, **kwargs):
        """
        Função que altera um produto pelo seu SKU ou insere um novo produto.
        :param sku: Código SKU do produto (obrigatorio);
        :param kwargs: Dict com informações para gerar o xml (obrigatório).
        Caso sku seja passado será realizado uma alteração, caso seja None o produto será criado.
        """    
        if bool(sku):
            uri = self._get_uri('produto').format(codigo=sku)
        else:
            uri = self._post_uri('produto')
            
        if "xml" not in kwargs:
            xml = self.render_xml_product(**kwargs)
        else:
            xml = kwargs['xml']
        payload = {
            'xml': xml,
        }
        resp = self._make_request('POST', uri, data=payload)
        return resp

    def updateStock(self, sku, quantity):
        """
        Função que altera a quatidade de um produto pelo seu sku.
        :param sku: Código SKU do produto (obrigatorio);
        :param quantity: Valor decimal de quantidade (obrigatorio)
        """
        vals = {
            'produto': {
                'codigo': sku,
                'estoque': quantity,
            },
        }
        xml = {
            'xml': self.render_xml_product(**vals),
        }
        
        return self.postProduct(**xml)

    def _construct_params(self, filters):
        """
        Função construtora dos parametros, transforma a string filters e converte em lista.
        :param filters: string com os parametros a serem convertidos;
        """
        res = dict()
        if len(filters) > 0:
            filters_value = ';'.join(filters)
            res['filters'] = filters_value
        else:
            res = None
        return res
        
    def _render(self, resource, **kwargs):
        """
        Busca o arquivo de template, juntamente com o dicionário de dados e envia a rotina de renderização. 
        :param resource: Nome do recurso a ser renderizado;
        :param kwargs: Dicionário contendo os dados para a renderização.
        """
        path = os.path.join(os.path.dirname(__file__), 'templates')
        xmlElem_send = render_xml(path, '%s.xml' % resource, True, **kwargs)
        xml_send = '<?xml version="1.0" encoding="UTF-8"?>'+etree.tostring(xmlElem_send, encoding=str)
        return xml_send

    def _get_uri(self, resource):
        """
        Obtem a URI de GET para o envio do resource.
        :param resource: Nome no recurso para retorno da url.
        """
        return localizar_uri(resource, METHOD_GET)

    def _post_uri(self, resource):
        """
        Obtem a URI de POST para o envio do resource.
        :param resource: Nome no recurso para retorno da url.
        """
        return localizar_uri(resource,METHOD_POST)

    def _put_uri(self, resource):
        """
        Obtem a URI de POST para o envio do resource.
        :param resource: Nome no recurso para retorno da url.
        """
        return localizar_uri(resource,METHOD_PUT)

    def _delete_uri(self, resource):
        """
        Obtem a URI de POST para o envio do resource.
        :param resource: Nome no recurso para retorno da url.
        """
        return localizar_uri(resource,METHOD_DELETE)

    def _make_request(self, method, uri, params=None, data=None):
        """
        Eniva a requisição wsdl na URI com o methodo passando o parametros e dados.
        :param method: Método de chamada a URI [GET,POST,PUT]
        :param uri: a URI da chamada;
        :param params: Lista de parametros a ser enviada junto ao metodo.
        :param: data: Dados passados na requisição.
        """
        logger.info('method = {}'.format(method))
        logger.info('uri = {}'.format(uri))
        logger.info('params = {}'.format(params))
        logger.info('data = {}'.format(data))
        url = '{}/{}?apikey={}'.format(uri, self.file_format, self.api_key)
        logger.info('url = {}'.format(url))
        if  method in ['PUT','GET','POST','DELETE']:
            try:
                resp = self.session.request(method, url, data=data, params=params)
                logger.debug(resp)
                resp.raise_for_status()
                if self.file_format == 'json':
                    return resp.json()
                else:
                    return resp.content
            except requests.exceptions.HTTPError as e:
                raise BlingApiRequestError(e.request, e.response)
            except requests.exceptions.RequestException as e:
                raise BlingApiRequestError(e.request)
        else:
            raise BlingApiMethodError(method)

    def render_xml_category(self, **kwargs):
        """
        Renderiza o xml da categoria.
        :param kwargs: Dicionário contendo os dados da renderização.
        """
        return self._render('categoria', **kwargs)

    def render_xml_store_category(self, **kwargs):
        """
        Renderiza o xml da categoria.
        :param kwargs: Dicionário contendo os dados da renderização.
        """
        return self._render('categoriaLoja', **kwargs)
    
    def render_xml_bill_to_pay(self, **kwargs):
        """
        Renderiza o xml da Contas a Pagar.
        :param kwargs: Dicionário contendo os dados da renderização.
        """
        return self._render('contapagar', **kwargs)
    
    def render_xml_bill_to_receive(self, **kwargs):
        """
        Renderiza o xml da Contas a Receber.
        :param kwargs: Dicionário contendo os dados da renderização.
        """
        return self._render('contareceber', **kwargs)
    
    def render_xml_contact(self, **kwargs):
        """
        Renderiza o xml do Contato.
        :param kwargs: Dicionário contendo os dados da renderização.
        """
        return self._render('contato', **kwargs)
    
    def render_xml_contract(self, **kwargs):
        """
        Renderiza o xml do Contrato.
        :param kwargs: Dicionário contendo os dados da renderização.
        """
        return self._render('contrato', **kwargs)
    
    def render_xml_warehouse(self, **kwargs):
        """
        Renderiza o xml do depósito.
        :param kwargs: Dicionário contendo os dados da renderização.
        """
        return self._render('deposito', **kwargs)
    
    def render_xml_payment_methods(self, **kwargs):
        """
        Renderiza o xml do Forma de Pagamento.
        :param kwargs: Dicionário contendo os dados da renderização.
        """
        return self._render('formapagamento', **kwargs)
    
    def render_xml_logistics(self, **kwargs):
        """
        Renderiza o xml da logistica.
        :param kwargs: Dicionário contendo os dados da renderização.
        """
        return self._render('logistica', **kwargs)
    
    def render_xml_consumer_invoice(self, **kwargs):
        """
        Renderiza o xml da Fatura de Venda.
        :param kwargs: Dicionário contendo os dados da renderização.
        """
        return self._render('nfce', **kwargs)
    
    def render_xml_invoice(self, **kwargs):
        """
        Renderiza o xml da NFe.
        :param kwargs: Dicionário contendo os dados da renderização.
        """
        return self._render('nfe', **kwargs)
    
    def render_xml_service_invoice(self, **kwargs):
        """
        Renderiza o xml da NFSe.
        :param kwargs: Dicionário contendo os dados da renderização.
        """
        return self._render('nfse', **kwargs)
    
    def render_xml_production_order(self, **kwargs):
        """
        Renderiza o xml da Ordem de Produção.
        :param kwargs: Dicionário contendo os dados da renderização.
        """
        return self._render('ordemproducao', **kwargs)
    
    def render_xml_sale_order(self, **kwargs):
        """
        Renderiza o xml do Pedido de Venda.
        :param kwargs: Dicionário contendo os dados da renderização.
        """
        return self._render('pedido', **kwargs)
    
    def render_xml_product(self, **kwargs):
        """
        Renderiza o xml do Produto.
        :param kwargs: Dicionário contendo os dados da renderização.
        """
        return self._render('produto', **kwargs)
    
    def render_xml_event_tracking(self, **kwargs):
        """
        Renderiza o xml do Envento de Rastreamento.
        :param kwargs: Dicionário contendo os dados da renderização.
        """
        return self._render('rastreamentoevento', **kwargs)
    
    def render_xml_link_tracking(self, **kwargs):
        """
        Renderiza o xml do Vinculo de Rastreamento.
        :param kwargs: Dicionário contendo os dados da renderização.
        """
        return self._render('rastreamentovincular', **kwargs)

