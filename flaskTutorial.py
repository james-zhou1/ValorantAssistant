import base64
from flask import Flask, request, render_template
from Backend.GEA_database_management import get_map_data_db
from Backend.GEA_visualizations import plot_activity, plot_data_for_map

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    data = request.form.to_dict()
    
    heatmap_images = process_data(data)

    toReturn = ''
    if(data['killLocations']):
        toReturn += f"""<img src="data:image/png;base64,{ heatmap_images['kill_locations'] }" >"""
    if(data['deathLocations']):
        toReturn += f"""<img src="data:image/png;base64,{ heatmap_images['death_locations'] }" >"""
    if(data['positioningGuide']):
        toReturn += f"""<img src="data:image/png;base64,{ heatmap_images['positioning_guide'] }" >"""
    
    if(toReturn == ''):
        toReturn = 'please check a box'

    return render_template('index.html', images=toReturn, data=data)
        
        


def process_data(data):
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
