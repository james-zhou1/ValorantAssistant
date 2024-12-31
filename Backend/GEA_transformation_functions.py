import os
import json
import tempfile
from collections import deque
from .GEA_constants import *
from .GEA_api_caller import *
from .GEA_classified import *

#============================================================================================================
#READ THIS            READ THIS             READ THIS               READ THIS      
# 1. you can ignore any function labeled as 'auxillary' (unless you want to write your own functions)
# 2. read all comments whenever you see the '=======' dividing line
# 3. read all comments above function headers 

#this whole library revolves around creating the GEA STRUCTURE.
# The GEA STRUCTURE is organized in a way that makes it 
# very useful to perform data analysis on Val match results.

# I will link an image to the structure here:
# [GEA STRUCTURE IMAGE LINK]


# if anything is unclear dm @ecneon on discord
#============================================================================


#FUNCTION DEFITIONS (you can collapse all of these)
#these access and save data




#Does not access API
#auxillary function for the get_data functions
#returns the new team configuration(flips teams)
#team_side is either string or dict, depending on if we are analyzing individual player or all player
def switch_teams(team_side):
    dbug_print("---SWITCHING TEAMS---")
    if isinstance(team_side, dict):

        for key, value in team_side.items(): #allplayer analysis
            if value['Side'] == "Attack":
                team_side[key]['Side'] = "Defense"
            elif value['Side'] == "Defense":
                team_side[key]['Side'] = "Attack"

    elif isinstance(team_side, str): #player analysis

        if team_side == "Attack":
            team_side = "Defense"
        else:
            team_side = "Attack"

    else:
        print("team_side has type ", type(team_side))
        raise ValueError("Invalid team side")

