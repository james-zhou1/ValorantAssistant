import requests
import time

#============================================================================================================
#ensures that we dont exceed the max requests. write this after every API request!!!!!
def limit_check(response):
    print("\t\t\trequest made.")

    # print(f"\t\t\t\tAlleged requests made: [{response.headers['x-ratelimit-limit']}]/30")
    print(f"\t\t\t\tAlleged requests remaining: [{response.headers['x-ratelimit-remaining']}]")
    if(int(response.headers['x-ratelimit-remaining']) <= 0):
        print(f"\t\t\t\tsleeping for [{response.headers['x-ratelimit-reset']} + 2] sec")
        time.sleep(int(response.headers['x-ratelimit-reset']) + 2) #add 2 extra seconds becauase its failed before
        

#ALL API REQUESTS SHOULD LOOK LIKE THIS
#       print("Making request...")
#       response = <API request statmement>
#       limit_check(response)
#============================================================================================================






#============================================================================================================
#FUNCTION DEFINITIONS(you can collapse)
#These all directly access API which is why theyre here

#Accesses API
#returns puuid of player
def get_puuid(name: str, tag: str, api_key: str):

    url = f"https://api.henrikdev.xyz/valorant/v1/account/{name}/{tag}"
    headers = {'Authorization': f'{api_key}'}

    print("Making request...")
    response = requests.get(url, headers=headers)
    limit_check(response)



    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to fetch puuid: {response.status_code}")
        error = response.json()['errors'][0]['message']
        details= response.json()['errors'][0]['details']
        code = response.json()['status']
        if details == "null":
            details = ""     
        else:
            details = f"Details: {details}"
        response_message = f"{error} Code:{code}....{details}"
        print(response_message, "\nEXITING PROGRAM")
        quit()

#Accesses API
#returns the player's raw data match history
#format is here: https://valapidocs.techchrism.me/endpoint/match-history 
def get_raw(puuid: str,api_key: str,queue: str, startIndex: int, endIndex: int):
    url = f"https://api.henrikdev.xyz/valorant/v1/raw"
    headers = {
        'Authorization': f'{api_key}',
    }
    body = {
        "type": "matchhistory",
        "value": puuid,
        "region": "na",
        "queries": f"?startIndex={startIndex}&endIndex={endIndex}&queue={queue}"
    }
    
 

    print("Making request...")
    response = requests.post(url, headers=headers, json=body)
    limit_check(response)

 
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to fetch raw_data: {response.status_code}")
        error = response.json()['errors'][0]['message']
        details= response.json()['errors'][0]['details']
        code = response.json()['status']
        if details == "null":
            details = ""     
        else:
            details = f"Details: {details}"
        response_message = f"{error} Code:{code}....{details}"
        print(response_message, "\nEXITING PROGRAM")
        quit()

#Accesses API
#returns match details of matchID
#format is here: https://valapidocs.techchrism.me/endpoint/match-details 
def get_match_details(matchID: str,api_key: str,):
    url = f"https://api.henrikdev.xyz/valorant/v1/raw"
    headers = {
        'Authorization': f'{api_key}',
    }
    body = {
        "type": "matchdetails",
        "value": matchID,
        "region": "na",
    }
    
    
    print("Making request...")
    response = requests.post(url, headers=headers, json=body)
    limit_check(response)
 
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to fetch match_details: {response.status_code}")
        error = response.json()['errors'][0]['message']
        details= response.json()['errors'][0]['details']
        code = response.json()['status']
        if details == "null":
            details = ""     
        else:
            details = f"Details: {details}"
        response_message = f"{error} Code:{code}....{details}"
        print(response_message, "\nEXITING PROGRAM")
        quit()


#Accessses API
#returns details from leaderboard endpoint
#format is here: https://app.swaggerhub.com/apis-docs/Henrik-3/HenrikDev-API/3.0.1#/default/get_valorant_v2_leaderboard__affinity_ 
def get_leaderboard_info(api_key:str, region: str, season:str):
    url = f"https://api.henrikdev.xyz/valorant/v2/leaderboard/{region}?season={season}"
    headers = {
        'Authorization': f'{api_key}',
    }

    print("Making request...")
    response = requests.get(url, headers=headers)
    limit_check(response)


    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to fetch leaderboard: {response.status_code}")
        error = response.json()['errors'][0]['message']
        details= response.json()['errors'][0]['details']
        code = response.json()['status']
        if details == "null":
            details = ""     
        else:
            details = f"Details: {details}"
        response_message = f"{error} Code:{code}....{details}"
        print(response_message, "\nEXITING PROGRAM")
        quit()
# ==========================================================================================================

