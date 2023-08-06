
import logging
import math

import numpy as np
from scipy.special import erfinv  # pylint: disable=no-name-in-module

import nni
from nni.common.hpo_utils import ParameterSpec, deformat_parameters, format_search_space
from nni.tuner import Tuner

class NeuralArchitectureSearch():

    def __init__(self):
        pass

    def __init__(self, optimize_mode=None):
        self.space = None

        # the grid to search in this epoch
        # when the space is fully explored, grid is set to None
        self.grid = None  # list[int | float]

        # a paremter set is internally expressed as a vector
        # for each dimension i, self.vector[i] is the parameter's index in self.grid[i]
        # in second epoch of above example, vector [1, 2, 0] means parameters {x: 7, y: 0.67, z: 2}
        self.vector = None  # list[int]

        # this tells which parameters are derived from previous epoch
        # in second epoch of above example, epoch_bar is [2, 1, 1]
        self.epoch_bar = None  # list[int]

        # this stores which intervals are possibly divisible (low < high after log and q)
        # in first epoch of above example, divisions are:
        #     {1: [(0,1/2), (1/2,1)], 2: [(1/2,1)]}
        # in second epoch:
        #     {1: [(0,1/4), (1/4,1/2), (1/2,3/4), (3/4,1)], 2: [(1/2,3/4)]}
        # and in third epoch:
        #     {1: [(0,1/8), ..., (7/8,1)], 2: []}
        self.divisions = {}  # dict[int, list[tuple[float, float]]]

        # dumped JSON string of all tried parameters
        self.history = set()

        if optimize_mode is not None:
            _logger.info(f'Ignored optimize_mode "{optimize_mode}"')

    def update_search_space(self, space):
        self.space = format_search_space(space)
        if not self.space:  # the tuner will crash in this case, report it explicitly
            raise ValueError('Search space is empty')
        self._init_grid()

    def generate_parameters(self, *args, **kwargs):
        while True:
            params = self._suggest()
            if params is None:
                raise nni.NoMoreTrialError('Search space fully explored')
            params = deformat_parameters(params, self.space)

            params_str = nni.dump(params, sort_keys=True)
            if params_str not in self.history:
                self.history.add(params_str)
                return params

    def receive_trial_result(self, *args, **kwargs):
        pass

    def import_data(self, data):
        # TODO
        # use tuple to dedup in case of order/precision issue causes matching failed
        # and remove `epoch_bar` to use uniform dedup mechanism
        for trial in data:
            params_str = nni.dump(trial['parameter'], sort_keys=True)
            self.history.add(params_str)

    def _suggest(self):
        # returns next parameter set, or None if the space is already fully explored
        while True:
            if self.grid is None:  # search space fully explored
                return None

            self._next_vector()

            if self.vector is None:  # epoch end, update grid and retry
                self._next_grid()
                continue

            old = all((self.vector[i] < self.epoch_bar[i]) for i in range(len(self.space)))
            if old:  # already explored in past epochs
                continue

            # this vector is valid, stop
            _logger.debug(f'vector: {self.vector}')
            return self._current_parameters()

    def _next_vector(self):
        # iterate to next vector of this epoch, set vector to None if epoch end
        if self.vector is None:  # first vector in this epoch
            self.vector = [0] * len(self.space)
            return

        # deal with nested choice, don't touch nested spaces that are not chosen by current vector
        activated_dims = []
        params = self._current_parameters()
        for i, spec in enumerate(self.space.values()):
            if spec.is_activated_in(params):
                activated_dims.append(i)

        for i in reversed(activated_dims):
            if self.vector[i] + 1 < len(self.grid[i]):
                self.vector[i] += 1
                return
            else:
                self.vector[i] = 0

        self.vector = None  # the loop ends without returning, no more vector in this epoch

    def _next_grid(self):
        # update grid information (grid, epoch_bar, divisions) for next epoch
        updated = False
        for i, spec in enumerate(self.space.values()):
            self.epoch_bar[i] = len(self.grid[i])
            if not spec.categorical:
                # further divide intervals
                new_vals = []  # values to append to grid
                new_divs = []  # sub-intervals
                for l, r in self.divisions[i]:
                    mid = (l + r) / 2
                    diff_l = _less(l, mid, spec)
                    diff_r = _less(mid, r, spec)
                    # if l != 0 and r != 1, then they are already in the grid, else they are not
                    # the special case is needed because for normal distribution 0 and 1 will generate infinity
                    if (diff_l or l == 0.0) and (diff_r or r == 1.0):
                        # we can skip these for non-q, but it will complicate the code
                        new_vals.append(mid)
                        updated = True
                    if diff_l:
                        new_divs.append((l, mid))
                        updated = (updated or l == 0.0)
                    if diff_r:
                        new_divs.append((mid, r))
                        updated = (updated or r == 1.0)
                self.grid[i] += new_vals
                self.divisions[i] = new_divs

        if not updated:  # fully explored
            _logger.info('Search space has been fully explored')
            self.grid = None
        else:
            size = _grid_size_info(self.grid)
            _logger.info(f'Grid subdivided, new size: {size}')

    def _init_grid(self):
        self.epoch_bar = [0 for _ in self.space]
        self.grid = [None for _ in self.space]
        for i, spec in enumerate(self.space.values()):
            if spec.categorical:
                self.grid[i] = list(range(spec.size))
            else:
                self.grid[i] = [0.5]
                self.divisions[i] = []
                if _less(0, 0.5, spec):
                    self.divisions[i].append((0, 0.5))
                if _less(0.5, 1, spec):
                    self.divisions[i].append((0.5, 1))

        size = _grid_size_info(self.grid)
        _logger.info(f'Grid initialized, size: {size}')

