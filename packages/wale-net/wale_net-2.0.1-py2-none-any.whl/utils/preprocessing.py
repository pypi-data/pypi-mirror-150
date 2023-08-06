# Third party imports
import numpy as np
import matplotlib.pyplot as plt
import cv2
from commonroad.visualization.draw_dispatch_cr import draw_object

# Custom imports
from utils.geometry import point_in_rectangle


def generate_scimg(scenario, now_point, theta, time_step, draw_shape=True):
    """Generate image input for neural network
    
    Arguments:
        scenario {[Commonroad scenario]} -- [Scenario object from CommonRoad]
        now_point {[list]} -- [[x,y] coordinates of vehicle right now that will be predicted]
        theta {[float]} -- [orientation of the vehicle that will be predicted]
        time_step {[float]} -- [Global time step of scenario]
    
    Keyword Arguments:
        draw_shape {bool} -- [Draw shapes of dynamic obstacles in image] (default: {True})
    
    Returns:
        img_gray [np.array] -- [Black and white image with 256 x 256 pixels of the scene]
    """

    my_dpi = 300
    fig = plt.figure(figsize=(256 / my_dpi, 256 / my_dpi), dpi=my_dpi)
    scenario.translate_rotate(np.array(-now_point), -theta)

    draw_object(scenario, draw_params={'time_begin': time_step, 'scenario': {'dynamic_obstacle': {'draw_shape': draw_shape}}})

    plt.gca().set_axis_off()
    plt.subplots_adjust(top=1, bottom=0, right=1, left=0, hspace=0, wspace=0)
    plt.gca().set_aspect('equal')
    plt.xlim(-64, 64)
    plt.ylim(-64, 64)

    fig.canvas.draw()
    plt.close()

    # convert canvas to image
    img = np.fromstring(fig.canvas.tostring_rgb(), dtype=np.uint8, sep='')
    img = img.reshape(fig.canvas.get_width_height()[::-1] + (3,))

    img_gray = ~cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    return img_gray


def generate_nbr_array(trans_traj_list, time_step, pp=31, window_size=[18, 78]):
    """Generates the array of trajectories around the vehicle being predicted
    
    Arguments:
        trans_traj_list {[type]} -- [description]
        time_step {[type]} -- [description]
    
    Keyword Arguments:
        pp {int} -- [description] (default: {31})
        window_size {list} -- [description] (default: {[18, 78]})
    
    Returns:
        [type] -- [description]
    """
    
    # Define window to identify neihbors
    r1 = [int(-i / 2) for i in window_size]  # [-9, -39]
    r2 = [int(i / 2) for i in window_size]

    nbrs = np.zeros((3, 13, pp, 2))
    pir_list = []
    for nbr in trans_traj_list:
        try:
            now_point_nbr = nbr[time_step]
        except IndexError:
            continue

        pir = point_in_rectangle(r1, r2, now_point_nbr)
        if pir:
            nbrs[pir] = nbr[time_step - pp:time_step]
            pir_list.append(pir)
    
    return nbrs, pir_list, r1, r2