#Does not access API
#auxillary function for analyze_match
#mutates output_dict, does it for specific player
def get_data_for_player(curr_match: dict, map_name: str, puuid: str, output_dict: dict):
    player_team = None
    player_agent = None
    for player in curr_match['players']:
        if player['subject'] == puuid:
            player_team = player['teamId']
            player_agent = allAgents[player['characterId']]
            break
    
    

    if player_team == "Red": #if player_team is None, player was not found
        team_side = "Attack"
    elif player_team == "Blue":
        team_side = "Defense"



    round_count = 0
    kill_array_index = 0
    for round_result in curr_match['roundResults']:
        if kill_array_index < len(curr_match['kills']): #as long as there are still kills to be checked, we continue
            dbug_print("\n")
            
            round_count += 1
            dbug_print('currently examining new round [', round_count, "]")
            dbug_print('  player is on ', team_side)

            if round_count > 24 or ( round_count % 12 == 1 and round_count > 1):  #switch teams when needed(after round 12,and in OT)  *not explicitly tested to be correct
               
                switch_teams( team_side)


                
        
            #get specified player's stats
            for player_stat in round_result['playerStats']:
                if player_stat['subject'] == puuid:
                    dbug_print("\tplayer stats found")
                    curr_round_stats = player_stat
                    break
            
            #location data will need these things
            loadout_value = curr_round_stats['economy']['loadoutValue']
            weapon = allGuns[curr_round_stats['economy']['weapon']]
            armor  = allArmor[curr_round_stats['economy']['armor']]



            #determine where to put the next entry in the array by loadout value
            array_spot = (int)(loadout_value/50)
            dbug_print("\tloadout value[", loadout_value, "]->array spot[", array_spot, "]")
        
        
        #calculate round length

            #calculate start time 
            round_start_time = curr_match['kills'][kill_array_index]['gameTime'] - curr_match['kills'][kill_array_index]['roundTime']
            
            #calculate start time of next round, if there is no next round, time = -1
            next_round_start_time = -1
            for kill_info in curr_match['kills']:
                if kill_info['round'] == round_count + 1:
                    next_round_start_time = kill_info['gameTime'] - kill_info['roundTime']
                    break
        

            #subtract the buy phase time
            buy_phase = 0
            if(round_count == 1 or round_count == 13 or round_count == 25):
                buy_phase = 45000
            else:
                buy_phase = 30000

            if(next_round_start_time == -1):
                round_length = curr_match['matchInfo']['gameLengthMillis'] - round_start_time #might be wrong because gameLengthMillis might not start from the start of round 1
            else:
                round_length = next_round_start_time - round_start_time - buy_phase
        #round length calculated
        
            dbug_print('\t\tround start(ms)  = ', round_start_time)
            dbug_print('\t\tnext round start(ms)  = ', next_round_start_time)
            dbug_print('\t\tbuy phase(ms)    =', buy_phase)
            dbug_print("\t\tround length(ms) = ", round_length)



            
            #loop through all kills in the current round
            while(kill_array_index < len(curr_match['kills']) and curr_match['kills'][kill_array_index]['round']+1 == round_count):
                dbug_print('\t\t\tcurrently examining kills on round ', curr_match['kills'][kill_array_index]['round']+1, 'should match ', round_count)
                curr_kill_info = curr_match['kills'][kill_array_index]

                if(curr_kill_info['victim'] == puuid):#our player died!

                    death_time_percentage = (int)(round(curr_kill_info['roundTime']/round_length, 2)*100)
                    dbug_print("\t\t\t\tdeath_time[0,100]: ", death_time_percentage, "%")#DBUG

                    #GET RID OF STUPID ISO ULT DATA
                    if abs(curr_kill_info['victimLocation']['x']) <= 20000 and abs(curr_kill_info['victimLocation']['y']) <= 20000:
                        
                        dbug_print('\t\t\t\tINSERTING death INTO SLOT: [', array_spot, "]")
                        output_dict[map_name][team_side]['death_info'][array_spot].append({

                            'Location': {'x': curr_kill_info['victimLocation']['x'], 'y':curr_kill_info['victimLocation']['y']},
                            'Armor' : armor,
                            'Agent' : player_agent
                        })

                    #add to the death time
                    output_dict[map_name]['All_Death_Times'][death_time_percentage]+=1
                
                if(curr_kill_info['killer'] == puuid):#our player got a kill!
                    
                    kill_time_percentage = (int)(round(curr_kill_info['roundTime']/round_length,2)*100)
                    dbug_print("\t\t\t\tkill_time[0,100]: ", kill_time_percentage, "%")#DBUG

                    #add kill info (a bit more complicated)
                    for player_loc in curr_kill_info['playerLocations']:

                        if player_loc['subject'] == puuid:

                            #GET RID OF STUPID ISO ULT DATA
                            if abs(player_loc['location']['x']) <= 20000 and abs(player_loc['location']['y']) <= 20000:
                                
                                dbug_print('\t\t\t\tINSERTING kill INTO SLOT: [', array_spot, "]")
                                
                                #add datapoint to output
                                output_dict[map_name][team_side]['kill_info'][array_spot].append({
                                    'Location': {'x': player_loc['location']['x'], 'y': player_loc['location']['y']},
                                    'ViewRadians': player_loc['viewRadians'],
                                    'Weapon': weapon,
                                    'Agent' : player_agent
                                })
                            break
                            

                    #add to the kill time
                    output_dict[map_name]['All_Kill_Times'][kill_time_percentage]+=1
                


                kill_array_index += 1

