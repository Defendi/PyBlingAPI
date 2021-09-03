from pyblingapi import BlingApi

Bling = BlingApi('44d23f8acdb04dce6293af6bb417c8bb9654c666134fc59b7682fd4ae16d870a2095dcfd')

resp = Bling.getCategory('3279036')

print(resp)
