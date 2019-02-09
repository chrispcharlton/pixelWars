def find_position(x_max, y_max, position, resolution):
    # Splits the surface (x_max,y_max) into a resolution by resolution grid and then gets the coordinates of the given position
    resolution_x = x_max / resolution
    resolution_y = y_max / resolution
    # TODO: this needs to always round down. could also split for greater readability
    position_s = (int(round((position[0]/resolution_x),0)),int(round((position[1]/resolution_y),0)))
    return position_s

x_max = 400
y_max = 400

position = (259,367)
resolution = 2
pos_s = find_position(x_max, y_max, position,resolution)
print(pos_s)

position = (6,50)
resolution = 40
pos_s = find_position(x_max, y_max, position,resolution)
print(pos_s)

