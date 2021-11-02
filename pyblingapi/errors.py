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

class BlingApiRequestError(Exception):
    def __init__(self, request, response=None):
        self.request = request
        self.response = response
        self.message = 'Falha na resposta da requisição %s, %s' % (str(request),str(response)) if bool(response) \
                       else 'Falha da requisição %s' % str(request)

    def __str__(self):
        return self.message

class BlingApiDateSelectError(Exception):
    def __init__(self):
        self.message = "Seleção entre datas é inválida. Utilize uma lista com 2 itens: [data_inicial,data_final], usando o padrão 'dd/mm/AAAA'"
        
    def __str__(self):
        return self.message

class BlingApiTypeContactError(Exception):
    def __init__(self):
        self.message = "O tipo de contato deve ser 'F' (Física), 'J' (Jurídica) ou 'E' para extrangeiros"
        
    def __str__(self):
        return self.message

class BlingStateError(Exception):
    def __init__(self, state):
        self.message = "A sistuação %s não existe." % str(state)
        
    def __str__(self):
        return self.message

class BlingApiMethodError(Exception):
    def __init__(self,Method):
        self.message = "O método %s é desconhecido ou inexistente. Utilize os seguintes métodos [GET,POST,PUT,DELETE]" % str(Method)
        
    def __str__(self):
        return self.message

class BlingApiResourceMethodError(Exception):
    def __init__(self,Resource,Method):
        self.message = "O recurso %, método %s, não possuí URL específica. Favor consulte o manual do Bling" % (str(Resource),str(Method))
        
    def __str__(self):
        return self.message
