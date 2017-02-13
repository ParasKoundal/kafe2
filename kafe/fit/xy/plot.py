import numpy as np

from .._base import PlotContainerBase, PlotFigureBase
from .._aux import step_fill_between
from . import XYFit


class XYPlotContainer(PlotContainerBase):
    FIT_TYPE = XYFit

    def __init__(self, xy_fit_object, n_plot_points_model=100):
        super(XYPlotContainer, self).__init__(fit_object=xy_fit_object)
        self._n_plot_points_model = n_plot_points_model

        self._plot_range_x = None

    # -- private methods

    def _compute_plot_range_x(self, pad_coeff=1.1, additional_pad=None):
        if additional_pad is None:
            additional_pad = (0, 0)
        _xmin, _xmax = self._fitter.x_range
        _w = _xmax - _xmin
        self._plot_range_x = (
            0.5 * (_xmin + _xmax - _w * pad_coeff) - additional_pad[0],
            0.5 * (_xmin + _xmax + _w * pad_coeff) + additional_pad[1]
        )

    # -- public properties

    @property
    def plot_data_x(self):
        return self._fitter.x

    @property
    def plot_data_y(self):
        return self._fitter.y_data

    @property
    def plot_data_xerr(self):
        return self._fitter.x_error

    @property
    def plot_data_yerr(self):
        return self._fitter.y_data_error

    @property
    def plot_model_x(self):
        _xmin, _xmax = self.plot_range_x
        return np.linspace(_xmin, _xmax, self._n_plot_points_model)

    @property
    def plot_model_y(self):
        return self._fitter.eval_model_function(x=self.plot_model_x)

    @property
    def plot_model_xerr(self):
        return None if np.allclose(self._fitter.x_error, 0) else self._fitter.x_error

    @property
    def plot_model_yerr(self):
        return None if np.allclose(self._fitter.y_data_error, 0) else self._fitter.y_data_error

    @property
    def plot_range_x(self):
        if self._plot_range_x is None:
            self._compute_plot_range_x()
        return self._plot_range_x

    @property
    def plot_range_y(self):
        return None

    # public methods

    def plot_data(self, target_axis, **kwargs):
        # TODO: how to handle 'data' errors and 'model' errors?
        if self._fitter.has_errors:
            return target_axis.errorbar(self.plot_data_x,
                                 self.plot_data_y,
                                 xerr=self.plot_data_xerr,
                                 yerr=self.plot_data_yerr,
                                 **kwargs)
        else:
            return target_axis.plot(self.plot_data_x,
                             self.plot_data_y,
                             **kwargs)

    def plot_model(self, target_axis, **kwargs):
        # TODO: how to handle 'data' errors and 'model' errors?
        if self._fitter.has_model_errors:
            return target_axis.errorbar(self.plot_model_x,
                                 self.plot_model_y,
                                 xerr=self.plot_model_xerr,
                                 yerr=self.plot_model_yerr,
                                 **kwargs)
        else:
            return target_axis.plot(self.plot_model_x,
                             self.plot_model_y,
                             **kwargs)

    def plot_model_error_band(self, target_axis, **kwargs):
        _band_y = self._fitter.y_error_band
        _y = self.plot_model_y
        if self._fitter.has_errors:
            return target_axis.fill_between(
                self.plot_model_x,
                _y - _band_y, _y + _band_y,
                **kwargs)
        else:
            return None  # don't plot error band if fitter input data has no errors...


class XYPlot(PlotFigureBase):

    PLOT_CONTAINER_TYPE = XYPlotContainer

    PLOT_TYPE_DEFAULT_CONFIGS = PlotFigureBase.PLOT_TYPE_DEFAULT_CONFIGS.copy()  # don't change original class variable
    PLOT_TYPE_DEFAULT_CONFIGS['model_error_band'] = dict(
        plot_container_method='plot_model_error_band',
        plot_container_method_static_kwargs=dict(
            alpha=0.5,
            linestyle='-',
            label='model %(subplot_id)s error',
            edgecolor='none',
            linewidth=2,
            zorder=-100
        ),
        plot_container_method_kwargs_cycler_args=tuple((
            dict(
                facecolor=('#a6cee3', '#b0dd8b', '#f59a96', '#fdbe6f', '#cbb1d2', '#b39c9a'),
            ),))
    )

    def __init__(self, fit_objects):
        super(XYPlot, self).__init__(fit_objects=fit_objects)
        self._plot_range_x = None
