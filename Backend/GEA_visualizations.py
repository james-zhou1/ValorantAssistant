
import base64
import io
from .GEA_constants import *



#============================================================================================================

#READ THIS
#DATA PLOTTING FUNCTIONS(feel free to collapse)
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import gaussian_kde
from scipy.ndimage import gaussian_filter
import matplotlib.colors as mcolors
from PIL import Image
from sklearn.neighbors import KernelDensity
import math

# Function to convert game coordinates to image coordinates
#auxiliary function
def game_to_image_coords(game_x, game_y, img_width, img_height, x_multiplier, x_scalar_add, y_multiplier, y_scalar_add):
    x = game_y * x_multiplier + x_scalar_add
    y = game_x * y_multiplier + y_scalar_add
    
    # Scale to image dimensions
    x *= img_width
    y = (1-y) * img_height
    return x, y




def plot_data_for_map(map_data: dict,map_name:str, attack_options: dict = None, defense_options: dict = None, scatterplot: bool = False, logscale: bool = False):
    
    if map_data['num_matches'] == 0:
        print(f"No recorded matches on {map_name}.")
        return
    
    #GETTING THE IMAGE
    map_img = Image.open(rf"Backend\map_images\{map_name} Map.png")
    map_img = np.array(map_img)  # Convert the image to a NumPy array
    img_height, img_width, _ = map_img.shape  # Get image dimensions


    

    selected_map = map_data


    combined_data = {
            'kill': [],
            'death': []
    }
    
    attack = attack_options is not None 
    defense = defense_options is not None 
    if(not attack and not defense):
       print("please select an option ")
       return

    if(attack):
        
        if(attack_options['kills'] != None):
            if 0 <= attack_options['kills']['lower'] <= 159 and 0 <= attack_options['kills']['upper'] <= 159 and attack_options['kills']['lower'] <= attack_options['kills']['upper']:
                for i in range(attack_options['kills']['lower'], attack_options['kills']['upper'] + 1):
                    curr_kill_value = selected_map['Attack']['kill_info'][i]
                    combined_data['kill'].extend(curr_kill_value)

        if(attack_options['deaths'] != None):
            if 0 <= attack_options['deaths']['lower'] <= 159 and 0 <= attack_options['deaths']['upper'] <= 159 and attack_options['deaths']['lower'] <= attack_options['deaths']['upper']:
                for i in range(attack_options['deaths']['lower'], attack_options['deaths']['upper'] + 1):
                    curr_death_value = selected_map['Attack']['death_info'][i]
                    combined_data['death'].extend(curr_death_value)


    if(defense):
        if(defense_options['kills'] != None):
            if 0 <= defense_options['kills']['lower'] <= 159 and 0 <= defense_options['kills']['upper'] <= 159 and defense_options['kills']['lower'] <= defense_options['kills']['upper']:
                for i in range(defense_options['kills']['lower'], defense_options['kills']['upper'] + 1):
                    curr_kill_value = selected_map['Defense']['kill_info'][i]
                    combined_data['kill'].extend(curr_kill_value)

        if(defense_options['deaths'] != None):
            if 0 <= defense_options['deaths']['lower'] <= 159 and 0 <= defense_options['deaths']['upper'] <= 159 and defense_options['deaths']['lower'] <= defense_options['deaths']['upper']:
                for i in range(defense_options['deaths']['lower'], defense_options['deaths']['upper'] + 1):
                    curr_death_value = selected_map['Defense']['death_info'][i]
                    combined_data['death'].extend(curr_death_value)


    bw = 0.06
    images = {}

    # Plot kill data
    if combined_data['kill']:
        x_coords = [loc['Location']['x'] for loc in combined_data['kill'] ]#x,y swapped!!!!
        y_coords = [loc['Location']['y'] for loc in combined_data['kill'] ]

        # Convert game coordinates to image coordinates
        img_coords = [game_to_image_coords(gx, gy, img_width, img_height, mapCoords[map_name]['xMultiplier'], mapCoords[map_name]['xScalar'], mapCoords[map_name]['yMultiplier'], mapCoords[map_name]['yScalar']) for gx, gy in zip(x_coords, y_coords)]
        img_coords = np.array(img_coords)



        kde = gaussian_kde(img_coords.T, bw_method=bw)
        xgrid = np.linspace(0, img_width, 200)
        ygrid = np.linspace(0, img_height, 200)
        Xgrid, Ygrid = np.meshgrid(xgrid, ygrid)
        grid_points = np.vstack([Xgrid.ravel(), Ygrid.ravel()]).T
        Z_Kill = kde(grid_points.T).reshape(Xgrid.shape)



        # Create a plot
        fig, ax = plt.subplots(figsize=(8, 8))

        # Display the map layout image with adjustable aspect ratio
        ax.imshow(map_img, extent=(0, img_width, 0, img_height), aspect='auto', alpha=1)

        if(logscale):
            Z_Kill = np.log(Z_Kill+1)  # Adding 1 to avoid log(0)
        # Display the heatmap
        heatmap = ax.imshow( Z_Kill, extent=(0, img_width, 0, img_height), origin='lower', cmap='magma', alpha=0.6, aspect='equal')

        # Plot the points directly on the image
        if(scatterplot):
            ax.scatter(img_coords[:, 0], img_coords[:, 1], color='green', s=25, alpha=0.3)  # Adjust color, size, and alpha as needed

        # Label axes
        ax.set_xlabel('X Coordinate')
        ax.set_ylabel('Y Coordinate')

        # Add a colorbar to serve as a key for the heatmap colors
        cbar = plt.colorbar(heatmap, ax=ax)
        cbar.set_label('Density')
        
        #set title
        if attack and defense:
            plt.title(f'Kill Locations on {map_name} \n On Attack and Defense')
        elif attack:
            plt.title(f'Kill Locations on {map_name} \n On Attack')
        elif defense:
            plt.title(f'Kill Locations on {map_name} \n On Defense')

        # Show the plot
        # plt.show()
        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        plt.close(fig)
        buf.seek(0)
        images['kill_locations'] = base64.b64encode(buf.read()).decode('utf-8')
                
        
            
            # direction = event.get('ViewRadians', 0)
            # dy = np.cos(direction) * 400 #x,y swapped!!!!
            # dx = np.sin(direction) * 400
            # plt.arrow(x, y, dx, dy, color='green', head_width=10, head_length=20, alpha=0.3, linewidth=0.5)
    
    # Plot death data
    if combined_data['death']:
        x_coords = [loc['Location']['x'] for loc in combined_data['death'] ]#x,y swapped!!!!
        y_coords = [loc['Location']['y'] for loc in combined_data['death'] ]
        

        # Convert game coordinates to image coordinates
        img_coords = [game_to_image_coords(gx, gy, img_width, img_height, mapCoords[map_name]['xMultiplier'], mapCoords[map_name]['xScalar'], mapCoords[map_name]['yMultiplier'], mapCoords[map_name]['yScalar']) for gx, gy in zip(x_coords, y_coords)]
        img_coords = np.array(img_coords)


        kde = gaussian_kde(img_coords.T, bw_method=bw)
        xgrid = np.linspace(0, img_width, 200)
        ygrid = np.linspace(0, img_height, 200)
        Xgrid, Ygrid = np.meshgrid(xgrid, ygrid)
        grid_points = np.vstack([Xgrid.ravel(), Ygrid.ravel()]).T
        Z_Death = kde(grid_points.T).reshape(Xgrid.shape)



        # Create a plot
        fig, ax = plt.subplots(figsize=(8, 8))

        # Display the map layout image with adjustable aspect ratio
        ax.imshow(map_img, extent=(0, img_width, 0, img_height), aspect='auto', alpha=1)

        if(logscale):
            Z_Death = np.log(Z_Death+1)  
        # Display the heatmap
        heatmap = ax.imshow( Z_Death, extent=(0, img_width, 0, img_height), origin='lower', cmap='magma', alpha=0.6, aspect='equal')

        # Plot the points directly on the image
        if(scatterplot):
            ax.scatter(img_coords[:, 0], img_coords[:, 1], color='red', s=25, alpha=0.3)  # Adjust color, size, and alpha as needed

        # Label axes
        ax.set_xlabel('X Coordinate')
        ax.set_ylabel('Y Coordinate')

        # Add a colorbar to serve as a key for the heatmap colors
        cbar = plt.colorbar(heatmap, ax=ax)
        cbar.set_label('Density')
        
        
        #set title
        if attack and defense:
            plt.title(f'Death Locations on {map_name} \n On Attack and Defense')
        elif attack:
            plt.title(f'Death Locations on {map_name} \n On Attack')
        elif defense:
            plt.title(f'Death Locations on {map_name} \n On Defense')

        # Show the plot
        # plt.show()
        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        plt.close(fig)
        buf.seek(0)
        images['death_locations'] = base64.b64encode(buf.read()).decode('utf-8')
                

    # Compute the difference between the two KDEs and apply log scale
    # Compute the difference between the two KDEs
    # Z_diff = Z_Kill - Z_Death 
    # Z_diff = np.where(np.abs(Z_diff) < 0.15, 0, Z_diff)
    # Z_diff = Z_diff/(Z_Kill+Z_Death + 10000)

    # Z_Kill = np.where(Z_Kill < 1, 0, Z_Kill)
    # Z_Death = np.where(Z_Death < 1, 0, Z_Death)
    Z_diff = ((Z_Kill + 1) / (Z_Death + 1))#*(Z_Kill + Z_Death)*(1000)

    Z_diff = gaussian_filter(Z_diff, sigma=4)

    # Create a custom colormap with a nonlinear transition to white
    colors = [(0, 'white'), (0.175, 'red'), (0.49,"black"),(0.51,"black"),(0.815, 'green'), (1, 'white')]
    cmap_diff = mcolors.LinearSegmentedColormap.from_list('custom_bwr', colors)
    norm = mcolors.TwoSlopeNorm(vmin=Z_diff.min(), vcenter=1, vmax=Z_diff.max())


    # Create a plot
    fig, ax = plt.subplots(figsize=(8, 8))

    # Display the map layout image with adjustable aspect ratio
    ax.imshow(map_img, extent=(0, img_width, 0, img_height), aspect='auto', alpha=0.5)

    # Display the heatmap
    heatmap = ax.imshow( Z_diff, extent=(0, img_width, 0, img_height), origin='lower', cmap=cmap_diff, alpha=0.6, aspect='equal', norm = norm)
    
    #Display the heatmap ORIGINAL
    # heatmap = ax.imshow( Z_diff, extent=(0, img_width, 0, img_height), origin='lower', cmap=cmap_diff, alpha=0.6, aspect='equal', vmin=-np.abs(Z_diff).max(), vmax=np.abs(Z_diff).max())

