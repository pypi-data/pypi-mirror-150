# @Author: Thomas Firmin <ThomasFirmin>
# @Date:   2022-05-03T15:41:48+02:00
# @Email:  thomas.firmin@univ-lille.fr
# @Project: Zellij
# @Last modified by:   ThomasFirmin
# @Last modified time: 2022-05-03T15:44:16+02:00
# @License: CeCILL-C (http://www.cecill.info/index.fr.html)
# @Copyright: Copyright (C) 2022 Thomas Firmin


import zellij.utils.progress_bar as pb
from abc import abstractmethod
import os
import numpy as np
import pandas as pd
import enlighten

import logging

logger = logging.getLogger("zellij.Meta")


class Metaheuristic(object):

    """Metaheuristic

    Metaheuristic is a core object which defines the structure of a metaheuristic in Zellij.
    It is an abtract class.

    Attributes
    ----------
    loss_func : LossFunc
        Loss function to optimize. must be of type :math:`f(x)=y` or :math:`f(x)=results,model`
        See :ref:`lf` for more information.

    search_space : Searchspace
        :ref:`sp` object containing bounds of all decision variables.

    f_calls : int
        Maximum number of calls to loss_func.

    save : boolean, optional
        If True save results into a file

    H : Fractal, optional
        If a :ref:`frac` is given, allows to use it.

    verbose : boolean, default=True
        Activate or deactivate the progress bar.

    See Also
    --------
    :ref:`lf` : Parent class for a loss function.
    :ref:`sp` : Defines what a search space is in Zellij.
    """

    def __init__(self, loss_func, search_space, f_calls, verbose=True):

        ##############
        # PARAMETERS #
        ##############

        self.loss_func = loss_func
        self.search_space = search_space
        self.f_calls = f_calls

        self.verbose = verbose

        #############
        # VARIABLES #
        #############

        # Modify labels in loss func according to SearchSpace labels
        self.loss_func.labels = self.search_space.labels
        # Index of the historic in loss function.
        self.lf_idx = len(self.loss_func.all_scores)

        if self.verbose:
            self.manager = enlighten.get_manager()
        else:
            self.manager = enlighten.get_manager(stream=None, enabled=False)

        self.main_pb = False

    def build_bar(self, total):
        """build_bar(total)

        build_bar is a method to build a progress bar.
        It is a purely aesthetic feature to get info on the execution.
        You can deactivate it, with `verbose=False`.

        Parameters
        ----------
        total : int
            Length of the progress bar.

        """

        if self.verbose:
            if (not hasattr(self.manager, "zellij_first_line")) or (
                hasattr(self.manager, "zellij_first_line")
                and not self.manager.zellij_first_line
            ):

                self.main_pb = True
                self.manager.zellij_first_line = True
                self.best_pb = pb.best_counter(self.manager)
                (
                    self.calls_pb_explor,
                    self.calls_pb_exploi,
                    self.calls_pb_pending,
                ) = pb.calls_counter(self.manager, self.f_calls)

                self.loss_func.manager = self.manager

            else:
                self.main_pb = False
                self.best_pb = False
                self.calls_pb_explor = False
                self.calls_pb_exploi = False
                self.calls_pb_pending = False

        self.meta_pb = pb.metaheuristic_counter(
            self.manager, total, self.__class__.__name__
        )

    def update_main_pb(self, nb, explor=True, best=False):
        """update_main_pb(nb, explor=True, best=False)

        Update the main progress bar with a certain number.

        Parameters
        ----------
        nb : int
            Length of the update. e.g. if the progress bar measure the number of iterations,
            at each iteration `nb=1`.
        explor : bool, default=True
            If True the color associated to the update will be blue. Orange, otherwise.
        best : bool default=False
            If True the score of the current solution will be displayed.

        """
        if self.main_pb and self.verbose:
            if best:
                self.best_pb.update()
            if explor:
                self.calls_pb_explor.update_from(self.calls_pb_pending, nb)
            else:
                self.calls_pb_exploi.update_from(self.calls_pb_pending, nb)

    def pending_pb(self, nb):
        """pending_pb(nb)

        Update the progress bar with a pending property (white). This update will be replaced when using
        `update_main_pb`.

        Parameters
        ----------
        nb : type
            Length of the pending objects.

        """
        if self.main_pb and self.verbose:
            self.calls_pb_pending.update(nb)

    def close_bar(self):
        """close_bar()

        Delete the progress bar. (must be executed at the end of `run` method)

        """
        if self.main_pb and self.verbose:
            self.best_pb.close()
            self.calls_pb_pending.close()

            self.main_pb = False
            self.manager.zellij_first_line = False

        self.meta_pb.close()

    @abstractmethod
    def run(self):
        """run()

        Abstract method, describe how to run a metaheuristic

        """
        pass

    def show(self, filepath="", save=False):
        """show(filepath="", save=False)

        Basic plots for all metaheuristic. uses :ref:`sp` plotting.

        Parameters
        ----------
        filepath : string, default=""
            If a filepath to a file containing points is given, it will read those points and plot them.
        save : bool, default=False
            If true, it saves the plots.

        """

        if filepath:
            all = os.path.join(filepath, "outputs", "all_evaluations.csv")

            all_data = pd.read_table(all, sep=",", decimal=".")
            all_scores = all_data["loss"].to_numpy()
        else:
            all_data = self.loss_func.all_solutions
            all_scores = np.array(self.loss_func.all_scores)

        self.search_space.show(
            all_data, all_scores, save, self.loss_func.plots_path
        )

        return all_data, all_scores
