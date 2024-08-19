import base64
import os
from flask import Flask, jsonify, request, render_template, session
from Backend.GEA_database_management import get_map_data_db
from Backend.GEA_visualizations import Map_Plotter, plot_activity, plot_data_for_map
from flask_caching import Cache
import pickle
import uuid

app = Flask(__name__, template_folder=os.getcwd())
app.secret_key = 'GEA-2D4E-G1V2-4I93Q'  # Necessary for session management

# Configure Flask-Caching
cache = Cache(app, config={'CACHE_TYPE': 'redis', 'CACHE_REDIS_URL': 'redis://localhost:6379/0', 'CACHE_DEFAULT_TIMEOUT': 3600})

def store_plotter (plotter: Map_Plotter):

    # Store the map_plotter object in Redis
    cache.set(session['user_id'], pickle.dumps(plotter))  # Store using user_id as key


def retrieve_plotter():
    serialized_map_plotter = cache.get(session['user_id'])

    # Check if the serialized object exists
    if serialized_map_plotter is not None:
        # Deserialize the map_plotter object
        map_plotter = pickle.loads(serialized_map_plotter)
    else:
        # Handle the case where the object is not found in the cache
        print('EMERGENCY. MAP PLOTTER NOT FOUND IN REDIS')
        map_plotter = None  # or create a new i


    return map_plotter


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/guide', methods=['POST'])
def guide():
    form_data = request.form.to_dict()  # Convert form data to a dictionary
    map_name = form_data['mapName']
    map_plotter = Map_Plotter('leaderboard_data_GEA', map_name)
   
    session['user_id'] = str(uuid.uuid4()) #'initialize' the session

    store_plotter(map_plotter)

    form_data['plotterObjectInfo'] = str(map_plotter)


    return render_template('guide.html', **form_data)

@app.route('/choose-side', methods=['POST'])
def choose_side():
    selected_option = request.form.get('option')
    
    # Logic to determine what data to return based on the selected option
    if selected_option == "Attack":
        data = "now im going to ask for buy values of you(Attackers) and the enemy team(Defenders)."
    elif selected_option == "Defense":
        data = "now im going to ask for buy values of you(Defenders) and the enemy team(Attackers)."
    else:
        data = "Invalid option selected."

    map_plotter = retrieve_plotter()
    
    return jsonify(option=selected_option, message=data)

@app.route('/generate-attack', methods = ['POST'])
def generate_attack():

    #retrieve map plotter from cache
    map_plotter = retrieve_plotter()

    #get the options the user seleced
    buy_val = request.form.get('option') 
    side = request.form.get('side')
    
    #set up the attackers buy value
    a_lower, a_upper = buy_values(buy_val)
    attack_options = {
        "kills": {"lower": a_lower//50, "upper": a_upper//50}, #between 0 160 
        "deaths": {"lower": a_lower//50, "upper": a_upper//50}         #note: MAKE KILLS AND DEATHS OPTIONS THE SAME(physically)
    }

    #update the map_plotter
    map_plotter.update_buy_range_attack(attack_options) 
    kills_bin = map_plotter.generate_kills_bin(attack = True,defense = False)
    deaths_bin = map_plotter.generate_deaths_bin(attack = True,defense = False)

    #if user is on attack, generate the positioning guide, otherwise do the combined heatmap
    if(side == 'Attack'):
        print('plotting position_guide...')
        pos_guide = map_plotter.create_positioning_guide(kills_bin,deaths_bin, attack = True, defense = False,  map_only = True, filter_sigma= 2.5)
        print('success!')
        return pos_guide
    else:
        print('plotting heatmap...')
        combined = kills_bin + deaths_bin
        combined_heatmap_image = map_plotter.create_plot(combined,attack = True,defense = False,kill = True,death = True,  map_only = True, log_scale=True, filter_sigma=2)
        print('success!')
        return combined_heatmap_image
    



@app.route('/generate-defense', methods = ['POST'])
def generate_defense():
    map_plotter = retrieve_plotter()
    print(f'BEHOLD THE MAP PLOTTER: {map_plotter}')

    buy_val = request.form.get('option')
    side = request.form.get('side')

    d_lower, d_upper = buy_values(buy_val) #DEFENDERS BUY
    defense_options = {
        "kills": {"lower": d_lower//50, "upper": d_upper//50}, #between 0 160
        "deaths": {"lower": d_lower//50, "upper":d_upper//50}
    }
    map_plotter.update_buy_range_defense(defense_options)
    kills_bin = map_plotter.generate_kills_bin(attack = False,defense = True)
    deaths_bin = map_plotter.generate_deaths_bin(attack = False,defense = True)

    #if user is on defense, generate the positioning guide, otherwise do the combined heatmap
    if(side == 'Defense'):
        print('plotting position_guide...')
        pos_guide = map_plotter.create_positioning_guide(kills_bin,deaths_bin, attack = False, defense = True,  map_only = True, filter_sigma= 2.5)
        print('success!')
        return pos_guide
    else:
        print('plotting heatmap...')
        combined = kills_bin + deaths_bin
        combined_heatmap_image = map_plotter.create_plot(combined,attack = False,defense = True,kill = True,death = True, map_only = True, log_scale=True, filter_sigma=2)
        print('success!')
        return combined_heatmap_image
    

@app.route('/advanced', methods=['POST'])
def advanced():

    return render_template('advanced.html')



@app.route('/submit', methods=['POST'])
def submit():
    data = request.form.to_dict()
    
    heatmap_images = process_data(data)

    toReturn = ''
    if(data.get('killLocations')):
        toReturn += f"""<img src="data:image/png;base64,{ heatmap_images['kill_locations'] }" >"""
    if(data.get('deathLocations')):
        toReturn += f"""<img src="data:image/png;base64,{ heatmap_images['death_locations'] }" >"""
    if(data.get('positioningGuide')):
        toReturn += f"""<img src="data:image/png;base64,{ heatmap_images['positioning_guide'] }" >"""
    
    if(toReturn == ''):
        toReturn = 'please check a box'

    return render_template('index.html', images=toReturn, data=data) #resetting the stuff is not working properly
        
        
def buy_values(buy_name: str):
        if(buy_name == 'pistol'):
            return 0,1000
        elif(buy_name == 'rifle'):
            return 3900, 5000
        elif(buy_name == 'all'):
            return 0, 7950
        elif(buy_name == 'fullbuy'):
            return 3600, 7950
        elif(buy_name == 'midbuy'):
            return 1000, 3900
        elif(buy_name == 'eco'):
            return 0, 3000

def process_data(data):
    
        

    a_lower, a_upper = buy_values(data['buyValue']) #ATTACKERS BUY

    d_lower, d_upper = buy_values(data['buyValue']) #DEFENDERS BUY


    attack_options = {
        "kills": {"lower": a_lower//50, "upper": a_upper//50}, #between 0 160 
        "deaths": {"lower": a_lower//50, "upper": a_upper//50}                  #note: MAKE KILLS AND DEATHS OPTIONS THE SAME(physically)

    }
    defense_options = {
        "kills": {"lower": d_lower//50, "upper": d_upper//50}, #between 0 160
        "deaths": {"lower": d_lower//50, "upper":d_upper//50}
    }

    print('getting from database')
    map_data = get_map_data_db('leaderboard_data_GEA', data['mapName'])
    print('plotting activity')

    return plot_data_for_map(map_data, data['mapName'], attack_options, defense_options, scatterplot = False, logscale = True)



if __name__ == '__main__':
    app.run(debug=True)