#SAVED THIS FOR SETTINGS
    # plt.imshow(Z_diff_log, cmap=cmap_diff, origin='lower', extent=[x_min, x_max, y_min, y_max], vmin=-np.abs(Z_diff_log).max(), vmax=np.abs(Z_diff_log).max(), alpha = 0.65)
    
    # Add a colorbar to serve as a key for the heatmap colors
    cbar = plt.colorbar(heatmap, ax=ax)
    cbar.set_label('<--Bad     Good-->')
    
    #set title
    if attack and defense:
        plt.title(f'Positioning Guide on {map_name} \n On Attack and Defense')
    elif attack:
        plt.title(f'Positioning Guide on {map_name} \n On Attack')
    elif defense:
        plt.title(f'Positioning Guide on {map_name} \n On Defense')


    plt.gca().set_aspect('equal', adjustable='box')
    # plt.show()

    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    plt.close(fig)
    buf.seek(0)
    images['positioning_guide'] = base64.b64encode(buf.read()).decode('utf-8')

    return images        

    
#plots kill heatmap, death heatmap, and combines them to make a positioning heatmap
def plot_data(all_data: dict, map_name: str, attack_options: dict = None, defense_options: dict = None, scatterplot: bool = False, logscale: bool = False):



    if map_name not in all_data:
        print(f"No recorded matches on {map_name}.")
        return
    
    #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    #YOU CAN JUST CALL plot_data_for_map 
    #like this: plot_data_for_map(all_data['map_name'], map_name, attack_options, defense_options, scatterplot, logscale)
    #i havent done it yet because i am scared of deleting all this code


    #GETTING THE IMAGE
    map_img = Image.open(rf"Backend\map_images\{map_name} Map.png")
    map_img = np.array(map_img)  # Convert the image to a NumPy array
    img_height, img_width, _ = map_img.shape  # Get image dimensions


    

    selected_map = all_data[map_name]


    combined_data = {
            'kill': [],
            'death': []
    }
    
    attack = attack_options is not None 
    defense = defense_options is not None 
    if(not attack and not defense):
       print("please select an option ")
       return

    if(attack):
        
        if(attack_options['kills'] != None):
            if 0 <= attack_options['kills']['lower'] <= 159 and 0 <= attack_options['kills']['upper'] <= 159 and attack_options['kills']['lower'] <= attack_options['kills']['upper']:
                for i in range(attack_options['kills']['lower'], attack_options['kills']['upper'] + 1):
                    curr_kill_value = selected_map['Attack']['kill_info'][i]
                    combined_data['kill'].extend(curr_kill_value)

        if(attack_options['deaths'] != None):
            if 0 <= attack_options['deaths']['lower'] <= 159 and 0 <= attack_options['deaths']['upper'] <= 159 and attack_options['deaths']['lower'] <= attack_options['deaths']['upper']:
                for i in range(attack_options['deaths']['lower'], attack_options['deaths']['upper'] + 1):
                    curr_death_value = selected_map['Attack']['death_info'][i]
                    combined_data['death'].extend(curr_death_value)


    if(defense):
        if(defense_options['kills'] != None):
            if 0 <= defense_options['kills']['lower'] <= 159 and 0 <= defense_options['kills']['upper'] <= 159 and defense_options['kills']['lower'] <= defense_options['kills']['upper']:
                for i in range(defense_options['kills']['lower'], defense_options['kills']['upper'] + 1):
                    curr_kill_value = selected_map['Defense']['kill_info'][i]
                    combined_data['kill'].extend(curr_kill_value)

        if(defense_options['deaths'] != None):
            if 0 <= defense_options['deaths']['lower'] <= 159 and 0 <= defense_options['deaths']['upper'] <= 159 and defense_options['deaths']['lower'] <= defense_options['deaths']['upper']:
                for i in range(defense_options['deaths']['lower'], defense_options['deaths']['upper'] + 1):
                    curr_death_value = selected_map['Defense']['death_info'][i]
                    combined_data['death'].extend(curr_death_value)


    bw = 0.06

    # Plot kill data
    if combined_data['kill']:
        x_coords = [loc['Location']['x'] for loc in combined_data['kill'] ]#x,y swapped!!!!
        y_coords = [loc['Location']['y'] for loc in combined_data['kill'] ]

        # Convert game coordinates to image coordinates
        img_coords = [game_to_image_coords(gx, gy, img_width, img_height, mapCoords[map_name]['xMultiplier'], mapCoords[map_name]['xScalar'], mapCoords[map_name]['yMultiplier'], mapCoords[map_name]['yScalar']) for gx, gy in zip(x_coords, y_coords)]
        img_coords = np.array(img_coords)


        # kde = KernelDensity(bandwidth=bw, kernel='gaussian') #NEW KDE FROM SKLEARN
        # kde.fit(img_coords)
        # xgrid = np.linspace(0, img_width, 200)
        # ygrid = np.linspace(0, img_height, 200)
        # Xgrid, Ygrid = np.meshgrid(xgrid, ygrid)
        # grid_points = np.vstack([Xgrid.ravel(), Ygrid.ravel()]).T
        # Z_Kill = np.exp(kde.score_samples(grid_points)).reshape(Xgrid.shape)

        kde = gaussian_kde(img_coords.T, bw_method=bw)
        xgrid = np.linspace(0, img_width, 200)
        ygrid = np.linspace(0, img_height, 200)
        Xgrid, Ygrid = np.meshgrid(xgrid, ygrid)
        grid_points = np.vstack([Xgrid.ravel(), Ygrid.ravel()]).T
        Z_Kill = kde(grid_points.T).reshape(Xgrid.shape)



        # Create a plot
        fig, ax = plt.subplots(figsize=(8, 8))

        # Display the map layout image with adjustable aspect ratio
        ax.imshow(map_img, extent=(0, img_width, 0, img_height), aspect='auto', alpha=1)

        if(logscale):
            Z_Kill = np.log(Z_Kill+1)  # Adding 1 to avoid log(0)
        # Display the heatmap
        heatmap = ax.imshow( Z_Kill, extent=(0, img_width, 0, img_height), origin='lower', cmap='magma', alpha=0.6, aspect='equal')

        # Plot the points directly on the image
        if(scatterplot):
            ax.scatter(img_coords[:, 0], img_coords[:, 1], color='green', s=25, alpha=0.3)  # Adjust color, size, and alpha as needed

        # Label axes
        ax.set_xlabel('X Coordinate')
        ax.set_ylabel('Y Coordinate')

        # Add a colorbar to serve as a key for the heatmap colors
        cbar = plt.colorbar(heatmap, ax=ax)
        cbar.set_label('Density')
        
        #set title
        if attack and defense:
            plt.title(f'Kill Locations on {map_name} \n On Attack and Defense')
        elif attack:
            plt.title(f'Kill Locations on {map_name} \n On Attack')
        elif defense:
            plt.title(f'Kill Locations on {map_name} \n On Defense')

        # Show the plot
        plt.show()

            
        
            
            # direction = event.get('ViewRadians', 0)
            # dy = np.cos(direction) * 400 #x,y swapped!!!!
            # dx = np.sin(direction) * 400
            # plt.arrow(x, y, dx, dy, color='green', head_width=10, head_length=20, alpha=0.3, linewidth=0.5)
    
    # Plot death data
    if combined_data['death']:
        x_coords = [loc['Location']['x'] for loc in combined_data['death'] ]#x,y swapped!!!!
        y_coords = [loc['Location']['y'] for loc in combined_data['death'] ]
        

        # Convert game coordinates to image coordinates
        img_coords = [game_to_image_coords(gx, gy, img_width, img_height, mapCoords[map_name]['xMultiplier'], mapCoords[map_name]['xScalar'], mapCoords[map_name]['yMultiplier'], mapCoords[map_name]['yScalar']) for gx, gy in zip(x_coords, y_coords)]
        img_coords = np.array(img_coords)


        # kde = KernelDensity(bandwidth=bw, kernel='gaussian') #NEW KDE FROM SKLEARN
        # kde.fit(img_coords)
        # xgrid = np.linspace(0, img_width, 200)
        # ygrid = np.linspace(0, img_height, 200)
        # Xgrid, Ygrid = np.meshgrid(xgrid, ygrid)
        # grid_points = np.vstack([Xgrid.ravel(), Ygrid.ravel()]).T
        # Z_Death = np.exp(kde.score_samples(grid_points)).reshape(Xgrid.shape)
        
        kde = gaussian_kde(img_coords.T, bw_method=bw)
        xgrid = np.linspace(0, img_width, 200)
        ygrid = np.linspace(0, img_height, 200)
        Xgrid, Ygrid = np.meshgrid(xgrid, ygrid)
        grid_points = np.vstack([Xgrid.ravel(), Ygrid.ravel()]).T
        Z_Death = kde(grid_points.T).reshape(Xgrid.shape)



        # Create a plot
        fig, ax = plt.subplots(figsize=(8, 8))

        # Display the map layout image with adjustable aspect ratio
        ax.imshow(map_img, extent=(0, img_width, 0, img_height), aspect='auto', alpha=1)

        if(logscale):
            Z_Death = np.log(Z_Death+1)  
        # Display the heatmap
        heatmap = ax.imshow( Z_Death, extent=(0, img_width, 0, img_height), origin='lower', cmap='magma', alpha=0.6, aspect='equal')

        # Plot the points directly on the image
        if(scatterplot):
            ax.scatter(img_coords[:, 0], img_coords[:, 1], color='red', s=25, alpha=0.3)  # Adjust color, size, and alpha as needed

        # Label axes
        ax.set_xlabel('X Coordinate')
        ax.set_ylabel('Y Coordinate')

        # Add a colorbar to serve as a key for the heatmap colors
        cbar = plt.colorbar(heatmap, ax=ax)
        cbar.set_label('Density')
        
        
        #set title
        if attack and defense:
            plt.title(f'Death Locations on {map_name} \n On Attack and Defense')
        elif attack:
            plt.title(f'Death Locations on {map_name} \n On Attack')
        elif defense:
            plt.title(f'Death Locations on {map_name} \n On Defense')

        # Show the plot
        plt.show()


    # Compute the difference between the two KDEs and apply log scale
    # Compute the difference between the two KDEs
    # Z_diff = Z_Kill - Z_Death 
    # Z_diff = np.where(np.abs(Z_diff) < 0.15, 0, Z_diff)
    # Z_diff = Z_diff/(Z_Kill+Z_Death + 10000)

    # Z_Kill = np.where(Z_Kill < 1, 0, Z_Kill)
    # Z_Death = np.where(Z_Death < 1, 0, Z_Death)
    Z_diff = ((Z_Kill + 1) / (Z_Death + 1))#*(Z_Kill + Z_Death)*(1000)

    Z_diff = gaussian_filter(Z_diff, sigma=4)

    # Create a custom colormap with a nonlinear transition to white
    colors = [(0, 'white'), (0.175, 'red'), (0.49,"black"),(0.51,"black"),(0.815, 'green'), (1, 'white')]
    cmap_diff = mcolors.LinearSegmentedColormap.from_list('custom_bwr', colors)
    norm = mcolors.TwoSlopeNorm(vmin=Z_diff.min(), vcenter=1, vmax=Z_diff.max())


    # Create a plot
    fig, ax = plt.subplots(figsize=(8, 8))

    # Display the map layout image with adjustable aspect ratio
    ax.imshow(map_img, extent=(0, img_width, 0, img_height), aspect='auto', alpha=0.5)

    # Display the heatmap
    heatmap = ax.imshow( Z_diff, extent=(0, img_width, 0, img_height), origin='lower', cmap=cmap_diff, alpha=0.6, aspect='equal', norm = norm)
    
    #Display the heatmap ORIGINAL
    # heatmap = ax.imshow( Z_diff, extent=(0, img_width, 0, img_height), origin='lower', cmap=cmap_diff, alpha=0.6, aspect='equal', vmin=-np.abs(Z_diff).max(), vmax=np.abs(Z_diff).max())

