import os

import h5py
import numpy as np

import matplotlib.pyplot as plt

from bokeh.plotting import figure, show, ColumnDataSource, save
from bokeh.models import LinearColorMapper, ColorBar, CustomJS, TableColumn, DataTable, Button
from bokeh.layouts import row, column

class DataMap:
    def __init__(self, preds, ytrue, label_mode="onehot"):
        if isinstance(preds, str):
            hdf5_file = h5py.File(preds, "r")
            preds = hdf5_file["pred"]
        self.preds = preds
        self.ytrue = ytrue

        self._n_samples = len(self.ytrue)
        self._n_epochs = len(preds)

        self.label_mode = label_mode
        self._score_fun = self._get_true_label_score_func()

    def _get_classes(self, y):
        y_c = None
        if self.label_mode == "onehot":
            y_c = np.argmax(y, axis=-1)
        return y_c

    def _get_pred_correct(self, ypred):
        ytrue_c = self._get_classes(self.ytrue)
        ypred_c = self._get_classes(ypred)
        pred_correct = ytrue_c == ypred_c
        return pred_correct

    def _get_true_label_score_func(self):
        if self.label_mode == "onehot":
            true_label_idxs = np.argmax(self.ytrue, axis=-1)

            def _score_func(epoc):
                return np.take_along_axis(self.preds[epoc], true_label_idxs[:, None], axis=1).reshape(-1)

        return _score_func

    def cal_confidence(self):
        confidencs_scores = np.zeros(self._n_samples)

        for epoch_e in range(self._n_epochs):
            confidencs_scores += self._score_fun(epoch_e)

        confidencs_scores /= self._n_epochs
        return confidencs_scores

    def cal_variability(self):
        confidences = self.cal_confidence()
        diffs = np.zeros(self._n_samples)

        for epoch_e in range(self._n_epochs):
            e_confidence = self._score_fun(epoch_e)
            diffs += np.power(e_confidence - confidences, 2)
        diffs /= self._n_epochs
        variability = np.sqrt(diffs)
        return variability

    def cal_correctness(self):
        correctness = np.zeros(self._n_samples)

        for epoch_e in range(self._n_epochs):
            correct = self._get_pred_correct(self.preds[epoch_e])
            correctness += correct
        correctness /= self._n_epochs
        return correctness

    def plot_plt(self, ax=None):
        confidencs = self.cal_confidence()
        variability = self.cal_variability()
        correctness = self.cal_correctness()
        size = (1 + correctness)

        if ax is None:
            plt.figure()
            ax = plt.gca()

        scatter = ax.scatter(variability, confidencs, c=correctness, s=size)
        ax.set_xlabel("Variability")
        ax.set_ylabel("Confidencs")
        cbar = plt.colorbar(scatter)
        cbar.set_label('Correctness')
        return ax

    def plot_bokeh(self, show_plot=False, filename=None, palette="Plasma256"):
        confidencs = self.cal_confidence()
        variability = self.cal_variability()
        correctness = self.cal_correctness()
        color_mapper = LinearColorMapper(palette=palette, low=min(correctness), high=max(correctness))

        source = ColumnDataSource(data=dict(
            confidencs=confidencs,
            variability=variability,
            correctness=correctness
        ))

        TOOLTIPS = [
            ("index", "$index"),
            ("confidencs", "@confidencs"),
            ("variability", "@variability"),
            ("correctness", "@correctness")
        ]
        TOOLS = "hover,pan,wheel_zoom,box_zoom,zoom_in,zoom_out,box_select,lasso_select,reset,save"

        datamap = figure(tools=TOOLS, tooltips=TOOLTIPS)
        datamap.xaxis.axis_label = 'Variability'
        datamap.yaxis.axis_label = 'Confidencs'

        datamap.scatter("variability", "confidencs", fill_alpha=0.6,
                        color={'field': 'correctness', 'transform': color_mapper},
                        line_color=None, source=source)
        color_bar = ColorBar(color_mapper=color_mapper, label_standoff=12)
        datamap.add_layout(color_bar, 'right')

        selected_collector = ColumnDataSource(data=dict(indexs=[], confidencs=[], variability=[], correctness=[]))

        columns = [
            TableColumn(field="indexs", title="Index"),
            TableColumn(field="confidencs", title="Confidencs"),
            TableColumn(field="variability", title="Variability"),
            TableColumn(field="correctness", title="Correctness")
        ]
        data_table = DataTable(source=selected_collector, columns=columns, width=400)

        source.selected.js_on_change('indices',
                                     CustomJS(args=dict(s1=source, cs=selected_collector),
                                              code=open(os.path.join(os.path.dirname(__file__), "selected.js")).read()))

        button = Button(label="Download", button_type="success")
        button.js_on_event("button_click",
                           CustomJS(args=dict(selected_data=selected_collector),
                                    code=open(os.path.join(os.path.dirname(__file__), "download.js")).read()))

        set_up = row(datamap, column(data_table, button))
        if show_plot:
            show(set_up, filename=filename)
        else:
            save(set_up, filename=filename)
