import numpy as np

from .._base import FitPlotBase
from .._aux import step_fill_between


class HistFitPlot(FitPlotBase):

    SUBPLOT_CONFIGS_DEFAULT = FitPlotBase.SUBPLOT_CONFIGS_DEFAULT

    def __init__(self, parent_fit):
        super(HistFitPlot, self).__init__(parent_fit=parent_fit)

    # -- private methods

    @property
    def plot_data_x(self):
        return np.arange(self._fitter.data_size)

    @property
    def plot_data_y(self):
        return self._fitter.data

    @property
    def plot_data_xerr(self):
        return None

    @property
    def plot_data_yerr(self):
        return self._fitter.data_error

    @property
    def plot_model_x(self):
        return self.plot_data_x

    @property
    def plot_model_y(self):
        return self._fitter.model

    @property
    def plot_model_xerr(self):
        return 0.5

    @property
    def plot_model_yerr(self):
        return None #self._fitter.model_error

    @property
    def plot_range_x(self):
        return (-0.5, self._fitter.data_size-0.5)

    @property
    def plot_range_y(self):
        return None  # no fixed range

    def _plot_data(self, target_axis):
        _y = self._fitter.data
        if self._fitter.has_errors:
            target_axis.errorbar(np.arange(len(_y)), _y,
                                 yerr=self._fitter.data_error,
                                 linestyle='',
                                 marker='o',
                                 label='data')
        else:
            target_axis.plot(self._fitter.data,
                             linestyle='',
                             marker='o',
                             label='data')

    def _plot_model(self, target_axis, **kwargs):
        # overwrite default plot method
        step_fill_between(self._axes,
                          self.plot_model_x,
                          self.plot_model_y,
                          xerr=self.plot_model_xerr,
                          yerr=self.plot_model_yerr,
                          draw_central_value=True,
                          **self._get_next_subplot_kwargs('model')
                          )

    # -- public methods