#SAVED THIS FOR SETTINGS
    # plt.imshow(Z_diff_log, cmap=cmap_diff, origin='lower', extent=[x_min, x_max, y_min, y_max], vmin=-np.abs(Z_diff_log).max(), vmax=np.abs(Z_diff_log).max(), alpha = 0.65)
    
    # Add a colorbar to serve as a key for the heatmap colors
    cbar = plt.colorbar(heatmap, ax=ax)
    cbar.set_label('<--Bad     Good-->')
    
    #set title
    if attack and defense:
        plt.title(f'Positioning Guide on {map_name} \n On Attack and Defense')
    elif attack:
        plt.title(f'Positioning Guide on {map_name} \n On Attack')
    elif defense:
        plt.title(f'Positioning Guide on {map_name} \n On Defense')


    plt.gca().set_aspect('equal', adjustable='box')
    plt.show()


    # plt.title(f"Game Events Visualization on {map_name}")
    # plt.xlabel('Y Coordinate')#x,y swapped!!!!
    # plt.ylabel('X Coordinate')
    # plt.grid(True)
    
    # # Add a legend to explain color codes
    # plt.scatter([], [], color='green', label='Kill Locations', alpha=0.3, s=50)
    # plt.scatter([], [], color='red', label='Death Locations', alpha=0.3, s=50)
    # plt.legend(loc='upper right')

    # plt.show()