# UNFINISHSED
#Does not access API 
#auxillary function for analyze_match
#mutates output_dict, different algorithm for all players
def get_data_for_all_players(curr_match: dict, map_name: str, output_dict: dict):
    

    all_players_stats = {
        
        player['subject']: {
            
            "Side": "Attack" if player['teamId'] == "Red" else "Defense" if player['teamId'] == "Blue" else "MISSING_DATA", 
            "Loadout_Value": None, 
            "Weapon": None, 
            "Armor": None,
            "Agent": allAgents[player['characterId']]
        
        } for player in curr_match['players']
    }
    
    round_count = 0
    for round_result in curr_match['roundResults']:
        round_count += 1

        dbug_print('\tcurrently examining new round [', round_count, "]")

        if round_count > 24 or ( round_count % 12 == 1 and round_count > 1):  #switch teams when needed(after round 12,and in OT)  *not explicitly tested to be correct
            switch_teams( all_players_stats)

        #get all the players buy values, weapons, armor (this may not be very effective, because we are getting all this info for players even if they didnt get a kill this round)
        dbug_print("\t\tgetting all player economies")
        if round_result['playerEconomies'] is not None and isinstance(round_result['playerEconomies'], list):
            for curr_player_economy in round_result['playerEconomies']:
                all_players_stats[curr_player_economy['subject']]['Loadout_Value'] = curr_player_economy['loadoutValue']
                all_players_stats[curr_player_economy['subject']]['Weapon'] = allGuns[curr_player_economy['weapon']]
                all_players_stats[curr_player_economy['subject']]['Armor'] = allArmor[curr_player_economy['armor']]
        else:
            break

        
        #time to pull out data
        if round_result['playerStats'] is not None and isinstance(round_result['playerStats'], list):
            for player_stat in round_result['playerStats']:

                if player_stat['kills'] is not None and isinstance(player_stat['kills'], list):
                    for curr_kill in player_stat['kills']:
                        dbug_print("\t\t\tProcessing new kill/death in round [", round_count, "]")
                        #put in DEATH INFO
                        
                        #GET RID OF STUPID ISO ULT DATA
                        if abs(curr_kill['victimLocation']['x']) > 20000 or abs(curr_kill['victimLocation']['y']) > 20000:
                            continue

                        #calculate where we put datapoint
                        array_spot = (int)(all_players_stats[curr_kill['victim']]['Loadout_Value']/50)
                    
                        dbug_print('\t\t\t\tINSERTING death INTO SLOT: [', array_spot, "]")

                        #add datapoint to output
                        output_dict[map_name][all_players_stats[curr_kill['victim']]['Side']]['death_info'][array_spot].append( {
                        
                            'Location': {'x': curr_kill['victimLocation']['x'], 'y':curr_kill['victimLocation']['y']},
                            'Armor' : all_players_stats[curr_kill['victim']]['Armor'],
                            'Agent' : all_players_stats[curr_kill['victim']]['Agent']

                        })

                        #put in KILL INFO
                        array_spot = (int)(all_players_stats[curr_kill['killer']]['Loadout_Value']/50)
                    
                        dbug_print('\t\t\t\tINSERTING kill INTO SLOT: [', array_spot, "]")

                        #in case killer location is not found, we skip this(killer location not found is actually possible to happen!)
                        for item in curr_kill['playerLocations']:
                            if item['subject'] == curr_kill['killer']:
                                killer_location = item
                                break
                        else:
                            continue

                        #GET RID OF STUPID ISO ULT DATA
                        if abs(killer_location['location']['x']) > 20000 or abs(killer_location['location']['y']) > 20000:
                            continue

                        output_dict[map_name][all_players_stats[curr_kill['killer']]['Side']]['kill_info'][array_spot].append({
                        
                            'Location': {'x': killer_location['location']['x'], 'y':killer_location['location']['y']},
                            'ViewRadians' : killer_location['viewRadians'],
                            'Weapon' : all_players_stats[curr_kill['killer']]['Weapon'],
                            'Agent' : all_players_stats[curr_kill['killer']]['Agent']

                        })
                else:
                    continue         
        else:
            break
        

#Does not access API
#auxillary function for get_all_location_data
#given match details (format: https://valapidocs.techchrism.me/endpoint/match-details)
#mutates output_dict by placing new data inside
def analyze_match(curr_match: dict, puuid: str, output_dict: dict):
    

    
    map_name = allMaps[curr_match['matchInfo']['mapId']]

    analyze_all_players = puuid == ""

    print(f"----CURRENT MAP: [{map_name}]----")

    if map_name not in output_dict:
        if(analyze_all_players):
            output_dict[map_name] = {
                
                'num_matches': 0, #number of matches analyzed for this specific map

               #No kill/death times for allplayers
                "Attack": {
                    #make these all linkedlists which apparently is using deque()
                    "kill_info": [[] for _ in range(160)],
                    "death_info": [[] for _ in range(160)]
                    #WE ARE DITCHING THE PLANT INFO!, making a separate dictionary that gets ALL plant data and defuse data(not just specific player)
                },
                "Defense": {
                    "kill_info": [[] for _ in range(160)],
                    "death_info": [[] for _ in range(160)]
                }
            }
        else:
            output_dict[map_name] = {

                'num_matches': 0, #number of matches analyzed for this specific map

                'All_Kill_Times' : [0]*101, #indexes 0 thru 100 = 101 elements (these are % numbers)
                'All_Death_Times': [0]*101,

                "Attack": {
                    #make these all linkedlists which apparently is using deque()
                    "kill_info": [[] for _ in range(160)],
                    "death_info": [[] for _ in range(160)],
                    #WE ARE DITCHING THE PLANT INFO!, making a separate dictionary that gets ALL plant data and defuse data(not just specific player)
                },
                "Defense": {
                    "kill_info": [[] for _ in range(160)],
                    "death_info": [[] for _ in range(160)]
                }
            }

    output_dict[map_name]['num_matches'] += 1 #add one match to the num matches analyzed

    if(analyze_all_players):
        
        get_data_for_all_players(curr_match, map_name, output_dict)
    else:
        get_data_for_player(curr_match, map_name, puuid, output_dict)
    
    return output_dict


