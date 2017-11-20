from .._base import CostFunctionBase, CostFunctionBase_Chi2, CostFunctionBase_NegLogLikelihood, CostFunctionBase_NegLogLikelihoodRatio, CostFunctionException
from kafe.fit._base.cost import CostFunctionBase_Chi2_Nuisance
import numpy as np

__all__ = ["XYCostFunction_UserDefined", "XYCostFunction_Chi2", "XYCostFunction_NegLogLikelihood"]


class XYCostFunction_UserDefined(CostFunctionBase):
    def __init__(self, user_defined_cost_function):
        """
        User-defined cost function for fits to *xy* data.
        The function handle must be provided by the user.

        :param user_defined_cost_function: function handle

        .. note::
            The names of the function arguments must be valid reserved
            names for the associated fit type (:py:obj:`~kafe.fit.XYFit`)!
        """
        super(XYCostFunction_UserDefined, self).__init__(cost_function=user_defined_cost_function)


class XYCostFunction_Chi2(CostFunctionBase_Chi2):
    def __init__(self, errors_to_use='covariance', fallback_on_singular=True, axes_to_use='xy'):
        """
        Built-in least-squares cost function for *xy* data.

        :param errors_to_use: which errors to use when calculating :math:`\chi^2`
        :type errors_to_use: ``'covariance'``, ``'pointwise'`` or ``None``
        :param axes_to_use: take into account errors for which axes
        :type axes_to_use: ``'y'`` or ``'xy'``
        """

        if axes_to_use.lower() == 'y':
            super(XYCostFunction_Chi2, self).__init__(errors_to_use=errors_to_use, fallback_on_singular=fallback_on_singular)
        elif axes_to_use.lower() == 'xy':
            _cost_function_description = "chi-square with projected x errors"
            if errors_to_use is None:
                _chi2_func = self.chi2_no_errors
                _cost_function_description += ' (no errors)'
            elif errors_to_use.lower() == 'covariance':
                if fallback_on_singular:
                    _chi2_func = self.chi2_xy_covariance_fallback
                else:
                    _chi2_func = self.chi2_xy_covariance
                _cost_function_description += ' (covariance matrix)'
            elif errors_to_use.lower() == 'pointwise':
                if fallback_on_singular:
                    _chi2_func = self.chi2_xy_pointwise_errors_fallback
                else:
                    _chi2_func = self.chi2_xy_pointwise_errors
                _cost_function_description += ' (pointwise errors)'
            else:
                raise CostFunctionException("Unknown value '%s' for 'errors_to_use': must be one of ('covariance', 'pointwise', None)")
            CostFunctionBase.__init__(self, cost_function=_chi2_func)
            self._formatter.latex_name = "\chi^2"
            self._formatter.name = "chi2"
            self._formatter.description = _cost_function_description
        else:
            raise CostFunctionException("Unknown value '%s' for 'axes_to_use': must be one of ('xy', 'y')")

        

    @staticmethod
    def chi2_no_errors(y_data, y_model):
        r"""A least-squares cost function calculated from 'y' data and model values,
        without considering uncertainties:

        .. math::
            C = \chi^2({\bf d}, {\bf m}) = ({\bf d} - {\bf m})\cdot({\bf d} - {\bf m})

        In the above, :math:`{\bf d}` are the measurements and :math:`{\bf m}` are the model
        predictions.

        :param y_data: measurement data
        :param y_model: model values
        :return: cost function value
        """
        return CostFunctionBase_Chi2.chi2_no_errors(data=y_data, model=y_model)

    @staticmethod
    def chi2_covariance(y_data, y_model, y_total_cov_mat_inverse):
        r"""A least-squares cost function calculated from 'y' data and model values,
        considering the covariance matrix of the 'y' measurements.

        .. math::
            C = \chi^2({\bf d}, {\bf m}) = ({\bf d} - {\bf m})^{\top}\,{{\bf V}^{-1}}\,({\bf d} - {\bf m})

        In the above, :math:`{\bf d}` are the measurements, :math:`{\bf m}` are the model
        predictions, and :math:`{{\bf V}^{-1}}` is the inverse of the total covariance matrix.

        :param y_data: measurement data
        :param y_model: model values
        :param y_total_cov_mat_inverse: inverse of the total covariance matrix
        :return: cost function value
        """
        return CostFunctionBase_Chi2.chi2_covariance(data=y_data, model=y_model, total_cov_mat_inverse=y_total_cov_mat_inverse)

    @staticmethod
    def chi2_pointwise_errors(y_data, y_model, y_total_error):
        r"""A least-squares cost function calculated from 'y' data and model values,
        considering pointwise (uncorrelated) uncertainties for each data point:

        .. math::
            C = \chi^2({\bf d}, {\bf m}, {\bf \sigma}) = \sum_k \frac{d_k - m_k}{\sigma_k}

        In the above, :math:`{\bf d}` are the measurements, :math:`{\bf m}` are the model
        predictions, and :math:`{\bf \sigma}` are the pointwise total uncertainties.

        :param y_data: measurement data
        :param y_model: model values
        :param y_total_error: total measurement uncertainties
        :return:
        """
        return CostFunctionBase_Chi2.chi2_pointwise_errors(data=y_data, model=y_model, total_error=y_total_error)

    @staticmethod
    def chi2_xy_covariance(y_data, y_model, projected_xy_total_cov_mat_inverse):
        return CostFunctionBase_Chi2.chi2_covariance(data=y_data, model=y_model, total_cov_mat_inverse=projected_xy_total_cov_mat_inverse)

    @staticmethod
    def chi2_xy_pointwise_errors(y_data, y_model, x_total_error, projected_xy_total_error):
        return CostFunctionBase_Chi2.chi2_pointwise_errors(y_data, y_model, total_error=projected_xy_total_error)

    @staticmethod
    def chi2_pointwise_errors_fallback(y_data, y_model, y_total_error):
        return CostFunctionBase_Chi2.chi2_pointwise_errors_fallback(data=y_data, model=y_model, total_error=y_total_error)

    @staticmethod
    def chi2_covariance_fallback(y_data, y_model, y_total_cov_mat_inverse):
        return CostFunctionBase_Chi2.chi2_covariance_fallback(data=y_data, model=y_model, total_cov_mat_inverse=y_total_cov_mat_inverse)

    @staticmethod
    def chi2_xy_pointwise_errors_fallback(y_data, y_model, projected_xy_total_error):
        return CostFunctionBase_Chi2.chi2_pointwise_errors_fallback(y_data, y_model, total_error=projected_xy_total_error)

    @staticmethod
    def chi2_xy_covariance_fallback(y_data, y_model, projected_xy_total_cov_mat_inverse):
        return CostFunctionBase_Chi2.chi2_covariance_fallback(data=y_data, model=y_model, total_cov_mat_inverse=projected_xy_total_cov_mat_inverse)