#combines the kill and death data to generate a general 'activity' heatmap
def plot_activity(all_data: dict, map_name: str, attack_options: dict = None, defense_options: dict = None, scatterplot: bool = False, logscale: bool = False):
    
    if map_name not in all_data:
        print(f"No recorded matches on {map_name}.")
        return
    
    #GETTING THE IMAGE
    map_img = Image.open(rf"Backend\map_images\{map_name} Map.png")
    map_img = np.array(map_img)  # Convert the image to a NumPy array
    img_height, img_width, _ = map_img.shape  # Get image dimensions


 
    selected_map = all_data[map_name]


    combined_data= []
    attack = attack_options is not None  #check which options we want
    defense = defense_options is not None 
    if(not attack and not defense):
       print("please select an option ")
       return

    if(attack):
        if(attack_options['kills'] != None):
            if 0 <= attack_options['kills']['lower'] <= 159 and 0 <= attack_options['kills']['upper'] <= 159 and attack_options['kills']['lower'] <= attack_options['kills']['upper']:
                for i in range(attack_options['kills']['lower'], attack_options['kills']['upper'] + 1):
                    curr_kill_value = selected_map['Attack']['kill_info'][i]
                    combined_data.extend(curr_kill_value)

        if(attack_options['deaths'] != None):
            if 0 <= attack_options['deaths']['lower'] <= 159 and 0 <= attack_options['deaths']['upper'] <= 159 and attack_options['deaths']['lower'] <= attack_options['deaths']['upper']:
                for i in range(attack_options['deaths']['lower'], attack_options['deaths']['upper'] + 1):
                    curr_death_value = selected_map['Attack']['death_info'][i]
                    combined_data.extend(curr_death_value)


    if(defense):
        if(defense_options['kills'] != None):
            if 0 <= defense_options['kills']['lower'] <= 159 and 0 <= defense_options['kills']['upper'] <= 159 and defense_options['kills']['lower'] <= defense_options['kills']['upper']:
                for i in range(defense_options['kills']['lower'], defense_options['kills']['upper'] + 1):
                    curr_kill_value = selected_map['Defense']['kill_info'][i]
                    combined_data.extend(curr_kill_value)

        if(defense_options['deaths'] != None):
            if 0 <= defense_options['deaths']['lower'] <= 159 and 0 <= defense_options['deaths']['upper'] <= 159 and defense_options['deaths']['lower'] <= defense_options['deaths']['upper']:
                for i in range(defense_options['deaths']['lower'], defense_options['deaths']['upper'] + 1):
                    curr_death_value = selected_map['Defense']['death_info'][i]
                    combined_data.extend(curr_death_value)


    
    x_coords = [loc['Location']['x'] for loc in combined_data ]
    y_coords = [loc['Location']['y'] for loc in combined_data ]

    # Convert game coordinates to image coordinates
    img_coords = [game_to_image_coords(gx, gy, img_width, img_height, mapCoords[map_name]['xMultiplier'], mapCoords[map_name]['xScalar'], mapCoords[map_name]['yMultiplier'], mapCoords[map_name]['yScalar']) for gx, gy in zip(x_coords, y_coords)]
    img_coords = np.array(img_coords)

    print('starting KDE...')
    kde = KernelDensity(bandwidth=12, kernel='gaussian') #NEW KDE FROM SKLEARN
    kde.fit(img_coords)
    xgrid = np.linspace(0, img_width, 200)
    ygrid = np.linspace(0, img_height, 200)
    Xgrid, Ygrid = np.meshgrid(xgrid, ygrid)
    grid_points = np.vstack([Xgrid.ravel(), Ygrid.ravel()]).T
    Z = np.exp(kde.score_samples(grid_points)).reshape(Xgrid.shape)
    print('finished KDE')

    # Create a plot
    fig, ax = plt.subplots(figsize=(8, 8))

    # Display the map layout image with adjustable aspect ratio
    ax.imshow(map_img, extent=(0, img_width, 0, img_height), aspect='auto', alpha=1)

    if(logscale):
        Z = np.log(Z+ 0.000004)  # Adding 1 to avoid log(0)
    # Display the heatmap
    heatmap = ax.imshow( Z, extent=(0, img_width, 0, img_height), origin='lower', cmap='magma', alpha=0.6, aspect='equal')

    # Plot the points directly on the image
    if(scatterplot):
        ax.scatter(img_coords[:, 0], img_coords[:, 1], color='blue', s=10, alpha=0.4)  # Adjust color, size, and alpha as needed

    # Label axes
    ax.set_xlabel('X Coordinate')
    ax.set_ylabel('Y Coordinate')

    # Add a colorbar to serve as a key for the heatmap colors
    cbar = plt.colorbar(heatmap, ax=ax)
    cbar.set_label('Density')
    
    if attack and defense:
        plt.title(f'Kills & Death Locations on {map_name} \n On Attack and Defense')
    elif attack:
        plt.title(f'Kills & Death Locations on {map_name} \n On Attack')
    elif defense:
        plt.title(f'Kills & Death Locations on {map_name} \n On Defense')

    # Show the plot
    #plt.show()



    # Save the plot to a BytesIO object
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    plt.close(fig)
    buf.seek(0)

    # Encode the image in base64
    image_base64 = base64.b64encode(buf.read()).decode('utf-8')

    return image_base64



    # Plot the scatter plot of points
    
    # plt.figure(figsize=(18, 8))
    # if(True):
    #     plt.subplot(1, 2, 1)
    #     plt.scatter(x_coords, y_coords, c='blue', alpha=0.3, s=30)  # Reduced size to half
        
        


    #     plt.title('All Locations')
    #     plt.xlabel('X coordinate')
    #     plt.ylabel('Y coordinate')
    #     plt.imshow(map_img, extent=[x_min-700, x_max+900, y_min-1500, y_max+1950], aspect='auto', alpha=1)

    #     # Plot the KDE contour map
    #     plt.subplot(1, 2, 2)
    #     contour = plt.contourf(X, Y, Z_Kill, levels=10, cmap='magma')  # Adjust levels as needed
    #     plt.colorbar(contour)
    #     plt.title('Topographical Heatmap with KDE')
    #     plt.xlabel('X coordinate')
    #     plt.ylabel('Y coordinate')
    #     plt.show()



    # # Apply logarithmic scaling to enhance contrast
    # Z1_log = np.log(Z_Kill+ 0.00000004)  # Adding 1 to avoid log(0)
    # #plt.contourf(X, Y, Z1_log, levels=10, cmap='magma')  # Adjust levels as needed
    
    # plt.imshow(map_img, extent=[x_min-700, x_max+900, y_min-1500, y_max+1950], aspect='auto', alpha=1)

    # plt.imshow(Z1_log, cmap='magma', origin='lower', extent=[x_min, x_max, y_min, y_max], alpha = 0.65)


    # #plt.imshow(Z1_log, cmap='magma', origin='lower', extent=[x_min+ 3*padding, x_max+ 3*padding, y_min+ 3*padding, y_max+ 3*padding])
    # plt.colorbar(label='Log Density')
    # plt.title('Logarithmic Scale Heatmap of KDE(Kills + Deaths)')
    # plt.xlabel('X coordinate')
    # plt.ylabel('Y coordinate')

    # plt.tight_layout()
    # plt.gca().set_aspect('equal', adjustable='box')
    # plt.show()


