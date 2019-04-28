import requests, json, base64, platform


def singleton(cls, *args, **kw):
    instances = {}
    def _singleton():
        if cls not in instances:
            instances[cls] = cls(*args, **kw)
        return instances[cls]
    return _singleton

@singleton
class Pedatren:
    __instance = None
    __baseUrl = ''
    __headers = {
        'content-type' : 'application/json',
        'connection' : 'keep-alive',
        'User-Agent' : 'App/0.1.0 Gerbang Pos Desktop '+ platform.system() + ' ' + platform.node() + ' ' + platform.machine() + ' ' + platform.processor()
    }
    __token = ''
    credentials = ''

    def __init__(self):
        self.__baseUrl = 'http://207.148.75.98:3000/api/v1'

    def getToken(self):
        return self.__token

    def getHeaders(self):
        return self.__headers

    def login(self, username=None, password=None):
        # saat login jika dengan self.__headers yg sudah ada token, maka akan selalu ok dan adalah user di token, bukan dari user & pass yg dikirim
        freshHeaders = {
            'content-type' : 'application/json',
            'connection' : 'keep-alive',
            'User-Agent' : 'App/0.1.0 Gerbang Pos Desktop '+ platform.system() + ' ' + platform.node() + ' ' + platform.machine() + ' ' + platform.processor()
        }

        response = requests.get(self.__baseUrl + '/auth/login', headers=freshHeaders, auth=(username,password))

        if response.status_code >= 200 and response.status_code < 300:
            self.__token = response.headers['x-token']
            self.__headers['x-token'] = response.headers['x-token']
            jwtPayload = response.headers['x-token'].split('.')[0]
            jwtPayload += "=" * ((4 - len(jwtPayload) % 4) % 4)
            self.credentials = json.loads(base64.b64decode(jwtPayload))

        else:
            self.__token = ''
            self.__headers.pop('x-token', None)

        return response

    def getListPerizinan(self):
        response = requests.get(self.__baseUrl + '/penjagapos/perizinan/santri', headers=self.__headers)
        return response

    def getItemPerizinan(self, id_perizinan):
        response = requests.get(self.__baseUrl + '/penjagapos/perizinan/santri/' + id_perizinan, headers=self.__headers)
        return response

    def getImage(self, relative_path):
        response = requests.get(self.__baseUrl + relative_path, headers=self.__headers)
        return response

    def getUserProfile(self):
        response = requests.get(self.__baseUrl + '/person/' + str(self.credentials['uuid_person']), headers=self.__headers)
        return response