class XYCostFunction_NegLogLikelihood(CostFunctionBase_NegLogLikelihood):
    def __init__(self, data_point_distribution='poisson'):
        r"""
        Built-in negative log-likelihood cost function for *xy* data.

        In addition to the measurement data and model predictions, likelihood-fits require a
        probability distribution describing how the measurements are distributed around the model
        predictions.
        This built-in cost function supports two such distributions: the *Poisson* and *Gaussian* (normal)
        distributions.

        In general, a negative log-likelihood cost function is defined as the double negative logarithm of the
        product of the individual likelihoods of the data points.

        :param data_point_distribution: which type of statistics to use for modelling the distribution of individual data points
        :type data_point_distribution: ``'poisson'`` or ``'gaussian'``
        """
        super(XYCostFunction_NegLogLikelihood, self).__init__(data_point_distribution=data_point_distribution)

    @staticmethod
    def nll_gaussian(y_data, y_model, y_total_error):
        r"""A negative log-likelihood function assuming Gaussian statistics for each measurement.

        The cost function is given by:

        .. math::
            C = -2 \ln \mathcal{L}({\bf d}, {\bf m}, {\bf \sigma}) = -2 \ln \prod_j \mathcal{L}_{\rm Gaussian} (x=d_j, \mu=m_j, \sigma=\sigma_j)

        .. math::
            \rightarrow C = -2 \ln \prod_j \frac{1}{\sqrt{2{\sigma_j}^2\pi}} \exp{\left(-\frac{ (d_j-m_j)^2 }{ {\sigma_j}^2}\right)}

        In the above, :math:`{\bf d}` are the measurements, :math:`{\bf m}` are the model predictions, and :math:`{\bf \sigma}`
        are the pointwise total uncertainties.

        :param y_data: measurement data
        :param y_model: model values
        :param y_total_error: total *y* uncertainties for data
        :return: cost function value
        """
        # "translate" the argument names
        return CostFunctionBase_NegLogLikelihood.nll_gaussian(data=y_data, model=y_model, total_error=y_total_error)


    @staticmethod
    def nll_poisson(y_data, y_model):
        r"""A negative log-likelihood function assuming Poisson statistics for each measurement.

        The cost function is given by:

        .. math::
            C = -2 \ln \mathcal{L}({\bf d}, {\bf m}) = -2 \ln \prod_j \mathcal{L}_{\rm Poisson} (k=d_j, \lambda=m_j)

        .. math::
            \rightarrow C = -2 \ln \prod_j \frac{{m_j}^{d_j} \exp(-m_j)}{d_j!}

        In the above, :math:`{\bf d}` are the measurements and :math:`{\bf m}` are the model
        predictions.

        :param y_data: measurement data
        :param y_model: model values
        :return: cost function value
        """
        # "translate" the argument names
        return CostFunctionBase_NegLogLikelihood.nll_poisson(data=y_data, model=y_model)


