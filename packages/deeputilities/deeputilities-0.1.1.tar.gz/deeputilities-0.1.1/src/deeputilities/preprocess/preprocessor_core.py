import sys

import multiprocessing
import threading
import traceback
import time
import random
import platform
import ia
import numpy as np
import cv2
if sys.version_info[0] == 2:
    # pylint: disable=redefined-builtin, import-error
    import cPickle as pickle
    from Queue import Empty as QueueEmpty, Full as QueueFull
    import socket
    BrokenPipeError = socket.error
elif sys.version_info[0] == 3:
    import pickle
    from queue import Empty as QueueEmpty, Full as QueueFull


_CONTEXT = None


# Added in 0.4.0.
def _get_context_method():
    vinfo = sys.version_info

    # get_context() is only supported in 3.5 and later (same for
    # set_start_method)
    get_context_unsupported = (
        vinfo[0] == 2
        or (vinfo[0] == 3 and vinfo[1] <= 3))

    method = None
    # Fix random hanging code in NixOS by switching to spawn method,
    # see issue #414
    # TODO This is only a workaround and doesn't really fix the underlying
    #      issue. The cause of the underlying issue is currently unknown.
    #      Its possible that #535 fixes the issue, though earlier tests
    #      indicated that the cause was something else.
    # TODO this might break the semaphore used to prevent out of memory
    #      errors
    if "NixOS" in platform.version():
        method = "spawn"
        if get_context_unsupported:
            ia.warn("Detected usage of imgaug.multicore in python <=3.4 "
                    "and NixOS. This is known to sometimes cause endlessly "
                    "hanging programs when also making use of multicore "
                    "augmentation (aka background augmentation). Use "
                    "python 3.5 or later to prevent this.")
    elif platform.system() == "Darwin" and vinfo[0:2] == (3, 7):
        # On Mac with python 3.7 there seems to be a problem with matplotlib,
        # resulting in the error "libc++abi.dylib: terminating with uncaught
        # exception of type std::runtime_error: Couldn't close file".
        # The error seems to be due to opened files that get closed in
        # child processes and can be prevented by switching to spawn mode.
        # See https://github.com/matplotlib/matplotlib/issues/15410
        # and https://bugs.python.org/issue33725.
        # It is possible that this problem also affects other python versions,
        # but here it only appeared (consistently) in the 3.7 tests and the
        # reports also seem to be focused around 3.7, suggesting explicitly
        # to update to 3.8.2.
        method = "spawn"

    if get_context_unsupported:
        return False
    return method


# Added in 0.4.0.
def _set_context(method):
    # method=False indicates that multiprocessing module (i.e. no context)
    # should be used, e.g. because get_context() is not supported
    globals()["_CONTEXT"] = (
        multiprocessing if method is False
        else multiprocessing.get_context(method))


# Added in 0.4.0.
def _reset_context():
    globals()["_CONTEXT"] = None


# Added in 0.4.0.
def _autoset_context():
    _set_context(_get_context_method())


# Added in 0.4.0.
def _get_context():
    if _CONTEXT is None:
        _autoset_context()
    return _CONTEXT


class Pool(object):
    """
    Wrapper around ``multiprocessing.Pool`` for multicore augmentation.
    Parameters
    ----------
    augseq : imgaug.augmenters.meta.Augmenter
        The augmentation sequence to apply to batches.
    processes : None or int, optional
        The number of background workers, similar to the same parameter in
        multiprocessing.Pool. If ``None``, the number of the machine's CPU
        cores will be used (this counts hyperthreads as CPU cores). If this is
        set to a negative value ``p``, then ``P - abs(p)`` will be used,
        where ``P`` is the number of CPU cores. E.g. ``-1`` would use all
        cores except one (this is useful to e.g. reserve one core to feed
        batches to the GPU).
    maxtasksperchild : None or int, optional
        The number of tasks done per worker process before the process is
        killed and restarted, similar to the same parameter in
        multiprocessing.Pool. If ``None``, worker processes will not be
        automatically restarted.
    seed : None or int, optional
        The seed to use for child processes. If ``None``, a random seed will
        be used.
    """
    # This attribute saves the augmentation sequence for background workers so
    # that it does not have to be resend with every batch. The attribute is set
    # once per worker in the worker's initializer. As each worker has its own
    # process, it is a different variable per worker (though usually should be
    # of equal content).
    _WORKER_AUGSEQ = None

    # This attribute saves the initial seed for background workers so that for
    # any future batch the batch's specific seed can be derived, roughly via
    # SEED_START+SEED_BATCH. As each worker has its own process, this seed can
    # be unique per worker even though all seemingly use the same constant
    # attribute.
    _WORKER_SEED_START = None

    def __init__(self, augseq, processes=None, maxtasksperchild=None,
                 seed=None):
        # make sure that don't call pool again in a child process
        assert Pool._WORKER_AUGSEQ is None, (
            "_WORKER_AUGSEQ was already set when calling Pool.__init__(). "
            "Did you try to instantiate a Pool within a Pool?")
        assert processes is None or processes != 0, (
            "Expected `processes` to be `None` (\"use as many cores as "
            "available\") or a negative integer (\"use as many as available "
            "MINUS this number\") or an integer>1 (\"use exactly that many "
            "processes\"). Got type %s, value %s instead." % (
                type(processes), str(processes))
        )

        self.augseq = augseq
        self.processes = processes
        self.maxtasksperchild = maxtasksperchild

        if seed is not None:
            assert iarandom.SEED_MIN_VALUE <= seed <= iarandom.SEED_MAX_VALUE, (
                "Expected `seed` to be either `None` or a value between "
                "%d and %d. Got type %s, value %s instead." % (
                    iarandom.SEED_MIN_VALUE,
                    iarandom.SEED_MAX_VALUE,
                    type(seed),
                    str(seed)
                )
            )
        self.seed = seed

        # multiprocessing.Pool instance
        self._pool = None

        # Running counter of the number of augmented batches. This will be
        # used to send indexes for each batch to the workers so that they can
        # augment using SEED_BASE+SEED_BATCH and ensure consistency of applied
        # augmentation order between script runs.
        self._batch_idx = 0

    @property
    def pool(self):
        """Return or create the ``multiprocessing.Pool`` instance.
        This creates a new instance upon the first call and afterwards
        returns that instance (until the property ``_pool`` is set to
        ``None`` again).
        Returns
        -------
        multiprocessing.Pool
            The ``multiprocessing.Pool`` used internally by this
            ``imgaug.multicore.Pool``.
        """
        if self._pool is None:
            processes = self.processes
            if processes is not None and processes < 0:
                # cpu count returns the number of logical cpu cores, i.e.
                # including hyperthreads could also use
                # os.sched_getaffinity(0) here, which seems to not exist on
                # BSD though.
                # In python 3.4+, there is also os.cpu_count(), which
                # multiprocessing.cpu_count() then redirects to.
                # At least one guy on stackoverflow.com/questions/1006289
                # reported that only os.* existed, not the multiprocessing
                # method.
                # TODO make this also check if os.cpu_count exists as a
                #      fallback
                try:
                    processes = _get_context().cpu_count() - abs(processes)
                    processes = max(processes, 1)
                except (ImportError, NotImplementedError):
                    ia.warn(
                        "Could not find method multiprocessing.cpu_count(). "
                        "This will likely lead to more CPU cores being used "
                        "for the background augmentation than originally "
                        "intended.")
                    processes = None

            self._pool = _get_context().Pool(
                processes,
                initializer=_Pool_initialize_worker,
                initargs=(self.augseq, self.seed),
                maxtasksperchild=self.maxtasksperchild)
        return self._pool
