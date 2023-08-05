import os

import numpy as np
from tensorflow import keras
import h5py


class PredLogger(keras.callbacks.Callback):
    def __init__(self, xdata, log_file, log_every=1, log_start=True):
        super(PredLogger, self).__init__()
        self.xdata = xdata

        self.log_file = log_file
        self._accepted_exe = ["hdf5", "h5", "he5"]
        self._handle_log_file()

        self.log_every = log_every
        self.log_start = log_start
        self._count = 0

        self._log_hdf: h5py.File = None

    def _handle_log_file(self):
        *_, ext = self.log_file.split(".")
        if ext not in self._accepted_exe:
            self.log_file += "." + self._accepted_exe[0]

        log_dir = os.path.dirname(self.log_file)
        if log_dir != "":
            os.makedirs(log_dir, exist_ok=True)

    def _check_log_count(self):
        is_step = False
        if self._count == 0 or self._count % self.log_every == 0:
            is_step = True
            self._count = 0
        return is_step

    def on_train_begin(self, logs=None):
        if os.path.exists(self.log_file):
            write_mode = "a"
        else:
            write_mode = "w"
        self._log_hdf = h5py.File(self.log_file, write_mode)

    def on_train_end(self, logs=None):
        if self._log_hdf is not None:
            self._log_hdf.close()

    def _add_dataset(self, dataset, data, data_shape):
        if data_shape is not (None):
            maxshape = (None, *data_shape)
        else:
            maxshape = (None)
        print(dataset, maxshape)
        self._log_hdf.create_dataset(dataset, data=data, compression="gzip", chunks=True, maxshape=maxshape)

    def _add_data(self, dataset, data):
        data = data[np.newaxis]
        if dataset not in self._log_hdf:
            pred_shape = data.shape[1:]
            self._add_dataset(dataset, data, pred_shape)
        else:
            self._log_hdf[dataset].resize((self._log_hdf[dataset].shape[0] + 1), axis=0)
            self._log_hdf[dataset][-data.shape[0]:] = data
        self._log_hdf.flush()  # Flush the buffers to the file

    def on_epoch_end(self, epoch, logs=None):
        if self._check_log_count():
            pred = self.model.predict(self.xdata)
            self._add_data("pred", pred)
            self._add_data("epoch", np.array([epoch]))

        self._count += 1
