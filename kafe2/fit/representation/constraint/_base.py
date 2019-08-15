import abc
import six

from kafe2.fit.representation._base import GenericDReprBase
from kafe2.core.constraint import GaussianSimpleParameterConstraint, GaussianMatrixParameterConstraint

__all__ = ["ConstraintDReprBase"]


@six.add_metaclass(abc.ABCMeta)
class ConstraintDReprBase(GenericDReprBase):
    BASE_OBJECT_TYPE_NAME = 'constraint'

    _CLASS_TO_OBJECT_TYPE_NAME = {
        GaussianSimpleParameterConstraint: 'simple',
        GaussianMatrixParameterConstraint: 'matrix'
    }
    _OBJECT_TYPE_NAME_TO_CLASS = {
        'simple': GaussianSimpleParameterConstraint,
        'matrix': GaussianMatrixParameterConstraint
    }

    def __init__(self, constraint=None):
        self._kafe_object = constraint
        super(ConstraintDReprBase, self).__init__()
