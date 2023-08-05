# This file is part of idtracker.ai a multiple animals tracking system
# described in [1].
# Copyright (C) 2017- Francisco Romero Ferrero, Mattia G. Bergomi,
# Francisco J.H. Heras, Robert Hinz, Gonzalo G. de Polavieja and the
# Champalimaud Foundation.
#
# idtracker.ai is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details. In addition, we require
# derivatives or applications to acknowledge the authors by citing [1].
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
# For more information please send an email (idtrackerai@gmail.com) or
# use the tools available at https://gitlab.com/polavieja_lab/idtrackerai.git.
#
# [1] Romero-Ferrero, F., Bergomi, M.G., Hinz, R.C., Heras, F.J.H.,
# de Polavieja, G.G., Nature Methods, 2019.
# idtracker.ai: tracking all individuals in small or large collectives of
# unmarked animals.
# (F.R.-F. and M.G.B. contributed equally to this work.
# Correspondence should be addressed to G.G.d.P:
# gonzalo.polavieja@neuro.fchampalimaud.org)
import logging

from torch.utils.data import DataLoader
from torchvision import transforms

from idtrackerai.network import normalize
from idtrackerai.utils import conf

from .identification_dataset import IdentificationDataset

num_workers_train = 1
num_workers_val = 1


def get_training_data_loaders(
    number_of_animals: int, train_data, val_data
) -> tuple[DataLoader, DataLoader]:
    logging.info("Creating training IdentificationDataset")
    training_set = IdentificationDataset(
        train_data,
        scope="training",
        transform=transforms.Compose([transforms.ToTensor(), normalize]),
    )
    train_loader = DataLoader(
        training_set,
        batch_size=conf.BATCH_SIZE_IDCNN,
        shuffle=True,
        num_workers=num_workers_train,
        persistent_workers=num_workers_train > 0,
    )
    train_loader.num_classes = number_of_animals
    train_loader.image_shape = training_set[0][0].shape

    logging.info("Creating validation IdentificationDataset")
    validation_set = IdentificationDataset(
        val_data,
        scope="validation",
        transform=transforms.Compose([transforms.ToTensor(), normalize]),
    )
    val_loader = DataLoader(
        validation_set,
        batch_size=conf.BATCH_SIZE_PREDICTIONS_IDCNN,
        num_workers=num_workers_val,
        persistent_workers=num_workers_val > 0,
    )
    val_loader.num_classes = number_of_animals
    val_loader.image_shape = validation_set[0][0].shape
    return train_loader, val_loader


def get_test_data_loader(test_data, number_of_classes):
    logging.debug("Creating test IdentificationDataset")
    test_set = IdentificationDataset(
        test_data,
        scope="predict",
        transform=transforms.Compose([transforms.ToTensor(), normalize]),
    )
    test_loader = DataLoader(
        test_set,
        batch_size=conf.BATCH_SIZE_PREDICTIONS_IDCNN,
        num_workers=num_workers_val,
        persistent_workers=num_workers_val > 0,
    )
    test_loader.num_classes = number_of_classes
    test_loader.image_shape = test_set[0][0].shape
    return test_loader