#Accesses API(indirectly)
#returns specified(puuid) player's data 
#if puuid is empty string, we will get everyone's data

#dont worry about the to_return_dict parameter. 
#it used to be for when I was storing GEA structures locally
#now i use a database and i can append onto the database directly

#data structure image link: [to be added]
def get_all_location_data(puuid: str, all_match_ids: list, examined_matches: set = None, to_return_dict:dict = None):
    
    if to_return_dict is None:
        to_return_dict = {}

    
    
    print("START!")
    numSkip = 0

    # print("\n".join(all_match_ids)) #debug print

    for index, match_id in enumerate(all_match_ids):

        if(examined_matches is not None and match_id in examined_matches):
            
            numSkip +=1
            # print(f'     skipped {numSkip}') #dbug print
        else:

            curr_match = get_match_details(match_id, API_KEY)

            print("\nExamining Match [", index+1, "]/", len(all_match_ids))

            to_return_dict = analyze_match(curr_match, puuid, to_return_dict)

            if(examined_matches is not None):
                examined_matches.add(match_id)

    print(f'Skipped {numSkip} matches. {len(all_match_ids) - numSkip} new matches were added out of {len(all_match_ids)}')
    return to_return_dict

#Accesses API(indirectly)
#returns an array of all of the match ids that we have access to (from the api)
def get_player_match_IDs(puuid: str):
    
    match_history: dict = get_raw(puuid, API_KEY, mode ,0 ,25)


    # print(json.dumps(match_history, indent=4)) #debug print


    total_elements = match_history['Total']
    
    history = []

    history.extend([match['MatchID'] for match in match_history['History']])

    if total_elements > 25:#matchhistory: limit = 25 at a time
        for i in range(25, total_elements, 25):

            # print(f'starting from {i}') #debug print

            next_batch = get_raw(puuid=puuid, api_key=API_KEY, queue=mode, startIndex=i, endIndex=i+25)

            # print(json.dumps(next_batch, indent=4)) #debug print

            history.extend([match['MatchID'] for match in next_batch['History']])

    return history


#TAKES LOT OF TIME !! !
#creates a dictionary where the keys are puuids, and the values are GEA structures corresponding to each puuid
#Only use this one if you need to distinguish between individual players stats
def get_individual_data_for_players(puuids: list):
    toReturn={}
    for currID in puuids:
        
        toReturn[currID] = get_all_location_data(currID,get_player_match_IDs(currID))

    return toReturn

#Accesses API(indirectly)
#returns a LIST of MatchIDs that are played around the given tier_range
#requires one player that has games within that range because thats how it works
def get_ranked_matches(starterPuuid: str, tier_range: tuple, examined_matches: set, limit: int) -> list[str]:
    
    #recursive helper. Performs DFS (sort of)
    def propogate(all_match_ids: set, puuidStack: list, examined: set, limit: int):
        if len(puuidStack) == 0:
            print('Weve hit a dead end in propogate(), this should be very rare. Pick a different starting puuid')
            print(f'Heres how many matches we still needed to get: {limit}')
            return all_match_ids

        dbug_print(f'\nExamining new player... limit = {limit}')

        puuid = puuidStack.pop()


        #get the initial list of match ids, using comp_updates
        comp_updates = get_comp_updates(puuid,API_KEY,"competitive",0, 10)

        #save one matchID thats within range to grab more players from if we need to
        saved = None

        #loop through all the matches we got from the api call
        for match in comp_updates['Matches']:

            #if the current rank played of match is within range and has not been examined, add to the set
            if match['TierBeforeUpdate'] in range(tier_range[0],tier_range[1]+1) and match['MatchID'] not in examined:
                dbug_print('\tAdding new matchID..')

                #add to examined and add to our return set
                all_match_ids.add(match['MatchID'])
                examined.add(match['MatchID'])

                limit -= 1
                if limit == 0:
                    dbug_print('Limit reached! returning')
                    return all_match_ids
                
                if saved is None:
                    saved = match['MatchID']
        
        #saved COULD BE NONE,

        #if we have no more players to choose from, add some
        if len(puuidStack) <= 6:
            dbug_print('Playerlist buffer <= 6, adding more')
            if saved is not None:
                match_details = get_match_details(saved ,API_KEY)
                for player in match_details['players']: 
                    if player['subject'] != puuid and player['subject'] is not None: #Need to also handle anonymous players
                        puuidStack.append(player['subject'])
        
        return propogate(all_match_ids, puuidStack, examined, limit)



    return list(propogate(set(),[starterPuuid], examined_matches, limit))

