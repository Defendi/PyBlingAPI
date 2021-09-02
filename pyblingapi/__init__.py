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

from lxml import etree
from pyblingapi.xml import render_xml

_logger = logging.getLogger(__name__)

def _render(method, **kwargs):
    path = os.path.join(os.path.dirname(__file__), 'templates')
    xmlElem_send = render_xml(path, '%s.xml' % method, False, **kwargs)
    xml_send = '<?xml version="1.0" encoding="UTF-8"?>'+etree.tostring(xmlElem_send, encoding=str)
    return xml_send

def xml_categoria(**kwargs):
    return _render('categoria', **kwargs)

def xml_categoria_loja(**kwargs):
    return _render('categoriaLoja', **kwargs)

def xml_conta_pagar(**kwargs):
    return _render('contapagar', **kwargs)

def xml_conta_receber(**kwargs):
    return _render('contareceber', **kwargs)

def xml_contato(**kwargs):
    return _render('contato', **kwargs)

def xml_contrato(**kwargs):
    return _render('contrato', **kwargs)

def xml_deposito(**kwargs):
    return _render('deposito', **kwargs)

def xml_forma_pagamento(**kwargs):
    return _render('formapagamento', **kwargs)

def xml_logistica(**kwargs):
    return _render('logistica', **kwargs)

def xml_nfce(**kwargs):
    return _render('nfce', **kwargs)

def xml_nfe(**kwargs):
    return _render('nfe', **kwargs)

def xml_nfse(**kwargs):
    return _render('nfse', **kwargs)

def xml_ordem_producao(**kwargs):
    return _render('ordemproducao', **kwargs)

def xml_pedido(**kwargs):
    return _render('pedido', **kwargs)

def xml_produto(**kwargs):
    return _render('produto', **kwargs)

def xml_rastreamento_evento(**kwargs):
    return _render('rastreamentoevento', **kwargs)

def xml_rastreamento_vincular(**kwargs):
    return _render('rastreamentovincular', **kwargs)


