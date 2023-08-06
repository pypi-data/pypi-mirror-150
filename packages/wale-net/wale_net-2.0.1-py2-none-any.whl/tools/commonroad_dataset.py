# Standard imports
import sys
import os
import pickle
import random
import math

# Third party imports
import progressbar
import cv2
from joblib import Parallel, delayed
import multiprocessing
import argparse
from commonroad.common.file_reader import CommonRoadFileReader

# Custom imports
if __name__ == '__main__' and not __package__:
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
    
from utils.geometry import transform_trajectories
from utils.preprocessing import generate_scimg, generate_nbr_array
from utils.visualization import draw_in_scene


# Parse arguments
parser = argparse.ArgumentParser()
parser.add_argument('--debug', action='store_true', default=False)
parser.add_argument('--small', action='store_true', default=False)
args = parser.parse_args()


# Initialization
random.seed(0)

data_directory = 'data/commonroad/'
scenario_directory = os.path.join(data_directory, 'scenes')

if args.small:
    sc_img_dir = os.path.join(data_directory, 'sc_imgs_small/')
else:
    sc_img_dir = os.path.join(data_directory, 'sc_imgs600/')

if not os.path.exists(sc_img_dir):
    os.makedirs(sc_img_dir)

pp = 31  # past points
fp = 50  # future points

hist_list = []
fut_list = []
nbrs_list = []
id_list = []
sliwi_size = 1

if args.small:
    sliwi_size = 10


def parse_scene(file_name):

    scenario, _ = CommonRoadFileReader(os.path.join(scenario_directory, file_name)).open()
    try:
        trajectories_list = [[scenario.dynamic_obstacles[i].prediction.trajectory.state_list[j].position for j in range(0, len(scenario.dynamic_obstacles[i].prediction.trajectory.state_list))] for i in range(0, len(scenario.dynamic_obstacles))]
        orientation_list = [[scenario.dynamic_obstacles[i].prediction.trajectory.state_list[j].orientation for j in range(0, len(scenario.dynamic_obstacles[i].prediction.trajectory.state_list))] for i in range(0, len(scenario.dynamic_obstacles))]
    except AttributeError:
        return [], [], [], []

    smpl_id = 0
    scene_id = scenario.benchmark_id

    # Iterate over all trajectories in a scenario
    for ti, traj in enumerate(trajectories_list):
        # check if trajectory is long enough
        if len(traj) < (pp + fp):
            continue

        # Iterate over possible windows within a trajectory
        for w in range(0, len(traj) - (pp + fp), sliwi_size):  # only add trajectories with temporal distant of 10 timesteps = 1 second
            time_step = pp + w
            now_point = traj[time_step]
            orientation = orientation_list[ti][time_step]

            # Adapt rotatin
            orientation -= math.pi / 2

            trans_traj_list = transform_trajectories(trajectories_list, now_point, orientation)

            hist = trans_traj_list[ti][w:pp + w]
            fut = trans_traj_list[ti][pp + w:pp + fp + w]

            # generate neighbors array
            nbrs, pir_list, r1, r2 = generate_nbr_array(trans_traj_list, time_step)

            hist_list.append(hist)
            fut_list.append(fut)
            nbrs_list.append(nbrs)
            id_list.append(scene_id + '_' + str(smpl_id).zfill(8))

            # genearte scene image
            img_gray = generate_scimg(scenario, now_point, orientation, time_step, draw_shape=False)

            if not args.debug:
                cv2.imwrite(sc_img_dir + scene_id + '_' + str(smpl_id).zfill(8) + '.png', img_gray)

            # Reload scenario to keep original orientation and translation
            scenario, _ = CommonRoadFileReader(os.path.join(scenario_directory, file_name)).open()

            if args.debug:
                img = draw_in_scene(fut, img_gray, nbr_utils=[r1, r2, pir_list])
                cv2.imshow('Debug visualization', img)
                cv2.waitKey(0)

            smpl_id += 1

    return [id_list, hist_list, fut_list, nbrs_list]


scenario_list = os.listdir(scenario_directory)
scenario_list.sort()
random.shuffle(scenario_list)

# Evaluate scenes on all available cores
if args.debug:
    num_cores = 1
else:
    num_cores = multiprocessing.cpu_count()
print("Running on {} cores".format(num_cores))

if args.small:
    scenario_list = ['ZAM_Tjunction-1_153_T-1.xml']

result_lists = Parallel(n_jobs=num_cores)(delayed(parse_scene)(i) for i in progressbar.progressbar(scenario_list))

# Encode results_list
hist_list = []
fut_list = []
nbrs_list = []
id_list = []
for res in result_lists:
    id_list.extend(res[0])
    hist_list.extend(res[1])
    fut_list.extend(res[2])
    nbrs_list.extend(res[3])


if args.small:
    output = {
        'id': id_list,
        'hist': hist_list,
        'fut': fut_list,
        'nbrs': nbrs_list
    }

    with open(os.path.join(data_directory, 'small.txt'), "wb") as fp:
        pickle.dump(output, fp)

else:

    # Create train, test and validation set
    val_split = 0.2
    test_split = 0.2
    train_split = 1 - val_split - test_split
    length = len(hist_list)

    train_idx = int(length * train_split)
    val_idx = train_idx + int(length * val_split) + 1

    train_output = {
        'id': id_list[:train_idx],
        'hist': hist_list[:train_idx],
        'fut': fut_list[:train_idx],
        'nbrs': nbrs_list[:train_idx]
    }

    validation_output = {
        'id': id_list[train_idx:val_idx],
        'hist': hist_list[train_idx:val_idx],
        'fut': fut_list[train_idx:val_idx],
        'nbrs': nbrs_list[train_idx:val_idx]
    }

    test_output = {
        'id': id_list[val_idx:],
        'hist': hist_list[val_idx:],
        'fut': fut_list[val_idx:],
        'nbrs': nbrs_list[val_idx:]
    }

    with open(os.path.join(data_directory, 'train600.txt'), "wb") as fp:
        pickle.dump(train_output, fp)

    with open(os.path.join(data_directory, 'validation600.txt'), "wb") as fp:
        pickle.dump(validation_output, fp)

    with open(os.path.join(data_directory, 'test600.txt'), "wb") as fp:
        pickle.dump(test_output, fp)


print('Ende')