#plots all data for all maps in a standard way(coordinate points)
def plot_all_data(all_data):
    combined_data_by_map = {}

    # Combine all data into one dictionary
    for map_name, sides in all_data.items():

        
        
        combined_data_by_map[map_name] = {
            'kill': [kill for side in sides.values() for kills in side.get('kill_info', []) for kill in kills ],
            'death': [death for side in sides.values() for deaths in side.get('death_info', []) for death in deaths ]
        }

    # Plotting the data
    for map_name, data in combined_data_by_map.items():
        plt.figure(figsize=(10, 8))

        

        
        # Plot kill data
        for event in data['kill']:
            if 'Location' in event and event['Location']:
                y = event['Location']['x'] 
                x = event['Location']['y']
                plt.scatter(x, y, marker='o', color='green', alpha=0.3, s=15)  # Reduced size to half
                direction = event.get('ViewRadians', 0)
                dx = np.cos(direction) * 400
                dy = np.sin(direction) * 400
                plt.arrow(x, y, dx, dy, color='green', head_width=10, head_length=20, alpha=0.3, linewidth=0.5)
        
        # Plot death data
        if data['death']:
            y_coords = [loc['Location']['x'] for loc in data['death'] ]
            x_coords = [loc['Location']['y'] for loc in data['death'] ]
            plt.scatter(x_coords, y_coords, c='red', alpha=0.3, s=15)  # Reduced size to half

        plt.title(f"Game Events Visualization on {map_name}")
        plt.xlabel('Y Coordinate')
        plt.ylabel('X Coordinate')
        plt.grid(True)
        
        # Add a legend to explain color codes
        plt.scatter([], [], color='green', label='Kill Locations', alpha=0.3, s=50)
        plt.scatter([], [], color='red', label='Death Locations', alpha=0.3, s=50)
        plt.legend(loc='upper right')

        plt.show()


