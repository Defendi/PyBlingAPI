
from pyblingapi import xml_categoria

categorias = {
    'categorias': [
    {
    'descricao': 'catgoria 01',
    'idCategoriaPai': '1',
    },
    {
    'descricao': 'catgoria 02',
    'idCategoriaPai': '2',
    },
    {
    'descricao': 'catgoria 03',
    'idCategoriaPai': '3',
    },
]}
 
xml = xml_categoria(**categorias)

print(xml)   