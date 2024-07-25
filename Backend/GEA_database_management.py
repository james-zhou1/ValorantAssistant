from .GEA_classified import CONNECTION_STRING
from .GEA_constants import allMaps
from .GEA_transformation_functions import compile_leaderboard_data, compile_match_data

from pymongo import MongoClient, UpdateOne

 
client = MongoClient(CONNECTION_STRING)


#returns the database given the name
def get_database_db(database_name: str):
   return client[database_name]

#clears all items in collection !WARNING!
def clear_collection_db(database_name:str, collection_name:str):
   get_database_db(database_name)[collection_name].delete_many({})



#THIS SECTION IS FOR 'fixed_data_GEA'
#=====================================================================================================================
#updates the examined matches set and creates if not already in there
def store_examined_matches_db(rank_category: str, data_set):
    # Convert the set to a list
    data_list = list(data_set)
    # Store the list in the collection
    client['fixed_data_GEA'][rank_category].update_one(
        {'_id': 'examined_matches'},
        {'$set': {'data_set': data_list}},
        upsert=True
    )
    print(f"updated examined_matches.")

#retrieves the examined matches as a set type
def get_examined_matches_db(rank_category: str):
    document = client['fixed_data_GEA'][rank_category].find_one({'_id': 'examined_matches'})
    if document and 'data_set' in document:
        # Convert the list back to a set
        data_set = set(document['data_set'])
        return data_set
    
    print(f'EXAMINED MATCHES SET NOT FOUND IN {rank_category}')
    return None

def get_map_data_db(rank_category: str, map_name: str):
  
   document = client['fixed_data_GEA'][rank_category].find_one({"_id": map_name})
   
   return document 

#initializes rank category with examined matches set and inserts an empty version of all maps
#requires that the rank category is already created
def init_rank_category_db(rank_category:str):
    db = client['fixed_data_GEA']

    if rank_category in db.list_collection_names():
        print(f"Collection '{rank_category}' already exists.")
    else:
        db.create_collection(rank_category)
        print(f"Collection '{rank_category}' created.")

    #add the examined matches set
    store_examined_matches_db(rank_category, set())

    for key, value in allMaps.items():
       insert_new_map_db(rank_category, value)
    
    


#helper for append_events
#inserts new map with no data to fixed_data_GEA database
def insert_new_map_db(rank_category: str, map_name: str):
   
   #MIGHT NEED TO CHECK IF MAP_NAME ALREADY EXISTS
   map_data = {
      "_id": map_name,
      "num_matches": 0,
      "Attack": {
         "kill_info": [[] for _ in range(160)],
         "death_info": [[] for _ in range(160)]
      },
      "Defense": {
         "kill_info": [[] for _ in range(160)],
         "death_info": [[] for _ in range(160)]
      }
   }

   client['fixed_data_GEA'][rank_category].insert_one(map_data)

#helper for append_events
#increases num_matches of specified map
def increase_num_matches_db(rank_category: str, map_name: str, amount: int):
   
   client['fixed_data_GEA'][rank_category].update_one({'_id': map_name}, {'$inc': {'num_matches': amount}})

#helper for append_events
#checks if map exists in fixed_data_GEA > rank_category
def does_map_exist_db(rank_category: str, map_name:str):
   document = client['fixed_data_GEA'][rank_category].find_one({'_id': map_name})
   return document is not None

#helper for analyze_new
#addes all the data in the GEA structure new_data into fixed_data_GEA > rank_category
def append_fixed_data_GEA_db(rank_category: str, new_data: dict):
   
   for map_name in new_data.keys():
      
      if(not does_map_exist_db(rank_category, map_name)): #may be redundant because i plan on initializing beforehand
         insert_new_map_db(rank_category, map_name)

      #append all the new data for Attack
      att_side = new_data[map_name]['Attack']
      def_side = new_data[map_name]['Defense']
      update_operations = []
      for i in range(160):
         update_operations.extend([
            #                              "push EACH element in curr_side[X_info][i]: list, onto Attack.X_info.{i}: list"
            UpdateOne({'_id': map_name}, {'$push': {f'Attack.kill_info.{i}': {'$each': att_side['kill_info'][i]}}}),
            UpdateOne({'_id': map_name}, {'$push': {f'Attack.death_info.{i}': {'$each': att_side['death_info'][i]}}}), #add for ATTACK


            UpdateOne({'_id': map_name}, {'$push': {f'Defense.kill_info.{i}': {'$each': def_side['kill_info'][i]}}}),
            UpdateOne({'_id': map_name}, {'$push': {f'Defense.death_info.{i}': {'$each': def_side['death_info'][i]}}}) #add for DEFENSE

         ])

      print(f'uploading data for {map_name}')

      client['fixed_data_GEA'][rank_category].bulk_write(update_operations, ordered = True)
      print("done")

      #append all the new data for Defense
      # curr_side = new_data[map_name]['Defense']
      # for i in range(160):
      #    update_operations = [
      #       UpdateOne({'_id': map_name}, {'$push': {f'Defense.kill_info.{i}': {'$each': curr_side['kill_info'][i]}}}),
      #       UpdateOne({'_id': map_name}, {'$push': {f'Defense.death_info.{i}': {'$each': curr_side['death_info'][i]}}})
      #    ]
      #    client['fixed_data_GEA'][rank_category].bulk_write(update_operations)

      print('adding to num matches')
      increase_num_matches_db(rank_category, map_name, new_data[map_name]['num_matches'])
   print('append_fixed_data_GEA_db is done')

#analyzes new players and accounts for examined matches.
def add_to_database_db(rank_category:str, allPlayers: list):

   examined_matches = get_examined_matches_db(rank_category)

   new_GEA_data = compile_match_data(allPlayers, examined_matches)

   store_examined_matches_db(rank_category, examined_matches)


#  import json
#  print(json.dumps(new_GEA_data, indent=4)) #debug print


   append_fixed_data_GEA_db(rank_category, new_GEA_data)

#call this every season
def update_leaderboard_data_db():
   
   examined_matches = get_examined_matches_db('leaderboard_data_GEA')
   new_leaderboard_data = compile_leaderboard_data(examined_matches, 20, 'na')
   store_examined_matches_db('leaderboard_data_GEA', examined_matches)
   append_fixed_data_GEA_db('leaderboard_data_GEA', new_leaderboard_data)

#===========================================================================================================================
