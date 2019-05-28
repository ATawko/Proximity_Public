import requests, json

class Geotab:
    """Main Geotab class, handles api requests & authentication"""

    def __init__(self, username, password, database):
        """Init method - defines variables & authenticates with Geotab"""
        self.__authenticated = False
        self.__locationStatus = False

        self.__geotabUsername = username
        self.__geotabPassword = password
        self.__geotabDatabase = database
        self.__geotabSessionID = ''
        self.__geotabServer = ''
        self.__errorMessage = ''

        self.__geotabLats = []
        self.__geotabLongs = [] 
        self.__geotabBearings = []
        self.__geotabDrivingStatus = []
        self.__geotabSpeed = []
        self.__geotabID = []


    def getLat(self): return self.__geotabLats
    def getLong(self): return self.__geotabLongs
    def getBearing(self): return self.__geotabBearings
    def getDrivingStatus(self): return self.__geotabDrivingStatus
    def getSpeed(self): return self.__geotabSpeed
    def getId(self): return self.__geotabID

    def getLocationStatus(self): return self.__locationStatus
    def getAuthStatus(self): return self.__authenticated
    def getError(self): return self.__errorMessage
    
    def __resetGeotabData(self):
        self.__geotabLats = []
        self.__geotabLongs = [] 
        self.__geotabBearings = []
        self.__geotabDrivingStatus = []
        self.__geotabSpeed = []
        self.__geotabID = []

    def authenticate(self):
        url = f'https://my.geotab.com/apiv1/Authenticate?database={self.__geotabDatabase}&userName={self.__geotabUsername}&password={self.__geotabPassword}'
        __resp = requests.get(url)
        __objResp = json.loads(__resp.content)

        if 'result' in __objResp:
            self.__geotabSessionID = __objResp['result']['credentials']['sessionId']
            self.__geotabServer = __objResp['result']['path']
            self.__authenticated = True
            return True
        else:
            self.__errorMessage = f"Error Message: {__objResp['error']['message']} - Error Name: {__objResp['error']['name']})"
            return False

    def getGeotabLocations(self, id):
        self.__resetGeotabData()
        if self.__authenticated == True:
            if id == "":
                #Get all devices
                url = 'https://' + self.__geotabServer + '/apiv1/ExecuteMultiCall?calls=[{"method":"Get","params":{"typeName":"DeviceStatusInfo"}}]&credentials={"database":"'+ self.__geotabDatabase +'","userName":"' + self.__geotabUsername + '","sessionId":"' + self.__geotabSessionID +'"}'
            else:
                #Get one device
                url = 'https://' + self.__geotabServer + '/apiv1/ExecuteMultiCall?calls=[{"method":"Get","params":{"typeName":"DeviceStatusInfo","search":{"deviceSearch":{"id":"' + id + '"}}}}]&credentials={"database":"' + self.__geotabDatabase + '","userName":"' + self.__geotabUsername + '","sessionId":"' + self.__geotabSessionID + '"}'

            __resp = requests.get(url)
            __objResp = json.loads(__resp.content)

            if 'result' in __objResp:
                for device in __objResp['result'][0]:
                    self.__geotabLats.append(device['latitude'])
                    self.__geotabLongs.append(device['longitude'])
                    self.__geotabBearings.append(device['bearing'])
                    self.__geotabDrivingStatus.append(device['isDriving'])
                    self.__geotabSpeed.append(device['speed'])
                    self.__geotabID.append(device['device']['id'])
                    
                self.__locationStatus = True
                return True
            else:
                self.__errorMessage = f"Error Message: {__objResp['error']['message']} - Error Name: {__objResp['error']['name']})"
                self.__locationStatus = False
                return False
        else:
            self.__locationStatus = False
            return False
        