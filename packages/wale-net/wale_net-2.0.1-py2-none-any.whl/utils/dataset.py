# Standard imports
import os
import pickle

# Thrid party imports
import torch
from torch.utils.data import Dataset
import cv2


# Dataset class for CommonRoad
class CRDataset(Dataset):

    def __init__(self, file_path, img_path=None, t_h=30, t_f=50, d_s=1, enc_size=64, grid_size=(13, 3)):
        with open(file_path, "rb") as fp:
            self.D = pickle.load(fp)
        self.t_h = t_h  # length of track history
        self.t_f = t_f  # length of predicted trajectory
        self.d_s = d_s  # down sampling rate of all sequences
        self.enc_size = enc_size  # size of encoder LSTM
        self.grid_size = grid_size  # size of social context grid
        if img_path is None:
            if '600' in file_path:
                self.img_path = 'data/commonroad/sc_imgs600'
            elif '60' in file_path:
                self.img_path = 'data/commonroad/sc_imgs60'
        else:
            self.img_path = img_path

    def __len__(self):
        return len(self.D['hist'])

    def __getitem__(self, idx):

        # Get track history 'hist' = ndarray, and future track 'fut' = ndarray
        smpl_id = self.D['id'][idx]
        hist = self.D['hist'][idx]
        fut = self.D['fut'][idx]

        nbrs = self.D['nbrs'][idx]
        neighbors = nbrs.reshape(nbrs.shape[0] * nbrs.shape[1], nbrs.shape[2], nbrs.shape[3])

        sc_img = cv2.imread(os.path.join(self.img_path, smpl_id + '.png'), cv2.IMREAD_GRAYSCALE)

        return smpl_id, hist, fut, neighbors, sc_img

    # Collate function for dataloader
    def collate_fn(self, samples):

        # Initialize neighbors and neighbors length batches:
        nbr_batch_size = 0
        for _, _, _, nbrs, _ in samples:
            nbr_batch_size += sum([len(nbrs[i]) != 0 for i in range(len(nbrs))])
        maxlen = self.t_h // self.d_s + 1
        nbrs_batch = torch.zeros(maxlen, nbr_batch_size, 2)

        # Initialize history, history lengths, future, output mask, lateral maneuver and longitudinal maneuver batches:
        hist_batch = torch.zeros(maxlen, len(samples), 2)
        fut_batch = torch.zeros(self.t_f // self.d_s, len(samples), 2)
        sc_img_batch = torch.zeros(len(samples), 1, 256, 256)

        count = 0
        smpl_ids = []
        for sampleId, (smpl_id, hist, fut, nbrs, sc_img) in enumerate(samples):

            # Set up history, future, lateral maneuver and longitudinal maneuver batches:
            hist_batch[0:len(hist), sampleId, 0] = torch.from_numpy(hist[:, 0])
            hist_batch[0:len(hist), sampleId, 1] = torch.from_numpy(hist[:, 1])
            fut_batch[0:len(fut), sampleId, 0] = torch.from_numpy(fut[:, 0])
            fut_batch[0:len(fut), sampleId, 1] = torch.from_numpy(fut[:, 1])
            sc_img_batch[sampleId, :, :, :] = torch.from_numpy(sc_img)
            smpl_ids.append(smpl_id)

            # Set up neighbor, neighbor sequence length, and mask batches:
            for nbr in nbrs:
                if len(nbr) != 0:
                    nbrs_batch[0:len(nbr), count, 0] = torch.from_numpy(nbr[:, 0])
                    nbrs_batch[0:len(nbr), count, 1] = torch.from_numpy(nbr[:, 1])
                    count += 1

        return smpl_ids, hist_batch, nbrs_batch, fut_batch, sc_img_batch
