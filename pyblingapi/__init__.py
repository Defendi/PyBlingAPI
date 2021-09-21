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
from pyblingapi.servidor import localizar_uri
from pyblingapi.errors import BlingApiRequestError, BlingApiDateSelectError, BlingApiTypeContactError
from pyblingapi.tools import checkData, SELECTDATEDATATYPE

logger = logging.getLogger(__name__)

class BlingApi(object):

    def __init__(self, api_key, file_format='json'):
        self.api_key = api_key
        self.session = requests.Session()
        self.file_format = str(file_format).lower()

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
            uri = self._get_uri('categorias').format(idCategoria=categoy_id)
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

            if not bool(id_type) or id_type == 'cnpj':
                filters.append('identificador[1]')
            else:
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

    def getProductBySupplier(self, sku, supplier_id):
        """
        Função que busca um produto pelo Fornecedor.
        :param sku: Código SKU do produto (obrigatorio);
        :param supplier_id: Identificador do fornecedor (obrigatorio)
        """
        uri = self._get_uri('produtosfornecedor').format(codigo=sku,id_fornecedor=supplier_id)
        resp = self._make_request('GET', uri)
        return resp

    def getInvoice(self, number=None, serie=None, issued_date=None, situation=None, type=None):
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
            uri = self._get_uri('notafiscal').format(numero=number,serie=serie)
        else:
            uri = self._get_uri('notafiscais')

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

    def getOrder(self, number=None, issued_date=None, change_date=None, expected_date=None, situation_id=None, contact_id=None):
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
        
    def _construct_params(self, filters):
        res = dict()
        if len(filters) > 0:
            filters_value = ';'.join(filters)
            res['filters'] = filters_value
        else:
            res = None
        return res
        
    def _render(self, resource, **kwargs):
        path = os.path.join(os.path.dirname(__file__), 'templates')
        xmlElem_send = render_xml(path, '%s.xml' % resource, True, **kwargs)
        xml_send = '<?xml version="1.0" encoding="UTF-8"?>'+etree.tostring(xmlElem_send, encoding=str)
        return xml_send

    def _get_uri(self, resource):
        return localizar_uri(resource)

    def _post_uri(self, resource):
        return localizar_uri(resource,method='POST')

    def _make_request(self, method, uri, params=None, data=None):
        logger.info('method = {}'.format(method))
        logger.info('uri = {}'.format(uri))
        logger.info('params = {}'.format(params))
        logger.info('data = {}'.format(data))
        url = '{}/{}?apikey={}'.format(uri, self.file_format, self.api_key)
        logger.info('url = {}'.format(url))
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

    def render_xml_category(self, **kwargs):
        return self._render('categoria', **kwargs)

    def render_xml_store_category(self, **kwargs):
        return self._render('categoriaLoja', **kwargs)
    
    def render_xml_bill_to_pay(self, **kwargs):
        return self._render('contapagar', **kwargs)
    
    def render_xml_bill_to_receive(self, **kwargs):
        return self._render('contareceber', **kwargs)
    
    def render_xml_contact(self, **kwargs):
        return self._render('contato', **kwargs)
    
    def render_xml_contract(self, **kwargs):
        return self._render('contrato', **kwargs)
    
    def render_xml_warehouse(self, **kwargs):
        return self._render('deposito', **kwargs)
    
    def render_xml_payment_methods(self, **kwargs):
        return self._render('formapagamento', **kwargs)
    
    def render_xml_logistics(self, **kwargs):
        return self._render('logistica', **kwargs)
    
    def render_xml_consumer_invoice(self, **kwargs):
        return self._render('nfce', **kwargs)
    
    def render_xml_invoice(self, **kwargs):
        return self._render('nfe', **kwargs)
    
    def render_xml_service_invoice(self, **kwargs):
        return self._render('nfse', **kwargs)
    
    def render_xml_production_order(self, **kwargs):
        return self._render('ordemproducao', **kwargs)
    
    def render_xml_sale_order(self, **kwargs):
        return self._render('pedido', **kwargs)
    
    def render_xml_product(self, **kwargs):
        return self._render('produto', **kwargs)
    
    def render_xml_event_tracking(self, **kwargs):
        return self._render('rastreamentoevento', **kwargs)
    
    def render_xml_link_tracking(self, **kwargs):
        return self._render('rastreamentovincular', **kwargs)

