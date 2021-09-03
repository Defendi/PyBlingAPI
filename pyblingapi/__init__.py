# © 2021 Alexandre Defendi, Nexuz System
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
#    _   __                         _____            __               
#   / | / /__  _  ____  ______     / ___/__  _______/ /____  ____ ___ 
#  /  |/ / _ \| |/_/ / / /_  /     \__ \/ / / / ___/ __/ _ \/ __ `__ \
# / /|  /  __/>  </ /_/ / / /_    ___/ / /_/ (__  ) /_/  __/ / / / / /
#/_/ |_/\___/_/|_|\__,_/ /___/   /____/\__, /____/\__/\___/_/ /_/ /_/ 
#                                     /____/                          

import os
import logging
import requests

from lxml import etree
from pyblingapi.xml import render_xml
from pyblingapi.servidor import localizar_uri

logger = logging.getLogger(__name__)

class BlingApi(object):

    def __init__(self, api_key, file_format='json'):
        self.api_key = api_key
        self.session = requests.Session()
        self.file_format = str(file_format).lower()

    def getCategories(self):
        uri = self._method_uri('categorias')
        resp = self._make_request('GET', uri)
        return resp

    def getCategory(self, idCategoria):
        uri = self._method_uri('categoria').format(idCategoria=idCategoria)
        resp = self._make_request('GET', uri)
        return resp

    def _render(self, resource, **kwargs):
        path = os.path.join(os.path.dirname(__file__), 'templates')
        xmlElem_send = render_xml(path, '%s.xml' % resource, False, **kwargs)
        xml_send = '<?xml version="1.0" encoding="UTF-8"?>'+etree.tostring(xmlElem_send, encoding=str)
        return xml_send

    def _method_uri(self, resource):
        return localizar_uri(resource)

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
            raise BlingError(e.request, e.response)
        except requests.exceptions.RequestException as e:
            raise BlingError(e.request)

    def xml_categoria(self, **kwargs):
        return self._render('categoria', **kwargs)

    def xml_categoria_loja(self, **kwargs):
        return self._render('categoriaLoja', **kwargs)
    
    def xml_conta_pagar(self, **kwargs):
        return self._render('contapagar', **kwargs)
    
    def xml_conta_receber(self, **kwargs):
        return self._render('contareceber', **kwargs)
    
    def xml_contato(self, **kwargs):
        return self._render('contato', **kwargs)
    
    def xml_contrato(self, **kwargs):
        return self._render('contrato', **kwargs)
    
    def xml_deposito(self, **kwargs):
        return self._render('deposito', **kwargs)
    
    def xml_forma_pagamento(self, **kwargs):
        return self._render('formapagamento', **kwargs)
    
    def xml_logistica(self, **kwargs):
        return self._render('logistica', **kwargs)
    
    def xml_nfce(self, **kwargs):
        return self._render('nfce', **kwargs)
    
    def xml_nfe(self, **kwargs):
        return self._render('nfe', **kwargs)
    
    def xml_nfse(self, **kwargs):
        return self._render('nfse', **kwargs)
    
    def xml_ordem_producao(self, **kwargs):
        return self._render('ordemproducao', **kwargs)
    
    def xml_pedido(self, **kwargs):
        return self._render('pedido', **kwargs)
    
    def xml_produto(self, **kwargs):
        return self._render('produto', **kwargs)
    
    def xml_rastreamento_evento(self, **kwargs):
        return self._render('rastreamentoevento', **kwargs)
    
    def xml_rastreamento_vincular(self, **kwargs):
        return self._render('rastreamentovincular', **kwargs)

class BlingError(Exception):
    def __init__(self, request, response=None):
        self.request = request
        self.response = response

