from __future__ import division
import torch
import torch.nn as nn
from .neural_network import outputActivation


class predictionNet(nn.Module):

    # Initialization
    def __init__(self, args):
        super(predictionNet, self).__init__()

        # Unpack arguments
        self.args = args

        # Use gpu flag
        self.use_cuda = args['use_cuda']

        # Flag for train mode (True) vs test-mode (False)
        self.train_flag = args['train_flag']

        # Sizes of network layers
        self.encoder_size = args['encoder_size']
        self.decoder_size = args['decoder_size']
        self.in_length = args['in_length']
        self.out_length = args['out_length']
        self.grid_size = args['grid_size']
        self.soc_conv_depth = args['soc_conv_depth']
        self.conv_3x1_depth = args['conv_3x1_depth']
        self.dyn_embedding_size = args['dyn_embedding_size']
        self.input_embedding_size = args['input_embedding_size']
        self.soc_embedding_size = (((args['grid_size'][0] - 4) + 1) // 2) * self.conv_3x1_depth
        self.scene_images = args['scene_images']
        self.multi_output = args['multi_output']
        self.dec_img_size = args['dec_img_size']

        # Define network weights

        # Input embedding layer
        self.ip_emb = torch.nn.Linear(2, self.input_embedding_size)

        # Encoder LSTM
        self.enc_lstm = torch.nn.LSTM(self.input_embedding_size, self.encoder_size, 1)

        # Vehicle dynamics embedding
        self.dyn_emb = torch.nn.Linear(self.encoder_size, self.dyn_embedding_size)

        # Convolutional social pooling layer and social embedding layer
        self.soc_conv = torch.nn.Conv2d(self.encoder_size, self.soc_conv_depth, 3)
        self.conv_3x1 = torch.nn.Conv2d(self.soc_conv_depth, self.conv_3x1_depth, (3, 1))
        self.soc_maxpool = torch.nn.MaxPool2d((2, 1), padding=(1, 0))

        if self.scene_images:
            # Convolutional processing of scene representation
            self.sc_conv1 = torch.nn.Conv2d(1, 64, kernel_size=3, stride=1, padding=1)
            self.sc_conv2 = torch.nn.Conv2d(64, 64, kernel_size=3, stride=1, padding=1)
            self.sc_conv3 = torch.nn.Conv2d(64, 64, kernel_size=3, stride=1, padding=1)
            self.sc_conv4 = torch.nn.Conv2d(64, 64, kernel_size=3, stride=1, padding=1)
            self.sc_conv5 = torch.nn.Conv2d(64, self.dec_img_size, kernel_size=3, stride=1, padding=1)
            self.sc_conv6 = torch.nn.Conv2d(self.dec_img_size, self.dec_img_size, kernel_size=3, stride=1, padding=1)
            self.sc_conv7 = torch.nn.Conv2d(self.dec_img_size, self.dec_img_size, kernel_size=3, stride=1, padding=1)
            self.sc_conv8 = torch.nn.Conv2d(self.dec_img_size, self.dec_img_size, kernel_size=3, stride=1, padding=1)

            self.sc_maxpool = torch.nn.MaxPool2d((2, 2), padding=(0, 0))

        # FC social pooling layer (for comparison):
        # self.soc_fc = torch.nn.Linear(self.soc_conv_depth * self.grid_size[0] * self.grid_size[1], (((args['grid_size'][0]-4)+1)//2)*self.conv_3x1_depth)

        # Decoder LSTM
        if self.scene_images:
            self.dec_lstm = torch.nn.LSTM(self.soc_embedding_size + self.dyn_embedding_size + self.dec_img_size, self.decoder_size)
            if self.multi_output:
                self.dec_lstm2 = torch.nn.LSTM(self.soc_embedding_size + self.dyn_embedding_size + self.dec_img_size, self.decoder_size)
                # Fully Connected layer for probs
                self.fc = torch.nn.Linear(self.soc_embedding_size + self.dyn_embedding_size + self.dec_img_size, 2)
        else:
            self.dec_lstm = torch.nn.LSTM(self.soc_embedding_size + self.dyn_embedding_size, self.decoder_size)
            if self.multi_output:
                self.dec_lstm2 = torch.nn.LSTM(self.soc_embedding_size + self.dyn_embedding_size, self.decoder_size)
                # Fully Connected layer for probs
                self.fc = torch.nn.Linear(self.soc_embedding_size + self.dyn_embedding_size, 2)

        # Output layers:
        self.op = torch.nn.Linear(self.decoder_size, 5)
        if self.multi_output:
            self.op2 = torch.nn.Linear(self.decoder_size, 5)

        # Activations:
        self.leaky_relu = torch.nn.LeakyReLU(0.1)
        self.relu = torch.nn.ReLU()
        self.softmax = torch.nn.Softmax(dim=1)

    # Forward Pass
    def forward(self, hist, nbrs, sc_img):

        # Forward pass hist:
        _, (hist_enc, _) = self.enc_lstm(self.leaky_relu(self.ip_emb(hist)))
        hist_enc = self.leaky_relu(self.dyn_emb(hist_enc.view(hist_enc.shape[1], hist_enc.shape[2])))

        # Forward pass nbrs
        _, (nbrs_enc, _) = self.enc_lstm(self.leaky_relu(self.ip_emb(nbrs)))
        nbrs_enc = nbrs_enc.view(nbrs_enc.shape[1], nbrs_enc.shape[2])

        if self.scene_images:
            # Forward pass sc_img
            sc_img = self.sc_maxpool(self.sc_conv1(sc_img))
            sc_img = self.sc_maxpool(self.sc_conv2(sc_img))
            sc_img = self.sc_maxpool(self.sc_conv3(sc_img))
            sc_img = self.sc_maxpool(self.sc_conv4(sc_img))
            sc_img = self.sc_maxpool(self.sc_conv5(sc_img))
            sc_img = self.sc_maxpool(self.sc_conv6(sc_img))
            sc_img = self.sc_maxpool(self.sc_conv7(sc_img))
            sc_img = self.sc_maxpool(self.sc_conv8(sc_img))

            sc_img = torch.squeeze(sc_img, 2)
            sc_img = torch.squeeze(sc_img, 2)

            # sc_img_plt = torch.squeeze(sc_img, 0).cpu().detach().numpy()

        # Masked scatter alternative
        soc_enc = nbrs_enc.reshape(hist.shape[1], self.grid_size[1], self.grid_size[0], self.encoder_size)
        soc_enc = soc_enc.permute(0, 3, 2, 1)

        # Apply convolutional social pooling:
        soc_enc = self.soc_maxpool(self.leaky_relu(self.conv_3x1(self.leaky_relu(self.soc_conv(soc_enc)))))
        soc_enc = soc_enc.view(-1, self.soc_embedding_size)

        # Concatenate encodings:
        enc = torch.cat((soc_enc, hist_enc), 1)
        if self.scene_images:
            enc = torch.cat((enc, sc_img), 1)

        fut_pred1 = self.decode(enc)

        if self.multi_output:
            probs = self.fc(enc)
            probs = self.softmax(probs)
            fut_pred2 = self.decode2(enc)

            return fut_pred1, fut_pred2, probs

        else:
            return fut_pred1

    def decode(self, enc):
        enc = enc.repeat(self.out_length, 1, 1)
        h_dec, _ = self.dec_lstm(enc)
        h_dec = h_dec.permute(1, 0, 2)
        fut_pred = self.op(h_dec)
        fut_pred = fut_pred.permute(1, 0, 2)
        fut_pred = outputActivation(fut_pred)
        return fut_pred

    def decode2(self, enc):
        enc = enc.repeat(self.out_length, 1, 1)
        h_dec, _ = self.dec_lstm2(enc)
        h_dec = h_dec.permute(1, 0, 2)
        fut_pred = self.op2(h_dec)
        fut_pred = fut_pred.permute(1, 0, 2)
        fut_pred = outputActivation(fut_pred)
        return fut_pred