#UNUSED
#adds multiple players ids to one big GEA structure
def get_all_players_location_data(players_match_data: dict, api_key: str):
    """
    players_match_data: dict with player puuid as keys and list of match IDs as values
    {
        "puuid1": [match_id1, match_id2, ...],
        "puuid2": [match_id1, match_id2, ...],
        ...
    }
    """
    to_return_dict = {}
    for puuid, match_ids in players_match_data.items():
        to_return_dict = process_player_match_history(puuid, match_ids, to_return_dict, API_KEY)
    return to_return_dict
#UNUSED
#helper for above
def process_player_match_history(puuid: str, match_ids: list, to_return_dict: dict, api_key: str):
    for index, match_id in enumerate(match_ids):
        curr_match = get_match_details(match_id, API_KEY)
        
        print("\nExamining Match [", index+1, "]")

        to_return_dict = analyze_match(curr_match, puuid, to_return_dict)
    return to_return_dict

#UNUSED
#combines multiple GEA structures into one
def combine(data_structures):

    combined = {}

    for data in data_structures:
        # print(json.dumps(data, indent=4))
        for map_name, map_data in data.items():
            if map_name not in combined:
                combined[map_name] = {
                    'num_matches': 0
                }
            combined[map_name]['num_matches'] += map_data['num_matches']

            phase = "Attack"
            phase_data = map_data[phase]
            if phase not in combined[map_name]:
                combined[map_name][phase] = {
                    "kill_info": [[] for _ in range(160)],
                    "death_info": [[] for _ in range(160)]
                }
            
            for i in range(160):

                # print(type(combined))
                # print(type(combined[map_name]))
                # print(type(combined[map_name][phase]))
                # print(type(combined[map_name][phase]["kill_info"]))
                # print((combined[map_name][phase]["kill_info"]))

                # print(type(combined[map_name][phase]["kill_info"][i]))
                # print("a")
                # print(type(phase_data))
                # print(type(phase_data["kill_info"][i]))
                # print(type(phase_data["death_info"][i]))
                # print(type())


                combined[map_name][phase]["kill_info"][i].extend(phase_data["kill_info"][i])
                combined[map_name][phase]["death_info"][i].extend(phase_data["death_info"][i])


            phase = "Defense"
            phase_data = map_data[phase]
            if phase not in combined[map_name]:
                combined[map_name][phase] = {
                    "kill_info": [[] for _ in range(160)],
                    "death_info": [[] for _ in range(160)]
                }
            
            for i in range(160):

                # print(type(combined))
                # print(type(combined[map_name]))
                # print(type(combined[map_name][phase]))
                # print(type(combined[map_name][phase]["kill_info"]))
                # print((combined[map_name][phase]["kill_info"]))

                # print(type(combined[map_name][phase]["kill_info"][i]))
                # print("a")
                # print(type(phase_data))
                # print(type(phase_data["kill_info"][i]))
                # print(type(phase_data["death_info"][i]))
                # print(type())


                combined[map_name][phase]["kill_info"][i].extend(phase_data["kill_info"][i])
                combined[map_name][phase]["death_info"][i].extend(phase_data["death_info"][i])

    return combined
#=================================================================================================================


#THESE ARE THE FUNCTIONS YOU CALL DIRECTLY IN THE CODE
#============================================================================================================
# A couple terms you should know: 
# *PLAYER SPECIFIC: 
#   means the data returned to us corresponds to one specific player
#   example: all of GEA joli's deaths, all of GEA joli's kills

#*NOT PLAYER SPECIFIC:
#   means the data returned to us is from all players in all matches
#   example: all players deaths in GEA joli's games, all players' kills in GEA joli's games




#creates GEA structure for one player
#*PLAYER SPECIFIC

# !! this needs examined_matches functionality
# it is prone to duplicate datapoints
#Only  use this if you dont plan on appending the results from multiple 
#analyze_individual calls from the same person
def analyze_individual(name: str, tag:str):

    puuid = get_puuid(name, tag, API_KEY)['data']['puuid']
    history = get_player_match_IDs(puuid) 

    print(f'   Number of Matches: [{len(history)}]')

    return get_all_location_data(puuid, history) 


