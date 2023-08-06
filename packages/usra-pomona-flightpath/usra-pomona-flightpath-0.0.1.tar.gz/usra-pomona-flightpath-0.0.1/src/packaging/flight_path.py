import math
import matplotlib.pyplot as plt
import json 
import argparse
import os

########## DEFINITIONS
#function that finds position of one coordinate relative to another coordinate on an XY plane.
#Based on Equirectangular projection of Earth (this leads to some error)
def coord_to_vector (coord1, coord2):
    R = 6371000 #radius of Earth in meters
    x = math.pi*(coord2[1]-coord1[1])/180*math.cos(math.pi/180*(coord1[0]+coord2[0])/2)
    X = R*x
    y = math.pi/180*(coord2[0]-coord1[0])
    Y = R*y
    return X, Y

#function that finds the coordinates of a position given its location relative to a coordinate.
#Based on Equirectangular projection of Earth (this leads to some error)
def vector_to_coord (coord, vector):
    R = 6371000 #radius of Earth in meters
    x = vector[0]/R
    y = vector[1]/R
    coordnew = [0]*2
    coordnew[0] = (y + coord[0]*math.pi/180)*180/math.pi
    coordnew[1] = x/math.cos(math.pi/180*(coord[0]+coordnew[0])/2)*180/math.pi+coord[1]
    return coordnew
    
def generate_vectors (R, separation, numb_of_sections):
    n = (numb_of_sections * 2) + 1
    x = [0] * n
    y = [0] * n
    x[0] = R # generates 1st vector for 1st waypoint
    y[0] = 0 

    for i in range(1, n - 2, 4): #generates a portion of 4 vectors to later represent a sequence of 4 waypoints
        x[i] = R - separation * (i + 1) / 2
        x[i + 1] = x[i]
        y[i] = math.sqrt(R ** 2 - x[i] ** 2)
        y[i + 1] = -y[i]
        x[i + 2] = R - separation * (i + 3) / 2
        x[i + 3] = x[i + 2]
        y[i + 2] = -(math.sqrt(R ** 2 - x[i + 2] ** 2))
        y[i + 3] = -y[i + 2]

    if (n - 1) % 4 != 0: # in case last sequence does not have 4 points (then it has two, by math)
        x[n-2] = -R
        y[n-2] = 0
        x[n-1] = -R
        y[n-1] = 0
        del x[-1]
        del y[-1]
    return x, y 

def plot_path(longitude_out, latitude_out, output_dir):
    plt.plot(longitude_out, latitude_out) #plots Lat, Long Points
    plt.grid(True)
    plt.gca().get_xaxis().get_major_formatter().set_useOffset(False)
    plt.gca().get_yaxis().get_major_formatter().set_useOffset(False)
    plt.title('Flight Coordinates')
    plt.savefig('%s/flight_coordinates.png' % (output_dir))   
    
def path_planning(output_dir, sep_coefficient, altitude, lat, long, radius, plot=True):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    path = {"coords":[]}

    ######### INPUTS   
    sep_coefficient = sep_coefficient   #29 / 74 #### INPUT ###### SEPARATION DISTANCE BETWEEN LINES, PLAY WITH IT
    path['Separation Coefficient'] = sep_coefficient

    altitude_meters = altitude * 0.3048
    altitude= altitude_meters #### INPUT ###### ALTITUDE OF FLIGHT
    path['Altitude'] = altitude
    if altitude>0:
        separation = altitude * sep_coefficient
        #print("The distance between the drone path is equal to: "+ str(separation))
        path["Distance between drone path"] = separation
    else:
        raise ValueError('That altitude cannot be reached. Please input an altitude greater than 0.')
        #print("That altitude cannot be reached.")
        quit()

    center_1 = [lat, long] #### INPUT ###### GPS LOCATION OF THE CENTER
    path['Center'] = center_1
    
    
    radius_1 = radius * 0.3048 #### INPUT ###### RADIUS OF THE CIRCLE
    path['Radius'] = radius_1

    ######## PATH GENERATION
    numb_of_sections = int(2 * radius_1 / separation)
    vectors = generate_vectors (radius_1, separation, numb_of_sections)
    n = len(vectors[0])
    latitude_out = [0] * n
    longitude_out = [0] * n

    for i in range(n):
        new_vector = [vectors[0][i], vectors[1][i]]
        new_coordinate = vector_to_coord (center_1, new_vector)
        latitude_out[i] = new_coordinate[0]
        longitude_out[i] = new_coordinate[1]
        #print( str(new_coordinate[0]) + " " + str(new_coordinate[1]) )
        path['coords'].append({"lat":new_coordinate[0],"long":new_coordinate[1]})

    with open(f'{output_dir}/flight_coordinates.json', 'w') as f:
        json.dump(path, f, indent=4)

    if plot is True:
        plot_path(longitude_out, latitude_out, output_dir)

#Example:
#path_planning(output_dir='TEST', sep_coefficient=1.4, altitude=30, lat=34, long=-117, radius=50, plot=False)