def plot_buy_frequency(all_data: dict, map_name: str):
    if map_name not in all_data:
        print(f"No recorded matches on {map_name}.")
        return
    
    selected_map = all_data[map_name]
    attack_buy_freq = [0] * 160
    defense_buy_freq = [0] * 160

    for i, (kill_info, death_info) in enumerate(zip(selected_map['Attack']['kill_info'], selected_map['Attack']['death_info'])):
        attack_buy_freq[i] += len(kill_info) + len(death_info)

    for i, (kill_info, death_info) in enumerate(zip(selected_map['Defense']['kill_info'], selected_map['Defense']['death_info'])):
        defense_buy_freq[i] += len(kill_info) + len(death_info)
    plt.figure(figsize=(10, 8))
    plt.subplot(2, 1, 1)
    plt.bar([i * 50 for i in range(len(attack_buy_freq))], attack_buy_freq, alpha=0.5, color='red', label='Attack')
    plt.title(f'Attack Buy Frequency on {map_name}')
    plt.xlabel('Index')
    plt.ylabel('Frequency')
    plt.legend()

    plt.subplot(2, 1, 2)
    plt.bar([i * 50 for i in range(len(defense_buy_freq))], defense_buy_freq, alpha=0.5, label='Defense')
    plt.title(f'Defense Buy Frequency on {map_name}')
    plt.xlabel('Index')
    plt.ylabel('Frequency')
    plt.legend()

    plt.tight_layout()
    plt.show()