class XYCostFunction_NegLogLikelihoodRatio(CostFunctionBase_NegLogLikelihoodRatio):
    def __init__(self, data_point_distribution='poisson'):
        r"""
        Built-in negative log-likelihood cost function for *xy* data.

        In addition to the measurement data and model predictions, likelihood-fits require a
        probability distribution describing how the measurements are distributed around the model
        predictions.
        This built-in cost function supports two such distributions: the *Poisson* and *Gaussian* (normal)
        distributions.

        In general, a negative log-likelihood cost function is defined as the double negative logarithm of the
        product of the individual likelihoods of the data points.

        :param data_point_distribution: which type of statistics to use for modelling the distribution of individual data points
        :type data_point_distribution: ``'poisson'`` or ``'gaussian'``
        """
        super(XYCostFunction_NegLogLikelihoodRatio, self).__init__(data_point_distribution=data_point_distribution)

    @staticmethod
    def nllr_gaussian(y_data, y_model, y_total_error):
        r"""A negative log-likelihood function assuming Gaussian statistics for each measurement.

        The cost function is given by:

        .. math::
            C = -2 \ln \mathcal{L}({\bf d}, {\bf m}, {\bf \sigma}) = -2 \ln \prod_j \mathcal{L}_{\rm Gaussian} (x=d_j, \mu=m_j, \sigma=\sigma_j)

        .. math::
            \rightarrow C = -2 \ln \prod_j \frac{1}{\sqrt{2{\sigma_j}^2\pi}} \exp{\left(-\frac{ (d_j-m_j)^2 }{ {\sigma_j}^2}\right)}

        In the above, :math:`{\bf d}` are the measurements, :math:`{\bf m}` are the model predictions, and :math:`{\bf \sigma}`
        are the pointwise total uncertainties.

        :param y_data: measurement data
        :param y_model: model values
        :param y_total_error: total *y* uncertainties for data
        :return: cost function value
        """
        # "translate" the argument names
        return CostFunctionBase_NegLogLikelihoodRatio.nllr_gaussian(data=y_data, model=y_model,
                                                                    total_error=y_total_error)


    @staticmethod
    def nllr_poisson(y_data, y_model):
        r"""A negative log-likelihood function assuming Poisson statistics for each measurement.

        The cost function is given by:

        .. math::
            C = -2 \ln \mathcal{L}({\bf d}, {\bf m}) = -2 \ln \prod_j \mathcal{L}_{\rm Poisson} (k=d_j, \lambda=m_j)

        .. math::
            \rightarrow C = -2 \ln \prod_j \frac{{m_j}^{d_j} \exp(-m_j)}{d_j!}

        In the above, :math:`{\bf d}` are the measurements and :math:`{\bf m}` are the model
        predictions.

        :param y_data: measurement data
        :param y_model: model values
        :return: cost function value
        """
        # "translate" the argument names
        return CostFunctionBase_NegLogLikelihoodRatio.nllr_poisson(data=y_data, model=y_model)

class XYCostFunction_Chi2_Nuisance(CostFunctionBase_Chi2_Nuisance):
    #CHiSquare Cosfunction with Nuisanceparameters
    def __init__(self):
        super(XYCostFunction_Chi2_Nuisance, self).__init__()

    @staticmethod
    def csn(y_data, y_model, y_total_uncor_cov_mat_inverse, y_total_uncor_cov_mat, nuisance_y_total_cor_cov_mat, y_nuisance_vector):

             return  CostFunctionBase_Chi2_Nuisance.csn(data=y_data, model=y_model, total_uncor_cov_mat_inverse=y_total_uncor_cov_mat_inverse, nuisance_total_cor_cov_mat=nuisance_y_total_cor_cov_mat, nuisance_vector=y_nuisance_vector)

