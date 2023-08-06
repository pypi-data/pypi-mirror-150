import cv2
import numpy as np
from scipy.stats import multivariate_normal
import matplotlib.pyplot as plt

# Global variables
rs_img = 4
pixel_pro_meter = 2
point_zero = 128


def detach_from_cuda(fut_gt, sc_img, fut_pred1, fut_pred2, probs):
    # detach variable from cuda
    try:
        sc_img = sc_img.cpu().detach().numpy()
    except AttributeError:
        pass
    try:
        fut_gt = fut_gt.cpu().detach().numpy()
    except AttributeError:
        pass
    try:
        fut_pred1 = fut_pred1.cpu().detach.numpy()
    except AttributeError:
        pass
    try:
        fut_pred2 = fut_pred2.cpu().detach().numpy()
    except AttributeError:
        pass
    try:
        probs = probs.cpu().detach().numpy()
    except AttributeError:
        pass
    
    return fut_gt, sc_img, fut_pred1, fut_pred2, probs


def draw_prediction(img, fut_pred, color=(0, 0, 1)):
    # copy for transparency
    overlay = img.copy()
    fut_pred = fut_pred.cpu()

    # if one dimension is the batch size
    if len(fut_pred.shape) == 3:
        fut_pred = fut_pred[:, 0, :]

    for p_pred in fut_pred:
        cv2.circle(overlay, (int((p_pred[0] * pixel_pro_meter + point_zero) * rs_img), int(((-p_pred[1] * pixel_pro_meter + point_zero) * rs_img))), 3, color, -1)
        # standarddeviation
        sigma_x = 1 / p_pred[2]
        cv2.circle(overlay, (int(((p_pred[0] - sigma_x) * pixel_pro_meter + point_zero) * rs_img), int(((-p_pred[1] * pixel_pro_meter + point_zero) * rs_img))), 2, (0, 1, 1), -1)
        cv2.circle(overlay, (int(((p_pred[0] + sigma_x) * pixel_pro_meter + point_zero) * rs_img), int(((-p_pred[1] * pixel_pro_meter + point_zero) * rs_img))), 2, (0, 1, 1), -1)

    # Following line overlays transparent rectangle over the image
    img = cv2.addWeighted(overlay, 0.5, img, 1 - 0.5, 0)

    return img


def draw_gt(img, fut_gt):
    try:
        fut_gt = fut_gt.cpu()
    except AttributeError:
        pass
    # if one dimension is the batch size
    if len(fut_gt.shape) == 3:
        fut_gt = fut_gt[:, 0, :]
    for p_gt in fut_gt:
        np_gt = np.array(p_gt)
        cv2.circle(img, (int((np_gt[0] * pixel_pro_meter + point_zero) * rs_img), int(((-np_gt[1] * pixel_pro_meter + point_zero) * rs_img))), 3, (1, 0, 0), -1)

    return img


def draw_img_encoding(img, sc_img_pred):
    # in case we have a batch size greater than 1
    if len(sc_img_pred.shape) > 1:
        sc_img_pred = sc_img_pred[0]
    for po_no, point in enumerate(sc_img_pred):
        pt1 = (img.shape[0] - 100, img.shape[1] - 50 - po_no * 10)
        pt2 = (pt1[0] + int(point) * 8, pt1[1])
        cv2.line(img, pt1, pt2, (1, 1, 1), 2)
    
    return img


def draw_neighbors_input(img, nbr_utils):
    # unpack neighbor utils
    [r1, r2, pir_list] = nbr_utils
    # neighbor rectangle
    cv2.rectangle(img, (int(point_zero + r1[0] * pixel_pro_meter) * rs_img, int(point_zero + r1[1] * pixel_pro_meter) * rs_img), (int(point_zero + r2[0] * pixel_pro_meter) * rs_img, int(point_zero + r2[1] * pixel_pro_meter) * rs_img), (1, 1, 0))
    # besetzte spots
    img_tr = img.copy()
    for pir in pir_list:
        p1 = (r1[0] + pir[0] * 6, r1[1] + pir[1] * 6)
        p2 = (r1[0] + (pir[0] + 1) * 6, r1[1] + (pir[1] + 1) * 6)
        cv2.rectangle(img_tr, (int(point_zero + p1[0] * pixel_pro_meter) * rs_img, int(point_zero + p1[1] * pixel_pro_meter) * rs_img), (int(point_zero + p2[0] * pixel_pro_meter) * rs_img, int(point_zero + p2[1] * pixel_pro_meter) * rs_img), (1, 1, 0), -1)
    for i in range(0, 3):
        for j in range(0, 13):
            p1 = (r1[0] + i * 6, r1[1] + j * 6)
            p2 = (r1[0] + (i + 1) * 6, r1[1] + (j + 1) * 6)
            cv2.rectangle(img_tr, (int(point_zero + p1[0] * pixel_pro_meter) * rs_img, int(point_zero + p1[1] * pixel_pro_meter) * rs_img), (int(point_zero + p2[0] * pixel_pro_meter) * rs_img, int(point_zero + p2[1] * pixel_pro_meter) * rs_img), (1, 1, 0))
    img = cv2.addWeighted(img_tr, 0.4, img, 0.6, 0)
    return img


