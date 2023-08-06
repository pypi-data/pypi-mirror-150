"""
Deep CCA with more customisation
==================================

Showing some examples of more advanced functionality with DCCA and pytorch-lightning
"""

import numpy as np

# %%
import pytorch_lightning as pl
from torch import optim
from torch.utils.data import Subset

from multiviewdata.torchdatasets import SplitMNIST
from cca_zoo.deepmodels import DCCA, get_dataloaders, _architectures

n_train = 500
n_val = 100
train_dataset = SplitMNIST(root="", mnist_type="MNIST", train=True, download=True)
val_dataset = Subset(train_dataset, np.arange(n_train, n_train + n_val))
train_dataset = Subset(train_dataset, np.arange(n_train))
train_loader, val_loader = get_dataloaders(train_dataset, val_dataset)

# The number of latent dimensions across models
latent_dims = 2
# number of epochs for deep models
epochs = 10

# TODO add in custom architecture and schedulers and stuff to show it off
encoder_1 = _architectures.Encoder(latent_dims=latent_dims, feature_size=392)
encoder_2 = _architectures.Encoder(latent_dims=latent_dims, feature_size=392)

# Deep CCA
dcca = DCCA(
    latent_dims=latent_dims, encoders=[encoder_1, encoder_2], scheduler="cosine"
)
trainer = pl.Trainer(max_epochs=epochs, enable_checkpointing=False)
trainer.fit(dcca, train_loader, val_loader)
