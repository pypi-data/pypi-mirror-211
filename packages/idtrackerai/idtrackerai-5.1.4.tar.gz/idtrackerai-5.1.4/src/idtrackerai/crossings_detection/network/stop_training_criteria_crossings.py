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
import sys

import numpy as np
from rich.status import Status

from idtrackerai.utils import conf


class StopTraining:
    """CROSSING Stops the training of the network according to the conditions specified
    in __call__
    """

    number_of_classes = 2
    epochs_before_checking_stopping_conditions = 10

    def __init__(self, num_epochs: int):
        logging.info("Setting the stopping criteria", stacklevel=3)
        self.num_epochs = num_epochs  # maximal num of epochs
        self.overfitting_counter: int = 0
        """Number of epochs in which the network is overfitting before
        stopping the training"""

        self.epochs_completed = -1

    def __call__(
        self,
        loss_training: float,
        loss_validation: list,
        accuracy_validation: float,
        status: Status,
    ):
        self.epochs_completed += 1
        # check that the model did not diverged (nan loss).
        if self.epochs_completed > 0 and (
            np.isnan(loss_training) or np.isnan(loss_validation[-1])
        ):
            status.stop()
            logging.info(
                "The model diverged with loss NaN, falling back "
                "to detecting crossings with the model area"
            )
            return True
        # check if it did not reached the epochs limit
        if self.epochs_completed > self.num_epochs - 1:
            status.stop()
            logging.info(
                "The number of epochs completed is larger than the number "
                "of epochs set for training, we stop the training"
            )
            return True
        # check that the model is not overfitting or if it reached a
        # stable saddle (minimum)
        if self.epochs_completed > self.epochs_before_checking_stopping_conditions:
            current_loss = loss_validation[-1]
            previous_loss = np.nanmean(
                loss_validation[-self.epochs_before_checking_stopping_conditions : -1]
            )
            # The validation loss in the first 10 epochs could have
            # exploded but being decreasing.
            if np.isnan(previous_loss):
                previous_loss = sys.float_info[0]
            losses_difference = previous_loss - current_loss
            # check overfitting
            if losses_difference < 0.0:
                self.overfitting_counter += 1
                if self.overfitting_counter >= conf.OVERFITTING_COUNTER_THRESHOLD_DCD:
                    status.stop()
                    logging.info("Overfitting")
                    return True
            else:
                self.overfitting_counter = 0
            # check if the error is not decreasing much
            if np.abs(
                losses_difference
            ) < conf.LEARNING_PERCENTAGE_DIFFERENCE_2_DCD * 10 ** (
                int(np.log10(current_loss)) - 1
            ):
                status.stop()
                logging.info(
                    "The losses difference is very small, we stop the training"
                )
                return True
            # if the individual accuracies in validation are 1. for all the animals
            if accuracy_validation == 1.0:
                status.stop()
                logging.info("The accuracy in validation is 100%, we stop the training")
                return True
            # if the validation loss is 0.
            if previous_loss == 0.0 or current_loss == 0.0:
                status.stop()
                logging.info("The validation loss is 0.0, we stop the training")
                return True

        return False
