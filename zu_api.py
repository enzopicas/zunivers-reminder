import requests
import json

#Check if user is registred ZUnivers player
def CheckUser(username, tag):
    if str(tag) != "0":
        code = requests.get("https://zunivers-api.zerator.com/public/user/" + username + "%23" + tag).status_code
    else:
        code = requests.get("https://zunivers-api.zerator.com/public/user/" + username).status_code

    if code == 200:
        return True
    else:
        return False

#Check activity of a specific player
def CheckActivity(username, tag):
    if str(tag) != "0":
        r = json.loads(requests.get("https://zunivers-api.zerator.com/public/user/"+str(username)+"%23"+str(tag)+"/activity").content)
    else:
        r = json.loads(requests.get("https://zunivers-api.zerator.com/public/user/"+str(username)+"/activity").content)

    loot = r['lootInfos']

    if loot[-1]['count'] > 0:
        return True
    else:
        return False

def CheckAs(username, tag):
    if str(tag) != "0":
        r = json.loads(requests.get("https://zunivers-api.zerator.com/public/tower/"+str(username)+"%23"+str(tag)).content)
    else:
        r = json.loads(requests.get("https://zunivers-api.zerator.com/public/tower/"+str(username)).content)

    towerStats = r['towerStats']

    print(towerStats[0]['towerSeasonIndex'])

    if towerStats[0]['maxFloorIndex'] < 5:
        return False # New !as available
    else:
        return True # Already on top
