import geotab
import requests, json, mpu, time, sys
from math import degrees, atan, cos, sin, atan2


def getProx(compare, target, data):
    print(f'Devices to compare: {len(compare.getLat())}')

    aryReturn = []
    inRange = 0
    aryTmp = []

    aryTmp.append(target.getLat()[0])
    aryTmp.append(target.getLong()[0])
    aryReturn.append(aryTmp)

    for x in range(len(compare.getLat())):
        proximity = getDistance(compare.getLat()[x], compare.getLong()[x], target.getLat()[0], target.getLong()[0])
        aryTmp = []

        if proximity < __proximity:
            print(f'Device: {compare.getId()[x]} is {proximity} meters away, at bearing: {getBearing(compare.getLat()[x], compare.getLong()[x], target.getLat()[0], target.getLong()[0])}')
            inRange += 1
            aryTmp.append(compare.getLat()[x])
            aryTmp.append(compare.getLong()[x])
            aryTmp.append(compare.getBearing()[x])
            aryTmp.append(compare.getSpeed()[x])
            aryTmp.append(compare.getDrivingStatus()[x])
            aryTmp.append(proximity)
            aryReturn.append(aryTmp)

    print(f'Devices in range: {inRange}')
    return aryReturn


def getDistance(lat1, lon1, lat2, lon2):
    dist = mpu.haversine_distance((lat1, lon1), (lat2, lon2)) * 1000
    return int(round(dist, 2))

def getBearing(lat1, lon1, lat2, lon2):
    Bearing = degrees(atan2(cos(lat1)*sin(lat2)-sin(lat1)*cos(lat2)*cos(lon2-lon1), sin(lon2-lon1)*cos(lat2)))
    Bearing = int((Bearing/22.5)+.5)
    arr=["N","NNE","NE","ENE","E","ESE", "SE", "SSE","S","SSW","SW","WSW","W","WNW","NW","NNW"]
    return arr[(Bearing % 16)]

#If you wish to run without arguments passed to script, provide values to the variables below
#Script Args
__userName1 = ""
__password1 = ""
__database1 = ""

__userName2 = ""
__password2 = ""
__database2 = ""

__targetDevice = ""
__proximity = 5000
#End Script Args

print("\nThis script will accept the following format of command line arguments:\n")
print("(Scenario 1): script.py Username, Password, Database 1, Database 2, Target Device ID In Database 2, Proximity (Meters)")
print("(Scenario 2): script.py Username 1, Password 1, Database 1, Username 2, Password 2, Database 2, Target Device ID In Database 2, Proximity (Meters)\n")


if len(sys.argv) == 1:
    print("You did not pass any arugments. If arguments are present in the script, it will continue to run. Otherwise it will close.\n")
    if (__userName1 == "") or (__password1 == "") or (__database1 == "") or (__userName2 == "") or (__password2 == "") or (__database2 == "") or (__targetDevice == ""):
        exit()
elif len(sys.argv) == 9:
    print("Scenario 1")
    __userName1 = sys.argv[1]
    __password1 = sys.argv[2]
    __database1 = sys.argv[3]
    __userName2 = sys.argv[4]
    __password2 = sys.argv[5]
    __database2 = sys.argv[6]
    __targetDevice = sys.argv[7]

    try:
        __proximity = int(sys.argv[8])
        print(f'Proximity: {__proximity}')
    except:
        print(f'Proximity argument: {sys.argv[8]} invalid. Falling back to default: {__proximity}')
elif len(sys.argv) == 7:
    print("Scenario 2")
    __userName1 = sys.argv[1]
    __userName2 = sys.argv[1]
    __password1 = sys.argv[2]
    __password2 = sys.argv[2]
    __database1 = sys.argv[3]
    __database2 = sys.argv[4]
    __targetDevice = sys.argv[5]

    try:
        __proximity = int(sys.argv[6])
        print(f'Proximity: {__proximity}')
    except:
        print(f'Proximity argument: {sys.argv[8]} invalid. Falling back to default: {__proximity}')  
else:
    print(f'Unknown Arguments, you entered: {sys.argv}')
    exit()


databaseCompare = geotab.Geotab(__userName1, __password1, __database1)
databaseTarget = geotab.Geotab(__userName2, __password2, __database2)

if databaseCompare.authenticate() == False:
    print(databaseCompare.getError())
    exit()

if databaseTarget.authenticate() == False:
    print(databaseTarget.getError())
    exit()
    
while databaseCompare.getAuthStatus and databaseTarget.getAuthStatus:    
    arrayData = []
    if databaseCompare.getGeotabLocations("") == False:
        print(databaseCompare.getError())
        exit()

    if databaseTarget.getGeotabLocations(__targetDevice) == False:
        print(databaseTarget.getError())
        exit()

    arrayData2 = getProx(databaseCompare, databaseTarget, arrayData)    

    print("")

    time.sleep(10)