def draw_in_scene(fut_gt, sc_img, fut_pred1=None, fut_pred2=None, probs=None, sc_img_pred=None, nbr_utils=None, scene_id=None):

    fut_gt, sc_img, fut_pred1, fut_pred2, probs = detach_from_cuda(fut_gt, sc_img, fut_pred1, fut_pred2, probs)

    if len(sc_img.shape) == 4:
        sc_img = sc_img[0]  # if batch size > 1

    # re-color image
    np_sc_img = cv2.cvtColor(np.array(sc_img / 255).reshape(256, 256, 1).astype(np.float32), cv2.COLOR_GRAY2BGR)
    np_sc_img = cv2.resize(np_sc_img, (np_sc_img.shape[0] * rs_img, np_sc_img.shape[1] * rs_img))
    
    # Draw ground truth
    np_sc_img = draw_gt(np_sc_img, fut_gt)

    # Plot prediction(s)
    if fut_pred1 is not None:
        np_sc_img = draw_prediction(np_sc_img, fut_pred1, color=(0, 0, 1))

    if fut_pred2 is not None:
        np_sc_img = draw_prediction(np_sc_img, fut_pred2, color=(0, 1, 0))
        
    if probs is not None:
        cv2.putText(np_sc_img, str(np.round(probs[0, 0], 3))[:4], (50, 200), cv2.FONT_HERSHEY_SIMPLEX, 1, color=(0, 0, 1))
        cv2.putText(np_sc_img, str(np.round(probs[0, 1], 3))[:4], (50, 250), cv2.FONT_HERSHEY_SIMPLEX, 1, color=(0, 1, 0))

    if sc_img_pred is not None:
        np_sc_img = draw_img_encoding(np_sc_img, sc_img_pred)

    if scene_id is not None:
        cv2.putText(np_sc_img, scene_id, (20, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.8, color=(1, 1, 1))
    
    if nbr_utils is not None:
        np_sc_img = draw_neighbors_input(np_sc_img, nbr_utils)

    return np_sc_img


def draw_with_probs(fut_gt, fut_pred, disc_length=1):

    # Detach from cuda
    fut_pred = fut_pred.cpu().detach().numpy()

    # Generate grid
    Z = None

    X = np.linspace(-25, 25, 1000)
    Y = np.linspace(0, 50, 1000)
    X, Y = np.meshgrid(X, Y)

    # Pack X and Y into a single 3-dimensional array
    pos = np.empty(X.shape + (2,))
    pos[:, :, 0] = X
    pos[:, :, 1] = Y

    prob_gt = []

    for t in range(0, fut_pred.shape[0]):
        mu_x = fut_pred[t, 0, 0]
        mu_y = fut_pred[t, 0, 1]
        sigma_x = 1 / fut_pred[t, 0, 2]
        sigma_y = 1 / fut_pred[t, 0, 3]
        rho = fut_pred[t, 0, 4]

        # calc mu and sigma array
        mu = np.array([mu_x, mu_y])
        sigma = np.array([[sigma_x**2, rho * sigma_x * sigma_y], [rho * sigma_x * sigma_y, sigma_y**2]])

        # The distribution on the variables X, Y packed into pos.
        F = multivariate_normal(mu, sigma)
        if Z is None:
            Z = F.pdf(pos)
        else:
            Z += F.pdf(pos)

        prob_gt.append(F.cdf([fut_gt[t, 0, 0] + disc_length / 2, fut_gt[t, 0, 1] + disc_length / 2]) - F.cdf([fut_gt[t, 0, 0] - disc_length / 2, fut_gt[t, 0, 1] - disc_length / 2]))

        # plt.cla()
        plt.imshow(F.pdf(pos) * prob_gt[t], cmap='Reds', interpolation='nearest')
        plt.plot((fut_gt[:t + 1, 0, 0] + 25) * 20, fut_gt[:t + 1, 0, 1] * 20, 'k-', marker='o', markersize=2)
        plt.plot((fut_pred[:t + 1, 0, 0] + 25) * 20, fut_pred[:t + 1, 0, 1] * 20, 'r-', marker='o', markersize=2)
        plt.legend(['Ground Truth', 'Mean of prediction'], loc='lower left')
        if t % 10 == 9:
            plt.text((fut_gt[t, 0, 0] + 25) * 20, fut_gt[t, 0, 1] * 20, str(prob_gt[t])[:6])
        plt.savefig('out/pred_visualization/' + str(t).zfill(3) + '.png')
        plt.pause(1e-5)