#creates a GEA strucutre for every player in allPlayers
# {
# [puuid] -> GEA structure,
# [puuid] -> GEA structure
#}
#*PLAYER SPECIFIC

# !! this needs examined_matches functionality
# it is prone to duplicate datapoints
#Only  use this if you dont plan on appending the results from multiple 
#analyze_individual calls from the same person
def analyze_group(allPlayers: list):
    allPuuids = []
    for player in allPlayers:
        allPuuids.append(get_puuid(player['name'], player['tag'], API_KEY)['data']['puuid'])
    
    return get_individual_data_for_players(allPuuids)


#creates one GEA structure for all mathes played by allPlayers
#allPlayers is an array of dictionaries
# [ {'name': str, 'tag':str}, ... ]
#*NOT PLAYER SPECIFIC
def compile_match_data(allPlayers: list, examined_matches: set):

    #create a big list of match IDS
    allMatchIDs = []
    for player in allPlayers:
        allMatchIDs.extend(get_player_match_IDs(get_puuid(player['name'], player['tag'], API_KEY)['data']['puuid']))

    print(f'   Number of Matches: [{len(allMatchIDs)}]')

    #keep track of examined matches to avoid duplicates
    return get_all_location_data("", allMatchIDs, examined_matches)
    



#does the same as compile_match_data, but does it for the top n leaderboard players of specified season and region
#*NOT PLAYER SPECIFIC
def compile_leaderboard_data(examined_matches:set, num_players: int, region: str = 'na', season: str = recent_season ):

    leaderboard = get_leaderboard_info(API_KEY, region, season)
    allMatchIDs = []
    for player in leaderboard['players']:
        if not player['IsBanned'] and not player['IsAnonymized']:
            
            print(f'getting matches for {player['gameName']}')

            allMatchIDs.extend(get_player_match_IDs(player['puuid']))
            num_players -= 1
            if num_players == 0:
                break

    print(f'   Number of Matches: [{len(allMatchIDs)}]')

    #keep track of examined matches to avoid duplicates
    return get_all_location_data("", allMatchIDs, examined_matches)




#takes in one player's puuid, and 
#returns a GEA structure containing data from
# "limit" number of UNIQUE matches 

def compile_rank_data(starterPuuid: str, tier_range: tuple, examined_matches: set, limit: int):

    allMatchIDs = get_ranked_matches(starterPuuid, tier_range, examined_matches, limit)

    #we put empty set for examined_matches because get_ranked_matches already garuntees we avoid duplicates.
    #allMatchIDs is already new 
    return get_all_location_data("", allMatchIDs, set())

#NO LONGER USING   ================================================================
#designated function for dealing with the fixed GEA data                        
#inputs the file names
def update_fixed_data(allPlayers: list, fixed_data: str, examined_matches: str): 
    #read
    # Load the fixed_data file into a dictionary
    if os.path.exists(fixed_data):
        with open(fixed_data, 'r') as file:
            fixed_data_dict = json.load(file)
    else:
        fixed_data_dict = {}

    # Load the examined_matches file into a set
    if os.path.exists(examined_matches):
        with open(examined_matches, 'r') as file:
            examined_matches_set = set(json.load(file))
    else:
        examined_matches_set = set()
    


    #data processing
    allMatchIDs = []
    for player in allPlayers:
        allMatchIDs.extend(get_player_match_IDs(get_puuid(player['name'], player['tag'], API_KEY)['data']['puuid']))

    print(f'   Number of Matches: [{len(allMatchIDs)}]')

    #keep track of examined matches to avoid duplicates
    fixed_data_dict = get_all_location_data("", allMatchIDs, examined_matches =examined_matches_set, to_return_dict= fixed_data_dict)
    


    #write
    # Save the updated fixed_data_dict to a temporary file and then rename it
    with tempfile.NamedTemporaryFile('w', delete=False) as temp_file:
        json.dump(fixed_data_dict, temp_file, indent=4)
        temp_file_path = temp_file.name
    os.replace(temp_file_path, fixed_data)

    # Save the updated examined_matches_set to a temporary file and then rename it
    with tempfile.NamedTemporaryFile('w', delete=False) as temp_file:
        json.dump(list(examined_matches_set), temp_file, indent=4)
        temp_file_path = temp_file.name
    os.replace(temp_file_path, examined_matches)
#============================================================================================================

