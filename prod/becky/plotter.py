import matplotlib.pyplot as plt

"""You will need to plt.ion() in the main code and plt.pause(0.0001) or
something may be necessary to continually update and ax.clear()"""

def boardplot(robot_coords, blocks, frame):
    """Plots everything on a board map"""

    if type(robot_coords) == tuple:
        # Get the location of the robot
        rx = robot_coords[0]
        ry = robot_coords[1]
        # Plot the robot as a triangle
        plt.scatter(ry,240-rx,color='y',marker='*')

    # Gets and plots the block coordinates
    for i in blocks.values():
        #xb_cm = round(i.coord[1]*240/1473, 2)
        #yb_cm = 240-round((1473-i.coord[1])*240/1473, 2)
        plt.scatter(i.map_coord_cm[1],240-i.map_coord_cm[0],color='b')

    """We now plot the rest of the grid"""

    plt.xlim(xmin=0,xmax=240)
    plt.ylim(ymin=0,ymax=240)

    # Horiztonal white start boxes
    plt.fill([8,8,52,52],[227,225,225,227],color='w')
    plt.fill([8,8,52,52],[195,193,193,195],color='w')
    plt.fill([0,0,70,70],[211,209,209,211],color='w')
    plt.fill([8,8,52,52],[13,15,15,13],color='w')
    plt.fill([8,8,52,52],[47,45,45,47],color='w')
    plt.fill([0,0,70,70],[31,29,29,31],color='w')
    # Horiztonal checks
    plt.fill([240,240,220,220],[79,81,81,79],color='w')
    plt.fill([240,240,220,220],[99,101,101,99],color='w')
    plt.fill([240,240,220,220],[119,121,121,119],color='w')
    plt.fill([240,240,220,220],[139,141,141,139],color='w')
    plt.fill([240,240,220,220],[159,161,161,159],color='w')
    # Safe Zone
    plt.fill([0,0,22,22],[98,100,100,98],color='g')
    plt.fill([0,0,22,22],[142,140,140,142],color='g')

    # Vertical white start boxes
    plt.fill([8,8,10,10],[13,45,45,13],color='w')
    plt.fill([50,50,52,52],[13,45,45,13],color='w')
    plt.fill([8,8,10,10],[227,195,195,227],color='w')
    plt.fill([50,50,52,52],[227,195,195,227],color='w')
    plt.fill([29,29,31,31],[0,240,240,0],color='w')

    # Vertical green
    plt.fill([20,20,22,22],[98,142,142,98],color='g')

    # Vertical check
    plt.fill([229,229,231,231],[60,180,180,60],color='w')

    # shelf
    plt.fill([0,0,9,9],[100,140,140,100],color=(0.651,0.502,0.3922))

    # red line
    plt.fill([119,121,121,119],[0,240,240,0],color='r')

    # Black background
    ax = plt.gca()
    ax.set_facecolor((0.5, 0.5, 0.5))

    # Plot
    plt.rcParams["figure.figsize"] = (7,7)
    plt.xticks([])
    plt.yticks([])
    plt.show()
    plt.pause(0.00001)
    ax.clear()
