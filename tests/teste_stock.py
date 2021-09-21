from pyblingapi import BlingApi

Bling = BlingApi('api-key')

xml = Bling.updateStock(sku='codigo', qty=10)

print(xml)