import requests
import json
import os.path, time
import pathlib
import datetime

from AnimeEntry import AnimeEntry
from refreshtoken import refresh_token



API_getUserListURL = ('https://api.myanimelist.net/v2/users/{}/animelist?fields=list_status&limit=1000')
API_getMostPopularListURL = ('https://api.myanimelist.net/v2/anime/ranking?ranking_type=bypopularity&limit=500')

userAnimeList_ID = []
sortedList = []

def load_access_token():

    f = open('token.json')
    data = json.load(f)
    
    fname = pathlib.Path('token.json')
    creation_time = datetime.datetime.fromtimestamp(fname.stat().st_ctime)
    expiration_time = creation_time + datetime.timedelta(seconds =  data["expires_in"])
    
    if expiration_time >= datetime.datetime.now():
        refresh_token()
        f = open('token.json')
        data = json.load(f)
    return data


def getUserList_api(username, my_headers):
    try:
        
        data = requests.get(API_getUserListURL.format(username), headers=my_headers).json()
    except Exception as exc:
        print(exc)
        data = None
    return data

def getPopularityRanking_api(my_headers):
    try:
        
        data = requests.get(API_getMostPopularListURL, headers=my_headers).json()
    except Exception as exc:
        print(exc)
        data = None 
    return data

def appendInList(username, my_headers):

    resp = getUserList_api(username, my_headers)
   
    next = True
    i=0
    while(next):
        

        for x in resp["data"]:

            status = resp["data"][i]["list_status"]["status"]
            if status == "completed":
                status = "Completed"
            elif status == "plan_to_watch":
                status = "Plan To Watch"
            elif status == "watching":
                status = "Watching"
            elif status == "dropped":
                status = "Dropped"
            else:
                status = "On Hold"
            userAnimeList_ID.append(AnimeEntry(resp["data"][i]["node"]["title"], resp["data"][i]["node"]["id"], "", resp["data"][i]["node"]["main_picture"]["medium"], status, resp["data"][i]["list_status"]["score"]))
            i+=1

           
                
        if ("next" in resp["paging"]):
            resp = requests.get(resp["paging"]["next"].format(username), headers=my_headers).json()
            next = True
        else:
            next = False
            
                
        

def sortListbyPopularity(username):
        
    try:
        token_data = load_access_token()
        my_headers = {'Authorization' : token_data["token_type"] + ' ' + token_data["access_token"]}
        userAnimeList_ID.clear()
        sortedList.clear()
        appendInList(username, my_headers)
        resp = getPopularityRanking_api(my_headers) 

        next = True

        while(next):
            i = 0
            
            for x in resp["data"]:
                tempAnimeID = resp["data"][i]["node"]["id"]
                for x in userAnimeList_ID:
                    if tempAnimeID == x.getId():
                        x.setGlobalRanking(resp["data"][i]["ranking"]["rank"])
                        sortedList.append(x)

                i+=1

            if ("next" in resp["paging"]):
                resp = requests.get(resp["paging"]["next"].format(username), headers=my_headers).json()
                next = True
            else:
                next = False
            
    except:
        sortedList.clear()
    return sortedList

def sortByStatusList(status):

    
    sortedList_byStatus = []
    for x in sortedList:
        if status == x.getStatus():
            sortedList_byStatus.append(x)

    if not sortedList_byStatus:
            sortedList_byStatus.append(AnimeEntry("very empty...", "", "", url_for('static', filename = 'wot.PNG'), status, ""))
    return sortedList_byStatus

def getSortedList():
    return sortedList

 